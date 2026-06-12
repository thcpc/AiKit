# Ingest 详细流程

## ⛔ 第零步：测试用例素材路由（在判断 raw 子目录之前执行）

⛔ ingest 工作流接到任何素材时，**第一步**先判断是否为测试用例素材：

| 判断维度 | 测试用例特征 |
|---------|-------------|
| 文件名 | 含 "用例"、"test case"、"回归"、"regression"、"TC-"、"用例清单" 等 |
| 内容形态 | "步骤 + 预期结果"、"前置条件 + 操作 + 校验" |
| frontmatter | `tags` 含 "用例" / "testcase" / "回归" |
| 路径 | 来自 `回归用例/`、`testcases/`、`tests/` 等目录 |

满足任一项 → 视为测试用例素材：

1. ⛔ **不要**自行迁移到 `raw/notes/`，**也不要**在 `wiki/` 创建任何页面
2. 提示用户："素材 `{文件名}` 是测试用例，应路由到 edk-baize-tests。"
3. 询问用户：
   - 选项 A（推荐）：交给 edk-baize-tests，调用其测试用例 ingest 工作流
   - 选项 B：当作普通素材消化进 wiki/（用于"了解已有用例"，不是创建用例）
4. 执行：
   - 选 A 且 edk-baize-tests 已安装 → 触发 edk-baize-tests 的对应工作流，本流程结束
   - 选 A 但 edk-baize-tests 未安装 → 提示用户安装，跳过本素材
   - 选 B → 继续走下面的标准 ingest 流程，但⛔ 严禁在 procedures/ 创建用例步骤页（用例步骤是 testcase 形态，不是 procedure）

⛔ batch-ingest 中遇到测试用例素材，按上述规则处理，**不可静默归入 wiki/**。如果同一批中混杂多种类型，应在批处理开始时一次性向用户展示分类结果并请求确认：

```
📂 批量素材分类：
- 普通文档（A/B/C 类）：N 个
- 测试用例：M 个 → 计划交给 edk-baize-tests
- 无法识别：K 个 → 需用户判断

确认继续？
```

## 素材来源判断（普通素材）

排除测试用例之后，再判断素材应归入哪个 raw/ 子目录：

- 若素材来源于 Sprial（如 URL 包含 `spiraservice.net`、标题含 RQ 编号等）→ `raw/sprial/`
- 若素材来源于 Teams 聊天记录 → `raw/teams/`
- 若素材为个人笔记、纯文本粘贴 → `raw/notes/`

⛔ **若 AI 无法判断素材类型，必须询问用户**，提供以下选项：
1. Sprial 需求 → `raw/sprial/`
2. Teams 聊天记录 → `raw/teams/`
3. 个人笔记 → `raw/notes/`

---

## 素材迁移

### A. 工作区素材迁移

若素材在工作区内但不在 raw/ 中：

1. 将文件**移动**到 `raw/` 对应子目录（⛔ 移动 = 复制到目标 + 删除源文件，不可只复制不删除）
2. 若素材为用户纯文本粘贴：保存为 `raw/notes/{日期}-{短标题}.md`
3. 若素材包含图片引用（如 `![[xxx.png]]` 或 `![](xxx.png)`）：
   - ⛔ **必须在整个工作区范围内搜索图片文件**（使用 file_search），不可仅检查素材所在目录
   - 找到后将图片文件**移动**到 `raw/assets/`（⛔ 必须删除源位置的图片文件）
   - 若搜索后确认工作区内不存在该图片，才标注 `[图片缺失: 文件名]`
4. ⛔ 确保溯源来源链接指向的 raw/ 文件确实存在，否则立即创建
5. ⛔ 源文件清理检查：完成后必须验证原始位置文件已被删除；若源目录变为空目录，一并删除

### B. 非工作区素材迁移

先尝试 `python3 scripts/import_external.py <wiki_root> <source_path> [--subdir <类型>]`，失败则改用 `py scripts/import_external.py <wiki_root> <source_path> [--subdir <类型>]`

脚本自动完成：**复制**文件到 raw/、扫描图片引用、搜索并复制图片到 raw/assets/。
⛔ 脚本只复制，**不删除源文件**。工作区外的文件 AI 无权删除，源文件由用户自行决定是否保留。
根据脚本输出的 JSON 报告，若有 `images_missing` 则在后续摘要页中标注 `[图片缺失: 文件名]`。

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

## 文档生成流程

1. 询问用户该文档是否和需求相关
2. 若需求相关，⛔ 必须按以下表格格式逐项询问用户，禁止跳过任何一项：

   | # | 字段 | 格式 | 说明 |
   |---|------|------|------|
   | 1 | 需求编号 | RQ:XXXXXX | AI推荐或用户输入 |
   | 2 | 迭代编号 | 如 6.6 | AI推荐或用户输入 |
   | 3 | 系统 | EDC/PRODGV/ADMIN/CTMS/DESIGN/ProCheck/eTMF | 多个逗号分割 |
   | 4 | 模块 | 自由文本 | 多个逗号分割 |

   ⛔ 输出时必须以表格形式展示已收集的信息，让用户确认后再继续。

3. 若非需求相关，根据文档类型执行对应处理（详见 doc-types.md）

## 测试用例更新流程

> ⛔ 已迁移至 edk-baize-tests 的对应工作流。ingest 完成后若涉及测试用例更新，触发 edk-baize-tests。
> 普通文档的 ingest 不会在 wiki/ 中创建用例页面。
