# Write Tests 工作流程指南

## 快速开始

### 1. 准备 XMind 文件
在 `testcases/design/` 目录中创建 XMind 文件，按照推荐的结构组织测试用例。

### 2. 激活 write-tests skill
在对话中说：
```
使用 write-tests skill 从 testcases/design/my-test.xmind 生成测试用例
```

### 3. 自动生成
系统会自动：
- 读取并解析 XMind 文件
- 根据规范生成测试用例代码
- 创建测试任务文档

## 详细工作流程

### 阶段 1: 设计测试用例（在 XMind 中）

1. **创建思维导图**
   - 打开 XMind
   - 创建新的思维导图
   - 设置根节点为功能模块名称

2. **添加测试场景**
   - 在根节点下添加测试场景
   - 每个场景代表一个功能点

3. **定义测试用例**
   - 在场景下添加测试用例
   - 格式：测试用例 {编号}: {标题}

4. **填写测试详情**
   - 添加 Priority 节点
   - 添加 Method 节点
   - 根据方法类型添加其他必需节点

5. **保存文件**
   - 保存到 `testcases/design/` 目录
   - 使用描述性的文件名

### 阶段 2: 生成测试用例（使用 write-tests skill）

1. **指定 XMind 文件**
   ```
   请从 testcases/design/payment-module.xmind 生成测试用例
   ```

2. **系统自动处理**
   - 读取 XMind 文件
   - 解析思维导图结构
   - 识别测试用例和详情

3. **生成测试代码**
   - 根据测试方法选择模板（KDT 或 DDT）
   - 填充测试用例详情
   - 生成 Python 测试文件

4. **保存测试文件**
   - 文件保存到 `testcases/tests/`
   - 文件名格式：`test_{module}_{scenario}_{id}.py`

### 阶段 3: 生成任务文档

1. **创建任务清单**
   - 列出所有测试用例
   - 包含优先级和方法信息
   - 添加统计信息

2. **生成执行计划**
   - 按优先级分组
   - 创建执行阶段

3. **保存任务文档**
   - 保存到 `.kiro/specs/test-task.md`
   - 使用 Markdown checkbox 格式

### 阶段 4: 实现和执行测试

1. **实现测试逻辑**
   - 打开生成的测试文件
   - 替换 TODO 注释为实际代码
   - 实现测试步骤和断言

2. **运行测试**
   ```bash
   pytest testcases/tests/
   ```

3. **更新任务状态**
   - 在 test-task.md 中标记完成的测试
   - 记录测试结果

## 命令示例

### 生成单个模块的测试
```
使用 write-tests skill 从 testcases/design/user-module.xmind 生成测试用例
```

### 生成多个模块的测试
```
使用 write-tests skill 依次处理以下文件：
1. testcases/design/user-module.xmind
2. testcases/design/payment-module.xmind
3. testcases/design/report-module.xmind
```

### 重新生成测试（覆盖现有文件）
```
使用 write-tests skill 重新生成 testcases/design/user-module.xmind 的测试用例，覆盖现有文件
```

## 常见问题

### Q: XMind 文件解析失败
**A**: 检查以下几点：
- 文件路径是否正确
- 文件是否存在于 testcases/design/ 目录
- XMind 文件是否损坏
- 是否使用了支持的 XMind 版本

### Q: 生成的测试用例格式不正确
**A**: 检查 XMind 结构：
- 确保包含所有必需节点（Priority, Method）
- 验证 Method 节点的值是否正确
- 检查层级结构是否符合规范

### Q: 测试任务文档没有生成
**A**: 可能的原因：
- .kiro/specs/ 目录不存在
- 没有成功生成任何测试用例
- 权限问题

### Q: 如何更新已生成的测试用例
**A**: 两种方式：
1. 手动编辑生成的测试文件
2. 修改 XMind 文件后重新生成（会覆盖）

## 最佳实践

### XMind 设计
- 使用清晰的命名
- 保持结构一致
- 添加足够的细节
- 定期备份 XMind 文件

### 测试用例生成
- 先生成少量测试验证流程
- 逐步增加测试用例
- 及时实现生成的测试
- 保持测试代码整洁

### 任务管理
- 定期更新任务状态
- 记录测试结果
- 跟踪失败的测试
- 维护测试文档

## 进阶技巧

### 批量生成
创建一个脚本来批量处理多个 XMind 文件：
```python
xmind_files = [
    "user-module.xmind",
    "payment-module.xmind",
    "report-module.xmind"
]

for file in xmind_files:
    # 使用 write-tests skill 处理每个文件
    pass
```

### 自定义模板
修改 references 目录下的模板文件来定制生成的测试代码格式。

### 集成 CI/CD
将生成的测试集成到 CI/CD 流程中：
```yaml
- name: Run Tests
  run: pytest testcases/tests/ --junitxml=test-results.xml
```

## 相关资源

- XMind 结构示例: `assets/xmind-structure-example.md`
- KDT 模板: `references/test_template_kdt.py`
- DDT 模板: `references/test_template_ddt.py`
- 任务文档模板: `references/test-task-template.md`
