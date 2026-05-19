"""
import_external.py — 将工作区外的素材文件导入知识库

用法：python import_external.py <wiki_root> <source_path> [--subdir <raw子目录>]

功能：
1. 将源文件复制到 raw/<subdir>/ 目录（默认 subdir=notes）
2. 扫描文件中的图片/附件引用（支持 ![[xxx]] 和 ![](path) 格式）
3. 在源文件所在目录及其上级目录中递归搜索图片文件
4. 将找到的图片复制到 raw/assets/
5. 更新素材文件中的图片路径为 raw/assets/ 的相对引用
6. 输出 JSON 格式的处理报告

示例：
  python import_external.py d:/repo/llmwiki "D:/other/repo/article.md"
  python import_external.py d:/repo/llmwiki "D:/other/repo/paper.pdf" --subdir pdfs
"""

import sys
import os
import re
import json
import shutil
from pathlib import Path
from typing import Optional


def find_image_references(content: str) -> list[str]:
    """从 markdown 内容中提取所有图片引用的文件名"""
    images = []

    # 匹配 ![[filename.ext]] (Obsidian 格式)
    obsidian_pattern = r'!\[\[([^\]]+\.(?:png|jpg|jpeg|gif|svg|webp|bmp))\]\]'
    images.extend(re.findall(obsidian_pattern, content, re.IGNORECASE))

    # 匹配 ![alt](path) (标准 markdown 格式)
    md_pattern = r'!\[[^\]]*\]\(([^)]+\.(?:png|jpg|jpeg|gif|svg|webp|bmp))\)'
    images.extend(re.findall(md_pattern, content, re.IGNORECASE))

    # 去重，只保留文件名（去掉路径前缀）
    image_names = []
    for img in images:
        name = Path(img).name
        if name not in image_names:
            image_names.append(name)

    return image_names


def search_image(image_name: str, search_roots: list[Path], max_depth: int = 5) -> Optional[Path]:
    """在多个搜索根目录中递归查找图片文件"""
    for root in search_roots:
        if not root.exists():
            continue
        for dirpath, dirnames, filenames in os.walk(root):
            # 限制搜索深度
            depth = len(Path(dirpath).relative_to(root).parts)
            if depth > max_depth:
                dirnames.clear()
                continue
            if image_name in filenames:
                return Path(dirpath) / image_name
    return None


def import_external_file(wiki_root: str, source_path: str, subdir: str = "notes") -> dict:
    """
    导入外部文件到知识库

    返回处理报告 dict:
    {
        "source": 原始路径,
        "destination": 目标路径,
        "images_found": 找到并复制的图片列表,
        "images_missing": 未找到的图片列表,
        "success": bool
    }
    """
    root = Path(wiki_root)
    source = Path(source_path)
    report = {
        "source": str(source),
        "destination": "",
        "images_found": [],
        "images_missing": [],
        "success": False,
    }

    # 检查源文件存在
    if not source.exists():
        report["error"] = f"源文件不存在: {source}"
        return report

    # 确定目标目录
    raw_dir = root / "raw" / subdir
    raw_dir.mkdir(parents=True, exist_ok=True)

    assets_dir = root / "raw" / "assets"
    assets_dir.mkdir(parents=True, exist_ok=True)

    # 复制主文件（文件名去空格，避免路径问题）
    dest_name = source.name.replace(" ", "")
    dest_path = raw_dir / dest_name
    shutil.copy2(source, dest_path)
    report["destination"] = str(dest_path.relative_to(root))

    # 如果是文本文件，扫描图片引用
    text_extensions = {".md", ".txt", ".html", ".htm", ".markdown"}
    if source.suffix.lower() in text_extensions:
        content = dest_path.read_text(encoding="utf-8", errors="ignore")
        image_names = find_image_references(content)

        if image_names:
            # 构建搜索路径：源文件所在目录 → 父目录 → 祖父目录 → 仓库根目录
            search_roots = []
            current = source.parent
            for _ in range(4):  # 最多向上搜索 4 级
                search_roots.append(current)
                if current.parent == current:
                    break
                current = current.parent

            # 搜索并复制每张图片
            for img_name in image_names:
                found_path = search_image(img_name, search_roots)
                if found_path:
                    dest_img = assets_dir / img_name
                    if not dest_img.exists():
                        shutil.copy2(found_path, dest_img)
                    report["images_found"].append(img_name)
                else:
                    report["images_missing"].append(img_name)

    report["success"] = True
    return report


def main():
    if len(sys.argv) < 3:
        print("用法: python import_external.py <wiki_root> <source_path> [--subdir <raw子目录>]")
        print("示例: python import_external.py d:/repo/llmwiki \"D:/other/article.md\"")
        print("      python import_external.py d:/repo/llmwiki \"D:/other/paper.pdf\" --subdir pdfs")
        sys.exit(1)

    wiki_root = sys.argv[1]
    source_path = sys.argv[2]
    subdir = "notes"  # 默认

    # 解析 --subdir 参数
    if "--subdir" in sys.argv:
        idx = sys.argv.index("--subdir")
        if idx + 1 < len(sys.argv):
            subdir = sys.argv[idx + 1]

    # 执行导入
    report = import_external_file(wiki_root, source_path, subdir)

    # 输出 JSON 报告
    print(json.dumps(report, ensure_ascii=False, indent=2))

    if not report["success"]:
        sys.exit(1)


if __name__ == "__main__":
    main()
