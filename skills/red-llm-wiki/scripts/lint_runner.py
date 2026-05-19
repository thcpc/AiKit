"""
lint_runner.py — 知识库健康检查脚本

用法：python lint_runner.py <wiki_root> [topic_name]

检查项：
1. 孤立页面（entities/ 下没有被其他页面引用的实体）
2. 断链（[[X]] 链接指向的 X.md 不存在）
3. index 一致性（index.md 里有记录但文件缺失的条目）

输出 JSON 格式的检查报告。
"""

import sys
import os
import re
import json
from pathlib import Path


# 匹配 [[链接名]] 或 [[链接名|别名]] 语法
WIKI_LINK_PATTERN = re.compile(r"\[\[([^\]|]+)(?:\|[^\]]+)?\]\]")


def find_all_md_files(directory: Path) -> list[Path]:
    """递归查找目录下所有 .md 文件"""
    return list(directory.rglob("*.md"))


def extract_wiki_links(file_path: Path) -> list[str]:
    """从文件中提取所有 [[X]] 链接"""
    try:
        content = file_path.read_text(encoding="utf-8")
    except (UnicodeDecodeError, FileNotFoundError):
        return []
    return WIKI_LINK_PATTERN.findall(content)


def check_orphan_pages(topic_dir: Path, all_links: set[str]) -> list[dict]:
    """检查孤立页面：entities/ 下没有被其他页面引用的实体"""
    issues = []
    entities_dir = topic_dir / "entities"
    if not entities_dir.exists():
        return issues

    for entity_file in entities_dir.glob("*.md"):
        entity_name = entity_file.stem
        if entity_name not in all_links:
            issues.append({
                "type": "orphan_page",
                "file": str(entity_file.relative_to(topic_dir)),
                "name": entity_name,
                "message": f"实体 '{entity_name}' 没有被其他页面引用",
            })
    return issues


def check_broken_links(topic_dir: Path, all_files: set[str], all_links_with_source: list[tuple[str, str]]) -> list[dict]:
    """检查断链：[[X]] 链接指向的 X.md 不存在"""
    issues = []
    for link_name, source_file in all_links_with_source:
        if link_name not in all_files:
            issues.append({
                "type": "broken_link",
                "link": link_name,
                "source": source_file,
                "message": f"链接 [[{link_name}]] 指向的页面不存在（来源: {source_file}）",
            })
    return issues


def check_index_consistency(topic_dir: Path) -> list[dict]:
    """检查 index 一致性：index.md 里有记录但文件缺失"""
    issues = []
    index_file = topic_dir / "index.md"
    if not index_file.exists():
        return issues

    try:
        content = index_file.read_text(encoding="utf-8")
    except (UnicodeDecodeError, FileNotFoundError):
        return issues

    # 提取 index.md 中引用的链接
    links_in_index = WIKI_LINK_PATTERN.findall(content)

    # 获取 topic 下所有文件名（不含扩展名）
    all_file_stems = set()
    for md_file in find_all_md_files(topic_dir):
        all_file_stems.add(md_file.stem)

    for link in links_in_index:
        if link not in all_file_stems:
            issues.append({
                "type": "index_missing_file",
                "link": link,
                "message": f"index.md 中记录了 [[{link}]]，但对应文件不存在",
            })

    return issues


def lint_topic(wiki_root: Path, topic_name: str) -> dict:
    """对单个 topic 执行 lint 检查"""
    topic_dir = wiki_root / "wiki" / topic_name
    if not topic_dir.exists():
        return {"error": f"Topic 目录不存在: {topic_dir}"}

    # 收集所有 md 文件
    all_md_files = find_all_md_files(topic_dir)
    all_file_stems = {f.stem for f in all_md_files}

    # 收集所有链接
    all_links: set[str] = set()
    all_links_with_source: list[tuple[str, str]] = []

    for md_file in all_md_files:
        links = extract_wiki_links(md_file)
        relative_path = str(md_file.relative_to(topic_dir))
        for link in links:
            all_links.add(link)
            all_links_with_source.append((link, relative_path))

    # 执行检查
    issues = []
    issues.extend(check_orphan_pages(topic_dir, all_links))
    issues.extend(check_broken_links(topic_dir, all_file_stems, all_links_with_source))
    issues.extend(check_index_consistency(topic_dir))

    return {
        "topic": topic_name,
        "total_files": len(all_md_files),
        "total_links": len(all_links),
        "issues": issues,
        "summary": {
            "orphan_pages": len([i for i in issues if i["type"] == "orphan_page"]),
            "broken_links": len([i for i in issues if i["type"] == "broken_link"]),
            "index_issues": len([i for i in issues if i["type"] == "index_missing_file"]),
        },
    }


def main():
    if len(sys.argv) < 2:
        print("用法: python lint_runner.py <wiki_root> [topic_name]")
        sys.exit(1)

    wiki_root = Path(sys.argv[1])
    if not wiki_root.exists():
        print(json.dumps({"error": f"Wiki 根目录不存在: {wiki_root}"}, ensure_ascii=False))
        sys.exit(1)

    # 如果指定了 topic，只检查该 topic；否则检查所有
    if len(sys.argv) >= 3:
        topic_name = sys.argv[2]
        result = lint_topic(wiki_root, topic_name)
        print(json.dumps(result, ensure_ascii=False, indent=2))
    else:
        wiki_dir = wiki_root / "wiki"
        if not wiki_dir.exists():
            print(json.dumps({"error": "wiki/ 目录不存在"}, ensure_ascii=False))
            sys.exit(1)

        results = []
        for topic_dir in wiki_dir.iterdir():
            if topic_dir.is_dir():
                result = lint_topic(wiki_root, topic_dir.name)
                results.append(result)

        print(json.dumps(results, ensure_ascii=False, indent=2))


if __name__ == "__main__":
    main()
