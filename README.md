# AI开箱办·办公整理助手

版本0.1.2，采用Apache-2.0许可。把已有材料整理成能复核的办公草稿：周报、反馈CSV、活动方案、票据附件、流程说明五项按需选用。

本项目是在已有Skill的试用经验基础上，借助AI整理规则、编写程序与练习材料。来源与具体借鉴见[ATTRIBUTION.md](ATTRIBUTION.md)；许可仅覆盖本项目有权许可的新增内容；第三方内容继续按原许可处理。许可范围见[LICENSE_STATUS.md](LICENSE_STATUS.md)。

## 三步先试周报

1. 下载并解压本项目，用能读取本地文件的AI助手打开此文件夹。纯聊天界面不一定支持。
2. 复制下面口令。仅下载不是加载，检查它是否真正读取文件。
3. 打开新生成的周报和核对表，再看examples/output对照。人、时间、数字和状态要核对。

```text
请完整读取 skill/kaixiang-office/SKILL.md，以及其中的周报参考。整理 examples/input/01_一周记录.txt，先不要读取examples/output。按默认格式给周报正文，核对表单独保存；输出放到新的练习目录，保留输入文件。告诉我实际读到的版本；不能读取的地方请说明。
```

例子里的29位是报名者，不是到场人数；1800元是预算申请；下周一是2026年11月9日。用户有自己的格式时，提供模板即可，不要求输出逐字相同。

## 其他任务怎样选

|手头材料|通常拿到什么|参考|
|---|---|---|
|工作记录|周报草稿与核对表|[weekly](skill/kaixiang-office/references/weekly.md)|
|明确评分范围的CSV|异常行、平均分与单选统计|[feedback](skill/kaixiang-office/references/feedback.md)|
|零散活动条件|方案草稿与待确认清单|[proposal](skill/kaixiang-office/references/proposal.md)|
|票据附件|整理副本与对应清单|[receipts](skill/kaixiang-office/references/receipts.md)|
|办事说明|步骤、分支、Mermaid文字源文件|[flow](skill/kaixiang-office/references/flow.md)|

## 实际运行反馈程序

需要Python 3，仅用标准库。工作目录为本项目根目录，输出选一个没用过的新目录：

```text
python skill/kaixiang-office/scripts/feedback_check.py examples/input/02_培训反馈.csv --score-column 满意度 --minimum 1 --maximum 5 --id-column 记录号 --single-choice-column 想学内容 --out my-feedback-result
```

这个例子实际结果：12条、9条有效评分、合计34、平均约3.78；“表格”选5次，占全部12条41.7%，占有填写的11条45.5%。原始精度保留，显示优先用rounded字段。

GBK文件显式加 --encoding gbk，制表符文件加 --delimiter tab。疑似多选只提醒，按整串保留，不拆成多选统计。重复ID不自动去重，原件不修改。

## 本地程序检查

```text
python -m unittest discover -s tests -v
```

共13项程序检查，包括范围、空白、重复ID、结构错误、编码、分隔符、疑似多选与拒绝覆盖；不代表AI准确率。执行时会在.test-output里创建虚构测试文件，该目录不进入发布包。无需安装分析库或联网。

## 使用范围

未在所有平台实测自动安装，没有通用安装器。不替代审批或财务审核，不自动上传、发通知或删除原件。票据目前仅用文本样张练习，图片和扫描件取决于工具能否实际读取。流程图能否出图取决于可用渲染器。

## 反馈问题

请写使用工具、Skill版本、预期结果、实际结果和可公开的最小示例。别上传真实单位资料、个人信息或账号凭据。公开仓库建立后可以使用Issues；不编造用户规模或效果数据。
