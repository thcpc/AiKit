# Healer 工作流

## 概述

本工作流用于调试和修改已生成的 Postman Collection。根据修改范围分为两种情况处理。

---

## 情况 1：仅修改 Postman Request JSON

当只需要修改已有接口的请求参数、Headers、Body、test script 等内容时，无需改动 api-plan 文件。

### 步骤

1. **定位问题** — 确认需要修改的接口（序号和名称）以及具体修改内容
2. **修改本地 JSON 文件** — 在 `{collection-folder}/` 目录下找到对应的 `{序号}-{接口名}.json` 文件，修改其内容
3. **同步到 Postman** — 使用 Postman MCP 的 `updateCollectionRequest` 工具将修改后的内容同步到 Postman Collection 中
4. **验证** — 在 Postman 中运行修改后的接口，确认问题已修复

### 适用场景

- 修复 test script 中的数据提取逻辑（如字段路径错误、匹配条件不对）
- 调整请求参数（如 Headers、Body、Query Params）
- 修改 pre-request script 逻辑
- 更新硬编码的筛选条件（如 targetCompany、targetSite 等）

---

## 情况 2：需要添加或删除步骤接口

当需要在调用链中新增、删除或重排接口时，必须同步修改 api-plan 文件以保持一致性。

### 步骤

1. **定位问题** — 确认需要新增/删除/调整的接口及原因
2. **修改 api-plan 文件** — 更新 `*.api-plan.md` 中的以下部分：
   - `API Sequence` — 添加/删除/重排接口序号
   - `User Input Data` — 如有新增用户输入参数，补充对应表格
   - `Data Flow` — 更新数据传递关系
   - `API Notes` — 添加/删除对应接口的补充说明
   - `Instruction` — 更新执行指令描述
3. **修改本地 JSON 文件** — 在 `{collection-folder}/` 目录下：
   - 新增接口：创建新的 `{序号}-{接口名}.json` 文件
   - 删除接口：删除对应的 JSON 文件
   - 重排序号：重命名受影响的 JSON 文件以保持序号连续
4. **同步到 Postman** — 使用 Postman MCP 工具同步变更：
   - 新增接口：使用 `createCollectionRequest` 添加（注意：新请求默认追加到 Collection 末尾）
   - 删除接口：使用 `deleteCollectionRequest` 删除
   - 修改接口：使用 `updateCollectionRequest` 更新
   - **调整顺序（必须）**：新增接口后，必须使用 `transferCollectionRequests` 将其移动到正确位置。参数格式：
     - `ids`：要移动的 request UID 数组（格式 `{ownerId}-{requestId}`）
     - `mode`：`"move"`
     - `target`：`{"id": "{ownerId}-{collectionId}", "model": "collection"}`
     - `location`：`{"id": "{ownerId}-{前一个requestId}", "model": "request", "position": "after"}`
5. **验证** — 在 Postman 中运行完整 Collection，确认调用链正常

### 适用场景

- 发现遗漏的前置查询接口（如缺少 site 选择步骤）
- 调用链中某个接口不再需要
- 需要在两个步骤之间插入新的数据查询接口
- 接口顺序需要调整

---

## 注意事项

- 修改本地 JSON 文件后，必须同步到 Postman，不能只改本地不同步
- 情况 2 中修改 api-plan 是必须的，确保文档与实际 Collection 保持一致
- 同步到 Postman 时使用 `updateCollectionRequest`（修改已有接口）或 `createCollectionRequest`（新增接口），必须串行执行，不可并行
- 如果修改涉及 test script 中的数据传递逻辑，需要检查下游接口是否受影响
