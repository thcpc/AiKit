"""
init.py — 初始化 red-tulin 工作目录

用法：
    python3 init.py <work_space> [--set-schema <language> <version>]

说明：
    在 <work_space> 下创建/检查 red-tulin 标准目录结构：
        designs/
        .relationship.json   (初始内容为空对象 {})
        .red-tulin.schema.md
        .red-tulin.log.md

    --set-schema：将 language/version 写入 .red-tulin.schema.md（用户在 init
    工作流中被询问后，由调用方传入此参数完成更新）。
"""

import sys
import json
from pathlib import Path
from datetime import datetime

# Windows 默认控制台编码可能是 GBK，无法打印 emoji，这里做兼容处理
if sys.stdout.encoding and sys.stdout.encoding.lower() != "utf-8":
    sys.stdout.reconfigure(encoding="utf-8", errors="replace")
    sys.stderr.reconfigure(encoding="utf-8", errors="replace")


def ensure_designs_dir(work_space: Path) -> str:
    """确保 designs/ 文件夹存在，返回创建提示（已存在则为空字符串）"""
    designs_dir = work_space / "designs"
    if not designs_dir.exists():
        designs_dir.mkdir(parents=True, exist_ok=True)
        return "designs/"
    return ""


def ensure_schema_file(work_space: Path) -> str:
    """确保 .red-tulin.schema.md 存在，返回创建提示"""
    schema_path = work_space / ".red-tulin.schema.md"
    if not schema_path.exists():
        schema_path.write_text(
            "# red-tulin 项目配置\n\n"
            "language: \n"
            "version: \n",
            encoding="utf-8",
        )
        return ".red-tulin.schema.md"
    return ""


def ensure_log_file(work_space: Path) -> str:
    """确保 .red-tulin.log.md 存在，返回创建提示"""
    log_path = work_space / ".red-tulin.log.md"
    if not log_path.exists():
        log_path.write_text("# red-tulin 代码编写日志\n\n", encoding="utf-8")
        return ".red-tulin.log.md"
    return ""


def ensure_relationship_file(work_space: Path) -> str:
    """确保 .relationship.json 存在（初始为空对象），返回创建提示"""
    rel_path = work_space / ".relationship.json"
    if not rel_path.exists():
        rel_path.write_text(json.dumps({}, indent=2, ensure_ascii=False), encoding="utf-8")
        return ".relationship.json"
    return ""


def update_schema(work_space: Path, language: str, version: str) -> None:
    """将 language/version 写入 .red-tulin.schema.md"""
    schema_path = work_space / ".red-tulin.schema.md"
    content = (
        "# red-tulin 项目配置\n\n"
        f"language: {language}\n"
        f"version: {version}\n"
    )
    schema_path.write_text(content, encoding="utf-8")


def is_schema_incomplete(work_space: Path) -> bool:
    """判断 .red-tulin.schema.md 中的 language 或 version 是否未填写"""
    schema_path = work_space / ".red-tulin.schema.md"
    if not schema_path.exists():
        return True
    content = schema_path.read_text(encoding="utf-8")
    for line in content.splitlines():
        line = line.strip()
        if line.startswith("language:") and line.split(":", 1)[1].strip() == "":
            return True
        if line.startswith("version:") and line.split(":", 1)[1].strip() == "":
            return True
    return False


def main():
    if len(sys.argv) < 2:
        print("用法: python3 init.py <work_space> [--set-schema <language> <version>]")
        sys.exit(1)

    work_space = Path(sys.argv[1])
    if not work_space.is_absolute():
        work_space = work_space.resolve()

    if not work_space.exists():
        print(f"错误: 工作目录不存在: {work_space}")
        sys.exit(1)

    created = []

    item = ensure_designs_dir(work_space)
    if item:
        created.append(item)

    item = ensure_schema_file(work_space)
    if item:
        created.append(item)

    item = ensure_log_file(work_space)
    if item:
        created.append(item)

    item = ensure_relationship_file(work_space)
    if item:
        created.append(item)

    # --set-schema 参数：更新 language/version
    if "--set-schema" in sys.argv:
        idx = sys.argv.index("--set-schema")
        if idx + 2 < len(sys.argv):
            language = sys.argv[idx + 1]
            version = sys.argv[idx + 2]
            update_schema(work_space, language, version)
            print(f"已更新 .red-tulin.schema.md: language={language}, version={version}")
        else:
            print("错误: --set-schema 需要提供 <language> <version> 两个参数")
            sys.exit(1)

    if created:
        print(f"已创建 {len(created)} 个目录/文件:")
        for c in created:
            print(f"  - {c}")
    else:
        print("所有目录和文件已存在，无需创建。")

    if is_schema_incomplete(work_space):
        print("\n[警告] .red-tulin.schema.md 中 language 或 version 尚未填写，"
              "请通过 --set-schema 参数补全。")

    print("\n工程已初始化好。")


if __name__ == "__main__":
    main()
