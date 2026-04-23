# API Repository Manager 工作流

## 概述

本工作流管理 `apiRepository` 文件夹，作为接口 JSON 文件的本地仓库。当 Generator 生成接口 JSON 文件后，Manager 负责判断每个接口应执行新增、更新还是跳过操作，并通过 `api_repository_manager.py` 脚本执行。

---

## apiRepository 文件结构

```
apiRepository/
├── apiRepositoryIndex.md    # Markdown 索引文件
├── admin-auth.1744105680123.json
├── admin-user-onboard-company.1744105680124.json
└── ...
```

### apiRepositoryIndex.md 格式

|  接口名   |  所属集合   |  映射文件   |
| --------  | --------   | --------   |
| admin/auth | designer-add-crf-item | admin-auth.1744105680123.json |

### 接口文件命名格式

`{接口名}.{时间戳}.json`
- 接口名：将 `/` 替换为 `-`
- 时间戳：13 位毫秒级时间戳

示例：`admin/user/onboard/company` → `admin-user-onboard-company.1744105680123.json`

---

## 脚本使用方式

脚本路径：`~/.kiro/powers/repos/edk-api-power/powers/edk-api-power/scripts/api_repository_manager.py`

### 初始化 apiRepository

首次使用时，脚本会自动在工作区根目录创建 `apiRepository/` 文件夹和 `apiRepositoryIndex.md` 索引文件。

### 命令行接口

```bash
# 新增
python ~/.kiro/powers/repos/edk-api-power/powers/edk-api-power/scripts/api_repository_manager.py add_new --api "admin/auth" --collection "designer-add-crf-item" --source "designer-add-crf-item/01-auth.json"

# 更新（追加集合）
python ~/.kiro/powers/repos/edk-api-power/powers/edk-api-power/scripts/api_repository_manager.py update --api "admin/auth" --collection "designer-new-crf-item"

# 更新（覆盖文件）
python ~/.kiro/powers/repos/edk-api-power/powers/edk-api-power/scripts/api_repository_manager.py update --api "admin/auth" --collection "designer-add-crf-item" --source "designer-add-crf-item/01-auth-v2.json"

# 查询
python ~/.kiro/powers/repos/edk-api-power/powers/edk-api-power/scripts/api_repository_manager.py query --api "admin/auth"

# 删除
python ~/.kiro/powers/repos/edk-api-power/powers/edk-api-power/scripts/api_repository_manager.py remove --api "admin/auth" --collection "designer-add-crf-item"
```

---

## Manager 操作逻辑

当 Generator 传来接口名、所属集合、source 文件路径时，Manager 按以下逻辑判断操作：

### 判断流程

1. **检查接口名是否已存在于 apiRepositoryIndex.md 中**
   - 如果**不存在** → 执行 `add_new`，结束
   - 如果**存在** → 进入循环检查

2. **循环检查所有同名接口记录**
   对每条同名记录：
   - 比较 source 文件中的 `event.script` 逻辑与已有接口的 script 逻辑是否相似
   - 如果**逻辑相似**：
     - 执行 `update` 场景1（追加所属集合），继续检查下一条
   - 如果**逻辑不相似**：
     - 检查该记录的所属集合是否与传入的集合相同
     - 如果**集合已存在** → 执行 `update` 场景2（覆盖文件），结束
     - 如果**集合不存在** → 跳出循环

3. **循环结束后**（所有同名记录都已检查完，且未被中途终止）
   - 执行 `add_new`，结束

### script 逻辑相似性判断

比较两个接口 JSON 文件中 `event` 数组里的 script 内容：
- 提取 `listen: "prerequest"` 和 `listen: "test"` 的 `script.exec` 数组
- 忽略变量名差异，比较核心逻辑结构（如：都是提取 token、都是构建请求体、都是加密密码）
- 如果核心逻辑相同（如都从 `res.payload.token` 提取 token），判定为相似
- 如果逻辑结构不同（如一个提取 token，另一个提取 companyId 列表），判定为不相似

---

## 与 Generator 的交互

### Generator → Manager（查询阶段）

Generator 在生成 JSON 文件前，先向 Manager 查询已有接口：

```bash
python ~/.kiro/powers/repos/edk-api-power/powers/edk-api-power/scripts/api_repository_manager.py query --api "admin/auth"
```

返回结果供 Generator 参考已有的 Collection JSON 来生成新的接口文件。

### Generator → Manager（提交阶段）

Generator 生成 JSON 文件后，用户确认提交时，对每个接口文件执行 Manager 操作逻辑：

1. 遍历 Generator 输出文件夹中的所有 JSON 文件
2. 从文件名和内容中提取接口名
3. 从 api-plan.md 文件名提取所属集合名
4. 按 Manager 操作逻辑判断执行 add_new 或 update

---

## 注意事项

- `apiRepository` 文件夹位于工作区根目录
- 索引文件 `apiRepositoryIndex.md` 是 Markdown 表格格式，便于人工查看
- 所有操作通过 `api_repository_manager.py` 脚本执行，输出 JSON 格式结果
- 脚本需要 Python 3.13 环境
