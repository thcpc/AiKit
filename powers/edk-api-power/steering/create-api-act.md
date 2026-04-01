# 创建 API 操作定义文件工作流

## 概述

本工作流引导用户逐步创建 `*.api-act.md` 格式的 API 操作定义文件。

---

## 步骤 1：收集基本信息

通过对话了解用户的需求：

1. **场景名称** — 这个 API 操作场景叫什么？（用于文件命名，如 `user-onboard`）
2. **Swagger 地址** — 提供一个或多个 Swagger/OpenAPI 文档的 URL
3. **BaseURL** — 每个服务的基础 URL，格式为 `{ServiceName}BaseUrl: {url}`

## 步骤 2：定义 API 调用顺序

引导用户定义 API 的调用顺序：

1. 询问用户需要调用哪些 API 端点
2. 确认调用顺序（哪个先，哪个后）
3. 格式化为编号列表：`{序号}.{service}/{endpoint}`

**示例：**
```markdown
## API Sequence

### User Onboard:
- 1.admin/auth
- 2.admin/user/onboard/company
- 3.admin/user/onboard/applications
- 4.admin/user/onboard
- 5.procheck/auth
- 6.procheck/study/list
```

## 步骤 3：收集用户输入数据

询问用户需要提供哪些输入数据：

1. 按逻辑分组（如 Login Info、Company Info 等）
2. 每个字段包含字段名和示例值
3. 敏感信息使用占位符（如 `"xxx"`）

**示例：**
```markdown
## User Input Data

### Login Info
username: "testuser"
password: "xxx"

### Company Info
company: "Test Corp"
lifecycle: "Phase 1"
```

## 步骤 4：编写执行指令

引导用户描述数据处理逻辑：

1. 如何根据 Swagger 定义转换用户输入数据为请求格式
2. 如何将前一个 API 的返回数据传递给下一个 API
3. 任何特殊的数据处理规则

**默认指令模板：**
```markdown
## Instruction

According to the Swagger definition, automatically convert the following user input data 
into the required request format for each api, call the api in sequence, and automatically 
pass the key data returned by the previous api to the next one.
```

用户可以在此基础上自定义。

## 步骤 5：收集 API 补充说明（可选但强烈推荐）

询问用户是否有需要补充的接口说明，这些信息能显著提高后续同步到 Postman 的正确率：

1. **接口参数差异** — 某些接口的参数可能和 Swagger 描述不完全一致，或者有特殊要求
2. **数据传递关系** — 哪个接口的数据传给哪个接口
3. **特殊逻辑** — 如密码加密、空 body、特殊 header 等

**引导问题：**
- "有没有哪些接口的请求参数比较特殊？比如 body 为空、需要加密、或者参数和 Swagger 不一致？"
- "接口之间的数据是怎么传递的？比如哪个接口的返回值需要传给后面的接口？"

**如果用户提供了补充信息，生成以下可选部分：**

```markdown
## API Notes

### 1.admin/auth
- method: POST
- body: {"userName": "xxx", "password": "xxx"}
- note: 需要加密密码

### 5.procheck/auth
- method: POST
- body: {}
- headers: Authorization 使用 Step 4 返回的 token
- note: 不需要用户名密码

## Data Flow

- Step 1 → token, userId
- Step 2 → companyId
- Step 3 → applicationId, sponsorId, envId
- Step 4 → onboard_token (用于 Step 5)
- Step 5 → procheck_token (用于 Step 6)
```

## 步骤 6：生成文件

将收集到的所有信息组合成 `*.api-act.md` 文件：

1. 文件名格式：`{场景名称}.api-act.md`（kebab-case）
2. 保存到用户指定的目录（默认为工作区根目录）
3. 生成后展示文件内容供用户确认

## 步骤 7：确认和修改

1. 展示生成的文件内容
2. 询问用户是否需要修改
3. 根据反馈进行调整
4. 确认最终版本

---

## 注意事项

- 如果用户提供了 Swagger URL，尝试使用 fetch 工具获取 API 定义以辅助生成
- API Sequence 中的端点名称应与 Swagger 定义中的路径一致
- User Input Data 中的字段名应与 API 请求参数对应
- 文件应保持 Markdown 格式的可读性
