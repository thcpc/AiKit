# 测试用例规范
## 目的

定义一系列测试用例的要求，测试人员需要按要求, 本文档定义如下规范
- Xmind 读取路径
- 输出路径
- 用例格式
- 测试方法
- 目标人员

## Xmind 读取路径
```
./testcases/design
```

## 输出路径
```
./testcases/tests
```
### 文件命名后缀
*.test.md

## 用例格式
### 采用 KDT 的用例格式
#### 包含要素
- Priority
	Critical, High, Medium, Low
- Method 
- Precondition
- Test Steps
- Expected Result
#### 示例
```
**Priority**: High
**Precondition**: Contract and site are configured with overhead rate
** Method **: 场景法
**Test Steps**:
1. Navigate to Create Payment Request page
2. Select contract and site
3. Verify Overhead Rate field is displayed
4. Verify the field is auto-populated and non-editable
5. Verify the value matches CTMS Financial Management/Contract configuration
**Expected Result**: Overhead Rate displays correctly after contract/site selection
```

### 采用 DDT 的用例格式
#### 包含要素
- Priority
   Critical, High, Medium, Low
- Test Data Description
#### 示例
```
**Priority**: High
**Test Data Description**:
|*** Test Cases *** | input |  Expected Result |
|------ | --------- | -------- |------- | 
| =MaxLength | ${TestData} | Pass |
| >MaxLength | ${TestData} | Fail |
| =MinLength | ${TestData} | Pass |
| <MinLength | ${TestData} | Fail |
```
## 测试方法
1. **等价类划分**
   - 把输入分成**有效等价类**和**无效等价类**
   - 每类取一个代表数据即可覆盖一类情况
   - DDT 用例格式

2. **边界值分析法**
   - 你已经知道：测**最小值、略小于最小值、最大值、略大于最大值、中间值**
   - DDT 用例格式

3. **场景法**
   - 模拟用户真实业务流程
   - 适用于登录、下单、支付、审批等流程
   - KDT 用例格式

4. **错误推测法**
   - 凭经验猜系统容易出错的地方
   - 如：空值、超长字符、特殊符号、并发、重复提交
   - KDT 用例格式

5. **因果图 / 判定表法**
   - 输入条件之间有**依赖、组合、互斥**时用
   - 适合多条件组合的逻辑判断
   - KDT 用例格式 
   
6. **正交试验法**
   - 多参数、多取值，用最少用例覆盖最多组合
   - 适合配置项、接口多参数测试
   - DDT 用例格式

7. **功能图法**
   - 把功能拆成状态、迁移、条件
   - 适合状态机类系统（如订单状态：待支付→已支付→已发货）
   - DDT 用例格式
## 目标人员

  测试人员