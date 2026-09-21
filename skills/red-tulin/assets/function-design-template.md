---
tags: [代码设计模板]
author: {{hostname}}
created: {{date:YYYY-MM-DD HH:mm:ss}}
updated: {{date:YYYY-MM-DD HH:mm:ss}}
language: [{{language}},{{version}}]
namespace: {{namespace}}
filename: {{filename}}
status: {{status}} (创建时默认状态为 Designing)
---
# 代码设计模板

> 使用说明：
> 1. 按需填写下面的章节，不适用的章节可以删除
> 2. 带 `<!-- -->` 的内容是填写说明，完成后可删除

---

## 函数定义

<!-- 独立函数（不属于任何类）。每个函数一个子章节。-->

### 函数调用流程
用(plantuml/mermaid)或分步列表描述 描述函数调用顺序和并行关系。


### 函数：{functionName}

<!-- 一句话描述函数职责 -->

#### 输入参数

| 参数名 | 类型 | 必填 | 说明 | 参考文件 |
|--------|------|------|------|---------|
| | | | | <!-- 如果参数结构来自某个文件/接口，填路径 --> |

#### 处理

<!-- 逐条描述处理逻辑，按执行顺序 -->
1. ...
2. ...

<!-- ⚠️ 注意：{需要特别关注的边界情况或约束} -->

#### 输出

| 返回类型 | 说明 |
|---------|------|
| | |

<!-- 如果返回复杂结构，用表格或代码块描述 -->
```
{
  "field1": "string",
  "field2": number
}
```

<!-- 「变更记录」章节格式统一定义在 assets/change-log-section.md 中，由 create_design.py 自动拼接到本文档末尾，此处不再重复。-->