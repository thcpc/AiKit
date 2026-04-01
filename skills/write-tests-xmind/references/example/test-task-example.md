# 测试任务

## 概述
从 XMind 文件生成的测试任务列表
- "Prodigy Dashboard.xmind" - Prodigy Dashboard 功能

## 测试用例清单

### 需求：Prodigy - Prodigy Dashboard

- [ ] 测试场景：用户重定向与 Dashboard 显示
  - 优先级: Critical, High, Medium
  - 文件: test_dashboard_redirect_display.prodigy.test.md
  - 用例数量: 3 个
    - [ ] 测试用例 TC-SIGN-005: 手动签名 Log Form 记录签名 Site
        - 优先级: Critical
        - 方法: 场景法
        - 文件: test_ig_sign_softlock_site_permission_001.test.md
        - 测试任务状态
            - [ ] 审核
            - [ ] 通过
            - [ ] 失败
            - [ ] 阻塞
            - [ ] 废弃

    - [ ] 测试用例 TC-SIGN-006: 手动签名 Grid Form 记录签名 Site
        - 优先级: Critical
        - 方法: 场景法
        - 文件: test_ig_sign_softlock_site_permission_001.test.md
        - 测试任务状态
            - [ ] 审核
            - [ ] 通过
            - [ ] 失败
            - [ ] 阻塞
            - [ ] 废弃

    - [ ] 测试用例 TC-SIGN-007: 签名 IG 记录签名 Site（Simple-Log Form）
        - 优先级: High
        - 方法: 场景法
        - 文件: test_ig_sign_softlock_site_permission_001.test.md
        - 测试任务状态
            - [ ] 审核
            - [ ] 通过
            - [ ] 失败
            - [ ] 阻塞
            - [ ] 废弃      

- [ ] 测试场景：应用入口与权限控制
  - 优先级: Critical, High
  - 方法: 场景法、错误推测法
  - 文件: test_application_entry.prodigy.test.md
  - 用例数量: 3 个
    - [ ] 测试用例 TC-SIGN-005: 手动签名 Log Form 记录签名 Site
        - 优先级: Critical
        - 方法: 场景法
        - 文件: test_ig_sign_softlock_site_permission_001.test.md
        - 测试任务状态
            - [ ] 审核
            - [ ] 通过
            - [ ] 失败
            - [ ] 阻塞
            - [ ] 废弃

    - [ ] 测试用例 TC-SIGN-006: 手动签名 Grid Form 记录签名 Site
        - 优先级: Critical
        - 方法: 场景法
        - 文件: test_ig_sign_softlock_site_permission_001.test.md
        - 测试任务状态
            - [ ] 审核
            - [ ] 通过
            - [ ] 失败
            - [ ] 阻塞
            - [ ] 废弃

    - [ ] 测试用例 TC-SIGN-007: 签名 IG 记录签名 Site（Simple-Log Form）
        - 优先级: High
        - 方法: 场景法
        - 文件: test_ig_sign_softlock_site_permission_001.test.md
        - 测试任务状态
            - [ ] 审核
            - [ ] 通过
            - [ ] 失败
            - [ ] 阻塞
            - [ ] 废弃

- [ ] 测试场景：Breadcrumb 下拉菜单切换
  - 优先级: Critical, High, Medium
  - 方法: 场景法、错误推测法
  - 文件: test_breadcrumb_switching.prodigy.test.md
  - 用例数量: 3 个
    - [ ] 测试用例 TC-SIGN-005: 手动签名 Log Form 记录签名 Site
        - 优先级: Critical
        - 方法: 场景法
        - 文件: test_ig_sign_softlock_site_permission_001.test.md
        - 测试任务状态
            - [ ] 审核
            - [ ] 通过
            - [ ] 失败
            - [ ] 阻塞
            - [ ] 废弃

    - [ ] 测试用例 TC-SIGN-006: 手动签名 Grid Form 记录签名 Site
        - 优先级: Critical
        - 方法: 场景法
        - 文件: test_ig_sign_softlock_site_permission_001.test.md
        - 测试任务状态
            - [ ] 审核
            - [ ] 通过
            - [ ] 失败
            - [ ] 阻塞
            - [ ] 废弃

    - [ ] 测试用例 TC-SIGN-007: 签名 IG 记录签名 Site（Simple-Log Form）
        - 优先级: High
        - 方法: 场景法
        - 文件: test_ig_sign_softlock_site_permission_001.test.md
        - 测试任务状态
            - [ ] 审核
            - [ ] 通过
            - [ ] 失败
            - [ ] 阻塞
            - [ ] 废弃

## 执行计划

### 第一阶段：Critical 优先级测试
1. 执行 Prodigy Dashboard 的 Critical 优先级测试用例
   - 用户重定向与 Dashboard 显示（用例 1, 2, 5, 6, 10）
   - 应用入口与权限控制（用例 1, 2, 4, 5, 8, 9, 11）
   - Breadcrumb 下拉菜单切换（用例 1, 2, 4, 5, 7, 9, 10）

### 第二阶段：High 优先级测试
1. 执行 Prodigy Dashboard 的 High 优先级测试用例
   - 用户重定向与 Dashboard 显示（用例 3, 4, 7, 8, 9, 12）
   - 应用入口与权限控制（用例 3, 6, 7, 10, 12）
   - Breadcrumb 下拉菜单切换（用例 3, 6, 8, 11, 12, 13）

### 第三阶段：Medium 优先级测试
1. 执行 Prodigy Dashboard 的 Medium 优先级测试用例
   - 用户重定向与 Dashboard 显示（用例 11）
   - Breadcrumb 下拉菜单切换（用例 14, 15）

## 测试统计

- 总测试用例数: 39 个
- Critical 优先级: 19 个
- High 优先级: 17 个
- Medium 优先级: 3 个
- Low 优先级: 0 个

### 按测试场景分类统计

**用户重定向与 Dashboard 显示**
- 用例数: 12 个
- Critical: 5 个, High: 6 个, Medium: 1 个

**应用入口与权限控制**
- 用例数: 12 个
- Critical: 7 个, High: 5 个

**Breadcrumb 下拉菜单切换**
- 用例数: 15 个
- Critical: 7 个, High: 6 个, Medium: 2 个

## 注意事项

1. 测试环境需要配置以下内容：
   - Prodigy Dashboard 测试需要配置：
     * 多个 Lifecycle 环境（Dev、Uat、Prod）
     * 多个 Role 和权限组
     * 多个 Level（Global、Sponsor、Study）
     * 多个 Sponsor 和 Study
     * 不同的 Module 应用访问权限

2. 测试数据准备：
   - Prodigy Dashboard 测试需要准备：
     * 不同权限的测试用户账号
     * 多个 Sponsor 和 Study 的测试数据
     * 不同 Level 下的应用访问权限配置
     * 不同 Lifecycle 下的 Role 配置

3. 测试执行顺序：
   - 建议按照优先级从高到低执行
   - 同一优先级内，建议按照测试场景顺序执行
   - 每个测试场景内，建议按照用例编号顺序执行

4. 缺陷跟踪：
   - 发现缺陷时，记录详细的复现步骤
   - 关联对应的需求编号和用例编号
   - 标注缺陷的严重程度和优先级

5. 测试报告：
   - 记录每个测试用例的执行结果（Pass/Fail）
   - 统计测试覆盖率
   - 汇总缺陷数量和分布
   - 提供测试结论和建议

## 测试重点

### User Dashboard 测试重点
- Lifecycle 和 Role 的显示逻辑和优先级
- Breadcrumb Component 在不同 Level 下的显示格式
- Applications 根据用户权限的动态过滤
- Administration 应用的特殊提示信息

### Enter Application 测试重点
- 不同 Level（Global、Sponsor、Study）下的应用列表
- Breadcrumb bar 的默认值显示
- 应用访问权限的验证
- Lifecycle 在 Breadcrumb bar 最右侧的显示

### Changing Breadcrumb Dropdown 测试重点
- 6 步切换流程的完整性和正确性
- 下拉菜单根据上下文动态更新
- 不同 Level 下 Breadcrumb 组件的显示差异
- 切换过程中的数据一致性
- 错误处理和快速切换的稳定性

## 测试覆盖范围

本测试用例集覆盖了 Prodigy Dashboard 的以下功能：

1. **用户登录和重定向**
   - 登录后自动跳转到 Dashboard
   - Dashboard 页面的基本布局和组件

2. **Lifecycle 和 Role 管理**
   - Lifecycle 列表显示和优先级
   - Role 根据 Lifecycle 动态显示
   - Lifecycle 和 Role 在 Breadcrumb 中的位置

3. **Level 切换和显示**
   - Global、Sponsor、Study 三个 Level
   - 不同 Level 下的 Breadcrumb 格式
   - 不同 Level 下的应用列表

4. **应用访问控制**
   - 根据用户权限显示应用
   - 不同 Level 下的应用分类
   - 无权限用户的处理

5. **Breadcrumb 下拉菜单切换**
   - 6 步切换流程（Lifecycle → Role → Level → Sponsor → Study → Module）
   - 下拉菜单的动态更新
   - 切换过程中的数据一致性

6. **异常场景处理**
   - 无权限用户访问
   - 网络错误处理
   - 快速连续切换

