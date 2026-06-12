# Baize Schema（知识库配置规范）

> 这个文件告诉 AI 如何维护你的知识库。你和 AI 可以一起调整它。

## 知识库信息

- 创建日期：{{date:YYYY-MM-DD HH:mm:ss}}
- 语言：{{LANGUAGE}}
- 版本：1.1
- WIKI_ROOT：{{WIKI_ROOT}}

## 目录结构

```
$WIKI_ROOT/
├── raw/
│   ├── sprial/             # Sprial 上的内容
│   ├── notes/              # 自己整理的片段笔记
│   ├── teams/              # Teams 聊天片段
│   └── assets/             # 图片等附件
├── wiki/
│   └── {topicName}/
│       ├── overview.md
│       ├── index.md
│       ├── entities/
│       ├── concepts/
│       ├── procedures/
│       ├── rules/
│       ├── comparisons/
│       ├── summaries/
│       └── synthesis/
├── queries/
├── log.md
├── topics.md
├── .baize-cache.json
└── .baize-schema.md
```

## 素材类型路由

| 来源 | raw 目录 | 提取方式 |
|------|----------|----------|
| Sprial 内容 | `raw/sprial/` | 直接读取 |
| 自己的笔记 | `raw/notes/` | 直接读取 |
| Teams 聊天 | `raw/teams/` | 直接读取 |
| 纯文本粘贴 | `raw/notes/` | 直接使用 |
| 图片等附件 | `raw/assets/` | 由其他文件引用 |

## 别名词表（Alias Table）

格式：每行一组同义词，用 `=` 分隔。

```
（初始为空，随使用积累）
```

维护原则：
- 只收录知识库里实际出现过的同义词
- 每组控制在 5 个以内
- 中英文混用时把最常用的放第一个

## 外部知识库（External Knowledge Bases）

| 名称 | 类型 | 路径 | SKILL | 说明 |
|------|------|------|-------|------|
| （未配置）| | | | |

> 使用 `extend-kb` 工作流添加新的外部知识库。
> - **名称**：知识库显示名称（如 "BA Knowledge Base"）
> - **类型**：`baize`（edk-baize 格式）或其他格式
> - **路径**：知识库的绝对路径
> - **SKILL**：查询时使用的 SKILL 名称（如 `edk-baize-ba-read`）
> - **说明**：简要描述知识库内容

## 置信度标注规范

每个 wiki 页面（concept/entity/procedure/rule/summary）的 frontmatter 必须包含 `confidence` 字段：

```yaml
---
confidence: EXTRACTED   # 可回溯到原文的事实
# 或
confidence: INFERRED    # 从原文推断出的结论
# 或
confidence: AMBIGUOUS   # 原文表述模糊，难以确定含义
# 或
confidence: UNVERIFIED  # 无法在原文中找到依据
---
```

⛔ lint 检查会统计各置信度数量，并要求抽查 EXTRACTED 条目的可回溯性。

## Lint（健康检查）

详细检查项见 SKILL 的 references/lint-checklist.md。

