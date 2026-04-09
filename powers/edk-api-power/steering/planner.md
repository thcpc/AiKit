# 创建 API 操作定义文件工作流

## 概述

本工作流引导用户创建 `*.api-plan.md` 格式的 API 操作定义文件。通过分析 Postman Collection JSON 文件，自动提取目标接口的前置依赖链、数据流和用户输入参数，直接生成 api-plan.md 文件。

---

## 步骤 1：收集基本信息并提取 API 请求

通过对话了解用户的需求：

1. **场景名称** — 这个 API 操作场景叫什么？（用于文件命名，如 `user-onboard`）
2. **Swagger 地址** — 提供一个或多个 Swagger/OpenAPI 文档的 URL
3. **BaseURL** — 每个服务的基础 URL，格式为 `{ServiceName}BaseUrl: {url}`
4. **Postman Collection JSON 文件** — 用户提供 `*.postman_collection.json` 文件路径
5. **目标接口** — 用户指定要分析哪个接口的前置条件

从 JSON 文件的 `item` 数组中提取所有 API 请求，过滤掉非 API 请求（静态资源 `.svg`、`.json` 翻译文件、`segment.io`、`mixpanel.com` 等第三方服务），记录每个请求的：
- 序号（在 Collection 中的出现顺序）
- URL path
- HTTP method
- Authorization header 的值（token 前缀揭示服务类型，如 `Admin`、`DESIGN`、`PROCHECK`）
- Request body（如有）

### 步骤 2：识别认证链

1. 找到第一个 `POST /auth` 请求（通常是 `admin/auth`），标记为认证起点
2. 追踪 Authorization header 中 token 前缀的变化，识别 token 切换点：
   - `Admin xxx` → 使用 admin_token
   - `DESIGN xxx` → 使用 design_token（说明之前有 design/auth）
   - `PROCHECK xxx` → 使用 procheck_token（说明之前有 procheck/auth）
3. 找到所有 `*/auth` 接口，确定认证链顺序
4. 找到 `*/user/onboard` 相关接口（company → applications → onboard），确定 onboard 链
5. **从 Swagger 读取 Response 结构**：对认证链中的每个接口，使用 mcp-swagger 的 `getEndpointDetails` 工具读取其 Response 定义，然后使用 `getSchemas` 工具递归展开引用的 Schema。**如果 `getSchemas` 返回空或失败，则启用 mcp-fetch fallback 策略**（参见下方"Schema 获取 Fallback 策略"章节）。通过 Swagger Response 结构来：
   - 确认 token 字段的实际路径（如 `payload.token` 还是 `data.accessToken`）
   - 确认 onboard/company 返回的数据结构（是数组还是对象、字段名是 `id` 还是 `companyId`、筛选字段是 `name` 还是 `companyName`）
   - 确认 onboard/applications 返回的嵌套结构（onboardSponsorList、onboardStudyList、onboardEnvs 等字段的实际名称和层级关系）
   - **禁止仅凭 Collection 中的硬编码值猜测 Response 结构**，必须以 Swagger 定义为准

### 步骤 3：分析目标接口的参数依赖

1. 读取目标接口的 request body
2. 提取 body 中所有参数字段及其值
3. **从 Swagger 读取前置接口的 Response 结构**：对调用链中每个前置接口，使用 mcp-swagger 的 `getEndpointDetails` 工具读取其 Response 定义，然后使用 `getSchemas` 工具递归展开所有引用的 Schema。**如果 `getSchemas` 返回空或失败，则启用 mcp-fetch fallback 策略**（参见下方"Schema 获取 Fallback 策略"章节）。完整理解返回数据的嵌套结构。这一步是**必须的**，不能跳过，原因如下：
   - 准确判断前置接口返回的是单条记录还是多条记录（数组/列表/树）
   - 确认产出数据的字段名（如 `id` vs `companyId`、`systemId` vs `applicationId`）
   - 理解嵌套结构的层级关系（如 `onboardSponsorList[].onboardStudyList[].onboardEnvs[]`）
   - 为后续编写 post-response script 提供准确的字段路径
   - **禁止仅凭接口路径名称或 Collection 中的硬编码值猜测 Response 结构**
4. 对每个参数值，反向追踪来源：
   - **ID 类型参数**（如 `formId: 369`）：搜索 URL 路径包含该 ID 的 GET 请求，或在目标接口之前出现的列表/树接口。**但必须判断该前置接口返回的是单条记录还是多条记录（列表/树）**：
     - 如果前置接口返回**单条记录**（如 `/user/info` 返回当前用户信息），则 ID 可以自动提取，标记为"前置接口"
     - 如果前置接口返回**多条记录**（如 `/folder/tree` 返回多个 form、`/items/{id}` 返回多个 item），则该 ID 代表用户的**选择**，必须标记为 🔸用户输入。因为无法自动决定用户要操作哪一条记录
     - **判断依据**：接口路径包含 `list`、`tree`、复数名词（如 `items`、`questions`、`folders`）时，通常返回多条记录
   - **嵌套结构中通过名称定位 ID（关键模式）**：当前置接口返回嵌套的列表/树结构时，ID 不是用户直接输入的值，而是通过**名称匹配**从嵌套结构中定位出来的中间变量。此时真正的用户输入是用于定位的名称，而非 ID 本身。必须分析嵌套结构的层级关系，识别每一层需要的筛选名称。
     - **示例 1（onboard/applications）**：`applicationId: 4` 不是用户输入，而是通过 `applicationName: "Designer"` 从 `onboard/applications` 返回的嵌套列表 `[application → sponsors → lifecycles → studies]` 中匹配出来的。真正的用户输入是 `applicationName`、`sponsorName`、`lifecycleName`、`studyName`。
     - **示例 2（crf/folder/tree）**：`formId: 369` 不是用户输入，而是通过 `visitName: "Response Assessment Screening/Baseline"` + `formName: "Target Lesions Assessment"` 从 `crf/folder/tree` 返回的嵌套树结构 `[list(visit/folder) → formList(form)]` 中匹配出来的。真正的用户输入是上层节点名称（visit/folder name）和 form 名称。
     - **识别方法**：当 Swagger Response Schema 显示返回的是多层嵌套结构（对象数组中包含子对象数组），且每层都有 `id` + `name` 字段时，该 ID 几乎一定是通过名称匹配定位的中间变量。
     - **User Input Data 中的表达**：不应将 `formId` 列为用户输入，而应列出定位所需的名称字段（如 `visitName`、`formName`），并在 Instruction 中说明如何通过名称在嵌套结构中匹配 ID。
   - **Token 类型参数**：追踪 Authorization header 的来源
   - **用户输入参数**（如 `controlType: "Text"`、`name: "TT"`、`caption: "Test1"`）：标记为 🔸用户输入
   - **Onboard 接口的筛选条件参数**：onboard/applications 返回的嵌套结构中，用户需要指定 company、applicationName、sponsor、lifecycle、study 等名称来匹配对应的 ID，这些名称是用户输入参数

### 步骤 4：构建完整调用链

按以下优先级排序：
1. 认证接口（admin/auth → onboard 链 → 子系统 auth）
2. 数据查询接口（获取 ID 的列表/树接口）
3. 目标接口

对于每个接口记录：
- 序号、HTTP method + URL path
- 需要的前置数据（Authorization token、query params、path params）
- 产出的数据（token、ID 等）

**从 Swagger 验证调用链中每个接口的 Request 和 Response 结构**：使用 mcp-swagger 的 `getEndpointDetails` 工具逐一读取调用链中每个接口的完整定义（包括 Request parameters/body 和 Response schema），然后使用 `getSchemas` 工具递归展开引用的 Schema。**如果 `getSchemas` 返回空或失败，则启用 mcp-fetch fallback 策略**（参见下方"Schema 获取 Fallback 策略"章节）。目的是：
- 验证调用链中每个接口的 HTTP method 是否与 Swagger 定义一致（Collection 中可能有误）
- 确认每个接口的 Request body/query/path 参数的字段名和类型
- 确认每个接口的 Response 结构，明确产出数据的字段路径
- 如果 Swagger 定义与 Collection 中的实际请求存在冲突，在分析报告中标注差异

### 步骤 5：构建数据流

以树形结构展示每个接口产出的数据如何流向后续接口：
```
Step N (接口路径) [需要: 前置数据]
  └→ 产出数据1 (用途说明)
  └→ 产出数据2 (用途说明)
```

**数据流中的字段路径必须基于 Swagger Response 结构**：每个"产出数据"的字段路径（如 `payload.token`、`payload[].id`、`payload[].onboardSponsorList[].sponsorId`）必须来自步骤 2-4 中通过 mcp-swagger 或 mcp-fetch fallback 读取的 Response Schema，不能凭猜测或 Collection 中的硬编码值推断。数据流中应标注：
- 产出数据的完整字段路径（如 `response.payload.token`）
- 该字段在 Swagger Schema 中的类型（如 `string`、`integer`、`array`）
- 如果产出数据来自数组/列表，标注需要的筛选条件

### 步骤 6：标注用户输入参数

遍历目标接口 body 中的所有字段，将无法从前置接口自动获取的参数标注为用户输入：
- 字符串类型的名称、标签、描述字段（如 `name`、`caption`、`cdashVariable`）
- 枚举/选择类型字段（如 `controlType`、`dataType`）
- 布尔开关字段（如 `required`、`detailsField`）
- 固定配置字段（如 `length`、`recordIds`）

**基于 Swagger Response 结构判断参数是否可自动获取**：判断某个参数是否为用户输入时，必须参考步骤 2-4 中通过 mcp-swagger 或 mcp-fetch fallback 读取的前置接口 Response Schema：
- 如果前置接口的 Response Schema 中明确包含该字段（如 `id`、`token`），且返回的是单条记录，则该参数可自动获取
- 如果前置接口的 Response Schema 显示返回的是数组（`type: array`）或嵌套列表结构，则从中提取的 ID 必须标记为 🔸用户输入
- 如果 Swagger Response Schema 中找不到某个字段的来源，则该参数必须标记为 🔸用户输入

**递归分析中间接口的筛选条件（关键，不可遗漏）：**

不仅分析目标接口的 body，还要递归分析调用链中每个中间接口的参数。当某个中间接口（如 onboard）的参数 ID 来自前置列表/树接口时，必须追问：
- 前置接口返回的是列表还是单个对象？
- 如果是列表，用什么条件从列表中筛选出这个特定 ID？
- 筛选条件（如 company 名称、sponsor 名称、lifecycle 名称、study 名称）就是用户输入参数

**示例：** `onboard` 接口的 `sponsorId: 361` 来自 `onboard/applications` 返回的嵌套列表，用户需要指定 sponsor 名称 "Edetek" 才能匹配到 361。因此 `sponsor: "Edetek"` 是用户输入参数。

**列表/树接口返回的 ID 必须视为用户输入（关键，不可遗漏）：**

当某个 ID 参数的来源是一个返回多条记录的接口（如 `folder/tree`、`items/{id}`、`questions/{id}`）时，不能假设"自动取第一条"，必须将该 ID 标记为 🔸用户输入。原因是：用户需要从多条记录中**选择**要操作的那一条，这个选择行为本身就是用户输入。

**更准确地说：ID 是中间变量，名称才是用户输入。** 当前置接口返回嵌套结构时，用户实际提供的是用于定位的**名称**（如 `formName`、`visitName`），ID 只是通过名称匹配后提取的中间值。因此在 User Input Data 中应列出名称字段而非 ID 字段。

**示例 1：** `crf/item` 接口的 `formId: 369` 来自 `crf/folder/tree` 返回的嵌套树结构。用户需要指定 `visitName: "Response Assessment Screening/Baseline"` 和 `formName: "Target Lesions Assessment"` 来定位 `formId: 369`。因此 User Input Data 中应列出 `visitName` 和 `formName`，而非 `formId`。`formId` 是 post-response script 通过名称匹配自动提取的中间变量。

**示例 2：** `onboard` 接口的 `sponsorId: 361` 来自 `onboard/applications` 返回的嵌套列表，用户需要指定 sponsor 名称 "Edetek" 才能匹配到 361。因此 `sponsorName: "Edetek"` 是用户输入参数，`sponsorId` 是中间变量。

**判断规则：** 如果一个前置接口的路径包含 `list`、`tree`、复数名词（`items`、`questions`、`folders`、`studies`），或其响应是数组/树结构，则从中提取的 ID 默认为用户输入参数，除非用户明确说明可以自动选择（如"取第一个"）。

**重要区分：** 即使列表/树接口产出的 ID 标记为用户输入，也不意味着该接口应从调用链中移除。如果该接口是目标接口的**必要前置查询**（用户需要先调用它才能看到可选项并做出选择），则应保留在调用链中。只有当用户可以直接提供 ID 而无需查询该接口时（如 formId 可以直接指定），才将该接口从调用链中移除。

在输出的参数来源表中，用 🔸 标记用户输入参数。

### 步骤 7：自检

生成完成后，执行以下自检：

1. **调用链完整性**：目标接口 body 中每个 ID 类型参数（integer 值）都能追溯到调用链中某个前置接口
2. **认证链连续性**：从 admin/auth 到目标接口，token 传递没有断裂
3. **无遗漏的数据查询接口**：URL 中包含动态 ID 的 GET 请求（如 `/items/{formId}`）已被纳入调用链
4. **用户输入参数标注完整**：所有非 ID、非 token 的参数都已标注来源
5. **无冗余接口**：调用链中没有包含与目标接口无关的噪音请求
6. **列表/树接口的 ID 未被误判为自动获取**：检查调用链中每个"产出 ID"的接口，如果该接口返回多条记录（list/tree/复数），则产出的 ID 应标记为用户输入，而非前置接口自动提取。**但要区分两种情况**：
   - **接口是目标接口的必要前置查询**（如 `crf/items/{formId}` 提供 itemgroupId 的可选列表、`crf/questions/{formId}` 提供 questionId 的可选列表）：**保留在调用链中**，但产出的 ID 标记为 🔸用户输入。因为用户需要先调用该接口才能看到可选项并做出选择。
   - **接口仅是 ID 的间接来源，且 ID 可以由用户直接提供**（如 `crf/folder/tree` 之于 formId，用户可以直接指定 formId 而无需先查询树结构）：**从调用链中移除**，将对应 ID 移入 User Input Data。
   - **判断标准**：如果目标接口的某个参数 ID 必须通过调用该列表接口才能获得有效值（即用户无法凭空提供），则该列表接口是必要前置，应保留在调用链中。
7. **树/文件夹结构查询接口未被遗漏**：检查 Collection 中是否存在路径包含 `tree`、`folder`、`structure` 的 GET 请求。如果目标接口的某个 ID 参数（如 `formId`）的可选值来自这类树结构接口，则该接口应作为必要前置查询保留在调用链中（产出的 ID 标记为 🔸用户输入）。常见遗漏场景：
   - `crf/folder/tree` 提供 formId 的可选列表（用户需要看到树结构才能选择目标 form）
   - `study/tree` 或 `project/tree` 提供 studyId、projectId 的可选列表
   - **判断标准**：如果用户在 UI 上需要先浏览树/文件夹结构再点击选择，则对应的查询接口是必要前置，不能省略
8. **嵌套结构中 ID 与名称的区分正确**：检查所有来自嵌套列表/树结构的 ID 参数，确认 User Input Data 中列出的是用于定位的**名称字段**（如 `formName`、`visitName`、`sponsorName`），而非 ID 本身（如 `formId`、`sponsorId`）。ID 是通过名称匹配从嵌套结构中提取的中间变量，不应作为用户输入。具体检查：
   - 每个来自嵌套结构的 ID，是否已识别出对应的名称筛选字段
   - 多层嵌套结构中，是否每一层的名称字段都已列出（如 `folder/tree` 需要 `visitName` + `formName` 两层名称）
   - Instruction 中是否说明了如何通过名称在嵌套结构中逐层匹配定位 ID
   - **反例**：如果 User Input Data 中出现 `formId: 🔸` 而没有 `formName` 和 `visitName`，则说明遗漏了名称字段
9. **Swagger Response 结构验证**：确认分析报告中所有字段路径、数据类型、嵌套结构均来自 mcp-swagger 或 mcp-fetch fallback 读取的 Swagger 定义，而非猜测。具体检查：
   - 每个前置接口的"产出数据"字段路径是否与 Swagger Response Schema 一致
   - 数据流中标注的字段类型（单条/数组/嵌套）是否与 Swagger Schema 的 `type` 定义一致
   - 如果 Swagger 定义缺失或不完整，在自检结果中标注 `⚠️ Swagger 定义缺失`，并说明使用了 Collection 中的实际请求作为补充参考
   - 如果使用了 mcp-fetch fallback，在自检结果中标注 `ℹ️ 通过 mcp-fetch fallback 获取 Schema`

如果自检发现问题，在输出文件末尾添加 `## ⚠️ 自检问题` 章节列出。

### 步骤 8：生成 api-plan.md

完成分析和自检后，直接生成 `*.api-plan.md` 文件（不再单独生成分析报告文件）：

1. 从调用链提取 API Sequence
2. 从用户输入参数汇总提取 User Input Data（按使用接口分组的表格格式）
3. 从数据流提取 Data Flow
4. 从调用链中各接口的 method、body、headers 提取 API Notes
5. 补充 Swagger 地址和 BaseURL（询问用户或从 Collection 中的 URL 推断）
6. 生成 Instruction（使用默认模板）
7. 将 Collection JSON 文件作为 Reference 引用
8. **文件命名使用场景名称**（步骤 1 中收集的场景名称），格式为 `{场景名称}.api-plan.md`，如 `designer-add-crf-item.api-plan.md`。不要使用 JSON 文件名命名。
9. 在文件末尾添加 `## ✅ 自检结果` 章节，记录步骤 7 的自检结果

生成后进入步骤 9（确认和修改）。

### 步骤 9：确认和修改

1. 展示生成的文件内容
2. 询问用户是否需要修改
3. 根据反馈进行调整
4. 确认最终版本

### 关键规则

1. **不要遗漏业务数据依赖**：不仅分析认证链，还要分析 body 中每个 ID 参数的来源接口
2. **URL 中的路径参数也是依赖**：如 `/crf/items/369` 中的 `369` 来自前置接口
3. **过滤噪音请求**：Collection 中可能包含大量并行 UI 加载请求，这些不是直接前置依赖
4. **区分必需前置和可选前置**：认证链和提供参数的接口是必需前置
5. **Authorization header 不加任何前缀**：所有 Authorization 值直接使用 token 变量（如 `{{admin_token}}`）
6. **用户输入参数必须标注**：所有无法自动获取的参数用 🔸 标记
7. **请严格按照步骤舒徐**

---

## Schema 获取 Fallback 策略

当 mcp-swagger 的 `getSchemas` 工具返回空或失败时（常见于大型 Swagger 文档超过 500KB 的情况），必须使用 mcp-fetch 工具直接从 Swagger JSON 文档中提取 Schema 定义。

### 触发条件

在步骤 2、3、4、5、6、7 中，当需要通过 `getSchemas` 展开某个 Schema 引用（如 `$ref: "#/definitions/CrfSimpleFormItemCreateRequest"`）时：
1. 先尝试调用 mcp-swagger 的 `getSchemas` 工具
2. 如果返回空结果（`"No schemas found"` 或空对象），则切换到 mcp-fetch fallback

### Fallback 操作步骤

1. **确定 Swagger JSON URL**：从步骤 1 收集的 Swagger 地址获取（如 `http://example.com/api/design/v2/api-docs`）

2. **提取目标 Schema 名称**：从 `getEndpointDetails` 返回的 `$ref` 字段中提取 Schema 名称。例如：
   - `"$ref": "#/definitions/Response«LoginAuthenticationResponse»"` → 目标名称为 `LoginAuthenticationResponse`
   - `"$ref": "#/definitions/CrfSimpleFormItemCreateRequest"` → 目标名称为 `CrfSimpleFormItemCreateRequest`

3. **使用 mcp-fetch 分段搜索**：Swagger JSON 文档通常很大，需要分段读取。使用 `mcp_fetch_fetch` 工具，通过 `start_index` 参数分段扫描 `definitions` 部分：
   ```
   # 第一次调用，从文档中后部开始（definitions 通常在 paths 之后）
   mcp_fetch_fetch(url=swagger_url, max_length=10000, start_index=400000)
   
   # 如果未找到目标 Schema，调整 start_index 继续搜索
   mcp_fetch_fetch(url=swagger_url, max_length=10000, start_index=450000)
   
   # 持续调整直到找到目标 Schema 名称
   ```

4. **定位策略**：
   - Swagger 2.0 文档结构为 `{"swagger":"2.0", ..., "paths":{...}, "definitions":{...}}`
   - `definitions` 部分通常在文档的后半部分（约 50%-90% 位置）
   - 搜索目标 Schema 名称字符串（如 `"CrfSimpleFormItemCreateRequest"`）
   - 找到后，向前后扩展读取范围以获取完整的 Schema 定义（包括所有 properties）

5. **递归展开引用**：如果提取的 Schema 中包含嵌套的 `$ref` 引用（如 `"$ref": "#/definitions/CrfItemDefinitionDto"`），需要继续用同样的方法提取被引用的 Schema，直到所有引用都被展开

6. **解析 Schema 结构**：从原始 JSON 文本中提取以下信息：
   - `type`：对象类型（`object`、`array` 等）
   - `properties`：所有字段及其类型、描述、示例值
   - `required`：必填字段列表
   - 嵌套的 `$ref` 引用及其展开后的结构

### 示例

假设需要获取 `CrfSimpleFormItemCreateRequest` 的 Schema：

```
# 步骤 1：getSchemas 失败
mcp_swagger_design_getSchemas(schemaName="CrfSimpleFormItemCreateRequest") → 返回空

# 步骤 2：使用 mcp-fetch fallback
mcp_fetch_fetch(
  url="http://example.com/api/design/v2/api-docs",
  max_length=10000,
  start_index=520000  # 从文档后半部分开始搜索
)

# 步骤 3：在返回内容中搜索 "CrfSimpleFormItemCreateRequest"
# 找到后提取完整定义：
# {
#   "type": "object",
#   "required": ["definition", "generate", "requireReviewDto"],
#   "properties": {
#     "definition": {"$ref": "#/definitions/CrfItemDefinitionDto"},
#     "formId": {"type": "integer", "format": "int32"},
#     "generate": {"$ref": "#/definitions/CrfItemGenerateDto"},
#     "itemgroupId": {"type": "integer", "format": "int32"},
#     "requireReviewDto": {"$ref": "#/definitions/RequireReviewDto"}
#   }
# }

# 步骤 4：递归展开 CrfItemDefinitionDto、CrfItemGenerateDto、RequireReviewDto
# 用同样的 mcp-fetch 方法搜索并提取这些子 Schema
```

### 注意事项

- mcp-fetch 返回的是原始 JSON 文本，需要手动解析（不是格式化的 JSON 对象）
- 大型文档可能需要多次调用 mcp-fetch 才能找到目标 Schema
- 每次调用建议 `max_length=10000`，避免单次返回过多内容
- 如果 Swagger URL 是 HTTP（非 HTTPS），`webFetch` 工具不可用，必须使用 `mcp_fetch_fetch`
- 在自检结果中标注使用了 fallback 策略：`ℹ️ 通过 mcp-fetch fallback 获取 Schema（getSchemas 返回空）`

---

## 注意事项

- 如果用户提供了 Swagger URL，使用 mcp-swagger 的 `searchEndpoints` 和 `getEndpointDetails` 工具按需获取 API 定义以辅助生成，不要一次性拉取整个 Swagger 文档
- API Sequence 中的端点名称应与 Swagger 定义中的路径一致
- User Input Data 中的字段名应与 API 请求参数对应
- 文件应保持 Markdown 格式的可读性
