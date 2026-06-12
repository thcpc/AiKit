# Wiki 目录结构（唯一标准）

⛔ **所有创建知识库的操作必须严格遵守本结构，禁止增加或减少层级。**

## 标准结构

```
$WIKI_ROOT/
├── raw/                    # 原始素材
│   ├── articles/           # 网页文章
│   ├── tweets/             # X/Twitter
│   ├── wechat/             # 微信公众号
│   ├── xiaohongshu/        # 小红书
│   ├── zhihu/              # 知乎
│   ├── pdfs/               # PDF
│   ├── xmind/              # XMind 文件
│   ├── notes/              # 笔记
│   └── assets/             # 图片等附件
├── wiki/                   # 知识库
│   └── {topicName}/        # 每个 topic 一个文件夹，名称来自 topics.md
│       ├── overview.md     # 主题总览
│       ├── index.md        # 主题索引
│       ├── entities/       # 实体页（具体事物：人/工具/API/产品）
│       ├── concepts/       # 概念页（定义/原理/方法论）
│       ├── procedures/     # 操作流程页（步骤序列/操作指南）
│       ├── rules/          # 业务规则页（约束/状态机/决策表）
│       ├── comparisons/    # 对比分析
│       ├── summaries/      # 素材摘要
│       └── synthesis/      # 主题分析
├── queries/                # 查询结果
├── log.md                  # 操作日志
├── topics.md               # 研究方向
├── .wiki-cache.json        # 缓存（未来规划）
└── .wiki-schema.md         # 配置规范
```

## ⛔ 核心规则

1. **WIKI_ROOT 就是知识库根目录本身**，`raw/`、`wiki/`、`queries/`、`log.md`、`topics.md`、`.wiki-schema.md` 都直接放在 WIKI_ROOT 下
2. **禁止在 WIKI_ROOT 下再增加一层父级文件夹**（例如 `my-wiki/raw/...` 是错的，应该是 `raw/...`）
3. **禁止增减 raw/ 子目录**：只有 `articles/`、`tweets/`、`wechat/`、`xiaohongshu/`、`zhihu/`、`pdfs/`、`xmind/`、`notes/`、`assets/` 九个，不要添加其他
4. **禁止改名**：所有目录和文件名严格按上面的标准
5. **禁止增减 wiki/{topic}/ 子目录**：只有 `entities/`、`concepts/`、`procedures/`、`rules/`、`comparisons/`、`summaries/`、`synthesis/` 七个

## 内容形态分类（决定文件落在哪个子目录）

⛔ ingest/digest 时必须严格按照以下分类决定页面归属，避免一篇巨长概念页混杂多种形态：

| 子目录 | 内容形态 | 判断特征 | 例子 |
|-------|---------|---------|------|
| **entities/** | 具体事物（名词，可唯一标识） | 有名字、有版本、可以"指着说就是它" | "OpenAI GPT-4"、"LangChain 框架" |
| **concepts/** | 抽象概念（是什么/为什么） | 解释定义、原理、分类，不含步骤 | "Transformer 架构设计理念" |
| **procedures/** | 操作流程（怎么做） | 有顺序步骤、可执行、可"照着做" | "部署 RAG 系统 5 步" |
| **rules/** | 业务规则（约束/校验/状态） | 状态机、不变式、决策表、检查清单 | "模型选型决策表" |
| **comparisons/** | 对比分析 | 多对象横向比较 | "RAG vs Fine-tuning" |
| **summaries/** | 素材摘要 | 单篇素材的全文消化记录 | "{日期}-{素材短标题}" |
| **synthesis/** | 跨素材综合分析 | 整合多篇素材形成新结论 | "{日期}-LLM 全栈分析" |

## WIKI_ROOT 的确认规则

用户表述 → WIKI_ROOT 解析：

| 用户说 | WIKI_ROOT |
|--------|-----------|
| "在当前项目" | 当前项目根目录本身 |
| "和项目同级" | 当前项目根目录本身（与上同义） |
| "项目根目录" | 当前项目根目录本身 |
| 具体路径 `xxx` | 严格使用 `xxx` |
| 没说 | ⛔ 必须询问，不要自己生成名称 |

⛔ **禁止**：用户没明确指定路径时，AI 自作主张加 `my-wiki/`、`wiki-data/`、`knowledge/` 等任何名称。

## init 后的自检步骤

⛔ init 完成后必须执行以下自检，并把结果展示给用户：

1. 列出 `$WIKI_ROOT` 下所有第一层目录和文件
2. 对照本文档的"标准结构"逐项核对：
   - [ ] `raw/` 存在且包含标准九个子目录
   - [ ] `wiki/` 存在
   - [ ] `queries/` 存在
   - [ ] `log.md` 存在
   - [ ] `topics.md` 存在
   - [ ] `.wiki-schema.md` 存在
   - [ ] **没有多余的目录或文件**（特别是没有 `xxx-wiki/` 这类自己加的父级）
3. 创建 topic 时必须包含 `entities/`、`concepts/`、`procedures/`、`rules/`、`comparisons/`、`summaries/`、`synthesis/` 七个子目录
4. 任何一项不符合 → 报告错误，停止后续操作，等待用户指示
