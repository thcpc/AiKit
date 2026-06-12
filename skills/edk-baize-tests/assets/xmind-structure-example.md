# XMind 结构示例

## 推荐的思维导图结构

```
支付请求模块
├── Overhead Rate 显示
│   ├── 测试用例 001: 选择合同和站点后显示 Overhead Rate
│   │   ├── Priority: High
│   │   ├── Method: 场景法
│   │   ├── Precondition: Contract and site are configured with overhead rate
│   │   ├── Test Steps
│   │   │   ├── 1. Navigate to Create Payment Request page
│   │   │   ├── 2. Select contract and site
│   │   │   ├── 3. Verify Overhead Rate field is displayed
│   │   │   ├── 4. Verify the field is auto-populated and non-editable
│   │   │   └── 5. Verify the value matches configuration
│   │   └── Expected Result: Overhead Rate displays correctly
│   │
│   └── 测试用例 002: Overhead Rate 字段只读验证
│       ├── Priority: Medium
│       ├── Method: 错误推测法
│       ├── Precondition: Overhead Rate is displayed
│       ├── Test Steps
│       │   ├── 1. Attempt to edit Overhead Rate field
│       │   └── 2. Verify field remains unchanged
│       └── Expected Result: Field is non-editable
│
└── 输入验证
    └── 测试用例 003: 字段长度验证
        ├── Priority: High
        ├── Method: 边界值分析法
        ├── Test Data Description
        │   ├── Test Cases | input | Expected Result
        │   ├── =MaxLength | ${TestData} | Pass
        │   ├── >MaxLength | ${TestData} | Fail
        │   ├── =MinLength | ${TestData} | Pass
        │   └── <MinLength | ${TestData} | Fail
        └── (DDT 格式，无需 Test Steps 和 Expected Result)
```

## 层级说明

### 第一层：功能模块
- 代表被测试的功能模块或系统
- 示例：支付请求模块、用户管理模块

### 第二层：测试场景
- 具体的测试场景或功能点
- 示例：Overhead Rate 显示、输入验证

### 第三层：测试用例
- 具体的测试用例标题
- 格式：测试用例 {编号}: {标题}
- 示例：测试用例 001: 选择合同和站点后显示 Overhead Rate

### 第四层：测试用例详情
必需节点：
- **Priority**: Critical / High / Medium / Low
- **Method**: 测试方法名称

KDT 格式额外节点：
- **Precondition**: 前置条件
- **Test Steps**: 测试步骤（包含子节点）
- **Expected Result**: 预期结果

DDT 格式额外节点：
- **Test Data Description**: 测试数据表格（包含子节点）

## 节点命名规则

### Priority 节点
- 必须使用以下值之一：Critical, High, Medium, Low
- 大小写敏感

### Method 节点
KDT 方法：
- 场景法
- 错误推测法
- 因果图/判定表法

DDT 方法：
- 等价类划分
- 边界值分析法
- 正交试验法
- 功能图法

### Test Steps 节点
- 每个步骤作为子节点
- 建议使用编号：1. 2. 3. ...
- 步骤描述清晰具体

### Test Data Description 节点
- 第一个子节点为表头
- 后续子节点为数据行
- 使用 | 分隔列

## 常见错误

❌ **错误示例 1：缺少必需节点**
```
测试用例 001: 测试标题
└── Test Steps
    └── 步骤 1
```
缺少 Priority 和 Method 节点

✅ **正确示例**
```
测试用例 001: 测试标题
├── Priority: High
├── Method: 场景法
├── Precondition: 前置条件
├── Test Steps
│   └── 步骤 1
└── Expected Result: 预期结果
```

❌ **错误示例 2：DDT 格式包含 Test Steps**
```
测试用例 002: 边界值测试
├── Priority: High
├── Method: 边界值分析法
├── Test Steps  ← DDT 不需要
└── Test Data Description
```

✅ **正确示例**
```
测试用例 002: 边界值测试
├── Priority: High
├── Method: 边界值分析法
└── Test Data Description
    ├── Test Cases | input | Expected Result
    ├── =MaxLength | ${TestData} | Pass
    └── >MaxLength | ${TestData} | Fail
```

## 最佳实践

1. **保持层级一致**：所有测试用例使用相同的层级结构
2. **清晰的命名**：使用描述性的标题
3. **完整的信息**：确保所有必需节点都存在
4. **合理的优先级**：根据业务重要性设置优先级
5. **选择正确的方法**：根据测试类型选择 KDT 或 DDT
