---
name: edk-baize-ba-read
description: >
  白泽外部 BA 知识库只读访问模块。在 edk-baize 的 query 或 digest 工作流中，
  读取外部 BA 知识库内容作为补充参考来源。对外部知识库严格只读，禁止任何修改操作。
license: MIT
compatibility: Requires edk-baize skill
metadata:
  author: red
  version: "1.0"
---

# edk-baize-ba-read

白泽的外部 BA 知识库只读访问模块。当 edk-baize 执行 query 或 digest 工作流时，可从外部 BA 知识库中读取内容作为参考来源。

## 变量

- `BA_WIKI_ROOT` = 外部 BA 知识库的绝对路径（从 `.baize-schema.md` 的"外部知识库"章节读取）

## 核心规则

⛔ **严格只读**：对外部 BA 知识库禁止以下任何操作：
- 禁止编辑文件内容
- 禁止删除文件或目录
- 禁止新增文件或目录
- 禁止移动或重命名
- 禁止执行任何会修改文件系统的命令

仅允许：读取文件内容（read_file / read_files）、列出目录结构（list_directory）、搜索文件（file_search / grep_search）。

## 工作流

### read-ba（读取外部 BA 知识库）

**触发**：由 edk-baize 的 query 或 digest 工作流内部调用，当用户确认查询范围包含外部 BA 知识库时触发。

⛔ 不可独立触发，必须作为 edk-baize query/digest 的子流程执行。

**流程**：

1. **读取配置**：从 `.baize-schema.md` 的"外部知识库"章节获取 BA 知识库绝对路径
2. **验证路径**：确认路径存在且可访问，若不可访问则报错并终止
3. **目录发现**：
   - 列出 `$BA_WIKI_ROOT` 下的一级目录
   - 对每个目录先读取 `README.md`（了解该目录的内容范围和定位）
4. **索引定位**：
   - 读取相关目录下的 `index.md` 索引文件
   - 根据用户查询关键词在索引中匹配相关条目
5. **内容读取**：
   - 根据索引匹配结果，读取具体的内容文件
   - 按相关性排序返回内容摘要
6. **返回结果**：将读取到的内容作为参考来源返回给 edk-baize 主流程，标注来源为"外部 BA 知识库"

### 查询策略

```
$BA_WIKI_ROOT/
├── {模块A}/
│   ├── README.md          ← 第一步：读取，了解模块范围
│   ├── index.md           ← 第二步：读取索引，定位具体文件
│   └── {具体文件}.md      ← 第三步：读取匹配的具体内容
├── {模块B}/
│   ├── README.md
│   ├── index.md
│   └── ...
└── ...
```

**查询优化规则**：
- 先通过 README.md 判断目录是否与查询相关，不相关的目录直接跳过
- 通过 index.md 精确定位，避免遍历所有文件
- 若 index.md 不存在，退化为列出目录文件列表 + 按文件名匹配

## 配置方式

在 `.baize-schema.md` 的"外部知识库"章节配置：

```markdown
## 外部知识库（External Knowledge Bases）

| 名称 | 类型 | 路径 | 说明 |
|------|------|------|------|
| BA知识库 | ba-read | D:\path\to\ba-wiki | BA 业务分析知识库（只读） |
```

## 引用格式

在 query/digest 输出中引用外部 BA 知识库内容时，使用以下格式：

```
[来源: {文件的绝对路径}]
```

⛔ 禁止使用 `[[]]` wiki link 引用外部知识库文件（因为不在本项目中，链接不可达）。

