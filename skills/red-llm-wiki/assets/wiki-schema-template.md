# Wiki Schema（知识库配置规范）

> 这个文件告诉 AI 如何维护你的知识库。你和 AI 可以一起调整它。

## 知识库信息

- 创建日期：{{date:YYYY-MM-DD HH:mm:ss}}
- 语言：{{LANGUAGE}}
- 版本：1.1

## 目录结构

详见 SKILL 的 `references/wiki-structure.md`（唯一标准，禁止增减层级）。

## 页面命名规范

详见 SKILL.md 的"页面命名规范"章节。

## 别名词表（Alias Table）

格式：每行一组同义词，用 `=` 分隔。

```
（初始为空，随使用积累）
```

维护原则：
- 只收录知识库里实际出现过的同义词
- 每组控制在 5 个以内
- 中英文混用时把最常用的放第一个

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

