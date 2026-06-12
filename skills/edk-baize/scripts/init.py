"""
init.py — 初始化 edk-baize 知识库目录结构

用法：
    python init.py <wiki_root>                # 初始化整个知识库根结构
    python init.py <wiki_root> --topic <name> # 在已有知识库下创建一个 topic 子结构

根据 references/wiki-structure.md 创建以下目录和文件：

根目录：
- raw/sprial/   — Sprial 上的内容
- raw/notes/    — 自己整理的片段笔记
- raw/teams/    — Teams 的聊天片段
- raw/assets/   — 图片等附件
- wiki/         — 知识库
- queries/      — 知识查询结果
- log.md        — 操作日志
- topics.md     — 整体目录

每个 topic（wiki/{topic}/）：
- entities/     — 实体页（具体事物）
- concepts/     — 概念页（抽象概念：是什么/为什么）
- procedures/   — 操作流程页（怎么做）
- rules/        — 业务规则页（约束/状态机/校验）
- comparisons/  — 对比分析
- summaries/    — 素材摘要
- synthesis/    — 跨素材综合分析
"""

import sys
import os
from pathlib import Path
from datetime import datetime


# 标准 topic 子目录（与 references/wiki-structure.md 一致，禁止增减）
TOPIC_SUBDIRS = [
    "entities",
    "concepts",
    "procedures",
    "rules",
    "comparisons",
    "summaries",
    "synthesis",
]


def create_topic_structure(wiki_root: str, topic_name: str) -> list[str]:
    """在已有知识库下创建一个 topic 子结构，返回创建的路径列表"""
    root = Path(wiki_root)
    topic_root = root / "wiki" / topic_name
    created = []

    for sub in TOPIC_SUBDIRS:
        full_path = topic_root / sub
        if not full_path.exists():
            full_path.mkdir(parents=True, exist_ok=True)
            created.append(f"wiki/{topic_name}/{sub}")

    # 创建 overview.md
    overview_path = topic_root / "overview.md"
    if not overview_path.exists():
        now = datetime.now().strftime("%Y-%m-%d %H:%M:%S")
        overview_path.write_text(
            f"# {topic_name} — 知识库总览\n\n> 创建于 {now}\n\n## 关于这个主题\n\n（待补充）\n\n## 最近更新\n\n（暂无）\n",
            encoding="utf-8",
        )
        created.append(f"wiki/{topic_name}/overview.md")

    # 创建 index.md
    index_path = topic_root / "index.md"
    if not index_path.exists():
        now = datetime.now().strftime("%Y-%m-%d %H:%M:%S")
        index_path.write_text(
            f"# {topic_name} — 索引\n\n> 最后更新：{now}\n\n## 概览\n\n- 主题：{topic_name}\n- 素材总数：0\n- Wiki 页面总数：0\n\n## 概念\n\n（暂无）\n\n## 实体\n\n（暂无）\n\n## 操作流程\n\n（暂无）\n\n## 业务规则\n\n（暂无）\n\n## 素材摘要\n\n（暂无）\n\n## 对比分析\n\n（暂无）\n\n## 综合分析\n\n（暂无）\n",
            encoding="utf-8",
        )
        created.append(f"wiki/{topic_name}/index.md")

    return created


def create_wiki_structure(wiki_root: str) -> list[str]:
    """创建知识库目录结构，返回创建的路径列表"""
    root = Path(wiki_root)
    created = []

    # 需要创建的目录（与 references/wiki-structure.md 一致）
    directories = [
        "raw/sprial",
        "raw/notes",
        "raw/teams",
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
            f"---\ncreated: {now}\nupdated: {now}\n---\n\n# 主题目录\n\n（暂无主题，请通过 ingest 添加素材）\n",
            encoding="utf-8",
        )
        created.append("topics.md")

    return created


def main():
    if len(sys.argv) < 2:
        print("用法: python init.py <wiki_root> [--topic <name>]")
        sys.exit(1)

    wiki_root = sys.argv[1]

    if not os.path.isabs(wiki_root):
        wiki_root = os.path.abspath(wiki_root)

    # 解析 --topic
    topic_name = None
    if "--topic" in sys.argv:
        idx = sys.argv.index("--topic")
        if idx + 1 < len(sys.argv):
            topic_name = sys.argv[idx + 1]
        else:
            print("错误: --topic 需要一个 topic 名称")
            sys.exit(1)

    if topic_name:
        # 仅创建 topic 子结构
        print(f"在 {wiki_root} 下创建 topic: {topic_name}")
        created = create_topic_structure(wiki_root, topic_name)
        if created:
            print(f"已创建 {len(created)} 个目录:")
            for item in created:
                print(f"  ✓ {item}")
        else:
            print(f"Topic '{topic_name}' 子目录已全部存在，无需创建。")
        return

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
