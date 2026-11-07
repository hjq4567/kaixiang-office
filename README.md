# AI开箱办·办公整理助手

把手里的工作记录、反馈表、活动条件、票据附件或办事说明交给AI，先整理成一份能核对、能接着改的草稿。

这里的Skill，是一份给AI看的办公说明书：几份文字文件，加一个可选的小程序。用能读取本地文件的AI助手打开就能先试；这份资料不用单独注册账号，你的AI工具是否需要登录取决于工具本身。

## 三步先试周报

1. [下载并解压资料](https://github.com/hjq4567/kaixiang-office/archive/refs/heads/main.zip)，让能读本地文件的AI助手打开解压后的文件夹。
2. 把下面这段话复制给它。先用虚构练习，不用准备自己的材料。
3. 打开新生成的周报与核对表，再去examples/output看参考结果。

```text
请完整读取 skill/kaixiang-office/SKILL.md，以及其中的周报参考。整理 examples/input/01_一周记录.txt，先不要读取 examples/output。按默认格式给周报正文，核对表单独保存；输出放到新的练习目录，保留输入文件。告诉我实际读到的版本；不能读取的地方请说明。
```

核对三处就能先看出有没有读对：29位是报名者，不是到场人数；1800元是预算申请；下周一是2026年11月9日。句子不用和示例逐字一样。

## 认一下文件放在哪里

```text
skill/kaixiang-office/  技能说明，AI从这里开始读
examples/input/         五类虚构练习的输入材料
examples/output/        对应参考结果，做完再看
tests/                  可选的程序检查
README.md               你正在看的使用说明
```

GitHub源码包和第16号资料包使用同一套目录和文件，上面的口令在两边通用。旧版资料包请换成新版后再照本页操作。

## 换一种办公任务试试

|你手头有什么|让它先整理什么|具体说明|
|---|---|---|
|一周记录|周报正文与核对表|[周报](skill/kaixiang-office/references/weekly.md)|
|培训反馈CSV|异常行、平均分、选项占比|[反馈表](skill/kaixiang-office/references/feedback.md)|
|零散活动条件|方案草稿和待确认清单|[方案](skill/kaixiang-office/references/proposal.md)|
|票据附件|副本、文件对应清单、异常项|[附件](skill/kaixiang-office/references/receipts.md)|
|办事说明|步骤、分支、流程文字源文件|[流程](skill/kaixiang-office/references/flow.md)|

可以这样问：“用办公整理助手，把附件里的活动条件整理成方案草稿。没定的先列出来，别替我补负责人。”

## 跑一下反馈检查程序

这一项需要Python 3，只用标准库；周报文字练习不需要跑程序。在解压后的项目根目录执行，结果放到新目录：

```text
python skill/kaixiang-office/scripts/feedback_check.py examples/input/02_培训反馈.csv --score-column 满意度 --minimum 1 --maximum 5 --id-column 记录号 --single-choice-column 想学内容 --out my-feedback-result
```

样例有12条反馈，9条有效评分、合计34分，平均约3.78。“表格”被选5次：占全部12条约41.7%，占有填写的11条约45.5%。原精度仍保留，显示时优先用rounded字段。

编码不一致时按提示加 --encoding gbk；制表符文件加 --delimiter tab。疑似多选会提醒，但不拆分；重复记录号只提醒，不自动去重。原件保留。

## 自己跑一遍程序检查

这一步可选，需要Python 3：

```text
python -B -m unittest discover -s tests -v
```

13项程序检查覆盖评分范围、空白、重复记录号、文件结构、编码、分隔符、多选提醒与拒绝覆盖，不代表AI准确率。产生的.test-output目录只是虚构测试文件，不放进发布包。

## 用之前记住这些范围

你已有固定格式时，直接把模板给它，不必照默认章节。资料本身不替你审批、报销或发通知；AI仍可能漏项，交出去前核对人、日期、金额和状态。

票据目前只用文本样张练习过，扫描件能否处理取决于工具。流程默认交可编辑的文字源文件，能不能出图片取决于是否有绘图工具。它不是独立App，也没有验证所有平台的自动安装。

## 遇到问题这样反馈

在[Issues](https://github.com/hjq4567/kaixiang-office/issues)写明：使用工具、版本、希望得到什么、实际得到什么，并附可公开的最小例子。不要上传真实单位资料或个人信息。

## 查看版本、许可与来源

当前版本0.1.3，采用[Apache-2.0](LICENSE)，仅覆盖本项目有权许可的新增内容，第三方内容继续按原许可处理。

项目是在已有Skill试用经验基础上，借助AI整理规则、编写程序与练习材料。具体参考和新增工作见[来源说明](ATTRIBUTION.md)，许可范围见[许可说明](LICENSE_STATUS.md)，修改记录见[CHANGELOG](CHANGELOG.md)。不宣称原作者参与或背书，也未证明比不加载Skill更快、更准。
