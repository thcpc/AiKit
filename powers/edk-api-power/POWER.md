---
name: "edk-api-power"
displayName: "EDK API Power"
description: "引导用户创建 API 操作定义文件（*.api-act.md），并通过 Postman MCP 在 Postman 桌面客户端中自动创建 Collection。支持 Swagger 定义解析、API 顺序编排和数据自动传递。"
keywords: ["edk", "api", "postman", "collection", "swagger", "api-act"]
author: "PengchengChen"
---

# EDK API Power

## Overview

EDK API Power 是一个引导式 MCP Power，提供三个核心工作流：

1. **创建 API 操作定义文件** — 通过交互式引导，帮助用户创建 `*.api-act.md` 格式的 API 操作定义文件，包含 Swagger 地址、BaseURL、API 调用顺序、用户输入数据和执行指令。
2. **执行 API 操作并同步到 Postman** — 读取 `*.api-act.md` 文件，通过 Postman MCP 在 Postman 桌面客户端中创建对应的 Collection。
3. **启动加密服务** — 启动本地加密服务（`scripts/encrypt-server.js`），为 Admin Auth 等需要密码加密的接口提供 RSA 加密支持。

## Available Steering Files

- **create-api-act** — 引导用户创建 `*.api-act.md` API 操作定义文件的完整工作流
- **sync-to-postman** — 读取 `*.api-act.md` 文件并通过 Postman MCP 创建 Collection 的工作流
- **encrypt-service** — 启动加密服务并在 API 调用中使用密码加密的工作流

## Onboarding

### 前置条件

- 已安装 Postman 桌面客户端
- 已获取 Postman API Key（在 Postman 设置 > API Keys 中生成）
- 已安装 Node.js（用于运行 Postman MCP Server）

### 安装 Postman MCP Server

Power 安装后会自动配置 Postman MCP Server。首次使用前，请确保在 `mcp.json` 中替换 API Key 占位符。

### 验证安装

安装完成后，可以在 Kiro 中使用 Postman MCP 的 `getAuthenticatedUser` 工具验证连接是否正常。

## Common Workflows

### 工作流 1：创建 API 操作定义文件

通过交互式引导创建 `*.api-act.md` 文件。

**步骤：**
1. 告诉 agent 你要创建一个 API 操作定义文件
2. 提供 Swagger 文档地址
3. 提供 BaseURL 信息
4. 定义 API 调用顺序
5. 提供用户输入数据（登录信息等）
6. 描述执行指令（数据如何在 API 之间传递）
7. Agent 生成 `*.api-act.md` 文件

**详细指引请读取 `create-api-act` steering 文件。**

### 工作流 2：同步到 Postman

读取已有的 `*.api-act.md` 文件，通过 Postman MCP 创建 Collection。

**步骤：**
1. 指定要同步的 `*.api-act.md` 文件
2. Agent 解析文件内容
3. Agent 通过 Postman MCP 创建 Collection 和 Requests
4. 在 Postman 桌面客户端中查看结果

**详细指引请读取 `sync-to-postman` steering 文件。**

### 工作流 3：启动加密服务

启动本地加密服务，为 Admin Auth 接口提供密码加密。

**步骤：**
1. 使用 `node scripts/encrypt-server.js` 启动加密服务（监听 `http://localhost:9876`）
2. 在调用 Admin Auth 接口前，先 POST `http://localhost:9876/encrypt` 发送 `{ "password": "明文密码" }`
3. 获取返回的 `{ "encrypted": "加密后的密码" }`
4. 将加密后的密码作为 Admin Auth 接口的 password 字段值

**详细指引请读取 `encrypt-service` steering 文件。**

## 密码加密规则

当 API Sequence 中包含 `admin/auth`（Admin Auth）接口时，必须通过 Postman pre-request script 动态加密密码：

1. 确保加密服务已启动（`http://localhost:9876`）
2. 创建 Admin Auth Request 时，请求体中保留明文密码
3. 通过 `createCollectionRequest` 的 `events` 参数添加 pre-request script
4. Script 在运行时自动调用 `POST http://localhost:9876/encrypt` 加密密码并替换请求体
5. **禁止**将加密后的密码写死在请求体中，必须通过 pre-request script 动态加密

## api-act.md 文件格式规范

`*.api-act.md` 文件是一个 Markdown 格式的 API 操作定义文件，包含以下部分：

### 必需部分

#### 1. Api Meta Information

包含 Swagger 文档地址和 BaseURL 定义。

```markdown
## Api Meta Information

### Swagger
- {swagger_url_1}
- {swagger_url_2}

### BaseURL
- {ServiceName}BaseUrl: {base_url}
```

#### 2. API Sequence

定义 API 的调用顺序，格式为 `{序号}.{service}/{endpoint}`。

```markdown
## API Sequence

### {场景名称}:
- 1.{service}/{endpoint}
- 2.{service}/{endpoint}
- 3.{service}/{endpoint}
```

#### 3. User Input Data

定义用户输入的数据，按逻辑分组。

```markdown
## User Input Data

### {分组名称}
{field}: "{value}"
{field}: "{value}"
```

#### 4. Instruction

描述执行指令，说明如何处理 API 调用和数据传递。

```markdown
## Instruction

{自然语言描述如何根据 Swagger 定义转换数据、调用 API、传递上下文数据}
```

### 可选部分（强烈推荐）

#### 5. API Notes

针对每个接口的补充说明，用于弥补 Swagger 文档无法表达的业务逻辑。这些信息能显著提高 Collection 创建的正确率。

```markdown
## API Notes

### 1.admin/auth
- method: POST
- body: {"userName": "xxx", "password": "xxx"}
- note: 需要通过 pre-request script 加密密码

### 4.admin/user/onboard
- method: POST
- body: {"applicationId": int, "sponsorId": int, "envId": int, "workForCompanyId": int, "companyLevelLogin": false}
- note: 不需要 userId 和 roleId；数据来自 Step 2 和 Step 3

### 5.procheck/auth
- method: POST
- body: {}
- headers: Authorization 使用 Step 4 onboard 后返回的 token
- note: 不需要用户名密码，通过 onboard token 认证

### 6.procheck/study/list
- method: POST
- body: {}
- note: Swagger 中是 POST 不是 GET
```

支持的字段：
- `method` — 覆盖 Swagger 中的方法（当 Swagger 不准确时）
- `body` — 请求体示例，明确哪些字段需要、哪些不需要
- `headers` — 额外的 header 说明
- `note` — 任何补充说明（加密、数据来源、特殊逻辑等）
- `response` — 响应数据结构示例（帮助编写 post-response script）

#### 6. Data Flow

描述接口之间的数据传递关系，明确每个接口需要从哪个前置接口获取哪些数据。

```markdown
## Data Flow

- Step 1 → token, userId
- Step 2 → companyId (作为 workForCompanyId)
- Step 3 → applicationId (=systemId), sponsorId, envId, roleId
- Step 4 → onboard_token (用于 Step 5)
- Step 5 → procheck_token (用于 Step 6)
```

#### 7. Reference Collection

提供一个从浏览器 DevTools 导出的 Postman Collection JSON 文件作为参考。这是最可靠的参考来源，包含了每个接口的真实 method、headers、body 和 URL。

```markdown
## Reference

- #[[file:temp.postman_collection.json]]
```

使用方式：
- 将浏览器中正确的操作流程通过 DevTools Network 面板导出为 HAR 或 Postman Collection 格式
- 文件中包含真实的请求参数、headers、body，可作为创建 Collection 时的权威参考
- 当 Swagger 定义与参考文件冲突时，以参考文件为准（因为它是实际可工作的请求）

## Troubleshooting

### Postman MCP 连接失败

**问题：** MCP Server 无法启动或连接
**解决方案：**
1. 确认 Node.js 已安装：`node --version`
2. 确认 API Key 正确：检查 `mcp.json` 中的 `POSTMAN_API_KEY`
3. 手动测试：`npx @postman/postman-mcp-server --full`
4. 重启 Kiro

### Swagger 文档无法访问

**问题：** 无法获取 Swagger 定义
**解决方案：**
1. 确认 Swagger URL 可以在浏览器中访问
2. 检查网络连接和 VPN 设置
3. 如果是内网地址，确保开发环境可以访问

### Collection 创建失败

**问题：** Postman MCP 创建 Collection 时报错
**解决方案：**
1. 确认 Postman API Key 有足够权限
2. 检查 Postman Workspace 是否存在
3. 查看 MCP 工具返回的错误信息

## Best Practices

- **编写 post-response script 前必须先详细阅读 Swagger 响应定义**：这是最重要的规则。必须在 Swagger 中找到接口的 Response definition，递归展开所有 `$ref`，完整理解返回数据的嵌套结构后，再编写数据提取代码。禁止猜测字段名或数据结构。
- 每个 `*.api-act.md` 文件对应一个完整的 API 操作场景
- API Sequence 中的顺序应反映实际的业务流程
- User Input Data 中避免硬编码敏感信息，使用占位符
- Instruction 部分尽量详细描述数据传递逻辑
- 文件命名建议使用场景名称，如 `user-onboard.api-act.md`
- **URL 必须严格按照 api-act.md 中的 BaseURL + Swagger path 构建，不要自行拼接或猜测**
- **请求体字段名必须严格使用 Swagger definitions 中定义的字段名（区分大小写），不要使用 User Input Data 中的原始字段名**
- **Authorization Header 不加 任何前缀**：直接使用 token 值，如 `{{admin_token}}`

## MCP Config Placeholders

- **`YOUR_POSTMAN_API_KEY`**: 你的 Postman API Key。
  - **获取方式：**
    1. 打开 Postman 桌面客户端
    2. 点击右上角头像 > Settings
    3. 选择 API Keys 标签
    4. 点击 "Generate API Key" 生成新的 Key
    5. 复制 Key 值替换此占位符

---

**MCP Server:** `@postman/postman-mcp-server`
**模式:** Full（包含所有 Postman API 工具）
