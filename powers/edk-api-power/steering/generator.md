# Generator 工作流

## 概述

本工作流读取 `*.api-plan.md` 文件，解析其中的 API 定义，生成符合 Postman Collection v2.1 格式的 JSON 文件到本地文件夹中。生成完成后征求用户确认，再决定是否同步到 Postman。

---

## 步骤 1：读取 api-plan.md 文件

1. 用户指定要处理的 `*.api-plan.md` 文件路径
2. 读取并解析文件内容
3. 提取以下信息：
   - Swagger 地址列表
   - BaseURL 映射
   - API 调用顺序（API Sequence）
   - 用户输入数据（User Input Data）
   - 执行指令（Instruction）
   - **API Notes（如有）** — 每个接口的补充说明
   - **Data Flow（如有）** — 接口之间的数据传递关系
   - **Reference Collection（如有）** — 参考 Collection JSON 文件

### 1.1 信息优先级规则

当 api-plan.md 中包含 `API Notes`、`Data Flow` 或 `Reference` 部分时，优先级如下：

1. **Reference Collection 中的真实请求** > 一切其他来源
2. **API Notes 中的 method** > Swagger 中的 method
3. **API Notes 中的 body 示例** > 从 Swagger definitions 推断的 body
4. **API Notes 中的 headers** > 默认的 header 设置
5. **Data Flow 中的数据传递关系** > 自行推断的数据传递逻辑

**Reference Collection 使用规则：**
- 如果 api-plan.md 中通过 `#[[file:xxx.json]]` 引用了参考 Collection 文件，必须先读取该文件
- 从参考文件中提取每个 API Sequence 对应接口的：method、headers、body、URL
- 参考文件中的 Authorization header 值是硬编码的 token，需要替换为 Postman 变量（如 `{{admin_token}}`）
- 参考文件中的 body 内容揭示了真实的请求参数结构，优先于 Swagger 定义

如果 API Notes 明确说明某个接口的 body 为 `{}`，则不要添加任何字段。



## 步骤 2：通过 mcp-swagger 按需读取 Swagger 定义

**核心原则：不要一次性拉取整个 Swagger 文档。使用 mcp-swagger MCP Server 按需读取每个接口的定义。**

### 3.1 配置 mcp-swagger

api-plan.md 中可能包含多个 Swagger URL。按以下策略处理：

- 在工作区的 `.kiro/settings/mcp.json` 中为每个 Swagger URL 配置一个独立的 mcp-swagger server 实例
- 命名规则：`swagger-{service}`（如 `swagger-admin`、`swagger-design`）

**操作步骤：**
1. 从 api-plan.md 的 `Swagger` 部分提取所有 Swagger URL
2. 检查工作区 `.kiro/settings/mcp.json` 中是否已配置对应的 mcp-swagger 实例
3. 如果未配置，自动添加配置
4. 根据 API Sequence 中的 service 前缀确定使用哪个 mcp-swagger 实例

### 3.2 按需读取接口定义

对 API Sequence 中的每个接口，使用 mcp-swagger 的工具按需读取：

- `getEndpointDetails` — 获取单个接口的完整定义（path + method）
- `getSchemas` — 获取指定 Schema/DTO 的定义
- `searchEndpoints` — 按关键词搜索接口

### 3.3 Swagger 路径匹配规则

去掉 service 前缀（如 `admin/`、`design/`），剩余部分即为 Swagger path。

| API Sequence 中的写法 | 对应的 Swagger path | 使用的 mcp-swagger 实例 |
|----------------------|--------------------|-----------------------|
| `admin/auth` | `/auth` | `swagger-admin` |
| `design/crf/folder/tree` | `/crf/folder/tree` | `swagger-design` |
| `procheck/study/list` | `/procheck/study/list` | `swagger-procheck` |


## 步骤 3：查询 apiRepository（Manager 交互）

对 API Sequence 中的每个接口，通过 `api_repository_manager.py` 查询是否已有记录：

```bash
py powers/edk-api-power/scripts/api_repository_manager.py query --api "{接口名}"
```

> **Python 命令兼容性：** 优先使用 `py`（Windows Launcher），如果失败则依次尝试 `python3`、`python`。

- 接口名格式：API Sequence 中的写法（如 `admin/auth`、`design/crf/folder/tree`）
- 如果返回非空结果，读取对应的映射文件内容作为参考
  ** 如果有多个，让用户指定选择哪个作为参考 **
- 参考已有的 Collection JSON 可以减少 Swagger 查询次数，提高生成质量
- ** 编写 event.script 逻辑时需参考读取的Swagger信息和已有接口的 event.script **，

## 步骤 4：密码加密处理（如有 admin/auth 接口）

如果 API Sequence 中包含 `admin/auth` 接口，且 User Input Data 中有 password 字段：

1. 确保加密服务已启动（使用 `controlPwshProcess` 启动 `node scripts/encrypt-server.js`）
2. 在生成的 Admin Auth Request JSON 中，请求体保留明文密码
3. 添加 pre-request script 通过 `http://localhost:9876/encrypt` 动态加密

pre-request script 内容：
```javascript
const password = pm.request.body ? JSON.parse(pm.request.body.raw).password : '';
pm.sendRequest({
    url: 'http://localhost:9876/encrypt',
    method: 'POST',
    header: { 'Content-Type': 'application/json' },
    body: { mode: 'raw', raw: JSON.stringify({ password: password }) }
}, function (err, res) {
    if (!err && res.code === 200) {
        const encrypted = res.json().encrypted;
        const body = JSON.parse(pm.request.body.raw);
        body.password = encrypted;
        pm.request.body.raw = JSON.stringify(body);
    }
});
```

## 步骤 5：创建输出文件夹

**文件夹命名规则：** 取 `*.api-plan.md` 文件名中 `*.api-plan.md` 之前的部分。

示例：
- `designer-add-crf-item.api-plan.md` → 文件夹名：`designer-add-crf-item`
- `procheck-study-list.api-plan.md` → 文件夹名：`procheck-study-list`

在工作区根目录下创建该文件夹。

## 步骤 6：为每个接口生成 JSON 文件

对 API Sequence 中的每个接口，生成一个独立的 JSON 文件。

### 6.1 文件命名规则

格式：`{序号}-{接口名}.json`

- 序号：API Sequence 中的序号，保持两位数（如 `01`、`02`）
- 接口名：将 API Sequence 中的路径转为 kebab-case，去掉 service 前缀

示例（以 `designer-add-crf-item.api-plan.md` 为例）：
```
designer-add-crf-item/
├── 01-auth.json
├── 02-user-onboard-company.json
├── 03-user-onboard-applications.json
├── 04-user-onboard.json
├── 05-design-auth.json
├── 06-crf-folder-tree.json
├── 07-crf-items.json
├── 08-crf-questions.json
└── 09-crf-item.json
```

### 6.2 JSON 文件格式

每个 JSON 文件遵循 Postman Collection v2.1 的 Request 格式：

```json
{
  "name": "{步骤序号}. {接口描述}",
  "request": {
    "method": "POST",
    "header": [
      { "key": "Content-Type", "value": "application/json" },
      { "key": "Authorization", "value": "{{admin_token}}" },
      { "key": "Language-Content", "value": "en_US" }
    ],
    "body": {
      "mode": "raw",
      "raw": "{\"userName\":\"CPC01\",\"password\":\"Admin@123\"}"
    },
    "url": {
      "raw": "http://dev-03-app-01.chengdudev.edetekapps.cn/api/admin/auth",
      "protocol": "http",
      "host": ["dev-03-app-01", "chengdudev", "edetekapps", "cn"],
      "path": ["api", "admin", "auth"]
    }
  },
  "event": [
    {
      "listen": "prerequest",
      "script": {
        "type": "text/javascript",
        "exec": ["// pre-request script lines"]
      }
    },
    {
      "listen": "test",
      "script": {
        "type": "text/javascript",
        "exec": ["// post-response script lines"]
      }
    }
  ]
}
```

### 6.3 构建每个 Request 的规则

对每个接口：

1. **确定 HTTP 方法** — 优先使用 API Notes > Reference Collection > Swagger 定义
2. **构建 URL** — `BaseURL + Swagger path`
3. **设置 Headers** — Content-Type、Authorization（使用 `{{variable}}` 格式，不加任何前缀）、Language-Content 等
4. **构建 Request Body** — 严格根据 Swagger `parameters` 定义构建（见下方验证规则）
5. **添加 events** — pre-request script（如密码加密、Integer 字段处理）和 test script（数据提取）

### 6.4 请求参数验证规则（严格）

构建每个 Request 的参数前，必须先通过 mcp-swagger 的 `getEndpointDetails` 工具确认：
- 该接口需要哪些参数
- 参数位置（in: body/query/header/path）
- 参数类型

**禁止：**
- 不要假设同名接口的参数相同
- 不要将 User Input Data 中的字段直接塞入 request body
- 不要猜测参数

### 6.5 字段名验证规则（严格）

请求体中的字段名必须严格使用 Swagger definitions 中定义的字段名，区分大小写。

### 6.6 响应数据结构分析与 test script

编写 test script 前，必须先通过 `getEndpointDetails` + `getSchemas` 获取完整的响应数据结构树，然后再编写数据提取代码。

**Auth 接口的 test script 必须提取 token：**
```javascript
const res = pm.response.json();
if (res.procCode === 200 && res.payload) {
    pm.collectionVariables.set("admin_token", res.payload.token || res.payload);
}
```

### 6.7 Authorization Header 规则

所有请求的 Authorization header 值直接使用 Postman 变量，不加任何前缀：
- `{{admin_token}}`
- `{{design_token}}`
- `{{procheck_token}}`

### 6.8 Integer 类型字段处理

当 Swagger 定义中字段类型为 Integer 时，不要在 raw body 中直接写 `"{{variableName}}"`。应通过 pre-request script 使用 `parseInt()` 动态构建请求体。

## 步骤 7：生成汇总 Collection JSON（可选）

在文件夹中额外生成一个 `_collection.json`，将所有接口按顺序组合为完整的 Postman Collection v2.1 格式：

```json
{
  "info": {
    "name": "{场景名称}",
    "schema": "https://schema.getpostman.com/json/collection/v2.1.0/collection.json"
  },
  "item": [
    // 按顺序包含所有 Request
  ]
}
```

## 步骤 8：征求用户确认

**⚠️ 必须在此暂停并征求用户确认，不可跳过此步骤直接进入步骤 10。**

**生成所有 JSON 文件后，必须征求用户确认再决定是否同步到 apiRepository**

向用户展示：
1. 生成的文件夹路径和文件列表
2. 每个接口的摘要（序号、名称、Method、URL）
3. 询问用户：

```
JSON 文件已生成到 {folder_name}/ 目录下，共 {count} 个接口文件。
是否要将这些接口同步到 apiRepository？
```


## 步骤 9：提交到 apiRepository（Manager 交互）


1. 遍历 Generator 输出文件夹中的所有接口 JSON 文件
2. 对每个文件，从 API Sequence 提取接口名，从 api-plan.md 文件名提取所属集合名
3. 按 Manager 操作逻辑判断操作类型：
   - 先查询 `py powers/edk-api-power/scripts/api_repository_manager.py query --api "{接口名}"`
   - 如果不存在 → 执行 `add_new`
   - 如果存在 → 比较 event.script 逻辑相似性，决定执行 `update` 场景1（追加集合）或场景2（覆盖文件）或 `add_new`（新记录）
4. 逐个执行操作，报告结果

**集合名提取规则：** 取 `*.api-plan.md` 文件名中 `.api-plan.md` 之前的部分。
示例：`designer-add-crf-item.api-plan.md` → 集合名：`designer-add-crf-item`


## 步骤 10：征求用户确认

**生成所有 JSON 文件后，必须征求用户确认再决定是否同步到 Postman。**

向用户展示：
1. 生成的文件夹路径和文件列表
2. 每个接口的摘要（序号、名称、Method、URL）
3. 询问用户：

```
JSON 文件已生成到 {folder_name}/ 目录下，共 {count} 个接口文件。
是否要将这些接口同步到 Postman？
```

提供选项：
- **同步到 Postman** — 继续执行 sender 工作流的步骤 3-6（确认 Workspace → 创建 Collection → 验证修正）
- **仅保留本地文件** — 结束工作流，用户可以手动导入或后续再同步
- **修改后再同步** — 用户可以手动编辑 JSON 文件后再触发同步



## 步骤 11：同步到 Postman（用户确认后）

如果用户选择同步，执行以下操作：

1. **确认 Postman Workspace** — 使用 `getWorkspaces` 列出可用 Workspace，询问用户选择
2. **创建 Collection** — 使用 `createCollection` 创建空 Collection
3. **逐个添加 Request** — 读取文件夹中的 JSON 文件，按序号顺序使用 `createCollectionRequest` 逐个添加（必须串行，不可并行）
4. **自动验证与修正** — 执行 sender 中步骤 6 的验证流程



---

## 注意事项

- 文件夹和 JSON 文件在工作区根目录下生成
- JSON 文件按序号排列，方便用户查看和编辑
- 同步到 Postman 前必须征求用户同意
- 所有 sender 中的严格规则（参数验证、字段名验证、URL 构建、响应分析等）同样适用于本工作流
