"""
读取 PDF 文件并输出纯文本内容。

用法：
  py scripts/read_pdf.py <pdf_path> [--pages START-END] [--outline-only]

参数：
  pdf_path        PDF 文件路径
  --pages         页码范围（如 1-10, 5-20），默认全部
  --outline-only  仅输出每页前 200 字符作为大纲预览

示例：
  py scripts/read_pdf.py raw/pdfs/Define-XML-v2.1-Specification.pdf
  py scripts/read_pdf.py raw/pdfs/Define-XML-v2.1-Specification.pdf --pages 1-20
  py scripts/read_pdf.py raw/pdfs/Define-XML-v2.1-Specification.pdf --outline-only
"""

import sys
import argparse
from pathlib import Path

try:
    from pypdf import PdfReader
except ImportError:
    print("ERROR: pypdf 未安装。请运行: py -m pip install pypdf", file=sys.stderr)
    sys.exit(1)


def main():
    parser = argparse.ArgumentParser(description="读取 PDF 文件并输出纯文本")
    parser.add_argument("pdf_path", help="PDF 文件路径")
    parser.add_argument("--pages", help="页码范围，如 1-10（1-indexed）", default=None)
    parser.add_argument("--outline-only", action="store_true",
                        help="仅输出每页前 200 字符作为大纲预览")
    args = parser.parse_args()

    pdf_path = Path(args.pdf_path)
    if not pdf_path.exists():
        print(f"ERROR: 文件不存在: {pdf_path}", file=sys.stderr)
        sys.exit(1)

    reader = PdfReader(str(pdf_path))
    total_pages = len(reader.pages)
    print(f"=== PDF 信息 ===")
    print(f"文件: {pdf_path.name}")
    print(f"总页数: {total_pages}")
    print()

    # 确定页码范围
    start_page = 0
    end_page = total_pages
    if args.pages:
        parts = args.pages.split("-")
        start_page = int(parts[0]) - 1  # 转为 0-indexed
        end_page = int(parts[1]) if len(parts) > 1 else start_page + 1

    if start_page < 0:
        start_page = 0
    if end_page > total_pages:
        end_page = total_pages

    print(f"读取范围: 第 {start_page + 1} 页 ~ 第 {end_page} 页")
    print(f"{'=' * 60}")
    print()

    total_chars = 0
    for i in range(start_page, end_page):
        text = reader.pages[i].extract_text() or ""
        total_chars += len(text)

        if args.outline_only:
            preview = text[:200].replace("\n", " ").strip()
            print(f"[Page {i + 1}] {preview}")
            print()
        else:
            print(f"{'─' * 40} Page {i + 1} {'─' * 40}")
            print(text)
            print()

    print(f"{'=' * 60}")
    print(f"总字符数: {total_chars}")


if __name__ == "__main__":
    main()
