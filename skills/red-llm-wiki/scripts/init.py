"""
init.py — 初始化 LLM-Wiki 知识库目录结构

用法：
  python init.py <wiki_root>              # 初始化根目录结构
  python init.py <wiki_root> --topic <名>  # 在已有知识库中创建新 topic 标准子目录

根目录会创建：
- raw/articles/, raw/tweets/, raw/wechat/, raw/xiaohongshu/,
  raw/zhihu/, raw/pdfs/, raw/xmind/, raw/notes/, raw/assets/
- wiki/
- queries/
- log.md
- topics.md

--topic 模式会在 wiki/{topicName}/ 下创建：
- entities/, concepts/, procedures/, rules/,
  comparisons/, summaries/, synthesis/
- overview.md, index.md
"""

import sys
import os
from pathlib import Path
from datetime import datetime


TOPIC_SUBDIRS = [
    "entities",
    "concepts",
    "procedures",
    "rules",
    "comparisons",
    "summaries",
    "synthesis",
]


def create_wiki_structure(wiki_root: str) -> list[str]:
    """创建知识库根目录结构，返回创建的路径列表"""
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


def create_topic_structure(wiki_root: str, topic_name: str) -> list[str]:
    """在已有知识库中创建新 topic 标准子目录，返回创建的路径列表"""
    root = Path(wiki_root)
    topic_dir = root / "wiki" / topic_name
    created = []

    # 创建子目录
    for subdir in TOPIC_SUBDIRS:
        full_path = topic_dir / subdir
        if not full_path.exists():
            full_path.mkdir(parents=True, exist_ok=True)
            created.append(f"wiki/{topic_name}/{subdir}")

    # 创建 overview.md
    overview_path = topic_dir / "overview.md"
    if not overview_path.exists():
        now = datetime.now().strftime("%Y-%m-%d %H:%M:%S")
        overview_path.write_text(
            f"# {topic_name} — 知识库总览\n\n> 创建于 {now}\n\n## 关于这个知识库\n\n（待补充）\n\n## 最近更新\n\n（暂无）\n",
            encoding="utf-8",
        )
        created.append(f"wiki/{topic_name}/overview.md")

    # 创建 index.md
    index_path = topic_dir / "index.md"
    if not index_path.exists():
        now = datetime.now().strftime("%Y-%m-%d %H:%M:%S")
        index_path.write_text(
            f"# {topic_name} — 索引\n\n> 最后更新：{now}\n\n## 概览\n\n- 主题：{topic_name}\n- 素材总数：0\n- Wiki 页面总数：0\n\n## 概念\n\n（暂无）\n\n## 实体\n\n（暂无）\n\n## 流程\n\n（暂无）\n\n## 规则\n\n（暂无）\n\n## 素材摘要\n\n（暂无）\n\n## 对比分析\n\n（暂无）\n\n## 综合分析\n\n（暂无）\n",
            encoding="utf-8",
        )
        created.append(f"wiki/{topic_name}/index.md")

    return created


def main():
    if len(sys.argv) < 2:
        print("用法:")
        print("  python init.py <wiki_root>               # 初始化根目录")
        print("  python init.py <wiki_root> --topic <名>  # 创建新 topic 子目录")
        sys.exit(1)

    wiki_root = sys.argv[1]
    if not os.path.isabs(wiki_root):
        wiki_root = os.path.abspath(wiki_root)

    # --topic 模式
    if "--topic" in sys.argv:
        idx = sys.argv.index("--topic")
        if idx + 1 >= len(sys.argv):
            print("错误: --topic 参数需要提供 topic 名称")
            sys.exit(1)
        topic_name = sys.argv[idx + 1]
        print(f"创建 topic 目录: {wiki_root}/wiki/{topic_name}")
        created = create_topic_structure(wiki_root, topic_name)
    else:
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
