"""Read-only CSV feedback checks. Python 3 standard library only."""
import argparse
import csv
from collections import Counter
from decimal import Decimal, InvalidOperation, ROUND_HALF_UP
import hashlib
import io
import json
import re
from pathlib import Path


def decimal_text(value):
    return None if value is None else format(value, 'f')


def ratio(count, total):
    return None if total == 0 else decimal_text(Decimal(count) * 100 / Decimal(total))


def rounded(value, places):
    if value is None:
        return None
    return format(Decimal(value).quantize(Decimal(1).scaleb(-places), rounding=ROUND_HALF_UP), 'f')


def analyze(path, score_column, minimum, maximum, id_column=None,
            single_choice_column=None, encoding='utf-8-sig', delimiter=','):
    try:
        low, high = Decimal(str(minimum)), Decimal(str(maximum))
    except InvalidOperation:
        raise ValueError('评分范围须填写数字，例如下限1、上限5') from None
    if not low.is_finite() or not high.is_finite() or low >= high:
        raise ValueError('评分范围须为两个有限数，且下限小于上限')
    data = path.read_bytes()
    try:
        text = data.decode(encoding)
    except UnicodeDecodeError:
        raise ValueError('文件编码与读取设置不一致。可能是Excel导出的GBK文件，请加 --encoding gbk 再试；也可另存为CSV UTF-8。不会自动转换或修改原文件。') from None
    except LookupError:
        raise ValueError('不认识这个文件编码。常用值为utf-8-sig或gbk，请核对 --encoding 参数。') from None
    delimiters = {'comma': ',', 'tab': '\t', 'semicolon': ';', ',': ',', '\t': '\t', ';': ';'}
    if delimiter not in delimiters:
        raise ValueError('不支持此分隔符，请用 --delimiter comma、tab或semicolon')
    separator = delimiters[delimiter]
    reader = csv.reader(io.StringIO(text, newline=''), strict=True, delimiter=separator)
    try:
        headers = next(reader)
    except StopIteration:
        raise ValueError('CSV为空')
    if not headers or any(not x.strip() for x in headers) or len(set(headers)) != len(headers):
        raise ValueError('列名不得为空或重复')
    required = [score_column] + [v for v in (id_column, single_choice_column) if v]
    if any(v not in headers for v in required):
        raise ValueError('找不到指定列：'+', '.join(v for v in required if v not in headers)+
                         '。请同时检查列名和分隔符；若表头被连成一列，制表符文件加 --delimiter tab，分号分隔文件加 --delimiter semicolon。')
    rows = []
    for index, cells in enumerate(reader, 1):
        if len(cells) != len(headers):
            raise ValueError('第'+str(index)+'条数据列数与表头不符；未跳过此行')
        rows.append(dict(zip(headers, cells)))
    valid, numeric, details = [], [], []
    counts, options, ids = Counter(), Counter(), Counter()
    empty_option = 0
    for index, row in enumerate(rows, 1):
        raw = row[score_column]
        clean = raw.strip()
        value = None
        if not clean:
            status = 'blank'
        else:
            try:
                value = Decimal(clean)
            except InvalidOperation:
                status = 'non_numeric'
            else:
                if not value.is_finite():
                    status = 'non_finite'
                else:
                    numeric.append(value)
                    status = 'valid' if low <= value <= high else 'out_of_range'
                    if status == 'valid':
                        valid.append(value)
        counts[status] += 1
        detail = {'record': index, 'id': row[id_column] if id_column else '',
                  'raw_score': raw, 'status': status,
                  'numeric_score': decimal_text(value) if value is not None and value.is_finite() else None}
        details.append(detail)
        if id_column and row[id_column].strip():
            ids[row[id_column].strip()] += 1
        if single_choice_column:
            choice = row[single_choice_column].strip()
            if choice:
                options[choice] += 1
            else:
                empty_option += 1
    n = len(rows)
    nonempty = n-empty_option if single_choice_column else None
    duplicate_ids = {k:v for k,v in ids.items() if v > 1}
    warnings = []
    if duplicate_ids:
        warnings.append('记录号重复；未自动去重，本报告按原始行计算，请先确认一行代表什么')
    if not valid:
        warnings.append('没有范围内有效评分，平均值为空，不写成0分')
    suspected_choices = [value for value in options if re.search(r'[;；,，/、|]', value)]
    if suspected_choices:
        warnings.append('疑似多选题，本程序只按整串统计，未拆分。请先确认题型；不可把下方整串占比解释为各个选项的选择率。')
    report = {
        'input': {'file':path.name,'sha256':hashlib.sha256(data).hexdigest(),'encoding':encoding},
        'scope': {'score_column':score_column,'minimum':decimal_text(low),'maximum':decimal_text(high),
                  'single_choice_column':single_choice_column,'delimiter':delimiter,
                  'row_semantics':'one CSV record; no automatic deduplication'},
        'total_records':n,
        'score': {'status_counts':{s:counts[s] for s in ['valid','blank','non_numeric','non_finite','out_of_range']},
                  'finite_numeric_count_before_range_check':len(numeric),
                  'finite_numeric_sum_before_range_check':decimal_text(sum(numeric,Decimal(0))),
                  'finite_numeric_mean_before_range_check':decimal_text(sum(numeric,Decimal(0))/len(numeric)) if numeric else None,
                  'valid_count':len(valid),'valid_sum':decimal_text(sum(valid,Decimal(0))),
                  'valid_mean':decimal_text(sum(valid,Decimal(0))/len(valid)) if valid else None},
        'single_choice': None,
        'duplicate_ids':duplicate_ids,'warnings':warnings,
        'limits':['不推断量表、不修复原始数据、不自动去重','选项单独统计，不因评分无效而删除该行选项','未提供参训总数，不计算回收率']}
    if single_choice_column:
        report['single_choice'] = {'nonempty_count':nonempty,'blank_count':empty_option,
            'counting_mode':'literal_whole_value','suspected_multi_choice_values':suspected_choices,
            'items':[{'value':key,'count':count,'all_records_denominator':n,
                      'percent_of_all_records':ratio(count,n),'nonempty_denominator':nonempty,
                      'percent_of_nonempty':ratio(count,nonempty),
                      'percent_rounded':{'of_all_records':rounded(ratio(count,n),1),
                                         'of_nonempty':rounded(ratio(count,nonempty),1)},
                      'suspected_multi_choice':key in suspected_choices} for key,count in options.items()]}
    report['score']['valid_mean_rounded'] = rounded(report['score']['valid_mean'],2)
    report['score']['finite_numeric_mean_before_range_check_rounded'] = rounded(report['score']['finite_numeric_mean_before_range_check'],2)
    return report, details


def main():
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument('input', type=Path)
    parser.add_argument('--score-column', required=True)
    parser.add_argument('--minimum', required=True)
    parser.add_argument('--maximum', required=True)
    parser.add_argument('--id-column')
    parser.add_argument('--single-choice-column')
    parser.add_argument('--encoding', default='utf-8-sig')
    parser.add_argument('--delimiter', default='comma', choices=['comma','tab','semicolon'])
    parser.add_argument('--out', type=Path, required=True)
    args = parser.parse_args()
    try:
        report, details = analyze(args.input, args.score_column, args.minimum, args.maximum,
                                  args.id_column, args.single_choice_column, args.encoding, args.delimiter)
        output = args.out
        if output.resolve() == args.input.resolve():
            raise ValueError('输出目录不能与输入文件相同')
        names = ['feedback_report.json','score_rows.csv']
        if any((output/name).exists() for name in names):
            raise ValueError('结果文件已存在，请换一个新结果目录，避免覆盖')
        output.mkdir(parents=True, exist_ok=True)
        with (output/names[0]).open('x',encoding='utf-8') as handle:
            json.dump(report,handle,ensure_ascii=False,indent=2)
        with (output/names[1]).open('x',encoding='utf-8',newline='') as handle:
            writer=csv.DictWriter(handle,fieldnames=['record','id','raw_score','status','numeric_score'])
            writer.writeheader();writer.writerows(details)
        print(json.dumps({'output':str(output),'records':report['total_records'],
                          'valid_scores':report['score']['valid_count'],'warnings':report['warnings']},ensure_ascii=False))
    except (ValueError, OSError, UnicodeError, csv.Error) as error:
        parser.exit(2, '未完成统计：'+str(error)+'\n')


if __name__ == '__main__':
    main()
