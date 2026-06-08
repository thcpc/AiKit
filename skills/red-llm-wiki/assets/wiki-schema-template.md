# Wiki Schema（知识库配置规范）

> 这个文件告诉 AI 如何维护你的知识库。你和 AI 可以一起调整它。

## 知识库信息

- 创建日期：{{date:YYYY-MM-DD HH:mm:ss}}
- 语言：{{LANGUAGE}}
- 版本：1.1

## 目录结构

```
$WIKI_ROOT/
├── raw/                    # 原始素材
│   ├── articles/           # 网页文章
│   ├── tweets/             # X/Twitter
│   ├── wechat/             # 微信公众号
│   ├── xiaohongshu/        # 小红书
│   ├── zhihu/              # 知乎
│   ├── pdfs/               # PDF
│   ├── notes/              # 笔记
│   └── assets/             # 图片等附件
├── wiki/                   # 知识库
│   ├── {topicName}/        # 文件名来自 topics.md
│         ├── overview.md
│         ├── index.md
│         ├── entities/
│         ├── concepts/
│         ├── comparisons/
│         ├── summaries/
│         ├── synthesis/
├── queries/                # 查询结果
├── log.md                  # 操作日志
├── topics.md               # 研究方向
├── .wiki-cache.json        # 缓存（未来规划）
└── .wiki-schema.md         # 本文件
```

## 页面命名规范

- 实体页：`wiki/{topicName}/entities/{名称}.md`
- 概念页：`wiki/{topicName}/concepts/{概念名}.md`
- 素材摘要：`wiki/{topicName}/summaries/{日期}-{短标题}.md`
- 对比分析：`wiki/{topicName}/comparisons/{对比主题}.md`
- 综合分析：`wiki/{topicName}/synthesis/{分析主题}.md`
- 主题总览：`wiki/{topicName}/overview.md`
- 主题索引：`wiki/{topicName}/index.md`

## 交叉引用规范

- 页面间使用 `[[页面名]]` 语法（Obsidian 兼容的双向链接）
- 素材引用格式：`[来源: 素材标题](../summaries/xxx.md)`
- 每个页面底部维护"相关页面"列表

## 页面格式规范

每个 wiki 页面应包含：

```
---
tags: [标签1, 标签2]
created: YYYY-MM-DD
updated: YYYY-MM-DD
sources: [关联素材列表]
---

# 页面标题

> 一句话摘要

## 正文内容

...
```

### 底部关联章节（按页面类型区分）

不同类型的页面使用不同的底部关联章节，**以对应模板为准**，不得统一简化为"相关页面"：

- **concept 页**（概念页）：`## 相关实体` → `## 关联概念` → `## 溯源来源`
- **entity 页**（实体页）：`## 关联概念` → `## 相关实体` → `## 溯源来源`
- **summary 页**（摘要页）：`## 与其他素材的关联` → `## 原文精彩摘录` → `## 相关页面` → `## 溯源来源`
- **synthesis 页**（综合分析）：`## 涉及概念` → `## 参考资料`
- **comparison 页**（对比分析）：`## 关联链接` → `## 相似的对比`
- **overview / index 页**：无强制底部关联章节

