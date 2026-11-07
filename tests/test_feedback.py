from pathlib import Path
from decimal import Decimal
import csv,hashlib,importlib.util,io,json,subprocess,sys,uuid,unittest
sys.dont_write_bytecode=True
O=Path(__file__).resolve().parents[1]
S=O/'skill/kaixiang-office/scripts/feedback_check.py'
spec=importlib.util.spec_from_file_location('feedback_check',S)
m=importlib.util.module_from_spec(spec);spec.loader.exec_module(m)

class FeedbackTests(unittest.TestCase):

    def file(self, text):
        d = O / '.test-output' / uuid.uuid4().hex
        d.mkdir(parents=True)
        p = d / 'input.csv'
        p.write_text(text, encoding='utf-8-sig')
        return p

    def test_sample_numeric_audit_and_denominators(self):
        p = O / 'examples/input/02_培训反馈.csv'
        before = hashlib.sha256(p.read_bytes()).hexdigest()
        report, rows = m.analyze(p, '满意度', 1, 5, '记录号', '想学内容')
        self.assertEqual(report['total_records'], 12)
        s = report['score']
        self.assertEqual(s['valid_count'], 9)
        self.assertEqual(Decimal(s['valid_sum']), Decimal(34))
        self.assertEqual(Decimal(s['finite_numeric_mean_before_range_check']), Decimal('4.3'))
        self.assertEqual(Decimal(s['valid_mean']), Decimal(34) / 9)
        self.assertEqual(s['status_counts'], {'valid': 9, 'blank': 1, 'non_numeric': 1, 'non_finite': 0, 'out_of_range': 1})
        choices = {x['value']: x for x in report['single_choice']['items']}
        self.assertEqual(choices['表格']['count'], 5)
        self.assertEqual(Decimal(choices['表格']['percent_of_all_records']), Decimal(5) * 100 / 12)
        self.assertEqual(Decimal(choices['表格']['percent_of_nonempty']), Decimal(5) * 100 / 11)
        self.assertEqual(len(rows), 12)
        self.assertEqual(before, hashlib.sha256(p.read_bytes()).hexdigest())

    def test_absent_valid_scores_are_null_not_zero(self):
        p = self.file('s\nNaN\nInfinity\n-1\n待核\n""\n')
        r, _ = m.analyze(p, 's', 1, 5)
        self.assertIsNone(r['score']['valid_mean'])
        self.assertEqual(r['score']['valid_count'], 0)
        self.assertEqual(r['score']['status_counts']['non_finite'], 2)

    def test_zero_is_valid_when_scale_allows_it(self):
        p = self.file('s\n0\n5\n')
        r, _ = m.analyze(p, 's', 0, 5)
        self.assertEqual(r['score']['valid_count'], 2)
        self.assertEqual(Decimal(r['score']['valid_mean']), Decimal('2.5'))

    def test_duplicate_ids_warn_without_changing_row_count(self):
        p = self.file('id,s\nx,1\nx,5\n')
        r, rows = m.analyze(p, 's', 1, 5, 'id')
        self.assertEqual(r['duplicate_ids'], {'x': 2})
        self.assertEqual(len(rows), 2)
        self.assertEqual(Decimal(r['score']['valid_mean']), 3)
        self.assertTrue(r['warnings'])

    def test_csv_structure_errors_do_not_silently_drop_data(self):
        for text in ['s,s\n1,2\n', 's,x\n2\n', 's,x\n2,3,4\n']:
            with self.subTest(text=text), self.assertRaises(ValueError):
                m.analyze(self.file(text), 's', 1, 5)

    def test_invalid_bounds_fail_readably(self):
        p = self.file('s\n3\n')
        for lo, hi in [('a', '5'), ('NaN', '5'), ('5', '1')]:
            with self.subTest(lo=lo), self.assertRaises(ValueError):
                m.analyze(p, 's', lo, hi)

    def test_cli_refuses_overwriting_results(self):
        p = self.file('s\n1\n5\n')
        out = p.parent / 'results'
        cmd = [sys.executable, '-X', 'utf8', str(S), str(p), '--score-column', 's', '--minimum', '1', '--maximum', '5', '--out', str(out)]
        first = subprocess.run(cmd, capture_output=True, text=True, encoding='utf-8')
        self.assertEqual(first.returncode, 0, first.stderr)
        original = (out / 'feedback_report.json').read_bytes()
        second = subprocess.run(cmd, capture_output=True, text=True, encoding='utf-8')
        self.assertEqual(second.returncode, 2)
        self.assertEqual(original, (out / 'feedback_report.json').read_bytes())
        self.assertIn('结果文件已存在', second.stderr)

class RevisionTests(FeedbackTests):

    def cli(self, p, out, *extra):
        cmd = [sys.executable, '-X', 'utf8', str(S), str(p), '--score-column', '满意度', '--minimum', '1', '--maximum', '5', '--out', str(out), *extra]
        return subprocess.run(cmd, capture_output=True, text=True, encoding='utf-8')

    def test_suspected_multi_select_punctuation_warns_without_splitting(self):
        for separator in [';', '；', ',', '，', '/', '、', '|']:
            with self.subTest(separator=separator):
                buf = io.StringIO()
                w = csv.writer(buf, lineterminator='\n')
                w.writerow(['id', 's', '选项'])
                w.writerow(['A', 5, '表格' + separator + '写作'])
                w.writerow(['B', 4, '资料'])
                p = self.file(buf.getvalue())
                r, rows = m.analyze(p, 's', 1, 5, 'id', '选项')
                self.assertEqual(len(rows), 2)
                self.assertEqual(len(r['single_choice']['items']), 2)
                self.assertIn('疑似多选题', ''.join(r['warnings']))
                item = r['single_choice']['items'][0]
                self.assertEqual(item['value'], '表格' + separator + '写作')
                self.assertTrue(item['suspected_multi_choice'])
                self.assertEqual(item['count'], 1)
                self.assertEqual(item['percent_rounded']['of_all_records'], '50.0')

    def test_gbk_cli_error_suggests_working_encoding(self):
        p = self.file('记录号,满意度\nA01,5\nA02,4\n')
        p.write_bytes(p.read_text(encoding='utf-8-sig').encode('gbk'))
        bad = self.cli(p, p.parent / 'bad')
        self.assertEqual(bad.returncode, 2)
        self.assertIn('--encoding gbk', bad.stderr)
        self.assertNotIn('Traceback', bad.stderr)
        self.assertFalse((p.parent / 'bad').exists())
        good = self.cli(p, p.parent / 'good', '--encoding', 'gbk')
        self.assertEqual(good.returncode, 0, good.stderr)
        r = json.loads((p.parent / 'good/feedback_report.json').read_text(encoding='utf-8'))
        self.assertEqual(r['score']['valid_mean_rounded'], '4.50')

    def test_tab_delimiter_has_hint_and_explicit_retry(self):
        p = self.file('记录号\t满意度\nA01\t5\nA02\t3\n')
        bad = self.cli(p, p.parent / 'bad')
        self.assertEqual(bad.returncode, 2)
        self.assertIn('--delimiter tab', bad.stderr)
        good = self.cli(p, p.parent / 'good', '--delimiter', 'tab')
        self.assertEqual(good.returncode, 0, good.stderr)
        r = json.loads((p.parent / 'good/feedback_report.json').read_text(encoding='utf-8'))
        self.assertEqual(r['score']['valid_mean_rounded'], '4.00')

    def test_rounded_fields_preserve_original_precision(self):
        p = O / 'examples/input/02_培训反馈.csv'
        r, _ = m.analyze(p, '满意度', 1, 5, '记录号', '想学内容')
        self.assertEqual(r['score']['valid_mean_rounded'], '3.78')
        self.assertTrue(r['score']['valid_mean'].startswith('3.777777'))
        x = r['single_choice']['items'][0]
        self.assertEqual(x['percent_rounded'], {'of_all_records': '41.7', 'of_nonempty': '45.5'})
        self.assertTrue(x['percent_of_all_records'].startswith('41.6666'))

    def test_header_only_has_null_means_and_no_false_percentages(self):
        p = self.file('s,option\n')
        r, _ = m.analyze(p, 's', 1, 5, single_choice_column='option')
        self.assertEqual(r['total_records'], 0)
        self.assertIsNone(r['score']['valid_mean_rounded'])
        self.assertEqual(r['single_choice']['items'], [])

    def test_unknown_encoding_is_a_readable_error(self):
        p = self.file('满意度\n3\n')
        bad = self.cli(p, p.parent / 'bad', '--encoding', 'not-a-real-encoding')
        self.assertEqual(bad.returncode, 2)
        self.assertIn('常用值', bad.stderr)
        self.assertNotIn('Traceback', bad.stderr)

def load_tests(loader,tests,pattern):
    return loader.loadTestsFromTestCase(RevisionTests)

if __name__=='__main__':
    unittest.main()
