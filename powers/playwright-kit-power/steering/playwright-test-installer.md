---
name: playwright-test-installer
description: 安装 Playwright 端到端测试所需的 npm 依赖和浏览器二进制文件
---

# Playwright Test Installer

## 用途

安装 Playwright 测试所需的所有依赖，包括 npm 包和浏览器二进制文件。

## 安装步骤

### 1. 初始化 npm 项目

如果当前目录没有 `package.json`，先初始化：

```bash
npm init -y
```

### 2. 安装 Playwright Test

```bash
npm install -D @playwright/test
```

### 3. 安装浏览器

```bash
npx playwright install
```

## 验证安装

安装完成后，运行以下命令验证：

```bash
npx playwright --version
```

## 注意事项

- 确保 Node.js 版本 >= 16
- 如果网络环境受限，可能需要配置代理
- 浏览器安装可能需要较长时间，请耐心等待
