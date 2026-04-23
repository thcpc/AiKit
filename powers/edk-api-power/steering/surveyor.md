# 问卷调查工作流（Surveyor）

## 概述

当用户请求创建 API Plan 但未提供足够信息（缺少 `*.api-form.md` 文件、未提供场景名称/Swagger/BaseURL/目标接口等关键信息）时，本工作流自动生成一份问卷文件 `questionnaire.api-form.md`，引导用户填写必要信息后再继续创建 Plan。

---

## 触发条件

当以下任一条件满足时，触发 Surveyor 工作流：

1. 用户请求创建 Plan，但**未提供** `*.api-form.md` 文件
2. 用户请求创建 Plan，但提供的信息不足以启动 Planner（缺少场景名称、Swagger 地址、BaseURL、目标接口中的**两项或以上**）
3. 用户明确要求创建问卷/表单

### 信息充足性判断

Planner 启动所需的**最低信息**：
- **场景名称** — 必需
- **Swagger 地址** — 必需（至少一个）
- **BaseURL** — 必需（至少一个）
- **目标接口** — 必需（接口路径 + HTTP method）
- **请求来源文件** — 可选（`*.postman_collection.json` 或 `*.har`）

如果用户提供了 `*.api-form.md` 文件且其中包含以上必需信息，则直接进入 Planner 工作流，不触发 Surveyor。

---

## 步骤 1：检查是否存在 api-form 文件

1. 检查用户消息中是否引用了 `*.api-form.md` 文件
2. 检查 workspace 根目录下是否存在 `*.api-form.md` 文件
3. 如果找到，读取文件内容并验证信息完整性（参见"信息充足性判断"）
4. 如果信息完整，直接将文件传递给 Planner 工作流
5. 如果文件不存在或信息不完整，进入步骤 2

---

## 步骤 2：生成问卷文件

1. 读取模板文件 `~/.kiro/powers/repos/edk-api-power/powers/edk-api-power/template/api-form.md`
2. 在 workspace 根目录下创建 `questionnaire.api-form.md`，内容复制自模板
3. 如果用户已提供了部分信息（如场景名称或 Swagger 地址），将已知信息预填到问卷中

---

## 步骤 3：提示用户

向用户输出以下提示信息：

```
已为你创建了问卷文件 questionnaire.api-form.md，请在文件中填写以下信息：

1. 场景名称 — 这个 API 操作场景叫什么
2. Swagger 地址 — Swagger/OpenAPI 文档的 URL
3. BaseURL — 每个服务的基础 URL
4. 接口名 — 目标接口的路径
5. 接口类型 — POST / GET / DELETE 等
6. 引用数据 — 可选，提供 Postman Collection JSON 或 HAR 文件路径

填写完毕后，请告诉我"根据 questionnaire.api-form.md 创建 Plan"。
```

---

## 步骤 4：等待用户回复

当用户回复以下任一内容时，进入 Planner 工作流：
- "根据 questionnaire.api-form.md 创建 Plan"
- "根据 xxx.api-form.md 创建 Plan"
- "api-form 填好了"
- "问卷填好了"
- "继续创建 Plan"
- 任何包含 `api-form` 和 `plan` 关键词的消息

此时读取对应的 `*.api-form.md` 文件，提取信息后传递给 Planner。

---

## 关键规则

1. **不要跳过问卷**：如果信息不足，必须先生成问卷，不要通过多轮对话逐一询问
2. **预填已知信息**：如果用户已提供了部分信息，在问卷中预填，减少用户工作量
3. **模板路径固定**：模板文件始终位于 `~/.kiro/powers/repos/edk-api-power/powers/edk-api-power/template/api-form.md`
4. **问卷文件位置固定**：生成的问卷文件始终位于 workspace 根目录
5. **文件命名**：默认命名为 `questionnaire.api-form.md`，如果用户指定了场景名称，可命名为 `{场景名称}.api-form.md`
