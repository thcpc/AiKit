# 测试任务

## 概述
从 XMind 文件 `{xmind_filename}` 生成的测试任务列表

生成时间：{generation_time}

## 测试用例集清单

#### 需求：{req_name}

- [ ] 测试场景: {scenario_name}
  - 优先级: {priority}
  - 文件: {test_file}
  - 用例数量: {number} 个
    - [ ] 测试用例 {case_id}: {case_title}
        - 优先级: {priority}
        - 方法: {method}
        - 文件: {test_file}
        - 测试任务状态
            - [ ] 审核
            - [ ] 通过
            - [ ] 失败
            - [ ] 阻塞
            - [ ] 废弃
  

    - [ ] 测试用例 {case_id}: {case_title}
        - 优先级: {priority}
        - 方法: {method}
        - 文件: {test_file}
        - 测试任务状态
          - [ ] 审核
          - [ ] 通过
          - [ ] 失败
          - [ ] 阻塞
          - [ ] 废弃

## 统计信息

- 总测试用例数: {total_cases}
- Critical 优先级: {critical_count}
- High 优先级: {high_count}
- Medium 优先级: {medium_count}
- Low 优先级: {low_count}

## 执行计划

### 阶段 1: Critical 优先级测试
执行所有 Critical 优先级的测试用例，确保核心功能正常。

### 阶段 2: High 优先级测试
执行所有 High 优先级的测试用例，验证重要功能。

### 阶段 3: Medium 优先级测试
执行所有 Medium 优先级的测试用例，覆盖常规功能。

### 阶段 4: Low 优先级测试
执行所有 Low 优先级的测试用例，完成全面测试。

## 测试方法分布

- 场景法: {scenario_count}
- 等价类划分: {equivalence_count}
- 边界值分析法: {boundary_count}
- 错误推测法: {error_count}
- 因果图/判定表法: {decision_count}
- 正交试验法: {orthogonal_count}
- 功能图法: {state_count}

## 注意事项

1. 执行测试前确保测试环境已正确配置
2. 按照优先级顺序执行测试
3. 记录测试结果和发现的问题
4. 更新测试用例状态（通过/失败）
5. 对失败的测试用例进行问题分析

## 相关文档

- XMind 设计文件: `testcases/design/{xmind_filename}`
- 测试用例代码: `testcases/tests/`
- 测试规范: `testcases/README.md`
