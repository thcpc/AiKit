---
name: init-tests
description: 测试初始化和配置的标准化 skill
version: 1.0.0
---

# Init Tests Skill

测试初始化和配置的标准化 skill。

## 用途

当需要为项目初始化测试环境或创建测试配置时，使用此 skill 提供的指导和最佳实践。

## 适用场景

- 初始化新项目的测试框架
- 设置测试目录结构
- 创建测试配置文件

## 标准目录结构

```
testcases/
├── design/  # 存放 Xmind 
├── tests/   # 存放 生成的测试用例
```

## 初始化步骤

1. 初始化工作区 python 环境：
```bash
py -3.13 -m venv .venv
```
如果上述命令失败尝试
```bash
python3.13 -m venv .venv
```

2. 配置 xmind-mcp
1.修改 ./kiro/settings/mcp.json 中添加配置 xmind-mcp 字段 （参考 references/xmind-mcp.conf.json）
2.修改新增的配置中 "${pwd}\\testcases\\design" 中的 ${pwd} 替换为 工程目录的绝对路径
** 不要修改已有的配置字段 **

3. 创建 testcases 的文件夹

```bash
.venv\Scripts\python .kiro/skiils/init-tests/references/create_dir.py
```

4. 创建 README.md
```bash
cp .kiro/skiils/init-tests/assets/README.md testcases/README.md
```

5. 创建 .gitignore
并在其中添加以下文件 
 - .kiro/settings
 - .kiro/skills
 - .venv 

## 相关资源

查看 `references/` 目录获取更多配置文件和示例代码。
