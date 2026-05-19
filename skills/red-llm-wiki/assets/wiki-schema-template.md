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

## Ingest（消化素材）规则

### 分级处理

**完整处理**（素材 > 1000 字）：
1. 生成摘要页（`wiki/{topicName}/summaries/` 下）
2. 提取 3-5 个关键概念
3. 检查是否需要创建新的实体页（`wiki/{topicName}/entities/`）
4. 检查是否需要创建或更新概念页（`wiki/{topicName}/concepts/`）
5. 更新 `wiki/{topicName}/index.md`
6. 更新 `log.md`
7. 更新 `wiki/{topicName}/overview.md`（如果知识库全貌有变化）

**简化处理**（素材 < 1000 字）：
1. 生成摘要页
2. 提取 1-3 个关键概念
3. 如果关键概念已有实体页，追加信息；否则标记 `[待创建]`
4. 更新 `wiki/{topicName}/index.md` 和 `log.md`
5. 跳过概念页和 overview 更新

### 素材类型路由

| 来源 | raw 目录 | 提取方式 |
|------|----------|----------|
| 网页文章 | `raw/articles/` | baoyu-url-to-markdown skill |
| X/Twitter | `raw/tweets/` | baoyu-url-to-markdown skill |
| 微信公众号 | `raw/wechat/` | wechat-article-to-markdown |
| YouTube | `raw/articles/` | youtube-transcript skill |
| B站视频 | `raw/articles/` | 未来规划 |
| 小红书 | `raw/xiaohongshu/` | 用户手动粘贴 |
| 知乎 | `raw/zhihu/` | 用户手动粘贴 或 baoyu-url-to-markdown |
| PDF | `raw/pdfs/` | 直接读取 |
| Markdown/文本/HTML | `raw/notes/` | 直接读取 |
| 纯文本粘贴 | `raw/notes/` | 直接使用 |

## 别名词表（Alias Table）

格式：每行一组同义词，用 `=` 分隔。

```
LLM = 大语言模型 = 大模型 = Large Language Model
RAG = 检索增强生成 = Retrieval Augmented Generation
fine-tuning = 微调 = 精调
prompt engineering = 提示工程 = 提示词工程
```

维护原则：
- 只收录知识库里实际出现过的同义词
- 每组控制在 5 个以内
- 中英文混用时把最常用的放第一个

## Query（查询）规则

1. 先读 `index.md`，定位相关条目
2. 用 Grep 在 `wiki/` 下搜索关键词
3. 阅读相关页面后综合回答
4. 回答中标注来源页面
5. 有价值的分析建议保存为新的 wiki 页面

## Lint（健康检查）规则

1. 检查范围：随机抽查 10 个页面 + 最近更新的 10 个页面
2. 检查项：
   - 页面间矛盾
   - 孤立页面
   - 缺失概念页
   - 缺少交叉引用
   - index 一致性
3. 输出中文报告，对每个问题给出修复建议
4. 如果发现问题，询问用户是否自动修复
