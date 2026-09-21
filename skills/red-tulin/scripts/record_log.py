"""
record_log.py — 向 .red-tulin.log.md 追加一条日志记录

用法：
    python3 record_log.py <work_space> --object <设计文件路径> --summary <变更摘要> [--change-id <ID>]

说明：
    按 assets/log-template.md 定义的格式：
        {{date:YYYY-MM-DD HH:mm:ss}} {{变更ID}} {{对象}}
        {{变更摘要}}

        ---

    追加一条记录到 .red-tulin.log.md 末尾。仅追加，不修改已有条目。
"""

import sys
import argparse
import uuid
from pathlib import Path
from datetime import datetime

# Windows 默认控制台编码可能是 GBK，无法打印 emoji，这里做兼容处理
if sys.stdout.encoding and sys.stdout.encoding.lower() != "utf-8":
    sys.stdout.reconfigure(encoding="utf-8", errors="replace")
    sys.stderr.reconfigure(encoding="utf-8", errors="replace")


def main():
    parser = argparse.ArgumentParser()
    parser.add_argument("work_space")
    parser.add_argument("--object", required=True, help="本次操作涉及的设计文件路径")
    parser.add_argument("--summary", required=True, help="变更摘要")
    parser.add_argument("--change-id", default=None, help="变更ID，未提供则自动生成 UUID")
    args = parser.parse_args()

    work_space = Path(args.work_space)
    if not work_space.is_absolute():
        work_space = work_space.resolve()

    log_path = work_space / ".red-tulin.log.md"
    if not log_path.exists():
        print(f"错误: 日志文件不存在: {log_path}，请先执行 init 工作流")
        sys.exit(1)

    change_id = args.change_id or str(uuid.uuid4())
    now = datetime.now().strftime("%Y-%m-%d %H:%M:%S")

    entry = f"{now} {change_id} {args.object}\n{args.summary}\n\n---\n"

    with log_path.open("a", encoding="utf-8") as f:
        f.write(entry)

    print(f"已追加日志记录: {args.object}")


if __name__ == "__main__":
    main()
