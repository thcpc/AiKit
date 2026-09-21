# SKILL 设计模板

> 使用说明：
> 1. 复制本文件，重命名为 `red-tulin.design.md`，放在对应 Skill 目录下
> 2. 填写各章节内容，这是设计文档，不会被 AI 直接引用
> 3. 设计完成后，根据本文档生成正式的 SKILL.md 和 references/ 文件
> 4. 带 `<!-- -->` 的内容是填写说明，完成后可删除

---

## SKILL 定义

### 目标

<!-- 用 2-4 句话描述这个 SKILL 要解决什么问题，为谁服务，核心价值是什么。-->
解决AI生成的代码难维护的问题，人主要负责设计，AI主要负责实现。人的设计要细化到接口做什么
而不是简单的一句话，并且代码跟随设计文档。并且可以让多人协作开发。
服务对象：代码开发者。
核心价值：代码设计回归人类，AI 只是帮忙实现。

### SKILL 名

<!-- 格式：kebab-case，全小写，例如 edk-baize、red-llm-wiki -->

`red-tulin`

### 快速开始

<!-- 用户只需几步就能上手，写触发语义或操作步骤 -->


## 目录结构

<!-- 定义数据目录的标准结构。-->

```
work-space/               # 终端所在的目录
├── designs/              # 代码设计文档，古法编程中的详细设计
│   └── {namespace}/      # 按命名空间/模块划分的子文件夹，设计文档存放于对应命名空间的子文件夹下
├── .relationship.json    # 设计文件间调用关系记录（class/method 级别）
├── .red-tulin.schema.md   # 语言，版本配置文件
└── .red-tulin.log.md      # 代码编写日志
```

## 核心规则

<!-- 列出禁止事项，例如：禁止增减子目录、禁止自动命名路径等 -->
1. 严格遵守 designs 中的设计文档来生成代码，不要臆想，胡乱发散。
2. 有不清晰，拿不准，歧义，需要用户询问，不可自我想象。
---

## 工作流定义

<!-- 每个工作流一节。按以下格式填写。-->

### init

**触发条件**：
<!-- 用户说什么话、或什么事件会触发这个工作流 -->
触发语义：图灵，请帮我初始化工程
**目标**：
<!-- 这个工作流完成后，用户得到了什么 -->
生成工作目录
**主要流程**：
<!-- 用流程图（plantuml/mermaid）或分步列表描述主要逻辑。-->
```plantuml
@startuml
start
:判断是否已经 designs 文件夹;
if (否) then
    :调用 init.py 初始化文件夹;
endif
:判断 .red-tulin.schema.md 是否存在;
if (否) then
    :调用 init.py 生成 .red-tulin.schema.md;
endif
:判断 .red-tulin.schema.md 中的 language 或 version 是否没有填写;
if (否) then
    :等待用户输入;
    note right
询问用户:
language 和 version 分别是什么
    end note
    :调用 init.py 更新 .red-tulin.schema.md;
endif
:判断 .red-tulin.log.md 是否存在;
if (否) then
    :调用 init.py 生成 .red-tulin.log.md;
endif
:判断 .relationship.json 是否存在;
if (否) then
    :调用 init.py 生成 .relationship.json（内容为空对象 {}）;
endif
:提示用户工程已初始化好;
end
@enduml
```
---

### create-design

**触发条件**：
<!-- 用户说什么话、或什么事件会触发这个工作流 -->
触发语义：图灵，请给我一个代码设计文件
**目标**：
<!-- 这个工作流完成后，用户得到了什么 -->
询问一些简单问题，根据设计场景引用 `class-design-template.md` 或 `function-design-template.md`，生成 {filename}.class-design.md 或 {filename}.function-design.md
**主要流程**：
```plantuml
@startuml 设计文档生成流程
start

:显示 .red-tulin.schema.md 中的\n项目默认 language/version 设置\n作为参考;
:询问用户\n等待用户输入;
note right
询问用户:
1.设计场景:
纯函数: 独立函数，无类
类: 有类定义、成员变量、方法
2.语言版本（默认继承项目设置，\n如需覆盖请直接说明）
3.文件名
4.命名空间
5.功能摘要（一句话简介）
end note

if (哪种设计场景) then (纯函数)
    :引用`function-design-template.md`;
else (类)
    :引用`class-design-template.md`;
endif

:调用 create_design.py 根据模板生成\ndesigns/{namespace}/{filename}.class-design.md\n或 designs/{namespace}/{filename}.function-design.md;
note right
language/version 未覆盖时，\n直接写入项目默认设置；\n用户覆盖时，写入用户指定的值。
end note
:调用 record_relationship.py 根据设计文档内容\n（类/方法/成员变量及"处理"中描述的调用关系）\n初始化 .relationship.json 中对应的记录;
end
@enduml
```

---


### change-design

**触发条件**：
<!-- 用户说什么话、或什么事件会触发这个工作流 -->
触发语义：
  - 图灵，请帮我更新 xxx 文件中的 yy 方法的处理逻辑为 “{修改内容}” 
  - 图灵，请帮我更新 xxx 文件中的 yy 方法的输入参数 "{修改内容}" 
  - 图灵，请帮我更新 xxx 文件中的 yy 方法的输出参数 “{修改内容}” 
  - 图灵，请帮我更新 xxx 文件中的 yy 类中的成员变量为 “{修改内容}”
**目标**：
<!-- 这个工作流完成后，用户得到了什么 -->
- 修改设计文档
- 如果有关联设计文档需要修改，得到确认后修改
- 记录变更日志
**主要流程**：

```plantuml
@startuml 文档修改全流程_无goto版
start
:Start;
if (改变的内容是否写在文件内?) then (是)
    :读取文件;
else (否)
endif

' 第一层循环嵌套
:分析修改内容，让用户确认;
note right :显示分析的意图
:等待用户输入;
if (是否确认?) then (确认)
else (否)
    :根据用户的输入再次分析;
    ' 重复执行上一段流程
    :分析修改内容，让用户确认;
    note right :显示分析的意图
    :等待用户输入;
endif

if (.relationship.json是否存在?) then (存在)
    :AI根据.relationship.json分析出影响点;
else (否)
    note right: 无影响，跳过影响点分析
endif

note left
显示影响点，并给出修改影响
|文件名 | 命名空间 | 修改点 | 修改内容 |
------------------------------
列说明:
文件名: 文件名
命名空间: 显示该设计文档的命名空间
修改点: 指明哪里修改，比如说某个方法
修改内容: 表明修改内容，模板如下格式:
具体项 (比如 "输入参数", "处理", "输出") : 从 "yyyyy" 变更为 "zzzzzz"
end note

' 第二层循环嵌套
:等待用户确认并给出反馈意见;
if (是否确认?) then (确认)
else (否)
    :给出反馈意见;
    :等待用户确认并给出反馈意见;
endif

:1.变更相关设计文档内容
2.在相关设计文档中记录「变更记录」
3.修改文档状态为 Changed
4.调用 record_relationship.py 更新 .relationship.json;
:记录日志（调用 record_log.py，\n写入 .red-tulin.log.md）;

note right
询问用户 "是否修改代码"
1.确认修改
2.我再看看
end note

:等待用户输入;
if (是否修改) then (1)
    :AI判断是否需要修改多个设计文档;
    if (需要多文件?) then (是)
        :调用 batch-make 流程;
    else (否)
        :调用 make 流程;
    endif
else (2)
endif

end
@enduml
```

---


### make
**触发条件**：
<!-- 用户说什么话、或什么事件会触发这个工作流 -->
触发语义：图灵，请根据 “xxxx.class-design.md” 或 “xxxx.function-design.md” 为我生成代码
**目标**：
<!-- 这个工作流完成后，用户得到了什么 -->
根据单个设计文档，生成对应代码
**目标代码文件路径的确定**：
<!-- 首次生成（Designed→Created）时，由 AI 根据 namespace 及项目既有代码结构推导目标源代码文件路径，
     无法唯一确定时需向用户询问确认；推导/确认结果写入 .relationship.json 对应记录的 codePath 字段。
     后续修改（Changed→Updated）及 validation 工作流直接读取 codePath，不重新推导，
     以保证多次操作使用同一目标文件；若 codePath 记录的文件已不存在，则视为路径失效，重新推导并更新。-->
**主要流程**：

```plantuml
@startuml
start
' 顶层初始状态判断
if (设计文档状态是否为\nDesigned 或 Changed?) then (否)
  :提示用户：\n该文件设计状态为未确定，因此忽略;
  end
else (是)
  if (是否新生成的方法?) then (是)
    :生成新方法
1. 生成代码
2. 添加注释，注释形式@<ID>;
  else (否)
    if (是否修改已存在方法的部分代码?) then (是)
      :修改代码
1. 注释要修改的代码（不能删除代码）
2. 生成新代码
3. 添加注释，注释形式@<ID>;
    else (否)
      if (是否修改已存在方法的所有代码?) then (是)
        ' 严格按需求串行两步：先注释旧方法，再生成新方法
        :1.注释掉旧方法-不可删除
2.添加注释，注释形式@<ID>;
        :生成新方法
1. 生成代码
2. 添加注释，注释形式@<ID>;
      else (否)
        if (删除已存在的方法?) then (是)
          :1.注释方法-不可直接删除
2.添加注释，注释形式@<ID>
3.标记该方法待从 .relationship.json 中移除;
        else (否)
          end
        endif
      endif
    endif
  endif
endif
' 所有合法业务分支在此汇聚，进入后续文档状态处理
if (判断该设计文档当前的状态) then (Designed)
  :Designed 状态
更新为 Created;
else (Changed)
  :Changed 状态
更新为 Updated;
endif
:调用 record_relationship.py
1. 将本次新增/修改/删除的目标代码文件路径写入 .relationship.json 对应记录的 codePath 字段
2. 同步移除本次删除方法对应的 methods 记录;
:记录日志（调用 record_log.py，写入 .red-tulin.log.md）;
end
@enduml
```

### batch-make
**触发条件**：
<!-- 用户说什么话、或什么事件会触发这个工作流 -->
1. 触发语义：图灵，请根据 folder文件夹 或 多个设计文档为我生成代码（此处"设计文档"泛指 {filename}.class-design.md / {filename}.function-design.md）
2. 触发事件：当 change-design 工作流需要修改多个设计文档，然后用户确认生成代码
**目标**：
批量对多个设计文档逐个执行 make 工作流
**主要流程**：
1. 为每个设计文档逐个执行 `make` 工作流
2. 执行 `validation` 工作流
3. 给出执行报告

### validation
**触发条件**：
<!-- 用户说什么话、或什么事件会触发这个工作流 -->
1.触发语义：图灵，请帮我检查代码
2.触发事件：batch-make 执行完成后（自动触发；单独执行 make 不会自动触发 validation）
1，2 是或的关系
**目标**：
<!-- 这个工作流完成后，用户得到了什么 -->
验证代码和对应关系
**主要流程**：
1. 检查状态为 Created、Updated 的设计文档是否和代码文件一一对应（读取 .relationship.json 中对应记录的 codePath 字段，不重新推导；若 codePath 记录的文件不存在，判定为不一致并在报告中列出）。
2. 检查状态为 Created、Updated 的设计文档中的函数是否都已实现。




## 文档类型 / 数据类型

<!-- 如果 SKILL 需要处理多种类型的输入，在这里定义各类型的处理策略。
     如果不需要区分，删除本节。-->

### design 文档状态

| 状态 | 含义 |
|------|------|
| Designing |  设计中，这个也是文档的初始状态。Designing → Designed 需由用户手动修改 frontmatter 中的 status 完成，不通过任何工作流自动触发  |
| Designed  |  设计完成，但是代码没有生成  |
| Created   |  对应代码已生成  |
| Changed   |  设计文档有修改，但没有同步到代码中 |
| Updated   |  修改已同步到代码中 |

---

## 模板定义

<!-- 列出需要创建哪些模板文件，每个模板放在 assets/ 目录下。-->

| 模板文件名 | 用途 | 对应文档类型 |
|-----------|------|-------------|
| class-design-template.md | 类代码设计文档的模板 | {filename}.class-design.md |
| function-design-template.md | 纯方法代码设计文档的模板 | {filename}.function-design.md |
| .project-structure.template.md |  定义工程的目录结构（暂时预留，后续补充对应工作流）   | .project-structure.md |
| log-template.md | 日志模板 | .red-tulin.log.md |
| change-log-section.md | 「变更记录」章节的共享格式定义，由 create_design.py 拼接进设计文档，避免在两个模板中重复定义 | 无独立文档，嵌入 {filename}.class-design.md / {filename}.function-design.md |

---

## 脚本定义

<!-- 列出需要创建哪些脚本，每个脚本放在 scripts/ 目录下。-->
- init.py
初始化工作路径，创建需要的文件夹
- create_design.py
根据模板（class-design-template.md / function-design-template.md），填充参数，并拼接 change-log-section.md 中定义的「变更记录」格式，生成代码设计文件
- record_relationship.py
根据信息，向 .relationship.json 中更新数据（create-design 首次生成设计文档时用于初始化记录，change-design 修改设计文档时用于更新记录）
- record_log.py
根据 log-template.md 格式，向 .red-tulin.log.md 追加一条日志记录
---

## 异常处理

<!-- 列出关键的异常场景和处理策略 -->

| 场景 | 处理方式 |
|------|---------|
| 触发 make 时，指定的设计文档不存在 | 中断流程，提示用户：“{filename} 不存在” |

---

## 规则（草稿）

<!-- 列出这个 SKILL 的核心约束规则 -->

1. 生成的代码，需严格按照定义中设计文档中的定义来，不可臆断，不可扩展，不可想象
2. 调用 python 脚本时，先使用python3 , 如果失败尝试 py, 如果再失败，则终止流程，提示用户 “请安装python 3.13”
3. 之前完成正确的功能，尽量不要修改。
比如当前的 instruction 是完善功能 A 的，那么只需要专注功能 A，不需要修改其他功能（比如功能 B）。
4. 生成的注释用中文，并使用 UTF-8 编码。
5. 生成的代码有时候会存在中文乱码的情况，所以你在生成中文的时候，需要检查是否有中文乱码，如果有乱码需要修正。
6. 如果修改某个函数的实现，先理解之前函数实现的逻辑。然后在原来的基础上，再进行修改（保留之前的函数逻辑，不要移除）
7. 你操作的环境是 windows 系统
8. 如果用户没有明确说，就不需要编写测试脚本，也不需要写专门的项目说明 md
9. 写代码，不考虑 fallback
10. 代码中不要有 emoji
---

## 待确认事项

<!-- 设计过程中还不确定的决策 -->

- [ ] ...

---

## 版本记录

| 日期 | 版本 | 变更说明 |
|------|------|---------|
| YYYY-MM-DD | v0.1 | 初稿 |
