# Ingest 详细流程

## 素材类型判断与迁移

### 工作区外素材

若用户给出的路径在工作区外：

先尝试 `python3 scripts/import_external.py <wiki_root> <source_path> [--subdir <类型>]`，失败则改用 `py scripts/import_external.py`。

脚本自动完成：**复制**文件到 raw/、扫描图片引用、搜索并复制图片到 raw/assets/。
⛔ 脚本只复制，**不删除源文件**（工作区外文件 AI 无权删除，由用户自行管理）。
根据脚本输出的 JSON 报告，若有 `images_missing` 则在后续摘要页中标注 `[图片缺失: 文件名]`。

### 工作区内素材迁移

若素材在工作区内但不在 raw/ 中：

1. 将文件**移动**到 `raw/` 对应子目录（⛔ 移动 = 复制到目标 + 删除源文件，不可只复制不删除）
2. 若素材为用户纯文本粘贴：保存为 `raw/notes/{日期}-{短标题}.md`
3. 若素材包含图片引用（如 `![[xxx.png]]` 或 `![](xxx.png)`）：
   - ⛔ **必须在整个工作区范围内搜索图片文件**（使用 file_search），不可仅检查素材所在目录
   - 找到后将图片文件**移动**到 `raw/assets/`（⛔ 必须删除源位置的图片文件）
   - 若搜索后确认工作区内不存在该图片，才标注 `[图片缺失: 文件名]`
4. ⛔ 确保溯源来源链接指向的 raw/ 文件确实存在，否则立即创建
5. ⛔ 源文件清理检查：完成后必须验证原始位置文件已被删除；若源目录变为空目录，一并删除

## 内容提取规则

### PDF

先尝试 `python3 scripts/read_pdf.py <pdf_path>`，失败则改用 `py scripts/read_pdf.py <pdf_path>`。
⛔ 必须用脚本，不得内联 Python 命令。

大型文档（PDF > 20 页，或文本 > 10000 字）必须先完整阅读再总结：
1. 先 `--outline-only` 获取大纲，了解整体章节结构
2. 再分段 `--pages` 读全文，不遗漏任何章节
3. 整理出完整章节结构大纲
4. 基于完整阅读提炼观点
5. ⛔ 禁止只读前几页就开始创建页面，"觉得够了"不是停止阅读的理由

### 其他格式

- Markdown/文本/HTML → 直接读取
- 纯文本粘贴 → 直接使用

## Topic 生成流程

1. **AI 预先生成推荐 Topic 名**：根据素材内容生成 1 个推荐的 Topic 名称，同时读取 topics.md 获取已有 Topic 列表

2. **展示选项，等待用户确认**（⛔ 门控步骤，必须等待用户回复）：
   - 1. AI 推荐：`{上一步生成的 Topic 名}`
   - 2. 自定义（用户直接输入 Topic 名）
   - 3-N. 已有 Topic 列表（从 topics.md 中读取，若为空则只有前两项）

3. 根据用户选择确定最终 TopicName

4. 搜索 topics.md：
   - Topic 不存在 → 调用 `python3 scripts/init.py <wiki_root> --topic {TopicName}`（失败则用 `py`）创建标准子目录（entities, concepts, procedures, rules, comparisons, summaries, synthesis）及 overview.md/index.md，然后 AI 将新 Topic 条目添加到 topics.md
   - Topic 已存在 → 直接在已有目录下操作

⛔ 严禁绕过 init.py 自行创建 topic 目录，必须用脚本以保证标准结构。

## 摘要页创建规则

⛔ 必须先读取对应模板，严格按模板章节结构输出，不得自行简化、合并或替换章节名称。

根据文档类型选择模板：
- **规范类** → `assets/summary-spec-template.md`
- **观点类** → `assets/summary-template.md`
- **培训类** → `assets/summary-training-template.md`

填充内容到 `wiki/{Topic}/summaries/`。

⛔ 通用约束：
- 规范类："文档结构"章节每个主要章节后必须有 `[[页面链接]]`
- 培训类："知识模块"章节每个模块后必须有 `[[页面链接]]`
- 溯源来源格式：`[[raw/{subdir}/{文件名}|显示名]]`，禁止纯文本或相对路径链接
- 每个关键事实后面标注来源：`([[raw/{subdir}/{文件名}|源文, L42-45]])`
- 数字和结论必须原文引用，不得用 AI 语言重述：
  - ❌ 差：该公司营收约 10 亿
  - ✅ 好：该公司营收"10.3 亿元"(raw/report.md, L128)

## 首页.canvas 生成规则

每次 ingest 完成后必须重新生成 `$WIKI_ROOT/首页.canvas`：

- **数据来源**：`topics.md`
- **布局风格**：极简理性逻辑架构风，纯白干净基底，中心放置核心总纲节点，向外发散多层分支架构，用纤细流畅连线串联各知识板块，层级分明条理清晰，留白舒适，专业知识库门户视觉。
- **结构规则**：
  - 中心节点：知识库标题 + Topic 总数 + 更新日期
  - 第二层：按领域分类的域节点（如"临床系统"、"开发技术"、"研究兴趣"），使用低饱和莫兰迪配色区分
  - 第三层：各 Topic 叶节点，每个节点使用 `text` 类型（不用 `file` 类型），内容为 `### Topic名\n\n关键词描述\n\n[[wiki/{Topic名}/overview]]`
  - 底部：`topics.md` 和 `log.md` 的快捷导航节点
  - 所有层级之间用 edges 连线串联（中心→域→Topic）
- **技术约束**：
  - 节点用 `text` 类型，通过 `[[wiki/xxx/overview]]` 链接保持可点击跳转
  - edges 无装饰，纤细连线即可
  - color 使用 Obsidian canvas 内置色号（"0"-"6"），低饱和沉稳

## 展示结果格式

ingest 完成后向用户展示：
- 已消化：（素材标题）
- 新增页面列表
- 更新页面列表
- 发现关联（与已有素材的联系）
- 融会建议（仅当发现新的交叉关系时提示）
