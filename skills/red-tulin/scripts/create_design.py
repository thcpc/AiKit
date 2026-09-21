"""
create_design.py — 根据模板生成代码设计文档

用法：
    python3 create_design.py <work_space> --kind <class|function> \
        --namespace <namespace> --filename <filename> \
        --language <language> --version <version>

说明：
    根据设计场景（class / function）读取对应模板
    (assets/class-design-template.md 或 assets/function-design-template.md)，
    填充 frontmatter 参数，拼接 assets/change-log-section.md 中定义的
    「变更记录」章节，生成：
        designs/{namespace}/{filename}.class-design.md
        或
        designs/{namespace}/{filename}.function-design.md

    初始状态固定为 Designing。
"""

import sys
import argparse
import socket
from pathlib import Path
from datetime import datetime

# Windows 默认控制台编码可能是 GBK，无法打印 emoji，这里做兼容处理
if sys.stdout.encoding and sys.stdout.encoding.lower() != "utf-8":
    sys.stdout.reconfigure(encoding="utf-8", errors="replace")
    sys.stderr.reconfigure(encoding="utf-8", errors="replace")


def load_template(skill_dir: Path, kind: str) -> str:
    template_name = "class-design-template.md" if kind == "class" else "function-design-template.md"
    template_path = skill_dir / "assets" / template_name
    if not template_path.exists():
        print(f"错误: 模板文件不存在: {template_path}")
        sys.exit(1)
    return template_path.read_text(encoding="utf-8")


def load_change_log_section(skill_dir: Path) -> str:
    section_path = skill_dir / "assets" / "change-log-section.md"
    if not section_path.exists():
        print(f"错误: 变更记录章节模板不存在: {section_path}")
        sys.exit(1)
    return section_path.read_text(encoding="utf-8")


def fill_frontmatter(template: str, namespace: str, filename: str,
                      language: str, version: str) -> str:
    now = datetime.now().strftime("%Y-%m-%d %H:%M:%S")
    hostname = socket.gethostname()

    replacements = {
        "{{hostname}}": hostname,
        "{{language}}": language,
        "{{version}}": version,
        "{{namespace}}": namespace,
        "{{filename}}": filename,
        "{{status}}": "Designing",
    }

    content = template
    # created/updated 均填当前时间
    content = content.replace("{{date:YYYY-MM-DD HH:mm:ss}}", now)
    for key, value in replacements.items():
        content = content.replace(key, value)
    return content


def fill_initial_change_log(section: str) -> str:
    """首次生成时，变更记录填"首次生成"相关占位"""
    now = datetime.now().strftime("%Y-%m-%d %H:%M:%S")
    content = section
    content = content.replace("{{date:YYYY-MM-DD HH:mm:ss}}", now)
    content = content.replace("{{操作类型}}", "生成")
    content = content.replace("{{初始化 / 生成 / 更新}}", "生成")
    content = content.replace("{{变更 / 关联更新}}", "首次生成")
    content = content.replace("{{ID}}", "N/A")
    content = content.replace("一句话总结本次操作", "首次生成设计文档")
    return content


def main():
    parser = argparse.ArgumentParser()
    parser.add_argument("work_space")
    parser.add_argument("--kind", required=True, choices=["class", "function"])
    parser.add_argument("--namespace", required=True)
    parser.add_argument("--filename", required=True)
    parser.add_argument("--language", required=True)
    parser.add_argument("--version", required=True)
    args = parser.parse_args()

    work_space = Path(args.work_space)
    if not work_space.is_absolute():
        work_space = work_space.resolve()

    skill_dir = Path(__file__).parent.parent  # red-tulin/

    template = load_template(skill_dir, args.kind)
    change_log_section = load_change_log_section(skill_dir)

    filled = fill_frontmatter(template, args.namespace, args.filename,
                               args.language, args.version)
    filled_log = fill_initial_change_log(change_log_section)

    suffix = "class-design.md" if args.kind == "class" else "function-design.md"
    target_dir = work_space / "designs" / args.namespace
    target_dir.mkdir(parents=True, exist_ok=True)
    target_path = target_dir / f"{args.filename}.{suffix}"

    if target_path.exists():
        print(f"错误: 设计文档已存在: {target_path}")
        sys.exit(1)

    full_content = filled.rstrip("\n") + "\n\n" + filled_log
    target_path.write_text(full_content, encoding="utf-8")

    print(f"已生成设计文档: {target_path}")


if __name__ == "__main__":
    main()
