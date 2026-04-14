# Trimer 工作流

## 概述

本工作流使用 `har_trim.py` 对 HAR 文件进行瘦身，删除 `entries[]._initiator.stack` 字段（通常占 HAR 文件体积的 50%+），生成更小的 `*.trim.har` 文件，便于后续 Planner 分析。

---

## 使用方式

```bash
py powers/edk-api-power/scripts/har_trim.py <input.har>
```

> **Python 命令兼容性：** 优先使用 `py`（Windows Launcher），如果失败则依次尝试 `python3`、`python`。

## 输入

- 一个 Chrome DevTools 导出的 HAR 文件（`*.har`）

## 输出

- 生成 `*.trim.har` 文件（与输入文件同目录，文件名加 `.trim` 后缀）
- 控制台输出 JSON 格式的处理结果，包含输入/输出文件大小和缩减比例

## 示例

```bash
py powers/edk-api-power/scripts/har_trim.py "edc submit.har"
# 输出: {"status":"ok","input":"edc submit.har","output":"edc submit.trim.har","inputSize":"1234.5KB","outputSize":"567.8KB","reduction":"54.0%"}
```

## 适用场景

- HAR 文件过大导致 Planner 分析时读取缓慢或截断
- 需要减小 HAR 文件体积以便提交到版本控制
- `_initiator.stack` 中的 JS 调用栈信息对 API 分析无用，可以安全删除
