# Trimer 工作流

## 概述

本工作流使用 `har_trim.py` 对 HAR 文件进行瘦身，删除 `entries[]._initiator.stack` 字段（通常占 HAR 文件体积的 50%+），生成更小的 `*.trim.har` 文件，便于后续 Planner 分析。

---

## 使用方式

```bash
py ~/.kiro/powers/repos/edk-api-power/powers/edk-api-power/scripts/har_trim.py <input.har>
```

> **Python 命令兼容性：** 优先使用 `py`（Windows Launcher），如果失败则依次尝试 `python3`、`python`。

## 输入

- 一个 Chrome DevTools 导出的 HAR 文件（`*.har`）

## 输出

- 生成 `*.trim.har` 文件（与输入文件同目录，文件名加 `.trim` 后缀）
- 控制台输出 JSON 格式的处理结果，包含：
  - 输入/输出文件大小和缩减比例
  - `stacksRemoved` — 删除的 `_initiator.stack` 字段数量
  - `verification` — 数据完整性校验结果（`passed` 或 `failed`）
  - `diffs` — 如果校验失败，列出差异详情（最多 20 条）

## 验证流程

脚本在 trim 完成后会自动执行数据完整性校验：

1. 重新读取原始 HAR 文件和 trim 后的文件
2. 对原始数据执行同样的 `_initiator.stack` 删除操作
3. 递归深度比较两个对象的所有字段（类型、键、值、数组长度）
4. 如果存在除 `_initiator.stack` 以外的差异，`status` 为 `warning`，`verification` 为 `failed`，并在 `diffs` 中列出具体差异路径
5. 如果无差异，`verification` 为 `passed`

## 示例

```bash
py ~/.kiro/powers/repos/edk-api-power/powers/edk-api-power/scripts/har_trim.py "edc submit.har"
# 成功: {"status":"ok","input":"edc submit.har","output":"edc submit.trim.har","inputSize":"1234.5KB","outputSize":"567.8KB","reduction":"54.0%","stacksRemoved":15,"verification":"passed"}
# 异常: {"status":"warning",...,"verification":"failed","diffs":[".log.entries[0].response: value mismatch"]}
```

## 适用场景

- HAR 文件过大导致 Planner 分析时读取缓慢或截断
- 需要减小 HAR 文件体积以便提交到版本控制
- `_initiator.stack` 中的 JS 调用栈信息对 API 分析无用，可以安全删除
