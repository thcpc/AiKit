"""
init.py — 初始化 SKILL 目录结构

用法：
    python3 init.py <skill_root> [--skill <name>]

说明：
    在 <skill_root> 下创建名为 <name> 的 SKILL 标准目录结构。
    若不指定 --skill，则在 <skill_root> 本身创建子目录结构。

创建内容：
    {skill_root}/{name}/
    ├── scripts/
    ├── references/
    └── assets/
"""

import sys
import os
from pathlib import Path
from datetime import datetime


def create_skill_structure(skill_dir: str) -> list[str]:
    """创建 SKILL 标准子目录结构，返回已创建的路径列表"""
    root = Path(skill_dir)
    created = []

    directories = ["scripts", "references", "assets"]

    for dir_name in directories:
        full_path = root / dir_name
        if not full_path.exists():
            full_path.mkdir(parents=True, exist_ok=True)
            created.append(str(full_path.relative_to(root.parent)))

    return created


def create_log_file(skill_dir: str, skill_name: str) -> str:
    """创建空的日志文件并写入初始条目"""
    log_path = Path(skill_dir) / f"{skill_name}.log.md"
    if not log_path.exists():
        now = datetime.now().strftime("%Y-%m-%d %H:%M:%S")
        log_path.write_text(
            f"# {skill_name} 变更日志\n\n"
            f"## {now} - 初始化\n\n"
            f"- **操作**：初始化\n"
            f"- **摘要**：由 red-tiangong init 工作流创建 SKILL 目录结构\n"
            f"- **design.md 变更**：首次创建\n"
            f"- **文件变更**：\n"
            f"  - 新增：scripts/、references/、assets/、{skill_name}.log.md\n"
            f"  - 更新：无\n",
            encoding="utf-8",
        )
        return str(log_path)
    return ""


def main():
    if len(sys.argv) < 2:
        print("用法: python3 init.py <skill_root> [--skill <name>]")
        print("示例: python3 init.py d:/skills --skill my-skill")
        sys.exit(1)

    skill_root = sys.argv[1]
    if not os.path.isabs(skill_root):
        skill_root = os.path.abspath(skill_root)

    # 解析 --skill 参数
    skill_name = None
    if "--skill" in sys.argv:
        idx = sys.argv.index("--skill")
        if idx + 1 < len(sys.argv):
            skill_name = sys.argv[idx + 1]
        else:
            print("错误: --skill 参数需要提供 SKILL 名称")
            sys.exit(1)

    # 确定目标目录
    if skill_name:
        skill_dir = os.path.join(skill_root, skill_name)
    else:
        skill_dir = skill_root
        skill_name = os.path.basename(skill_root)

    # 检查目录是否已存在
    if os.path.exists(skill_dir) and os.listdir(skill_dir):
        print(f"⚠️  目录已存在且非空: {skill_dir}")
        print("请确认是否继续（将在已有目录中创建缺失的子目录）[y/N]: ", end="")
        answer = input().strip().lower()
        if answer != "y":
            print("已取消。")
            sys.exit(0)

    print(f"初始化 SKILL 目录: {skill_dir}")

    # 创建目录结构
    created = create_skill_structure(skill_dir)

    # 创建日志文件
    log_path = create_log_file(skill_dir, skill_name)
    if log_path:
        created.append(f"{skill_name}.log.md")

    # 复制并替换 design 模板中的占位符
    tiangong_dir = Path(__file__).parent.parent  # red-tiangong 目录
    template_path = tiangong_dir / "assets" / "skill-design-template.md"
    design_path = Path(skill_dir) / f"{skill_name}.design.md"
    if template_path.exists() and not design_path.exists():
        content = template_path.read_text(encoding="utf-8")
        content = content.replace("{skill-name}", skill_name)
        content = content.replace("{skill}", skill_name)
        design_path.write_text(content, encoding="utf-8")
        created.append(f"{skill_name}.design.md")

    if created:
        print(f"已创建 {len(created)} 个目录/文件:")
        for item in created:
            print(f"  ✓ {item}")
    else:
        print("所有目录和文件已存在，无需创建。")

    print(f"\n✅ 初始化完成。")
    print(f"下一步：填写 {skill_name}.design.md，然后对天工说'天工，执行设计'")


if __name__ == "__main__":
    main()
