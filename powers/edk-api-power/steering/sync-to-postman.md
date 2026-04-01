# 同步到 Postman 工作流

## 概述

本工作流读取 `*.api-act.md` 文件，解析其中的 API 定义，并通过 Postman MCP 在 Postman 桌面客户端中创建对应的 Collection。

---

## 步骤 1：读取 api-act.md 文件

1. 用户指定要同步的 `*.api-act.md` 文件路径
2. 读取并解析文件内容
3. 提取以下信息：
   - Swagger 地址列表
   - BaseURL 映射
   - API 调用顺序
   - 用户输入数据
   - 执行指令
   - **API Notes（如有）** — 每个接口的补充说明（method、body、headers、note）
   - **Data Flow（如有）** — 接口之间的数据传递关系

### 信息优先级规则（关键）

当 api-act.md 中包含 `API Notes`、`Data Flow` 或 `Reference` 部分时，这些信息的优先级高于从 Swagger 推断的信息：

1. **Reference Collection 中的真实请求** > 一切其他来源（这是实际可工作的请求，最可靠）
2. **API Notes 中的 method** > Swagger 中的 method
3. **API Notes 中的 body 示例** > 从 Swagger definitions 推断的 body
4. **API Notes 中的 headers** > 默认的 header 设置
5. **Data Flow 中的数据传递关系** > 自行推断的数据传递逻辑

**Reference Collection 使用规则：**
- 如果 api-act.md 中通过 `#[[file:xxx.json]]` 引用了参考 Collection 文件，必须先读取该文件
- 从参考文件中提取每个 API Sequence 对应接口的：method、headers、body、URL
- 参考文件中的 Authorization header 值是硬编码的 token，需要替换为 Postman 变量（如 `{{admin_token}}`）
- 参考文件中的 token 前缀（如 `Admin`、`PROCHECK`）揭示了 Authorization 的格式规则：admin 接口用 `Admin {{token}}`，procheck 接口用 `PROCHECK {{token}}`
- 参考文件中的 body 内容揭示了真实的请求参数结构，优先于 Swagger 定义

如果 API Notes 明确说明某个接口的 body 为 `{}`，则不要添加任何字段。
如果 API Notes 明确说明某个接口不需要用户名密码，则不要传入。

## 步骤 2：获取 Swagger 定义

1. 使用 fetch 工具访问 Swagger URL
2. 解析 API 端点定义（路径、方法、参数、请求体格式）
3. 将 API Sequence 中的端点与 Swagger 定义匹配

## 步骤 2.5：密码加密处理（如有 admin/auth 接口）

如果 API Sequence 中包含 `admin/auth` 接口，且 User Input Data 中有 password 字段：

1. 确保加密服务已启动（使用 `controlPwshProcess` 启动 `node scripts/encrypt-server.js`）
2. **不要**将加密后的密码写死在请求体中
3. 在创建 Admin Auth Request 时，请求体中保留明文密码
4. 通过 `createCollectionRequest` 的 `events` 参数添加 pre-request script，脚本内容如下：

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

5. `events` 参数格式：
```json
[{
    "listen": "prerequest",
    "script": {
        "type": "text/javascript",
        "exec": ["上述脚本内容（每行一个数组元素）"]
    }
}]
```

## 步骤 3：确认 Postman Workspace

1. 使用 Postman MCP 的 `getWorkspaces` 工具列出可用的 Workspace
2. 询问用户要在哪个 Workspace 中创建 Collection
3. 如果需要，使用 `createWorkspace` 创建新的 Workspace

## 步骤 4：创建 Collection

1. 使用 Postman MCP 的 `createCollection` 工具创建新的空 Collection（不要包含任何 placeholder 占位请求）
2. Collection 名称建议使用 api-act.md 文件中的场景名称
3. 严格按照 API Sequence 定义的顺序，依次使用 `createCollectionRequest` 逐个添加 Request（必须按 1→2→3→...→N 的顺序串行创建，不可并行，以确保最终顺序与定义一致）

### 创建 Request 的规则

对于 API Sequence 中的每个端点：

1. **确定 HTTP 方法** — 从 Swagger 定义中获取（GET/POST/PUT/DELETE 等）
2. **构建 URL** — 严格使用 api-act.md 中定义的 BaseURL + Swagger 中的 path（见下方 URL 构建规则）
3. **设置 Headers** — 根据 Swagger 定义设置 Content-Type 等
4. **构建 Request Body** — 必须严格根据 Swagger 中该接口的 `parameters` 定义来构建（见下方请求参数验证规则）
5. **添加描述** — 包含端点说明和数据传递逻辑

### 请求参数验证规则（严格，最重要）

**构建每个 Request 的参数（body、query、header）之前，必须先详细阅读 Swagger 中该接口的 `parameters` 定义，确认该接口需要哪些参数、参数位置（in: body/query/header/path）和参数类型。**

**这是最重要的规则。不遵守此规则会导致传入错误的参数，造成接口调用失败。**

验证步骤：
1. 在 Swagger 中找到该接口的 `parameters` 数组
2. 检查每个参数的 `in` 字段（body/query/header/path）
3. 如果有 `in: body` 参数，查看其 `schema` 引用的 definition，获取完整的字段列表
4. 如果没有 `in: body` 参数，则该接口不需要 request body（body 应为 `{}` 或不传）
5. 不同服务的同名接口（如 admin/auth 和 procheck/auth）参数可能完全不同，必须分别查看各自的 Swagger 定义

**禁止：**
- 不要假设同名接口的参数相同（如 admin 的 `/auth` 需要 userName/password，但 procheck 的 `/auth` 可能只需要 Authorization header）
- 不要将 User Input Data 中的字段直接塞入 request body，必须先确认 Swagger 中该接口是否需要这些字段
- 不要猜测参数，必须从 Swagger 定义中获取

### URL 构建规则（严格）

**URL = api-act.md 中的 BaseURL + Swagger 中的 path**

构建步骤：
1. 根据 API Sequence 中的 service 前缀（如 `admin/`、`procheck/`）确定使用哪个 BaseURL
2. 根据 API Sequence 中的端点名称，在对应的 Swagger 文档中查找匹配的 path
3. 最终 URL = BaseURL + Swagger path

**示例：**
- API Sequence: `admin/auth` → 在 admin Swagger 中查找 → 匹配 `/auth` → URL = `AdminBaseUrl + /auth`
- API Sequence: `admin/user/onboard/company` → 匹配 `/user/onboard/company` → URL = `AdminBaseUrl + /user/onboard/company`
- API Sequence: `procheck/auth` → 在 procheck Swagger 中查找 → 匹配 `/auth` → URL = `ProCheckBaseUrl + /auth`
- API Sequence: `procheck/study/list` → 匹配 `/procheck/study/list` → URL = `ProCheckBaseUrl + /procheck/study/list`

**禁止：**
- 不要自行拼接或猜测 URL 路径
- 不要混淆 Swagger basePath 和 api-act.md 中的 BaseURL
- api-act.md 中的 BaseURL 已经包含了服务的完整前缀，直接拼接 Swagger path 即可

### 字段名验证规则（严格）

**请求体中的字段名必须严格使用 Swagger definitions 中定义的字段名，区分大小写。**

验证步骤：
1. 找到 Swagger 中该接口引用的 definition（如 `$ref: "#/definitions/login information"`）
2. 读取该 definition 的 `properties`，获取所有字段名
3. 请求体中的字段名必须与 definition 中的 `properties` key 完全一致（包括大小写）
4. 将 User Input Data 中的字段映射到 Swagger 字段名

**示例：**
- Swagger definition `login information` 中字段为 `userName`（不是 `username`）
- User Input Data 中 `username: "CPC01"` → 映射为 `"userName": "CPC01"`

**禁止：**
- 不要使用 User Input Data 中的原始字段名作为请求体字段名
- 不要猜测字段名，必须从 Swagger definitions 中获取

### 数据传递处理

根据 Instruction 部分的描述：

1. 标注哪些字段来自用户输入
2. 标注哪些字段来自前一个 API 的响应
3. 在 Request 描述中说明数据来源

### 响应数据结构分析规则（严格，最重要）

**编写 post-response script（test script）之前，必须先详细阅读 Swagger 中该接口的响应（Response）定义，完整理解返回数据的结构，然后再编写数据提取代码。**

**这是最重要的规则，直接决定数据传递是否正确。不遵守此规则会导致后续接口全部失败。**

分析步骤：
1. 在 Swagger 文档中找到该接口的 `responses` 定义（通常是 `200` 响应）
2. 查看响应引用的 `$ref` definition，递归展开所有嵌套的 `$ref`，直到获得完整的数据结构树
3. 特别注意以下几点：
   - 字段名的大小写（如 `systemId` 不是 `applicationId`）
   - 数据类型（array vs object，嵌套层级）
   - 嵌套结构（如 `payload` 是数组，数组元素中又包含子数组）
4. 根据完整的数据结构树编写提取代码，确保正确导航每一层嵌套

**禁止：**
- 不要猜测响应数据结构，必须从 Swagger 定义中获取
- 不要假设字段名（如不要假设有 `applicationId` 字段，要看 Swagger 中实际叫什么）
- 不要忽略嵌套结构（如响应可能是 `payload[].onboardSponsorList[].onboardEnvs[].onboardRoleList[]` 这样的多层嵌套）
- 不要使用 `target.xxx || target.yyy` 这种猜测式写法，应该使用 Swagger 中明确定义的字段名

**示例 — 正确做法：**

假设 Swagger 定义的响应结构为：
```
Response 200:
  procCode: integer
  payload: array of SystemDto
    SystemDto:
      systemId: integer
      systemName: string
      onboardSponsorList: array of SponsorDto
        SponsorDto:
          sponsorId: integer
          name: string
          onboardEnvs: array of EnvDto
            EnvDto:
              id: integer
              name: string
              onboardRoleList: array of RoleDto
                RoleDto:
                  id: integer
                  roleName: string
```

则 post-response script 应该按照此结构逐层导航：
```javascript
const res = pm.response.json();
if (res.procCode === 200 && res.payload) {
    const systems = Array.isArray(res.payload) ? res.payload : [res.payload];
    // 根据 Swagger 定义，用 systemName 查找，用 systemId 提取
    const target = systems.find(s => s.systemName === 'PROCHECK');
    if (target) {
        pm.collectionVariables.set('applicationId', String(target.systemId));
        // 继续导航嵌套结构
        if (target.onboardSponsorList && target.onboardSponsorList.length > 0) {
            const sponsor = target.onboardSponsorList.find(s => s.name === 'Edetek') || target.onboardSponsorList[0];
            pm.collectionVariables.set('sponsorId', String(sponsor.sponsorId));
            // 继续导航下一层
            if (sponsor.onboardEnvs && sponsor.onboardEnvs.length > 0) {
                const env = sponsor.onboardEnvs.find(e => e.name === 'dev') || sponsor.onboardEnvs[0];
                pm.collectionVariables.set('envId', String(env.id));
                if (env.onboardRoleList && env.onboardRoleList.length > 0) {
                    pm.collectionVariables.set('roleId', String(env.onboardRoleList[0].id));
                }
            }
        }
    }
}
```

**示例 — 错误做法（禁止）：**
```javascript
// ❌ 错误：猜测字段名，不看 Swagger 定义
const target = apps.find(a => a.applicationName === 'PROCHECK' || a.name === 'PROCHECK');
pm.collectionVariables.set('applicationId', String(target.applicationId || target.id));
// ❌ 错误：忽略嵌套结构，假设 sponsorId 在顶层
if (target.sponsorId) pm.collectionVariables.set('sponsorId', String(target.sponsorId));
```

### 自动数据传递规则（关键）

**每个 Request 必须通过 test script（post-response script）提取响应中的关键数据，并设置为 Postman Collection 变量，供后续请求自动使用。**

**前提条件：必须先完成上方「响应数据结构分析」，确认完整的响应数据结构后，再编写提取代码。**

实现方式：通过 `createCollectionRequest` 的 `events` 参数添加 `listen: "test"` 类型的 script。

**编写 test script 的标准流程：**
1. 阅读 Swagger 中该接口的 Response definition，展开所有 `$ref`，画出完整数据结构树
2. 确定需要提取哪些字段（供后续接口使用）
3. 根据数据结构树编写逐层导航的提取代码
4. 每个提取的变量添加 `console.log` 输出，方便调试

**Auth 接口的 test script 必须提取 token：**
```javascript
const res = pm.response.json();
if (res.procCode === 200 && res.payload) {
    pm.collectionVariables.set("admin_token", res.payload.token || res.payload);
}
```

**Onboard 类接口的 test script 必须提取后续步骤需要的 ID：**
- company 接口 → 先阅读 Swagger Response 定义，确认字段名后提取 companyId
- applications 接口 → 先阅读 Swagger Response 定义，确认完整嵌套结构后提取 applicationId, sponsorId, envId, roleId 等
- onboard 接口 → 先阅读 Swagger Response 定义，确认字段名后提取 token 或 session 信息

**events 参数格式（同时包含 prerequest 和 test）：**
```json
[
    {
        "listen": "prerequest",
        "script": { "type": "text/javascript", "exec": ["..."] }
    },
    {
        "listen": "test",
        "script": { "type": "text/javascript", "exec": ["..."] }
    }
]
```

## 步骤 5：设置 Environment（可选）

1. 使用 `createEnvironment` 创建环境变量
2. 将 BaseURL 设置为环境变量
3. 将用户输入数据中的通用字段设置为环境变量

## 步骤 6：自动验证与修正（必须执行）

**所有 Request 创建完成后，必须执行以下自动验证流程。验证不通过的项必须立即调用 `updateCollectionRequest` 修正，不得跳过。**

### 6.1 读取已创建的 Collection

1. 使用 `getCollection` 获取 Collection 的完整结构（使用 `model=full`）
2. 遍历所有 Request，逐个使用 `getCollectionRequest`（带 `populate=true`）读取完整的请求详情

### 6.2 逐条验证注意事项

对每个 Request 执行以下检查：

#### 检查 1：Authorization Header 不加任何前缀（最高优先级）

- 读取 Request 的 `headerData`，找到 `Authorization` header
- 验证其 value 是否为纯 Postman 变量格式（如 `{{admin_token}}`、`{{onboard_token}}`、`{{procheck_token}}`）
- **不合规判定**：value 中包含任何前缀文本（如 `Admin {{token}}`、`PROCHECK {{token}}`、`Bearer {{token}}`）
- **修正方式**：调用 `updateCollectionRequest` 更新 `headerData`，移除所有前缀，只保留 `{{variable_name}}`

#### 检查 2：URL 必须是字符串格式

- 验证 Request 的 `url` 字段是纯字符串，不是对象格式
- **不合规判定**：`url` 是 `{"raw": "..."}` 对象格式
- **修正方式**：调用 `updateCollectionRequest` 将 `url` 更新为纯字符串

#### 检查 3：Integer 类型字段不能用 Postman 变量模板

- 检查 `rawModeData`（request body）中是否有 `"{{variableName}}"` 格式的值用于 Integer 类型字段
- **不合规判定**：body 中存在 `"{{companyId}}"` 或 `"{{applicationId}}"` 等应为 Integer 的字段使用了字符串模板
- **修正方式**：确保该 Request 有 pre-request script 通过 `parseInt()` 动态构建请求体

#### 检查 4：接口顺序一致性

- 验证 Collection 中 Request 的顺序与 api-act.md 中 API Sequence 定义的顺序一致
- **不合规判定**：顺序不匹配
- **修正方式**：使用 `transferCollectionRequests` 调整顺序

#### 检查 5：无 placeholder 占位请求

- 验证 Collection 中不存在名为 "placeholder" 或 URL 为 "http://placeholder" 的请求
- **不合规判定**：存在占位请求
- **修正方式**：调用 `deleteCollectionRequest` 删除

### 6.3 输出验证报告

验证完成后，输出简要报告：
- 列出检查的 Request 数量
- 列出发现的问题数量和已修正的项
- 如果全部通过，提示用户可以在 Postman 中 Run Collection

---

## Postman MCP 常用工具

以下是本工作流中常用的 Postman MCP 工具：

- `getWorkspaces` — 获取 Workspace 列表
- `createWorkspace` — 创建新 Workspace
- `createCollection` — 创建 Collection
- `updateCollection` — 更新 Collection
- `createEnvironment` — 创建 Environment
- `createCollectionFolder` — 在 Collection 中创建文件夹
- `createCollectionRequest` — 在 Collection 中创建 Request

## 注意事项

- **禁止 placeholder 占位请求**：创建 Collection 时，不要在 `item` 中放入任何 placeholder 或占位请求。应先创建空 Collection，再逐个添加真实 Request。
- **严格保证接口顺序**：Request 的创建顺序必须与 API Sequence 中定义的顺序完全一致。必须按序号 1→2→3→...→N 串行调用 `createCollectionRequest`，不可并行创建，否则 Postman 中的显示顺序会错乱。
- **Authorization Header 不加任何前缀**：所有请求的 Authorization header 值直接使用 token 值（如 `{{admin_token}}`），不要添加任何前缀。 优先级最高，严格执行
- **createCollection 中 URL 必须用字符串格式**：在 `createCollection` 的 item 中定义 request 时，`url` 字段必须使用纯字符串（如 `"url": "http://example.com/api/auth"`），不要使用对象格式（如 `"url": {"raw": "..."}`），否则 Postman 可能无法正确解析 URL。
- **Integer 类型字段不能用 Postman 变量模板**：当 Swagger 定义中字段类型为 Integer 时，不要在 raw body 中直接写 `"{{variableName}}"`（会被当作字符串）。应通过 pre-request script 使用 `parseInt(pm.collectionVariables.get('variableName'))` 动态构建请求体。
- 创建 Collection 前先确认 Postman MCP 连接正常
- 如果 Swagger URL 无法访问，提示用户手动提供 API 定义
- 大量 API 时分批创建，避免超时
- 创建完成后建议用户在 Postman 中手动验证
