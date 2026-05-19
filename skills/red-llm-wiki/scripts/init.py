"""
init.py — 初始化 LLM-Wiki 知识库目录结构

用法：python init.py <wiki_root>

创建以下目录和文件：
- raw/articles/, raw/tweets/, raw/wechat/, raw/xiaohongshu/,
  raw/zhihu/, raw/pdfs/, raw/notes/, raw/assets/
- wiki/
- queries/
- log.md
- topics.md
"""

import sys
import os
from pathlib import Path
from datetime import datetime


def create_wiki_structure(wiki_root: str) -> list[str]:
    """创建知识库目录结构，返回创建的路径列表"""
    root = Path(wiki_root)
    created = []

    # 需要创建的目录
    directories = [
        "raw/articles",
        "raw/tweets",
        "raw/wechat",
        "raw/xiaohongshu",
        "raw/zhihu",
        "raw/pdfs",
        "raw/xmind",
        "raw/notes",
        "raw/assets",
        "wiki",
        "queries",
    ]

    for dir_path in directories:
        full_path = root / dir_path
        if not full_path.exists():
            full_path.mkdir(parents=True, exist_ok=True)
            created.append(str(dir_path))

    # 创建 log.md
    log_path = root / "log.md"
    if not log_path.exists():
        now = datetime.now().strftime("%Y-%m-%d %H:%M:%S")
        log_path.write_text(
            f"# 操作日志\n\n## {now} - init\n\n- **操作**：init\n- **备注**：知识库初始化\n",
            encoding="utf-8",
        )
        created.append("log.md")

    # 创建 topics.md
    topics_path = root / "topics.md"
    if not topics_path.exists():
        now = datetime.now().strftime("%Y-%m-%d %H:%M:%S")
        topics_path.write_text(
            f"---\ncreated: {now}\nupdated: {now}\n---\n",
            encoding="utf-8",
        )
        created.append("topics.md")

    return created


def main():
    if len(sys.argv) < 2:
        print("用法: python init.py <wiki_root>")
        sys.exit(1)

    wiki_root = sys.argv[1]

    if not os.path.isabs(wiki_root):
        wiki_root = os.path.abspath(wiki_root)

    print(f"初始化知识库: {wiki_root}")
    created = create_wiki_structure(wiki_root)

    if created:
        print(f"已创建 {len(created)} 个目录/文件:")
        for item in created:
            print(f"  ✓ {item}")
    else:
        print("所有目录和文件已存在，无需创建。")


if __name__ == "__main__":
    main()
