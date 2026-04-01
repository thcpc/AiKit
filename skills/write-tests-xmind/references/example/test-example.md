# 测试用例 - [44237] Pay 节点后确认收据

## 测试套件信息
- **功能模块**: 付款收据确认
- **需求编号**: 44237
- **测试目标**: 验证在 Pay 节点后能够确认收据
- **状态**
   - [ ] 废弃 原因：
   - [ ] 已审核

---

## TC-44237-001: Confirm Receipt 按钮可用性

**Priority**: Critical
**Method**: 功能图法
**Test Data Description**:
**状态**
   - [ ] 废弃 原因：
   - [ ] 已审核

| CTMS Status | PR Status | Confirm Receipt 按钮 | 备注 |
|------------|-----------|---------------------|------|
| Paid | Payment Not Received | 可用 | 正常场景 |
| Paid | Receipt Confirmed | 不可用 | 已确认 |
| Approved | Payment Not Received | 不可用 | CTMS 未支付 |
| Pending | Payment Not Received | 不可用 | CTMS 未支付 |
| Paid | Draft | 不可用 | PR 状态不对 |

**Test Steps**:
1. 创建 PR 并推进到 Pay 节点
2. 在 CTMS 中将状态 {CTMS Status} 设置为 Paid
3. 验证 PR 状态 {PR Status}自动变为 "Payment Not Received"
4. 验证 "Confirm Receipt" 按钮在 PR 列表中可用
5. 测试上表中的各种状态组合
6. 验证按钮可用性符合规则

**Expected Result**: 
- 只有当 CTMS Status = Paid 且 PR Status = Payment Not Received 时按钮可用
- 其他状态组合按钮不可用

---

## TC-44237-002: 确认收据 - 选择 Yes

**Priority**: Critical
**Method**: 场景法
**Precondition**: 
- CTMS Status = Paid
- PR Status = Payment Not Received
- Confirm Receipt 按钮可用
**状态**
   - [ ] 废弃 原因：
   - [ ] 已审核

**Test Steps**:
1. 点击 "Confirm Receipt" 按钮
2. 验证弹出确认对话框或面板
3. 在 "Received Payment" 字段选择 "Yes"
4. 验证以下字段显示:
   - Receipt Date (必填,日期选择器)
   - Upload Files (非必填,文件上传)
5. 不选择 Receipt Date,尝试提交
6. 验证系统提示 Receipt Date 为必填
7. 选择 Receipt Date (例如: 2026-03-05)
8. 可选: 上传收据文件
9. 提交确认
10. 验证 PR 状态变为 "Receipt Confirmed"
11. 验证 Receipt Date 在 PR 列表和详情页显示
12. 验证 Receipt Date 显示在 Paid Date 字段之后
13. 验证 "Confirm Receipt" 按钮不再可用

**Expected Result**: 
- 选择 Yes 后显示 Receipt Date 和 Upload Files 字段
- Receipt Date 必填验证生效
- 提交后状态变为 "Receipt Confirmed"
- Receipt Date 正确显示在列表和详情页

---

## TC-44237-003: 确认收据 - 选择 No

**Priority**: Critical
**Method**: 场景法
**Precondition**: 
- CTMS Status = Paid
- PR Status = Payment Not Received
**状态**：
   - [ ] 废弃 原因：
   - [ ] 已审核

**Test Steps**:
1. 点击 "Confirm Receipt" 按钮
2. 在 "Received Payment" 字段选择 "No"
3. 验证 Comments 字段显示(必填)
4. 不输入 Comments,尝试提交
5. 验证系统提示 Comments 为必填
6. 输入 Comments (例如: "Payment not received yet, will check with finance")
7. 提交
8. 验证 PR 状态仍为 "Payment Not Received"
9. 验证 Comments 保存成功
10. 验证 "Confirm Receipt" 按钮仍然可用
11. 再次点击 "Confirm Receipt" 按钮
12. 验证可以重新尝试确认

**Expected Result**: 
- 选择 No 后显示 Comments 必填字段
- 提交后状态保持 "Payment Not Received"
- 可以继续点击 Confirm 按钮直到选择 Yes

---

## TC-44237-004: Receipt Date 和 Paid Date 字段显示

**Priority**: High
**Method**: 场景法
**状态**：
   - [ ] 废弃 原因：
   - [ ] 已审核
**Precondition**: 
- PR 已确认收据


**Test Steps**:
1. 在 PR 列表页面查看已确认收据的 PR
2. 验证 "Paid Date" 字段显示
3. 验证 "Receipt Date" 字段显示在 "Paid Date" 之后
4. 点击进入 PR 详情页
5. 验证详情页也显示 "Paid Date" 字段
6. 验证详情页也显示 "Receipt Date" 字段
7. 验证两个日期的显示位置和格式正确
8. 验证日期值与确认时输入的一致

**Expected Result**: 
- Paid Date 和 Receipt Date 都在列表和详情页显示
- Receipt Date 显示在 Paid Date 之后
- 日期格式和值正确

---

## TC-44237-005: Voucher 文件类型更新

**Priority**: High
**Method**: 场景法
**状态**：
   - [ ] 废弃 原因：
   - [ ] 已审核
**Precondition**: 
- 支持上传 Voucher 类型文件


**Test Steps**:
1. 在确认收据时上传文件
2. 选择 File Type = Voucher
3. 验证日期字段标签显示为 "Voucher Date" (而不是 "Payment Receipt Date")
4. 输入 Voucher Date
5. 保存
6. 在 EDC 中查看该 PR
7. 验证 Voucher Date 可以正确回显
8. 验证字段标签为 "Voucher Date"

**Expected Result**: 
- File Type = Voucher 时,日期字段更名为 "Voucher Date"
- Voucher Date 在 EDC 中正确回显

---

## TC-44237-006: EDC Source 限制

**Priority**: Critical
**Method**: 场景法
**状态**：
   - [ ] 废弃 原因：
   - [ ] 已审核
**Precondition**: 
- 存在 source = EDC 的 PR
- 存在 source = CTMS 的 PR


**Test Steps**:
1. 在 EDC 中打开 source = EDC 的 PR
2. 验证可以在 EDC 中确认收据
3. 在 CTMS 中打开同一个 PR
4. 验证 CTMS 中无法确认收据(按钮不可用或隐藏)
5. 在 CTMS 中打开 source = CTMS 的 PR
6. 验证可以在 CTMS 中确认收据
7. 在 EDC 中打开同一个 PR
8. 验证 EDC 中无法确认收据

**Expected Result**: 
- source = EDC 的 PR 只能在 EDC 中确认
- source = CTMS 的 PR 只能在 CTMS 中确认
- 跨系统无法确认收据

---

## TC-44237-007: 工作流节点限制

**Priority**: High
**Method**: 场景法
**状态**：
   - [ ] 废弃 原因：
   - [ ] 已审核
**Precondition**: 
- 工作流配置完整



**Test Steps**:
1. 创建 PR (状态: Draft)
2. 验证 Confirm Receipt 操作不可用
3. 推进到 Auditing 节点
4. 验证 Confirm Receipt 操作可用(如果 CTMS Status = Paid)
5. 推进到其他节点
6. 验证只有 Draft 和 Auditing 节点可以执行 Confirm Receipt
7. 在非允许节点尝试确认
8. 验证系统阻止操作或提示错误

**Expected Result**: 
- 只有 Draft 和 Auditing 工作流节点可以确认收据
- 其他节点无法执行该操作

---

## TC-44237-008: 多次选择 No 的场景

**Priority**: Medium
**Method**: 场景法
**状态**：
   - [ ] 废弃 原因：
   - [ ] 已审核
**Precondition**: 
- CTMS Status = Paid
- PR Status = Payment Not Received



**Test Steps**:
1. 第一次点击 "Confirm Receipt",选择 No,输入 Comments: "Not received - Day 1"
2. 提交,验证状态仍为 "Payment Not Received"
3. 第二次点击 "Confirm Receipt",选择 No,输入 Comments: "Not received - Day 2"
4. 提交,验证状态仍为 "Payment Not Received"
5. 第三次点击 "Confirm Receipt",选择 Yes,输入 Receipt Date
6. 提交,验证状态变为 "Receipt Confirmed"
7. 查看 Comments 历史记录
8. 验证所有 Comments 都被保存

**Expected Result**: 
- 可以多次选择 No 并记录 Comments
- 最终选择 Yes 后状态变为 Receipt Confirmed
- Comments 历史完整保存

---

## TC-44237-009: Receipt Date 的日期验证

**Priority**: High
**Method**: 边界值分析法
**状态**：
   - [ ] 废弃 原因：
   - [ ] 已审核
**Test Data Description**:

| 测试用例 | Receipt Date | Paid Date | 预期结果 | 备注 |
|---------|-------------|-----------|---------|------|
| 正常值 | 2026-03-05 | 2026-03-01 | 接受 | Receipt Date > Paid Date |
| 边界值-相同 | 2026-03-01 | 2026-03-01 | 接受 | Receipt Date = Paid Date |
| 异常值-早于 | 2026-02-28 | 2026-03-01 | 拒绝或警告 | Receipt Date < Paid Date |
| 异常值-未来 | 2026-12-31 | 2026-03-01 | 拒绝或警告 | Receipt Date 在未来 |
| 边界值-今天 | 2026-03-05 | 2026-03-01 | 接受 | Receipt Date = 今天 |



**Test Steps**:
1. 测试上表中的每种日期组合
2. 验证系统的日期验证规则
3. 验证错误提示信息清晰

**Expected Result**: 
- Receipt Date 应该 >= Paid Date
- Receipt Date 不应该在未来
- 日期验证规则合理且提示清晰

---

## TC-44237-010: 上传文件的类型和大小限制

**Priority**: Medium
**Method**: 边界值分析法
**Precondition**: 
- 确认收据时选择 Yes

**Test Steps**:
1. 尝试上传不同类型的文件:
   - PDF 文件 → 应接受
   - 图片文件 (JPG, PNG) → 应接受
   - Word 文档 → 验证是否接受
   - Excel 文件 → 验证是否接受
   - 可执行文件 (.exe) → 应拒绝
2. 测试文件大小:
   - 1KB 文件 → 应接受
   - 10MB 文件 → 应接受
   - 50MB 文件 → 验证是否接受
   - 100MB 文件 → 验证是否接受
   - 200MB 文件 → 应拒绝或警告
3. 验证错误提示清晰

**Expected Result**: 
- 支持常见文档和图片格式
- 拒绝可执行文件和超大文件
- 错误提示清晰

---

## TC-44237-011: 确认收据的权限控制

**Priority**: High
**Method**: 场景法
**Precondition**: 
- 存在不同权限级别的用户

**Test Steps**:
1. 使用只读权限用户登录
2. 验证 "Confirm Receipt" 按钮不可见或禁用
3. 使用财务权限用户登录
4. 验证 "Confirm Receipt" 按钮可用
5. 使用普通编辑权限用户登录
6. 验证按钮可用性符合业务规则

**Expected Result**: 
- 权限控制正确
- 只有授权用户可以确认收据

---

## TC-44237-012: CTMS 和 EDC 的数据同步

**Priority**: Critical
**Method**: 场景法
**Precondition**: 
- CTMS 和 EDC 集成正常

**Test Steps**:
1. 在 CTMS 中将 PR 状态设置为 Paid
2. 在 EDC 中验证 PR 状态同步为 "Payment Not Received"
3. 在 EDC 中确认收据(选择 Yes)
4. 在 CTMS 中验证状态同步为 "Receipt Confirmed"
5. 验证 Receipt Date 在 CTMS 中正确显示
6. 验证上传的文件在 CTMS 中可访问

**Expected Result**: 
- CTMS 和 EDC 之间数据实时同步
- 状态、日期、文件都正确同步
