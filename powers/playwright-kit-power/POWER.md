---
name: "playwright-kit-power"
displayName: "Playwright Kit Power"
description: "调用 Playwright MCP 进行端到端浏览器测试的 Power，支持测试计划生成、测试代码生成、测试调试修复三大工作流，节约上下文空间"
keywords: ["playwright", "e2e", "test", "browser", "automation", "end-to-end", "testing"]
author: "PengchengChen"
---

# Playwright Kit Power

## Overview

Playwright Kit Power 是一个端到端浏览器测试 Power，将 Playwright Agent 迁移为 Kiro Power 形式以节约上下文空间。提供以下核心工作流：

1. **测试计划生成（Planner）** — 浏览目标网页，分析用户流程，生成全面的测试计划文档
2. **测试代码生成（Generator）** — 根据测试计划，通过 Playwright MCP 实时执行步骤并生成测试代码
3. **测试调试修复（Healer）** — 运行测试，诊断失败原因，自动修复测试代码
4. **依赖安装（Installer）** — 安装 Playwright 测试所需的依赖

## Available Steering Files

- **playwright-test-installer** — 安装 Playwright 测试所需的 npm 依赖
- **playwright-test-planner** — 浏览网页并生成全面的测试计划文档
- **playwright-test-generator** — 根据测试计划实时执行步骤并生成 Playwright 测试代码
- **playwright-test-healer** — 运行失败的测试，诊断问题并自动修复

## Onboarding

### 前置条件

- 已安装 Node.js（v16+）
- 已安装 npm

### 安装依赖

首次使用前，请通过 `playwright-test-installer` steering 安装依赖：

```bash
npm init -y
npm install -D @playwright/test
npx playwright install
```

### 验证安装

安装完成后，可以使用 `test_list` 工具验证 Playwright MCP 是否正常工作。

## Common Workflows

### 工作流 1：安装依赖（Installer）

安装 Playwright 测试所需的 npm 依赖。

**步骤：**
1. 初始化 npm 项目（如果尚未初始化）
2. 安装 `@playwright/test` 作为开发依赖
3. 安装浏览器二进制文件

**详细指引请读取 `playwright-test-installer` steering 文件。**

### 工作流 2：生成测试计划（Planner）

浏览目标网页，分析界面元素和用户流程，生成全面的测试计划。

**步骤：**
1. 调用 `planner_setup_page` 设置目标页面
2. 使用 `browser_*` 工具探索界面
3. 分析用户流程和交互元素
4. 使用 `planner_save_plan` 保存测试计划

**详细指引请读取 `playwright-test-planner` steering 文件。**

### 工作流 3：生成测试代码（Generator）

根据测试计划，通过 Playwright MCP 实时执行每个步骤并生成测试代码。

**步骤：**
1. 获取测试计划中的步骤和验证规范
2. 调用 `generator_setup_page` 设置页面
3. 逐步使用 Playwright 工具执行操作
4. 通过 `generator_read_log` 获取执行日志
5. 使用 `generator_write_test` 写入测试文件

**详细指引请读取 `playwright-test-generator` steering 文件。**

### 工作流 4：调试修复测试（Healer）

运行测试，诊断失败原因，自动修复测试代码。

**步骤：**
1. 使用 `test_run` 运行所有测试
2. 对失败的测试使用 `test_debug` 进入调试模式
3. 使用 Playwright MCP 工具检查页面状态
4. 分析根本原因并修复代码
5. 重新运行验证修复

**详细指引请读取 `playwright-test-healer` steering 文件。**

### 各工作流交互关系

1. 用户 → Installer：安装依赖
2. 用户 → Planner：生成测试计划
3. Planner → Generator：根据计划生成测试代码
4. Generator → Healer：修复失败的测试
5. 用户 → Healer：直接调试已有测试

## Troubleshooting

### Playwright MCP 连接失败

**问题：** MCP Server 无法启动
**解决方案：**
1. 确认 Node.js 已安装：`node --version`
2. 确认 Playwright 已安装：`npx playwright --version`
3. 手动测试：`npx playwright run-test-mcp-server`
4. 重启 Kiro

### 浏览器未安装

**问题：** 运行测试时提示浏览器未安装
**解决方案：**
```bash
npx playwright install
```

### 测试超时

**问题：** 测试执行超时
**解决方案：**
1. 检查网络连接
2. 增加测试超时时间
3. 确认目标页面可访问

## Best Practices

- 测试计划应覆盖 Happy Path、边界条件和错误处理
- 每个测试文件只包含一个测试用例
- 使用描述性的测试名称
- 在每个步骤前添加注释说明
- 优先使用 Playwright 推荐的定位器（role、text、label）
- 避免使用 `networkidle` 等已弃用的 API
- 测试应相互独立，可以任意顺序运行

## MCP Tools Reference

Power 通过 `playwright-test` MCP Server 提供以下工具：

### 浏览器操作
- `browser_navigate` — 导航到指定 URL
- `browser_click` — 点击元素
- `browser_snapshot` — 获取页面快照
- `browser_fill_form` — 填写表单
- `browser_close` — 关闭浏览器
- `browser_wait_for` — 等待条件满足
- `browser_verify_text_visible` — 验证文本可见
- `browser_evaluate` — 执行 JavaScript
- `browser_verify_element_visible` — 验证元素可见
- `browser_type` — 输入文本
- `browser_verify_value` — 验证值
- `browser_run_code` — 运行代码
- `browser_verify_list_visible` — 验证列表可见
- `browser_open` — 打开浏览器
- `browser_press_key` — 按键操作

### 测试管理
- `test_run` — 运行测试
- `test_list` — 列出测试
- `test_debug` — 调试测试
- `browser_install` — 安装浏览器

### 计划生成
- `planner_setup_page` — 设置计划页面

### 代码生成
- `generator_setup_page` — 设置生成器页面
- `generator_read_log` — 读取生成日志
- `generator_write_test` — 写入测试文件
