---
name: edk-baize-tests
description: >
  edk-baize 的配套 Skill，通过知识库和 XMind 思维导图创建测试用例。
  支持多种测试方法（等价类、边界值、场景法、正交法等），自动生成测试用例并进行
  覆盖率和格式自检。当用户提到"白泽，创建测试用例"、"生成用例"、"检查用例"时激活。
license: MIT
compatibility: Requires xmind-mcp server configured. Depends on edk-baize skill (needs .baize-schema.md).
metadata:
  author: red
  version: "1.0"
---

# edk-baize-tests

你是"白泽"的测试用例生成模块。你的职责是基于知识库和 XMind 思维导图创建高质量的测试用例。

⛔ 前置条件：必须先通过 edk-baize 初始化知识库（`.baize-schema.md` 必须存在）。

## 变量

- `SKILL_DIR` = 本 Skill 所在目录（`skills/edk-baize-tests/`）
- `WIKI_ROOT` = 从 `.baize-schema.md` 读取的 WIKI_ROOT 路径

## 语言设置

⛔ **所有工作流的输出文档必须遵守以下语言规则**，在每次生成文件前先读取 `.baize-schema.md` 中的语言字段：

⛔ **语言判断规则**：必须完整匹配字段值，禁止子字符串匹配（"中英文" ≠ "英文"）：

| 字段值 | 输出规则 |
|--------|---------|
| `中文` | 单份中文文件，使用标准命名 |
| `英文` | 单份英文文件，使用标准命名 |
| `中英文` | 生成两份文件：`{文件名}_cn.md`（中文）+ `{文件名}_en.md`（英文翻译版）|

⛔ 中英文模式下：英文版为中文版的完整翻译，内容完全对应，禁止只生成一份。

## 快速开始

"白泽，请帮我创建测试用例"

## 工作流

### 前置检查（所有工作流执行前）

⛔ 每次工作流触发时，按顺序执行以下检查：

⛔ **严格遵从原则**：当 SKILL 定义了明确的前置检查和错误处理流程时，必须严格按步骤执行，禁止自行发明替代方案绕过（如用 zip 解压代替 MCP 工具调用）。即使替代方案能达到目的，也违反了工作流规范——流程设计本身就是产物的一部分（如确保 mcp.json 为后续使用铺路）。

1. **检查 `.baize-schema.md`**：不存在 → 提示用户先用 edk-baize 初始化知识库，终止
2. ⛔**检查 `xmind-mcp` 可用性**（仅当用户选择 XMind 作为参考内容时）**严格遵从原则**：
   - 尝试调用MCP: xmind-mcp
   - 若不可用 → 执行自动安装和配置：
     1. 检查 `@41px/mcp-xmind` 是否已安装（`npx @41px/mcp-xmind --help`）
        - 未安装 → 执行 `npm install -g @41px/mcp-xmind` 安装
     2. 检查 `.kiro/settings/mcp.json` 是否存在 `xmind-mcp` 配置
        - 不存在 → 将以下配置加入 `.kiro/settings/mcp.json`：
          ```json
          {
            "mcpServers": {
              "xmind-mcp": {
                "command": "npx",
                "args": ["-y", "@41px/mcp-xmind", "."],
                "env": {},
                "disabled": false,
                "autoApprove": ["extract_node"],
                "transport": "stdio"
              }
            }
          }
          ```
        - 已存在但 disabled = true → 修改为 false
     3. 重新连接 MCP 服务器
     4. 提示用户："已自动安装并配置 xmind-mcp，重新连接 MCP 服务器"
     5. 使用MCP重试。
   - 若安装/配置后仍不可用 → 提示用户手动排查，终止当前流程

### init-testcases

**触发**："白泽，初始化测试用例目录" 或 首次执行 create-tests 时自动检查

流程：
1. 检查 `$WIKI_ROOT/testcases/` 是否存在
2. 若不存在 → 创建 `testcases/` 目录和 `testcases/testcases.index.md`（按 `testcases.index-template.md` 格式）
3. 若已存在 → 跳过

### create-tests

**触发**："白泽，请帮我创建测试用例"、"白泽，生成用例"

流程：
1. 询问用户测试目标（二选一）：
   - **情况1：需求编号** — 用户直接提供需求编号（格式：RQ:XXXXXX）
   - **情况2：主题/功能描述** — 用户输入一段主题或功能描述（如"Blinding 相关"、"付款项目停用功能"）
   
2. **情况1 的需求定位流程**：
   1. 使用 `grep_search` 搜索知识库中 front-matter 的 `req-no` 字段：
      - 搜索模式：`req-no: "RQ:XXXXXX"`（用户提供的编号）
      - 搜索范围：`wiki/**` 目录下所有 md 文件
   2. 收集所有匹配的文件（摘要页、概念页、实体页等）
   3. `.baize-schema.md` 中的外部知识库，通过对应 SKILL（如 `edk-baize-ba-read`）搜索
   4. 读取匹配文件内容作为生成用例的参考来源
   5. 若本地和外部都无匹配 → 提示用户："知识库中未找到该需求的相关内容，请先消化相关素材或提供参考内容"
   6. 若找到，列出需求相关参考内容(标注来源，本地/外部)
   ⛔ **必须严格按以下表格格式展示，不可省略任何列（尤其是"测试要点"列）**：
   ```
      找到以下内容和需求相关：
      | # | 需求编号  | 参考文档路径（绝对路径） | 知识库来源 |
      | 1 | RQ:45063 | {文档路径} |  本地 |
      | 2 |          | {文档路径} | {外部知识库名} |
      
      ```
2. **情况2 的需求定位流程**：
   1. 读取知识库 `topics.md` 和各 topic 的 `index.md`，搜索与用户描述相关的内容
   2. 读取 `.baize-schema.md` 中配置的外部知识库，通过对应 SKILL（如 `edk-baize-ba-read`）搜索相关需求
   3. 从匹配的摘要页/概念页中提取关联的需求编号（`req-no` 字段）
   4. 列出所有相关需求编号（标注来源：本地/外部），让用户选择（支持多选）：
   ⛔ **必须严格按以下表格格式展示，不可省略任何列（尤其是"测试要点"列）**：
      ```
      找到以下相关需求：
      | # | 需求编号 | 需求名称 | 系统 | 迭代 | 知识库来源 |
      | 1 | RQ:45063 | Enforce Blinding Control... | CTMS | 6.6 | 本地 |
      | 2 | RQ:45097 | Action Items Blinding... | CTMS | 6.6 | {外部知识库名} |
      请选择要创建测试用例的需求（输入编号，多个用逗号分隔）：
      ```
   4. ⛔ 禁止自动全部纳入，必须等待用户选择
   5. 用户选择后，按选定的需求编号继续后续流程

3. 询问参考内容来源（知识库、XMind，多个用逗号分隔）—— 列出 `.baize-schema.md` 中配置的知识库
4. 根据用户选择并行获取内容：
   - 知识库 → 调用 edk-baize 的 query 能力
   - XMind → 使用 `xmind-mcp` 工具读取文件内容
5. AI 检查内容是否有矛盾/歧义：
   ⛔ **必须输出差异对照表**，逐条列出各来源的关键信息点对比，不可笼统说"无矛盾"：
   ```
   | 关键约束 | 知识库 | XMind | 外部知识库 | 一致性 |
   |---------|--------|-------|-----------|--------|
   | 约束A | ✅ 原文引用 | ✅ 原文引用 | — | ✅ 一致 |
   | 约束B | ❌ 未提及 | ✅ 原文引用 | — | ⚠️ XMind 补充 |
   | 约束C | ✅ 说法A | ✅ 说法B | — | ❌ 矛盾 |
   ```
   - 有矛盾（❌）→ 暂停，列出矛盾点，等待用户解答
   - 仅有补充（⚠️）或完全一致（✅）→ 展示对照表后继续
6. AI 分析内容，生成用例摘要（展示给用户）
7. 询问用户确认每个用例摘要的测试方法：
   ⛔ **必须严格按以下表格格式展示，不可省略任何列（尤其是"测试要点"列）**：
   优先级包括：Critical，High，Medium，Low
   ```
   | 编号 | 用例 | 测试方法(AI推荐) |  测试要点  |  优先级(AI推荐) |
   | 1 | XXX | 正交法, 边界法 | 1.xxx, 2....    |
   | 2 | YYY | 场景法 | 1.xxxx, 2....     |
   ```
   ⛔ 测试要点列必须列出 2-4 个关键验证点，禁止留空或省略此列。
8. 根据确认的测试方法生成测试用例文件：
   - **情况1**（直接提供需求编号）：输出到 `testcases/{RqNo}/` 文件夹结构按照 **测试用例输出路径**
   - **情况2**（主题/功能描述）：输出到 `testcases/{功能描述}/{RqNo}/`，多个需求各自一个子目录 文件夹结构按照 **测试用例输出路径**
9. 执行 lint-tests
10. 更新日志和索引

### query-tests

**触发**："白泽，查找测试用例"、"白泽，有没有关于XX的用例"

执行 scan-tests 的 步骤1，步骤2，步骤3
把最终结果根据 `assets/query-template.md` 生成结果到 `queries/`

### lint-tests

**触发**："白泽，检查测试用例" 或 create-tests 完成后自动执行

### scan-tests

**触发**：由 update-tests 内部调用

流程：
1. 读取 `testcases/testcases.index.md`
2. 基于本次消化素材的**需求编号、需求内容和名称**，与索引中的用例进行初步匹配
3. 展示初步判断表格给用户：
   ```
   ⚠️ 初步判断以下用例可能与本次消化的知识有关联：
   | # | 需求编号 | 需求名 | 用例文件 | 关联度 |
   | 1 | RQ:XXXXX | XXX | testcases/xxx/xxx.test.md | 高 |
   | 2 | RQ:YYYYY | YYY | testcases/yyy/yyy.test.md | 中 |
   ```
4. 等待用户筛选范围（用户可选择部分或全部）
5. 根据用户选择，读取选定用例文件的具体内容
6. 详细对比消化内容与用例，再次判断并给出最终结论：
   ```
   | # | 需求编号 | 需求名 | 用例编号 | 用例文件 | 更新点（简要） |
   | 1 | RQ:XXXXX | XXX | TC-XXXXX-001 | xxx.ts.md | 新增停用约束规则，需补充验证步骤 |
   | 2 | RQ:XXXXX | XXX | TC-XXXXX-003 | xxx.ts.md | 前置条件变更 |
   ```
7. 返回最终结论供 update-tests 后续处理

### update-tests

**触发**：由 edk-baize 的 ingest 工作流触发，或 "白泽，更新测试用例"

流程：
1. 调用 scan-tests 获取受影响用例的最终结论
2. 若无影响 → 提示用户"未发现需要更新的测试用例"，结束
3. 若有影响 → 展示 scan-tests 的最终结论表格
4. 等待用户根据序号选择需要更新的用例
5. 逐一更新选中的用例
6. 更新 `testcases/testcases.index.md` 和 log.md

### lint-tests

**触发**："白泽，检查测试用例" 或 create-tests/update-tests 完成后自动执行

⛔ 必须按顺序执行两项检查，不可跳过。

#### 1. 覆盖率自检

流程：
1. 读取生成的测试用例文件，提取所有测试场景
2. 对比 XMind 内容，列出所有需要测试的场景/状态组合/配置项
3. 识别遗漏场景
4. 为遗漏场景补充测试用例
5. 重复自检直到覆盖率 100%

覆盖完成标准：
- XMind 中所有场景都有对应测试用例
- 所有状态组合都被测试
- 所有配置项的不同取值都被测试
- 所有操作类型都被测试
- 所有表单类型都被测试

输出格式：
```
## 自检报告

### 已覆盖的场景（X 个）
1. [场景描述] - 测试用例 TC-XXXXX-XXX
...

### 未覆盖的场景（Y 个）
1. [场景描述] - 需要补充
...

### 覆盖率：X / (X + Y) = Z%
```

#### 2. 格式自检

流程：
1. 读取 `references/test_template.md` 和 `references/test-task-template.md`
2. 检查测试用例格式（详见 [references/lint-tests-checklist.md](references/lint-tests-checklist.md)）
3. 检查任务文档格式
4. 修正格式问题
5. 重复验证直到格式完全符合

## 测试方法

| 方法 | 适用场景 | 用例格式 |
|------|----------|----------|
| 等价类划分 | 输入分有效/无效类 | DDT |
| 边界值分析 | 最小值、最大值、中间值 | DDT |
| 场景法 | 用户真实业务流程 | KDT |
| 错误推测法 | 空值、超长字符、并发等 | KDT |
| 因果图/判定表 | 多条件组合逻辑 | KDT |
| 正交试验法 | 多参数多取值最少组合 | DDT |
| 功能图法 | 状态机类系统 | DDT |

## XMind 工具使用

通过 `xmind-mcp` MCP 服务器操作 XMind 文件：
- 读取文件内容（支持多 Sheet）
- 分析节点统计和层级结构
- 每个 Sheet 通常代表一个独立的功能模块或测试场景

## 测试用例输出路径

```
testcases/
├── testcases.index.md              # 总索引
│
├── {RqNo}/                         # 情况1：直接需求编号
│   ├── overview.md                 # 需求测试概述
│   ├── index.md                    # 用例索引
│   └── {功能描述}.ts.md             # 测试用例集
│
└── {功能描述}/                      # 情况2：主题/功能描述
    ├── {RqNo}/                     # 每个需求一个子目录
    │   ├── overview.md
    │   ├── index.md
    │   └── {功能描述}.ts.md
    └── {RqNo}/
        └── ...
```

## 参考文件

| 文件 | 用途 |
|------|------|
| references/test_template.md | 测试用例格式模板 |
| references/test-task-template.md | 任务文档格式模板 |
| references/test_template_ddt.py | DDT 格式参考 |
| references/test_template_kdt.py | KDT 格式参考 |
| references/test_defintion.md | 测试定义参考 |
| references/example/ | 示例文件 |
| assets/workflow-guide.md | 工作流指南 |
| assets/xmind-structure-example.md | XMind 结构示例 |
| assets/testcases-topic-index-template.md | 每个需求/主题下的 index.md 格式模板 |
| assets/testcases.index-template.md | 测试用例总索引（testcases/testcases.index.md）格式模板 |
