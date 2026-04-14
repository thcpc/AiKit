#!/usr/bin/env python3
"""
API Repository Manager
管理 apiRepository 文件夹中的接口索引和 JSON 文件。
提供 add_new、update、query、remove 四个操作。

Python 版本: 3.13
"""

import os
import sys
import json
import shutil
import time
import argparse
from pathlib import Path

REPO_DIR = "apiRepository"
INDEX_FILE = os.path.join(REPO_DIR, "apiRepositoryIndex.md")

INDEX_HEADER = """|  接口名   |  所属集合   |  映射文件   |
| --------  | --------   | --------   |
"""


def _ensure_repo():
    """确保 apiRepository 文件夹和索引文件存在。"""
    os.makedirs(REPO_DIR, exist_ok=True)
    if not os.path.exists(INDEX_FILE):
        with open(INDEX_FILE, "w", encoding="utf-8") as f:
            f.write(INDEX_HEADER)


def _read_index():
    """读取索引文件，返回行列表（每行为 dict: 接口名, 所属集合, 映射文件）。"""
    _ensure_repo()
    entries = []
    with open(INDEX_FILE, "r", encoding="utf-8") as f:
        lines = f.readlines()
    for line in lines:
        line = line.strip()
        if not line.startswith("|") or line.startswith("|  接口名") or line.startswith("| ----"):
            continue
        parts = [p.strip() for p in line.split("|") if p.strip()]
        if len(parts) >= 3:
            entries.append({
                "接口名": parts[0],
                "所属集合": parts[1],
                "映射文件": parts[2],
            })
    return entries


def _write_index(entries):
    """将 entries 写回索引文件。"""
    _ensure_repo()
    with open(INDEX_FILE, "w", encoding="utf-8") as f:
        f.write(INDEX_HEADER)
        for e in entries:
            f.write(f"| {e['接口名']}         |  {e['所属集合']}   |   {e['映射文件']}  |\n")


def _api_to_filename(api_name):
    """将接口名转为文件名前缀：替换 / 为 -。"""
    return api_name.replace("/", "-")


def _generate_mapped_filename(api_name):
    """生成映射文件名：{接口名}.{13位时间戳}.json。"""
    prefix = _api_to_filename(api_name)
    ts = int(time.time() * 1000)
    return f"{prefix}.{ts}.json"


def add_new(api, collection, source):
    """
    新增接口到 apiRepository。
    - 将 source 文件拷贝到 apiRepository 目录下，按命名格式重命名
    - 在 apiRepositoryIndex.md 中添加记录
    """
    _ensure_repo()
    if not os.path.exists(source):
        print(json.dumps({"error": f"Source file not found: {source}"}, ensure_ascii=False))
        sys.exit(1)

    mapped_name = _generate_mapped_filename(api)
    dest_path = os.path.join(REPO_DIR, mapped_name)
    shutil.copy2(source, dest_path)

    entries = _read_index()
    entries.append({
        "接口名": api,
        "所属集合": collection,
        "映射文件": mapped_name,
    })
    _write_index(entries)
    print(json.dumps({"status": "ok", "action": "add_new", "api": api, "collection": collection, "映射文件": mapped_name}, ensure_ascii=False))


def update(api, collection, source=None):
    """
    更新接口。
    - 场景1（无 source）：更新已有接口的所属集合，以逗号分隔追加
    - 场景2（有 source）：用新文件覆盖原有映射文件（生成新时间戳）
    """
    _ensure_repo()
    entries = _read_index()
    found = False

    for e in entries:
        if e["接口名"] == api:
            if source is None:
                # 场景1：追加所属集合
                existing = [c.strip() for c in e["所属集合"].split(",")]
                if collection not in existing:
                    existing.append(collection)
                    e["所属集合"] = ", ".join(existing)
                found = True
            else:
                # 场景2：同一集合，覆盖文件
                if collection in [c.strip() for c in e["所属集合"].split(",")]:
                    if not os.path.exists(source):
                        print(json.dumps({"error": f"Source file not found: {source}"}, ensure_ascii=False))
                        sys.exit(1)
                    # 删除旧文件
                    old_path = os.path.join(REPO_DIR, e["映射文件"])
                    if os.path.exists(old_path):
                        os.remove(old_path)
                    # 拷贝新文件
                    new_name = _generate_mapped_filename(api)
                    shutil.copy2(source, os.path.join(REPO_DIR, new_name))
                    e["映射文件"] = new_name
                    found = True

    if found:
        _write_index(entries)
        print(json.dumps({"status": "ok", "action": "update", "api": api, "collection": collection}, ensure_ascii=False))
    else:
        print(json.dumps({"status": "not_found", "action": "update", "api": api}, ensure_ascii=False))


def query(api):
    """
    查询接口。返回所有接口名匹配的记录列表。
    """
    entries = _read_index()
    results = [e for e in entries if e["接口名"] == api]
    print(json.dumps(results, ensure_ascii=False))


def remove(api, collection):
    """
    删除接口。
    - 场景1：相同接口有多条记录，移除满足条件的那条，删除对应映射文件
    - 场景2：相同接口只有一条记录但有多个所属集合，仅移除指定集合名
    """
    _ensure_repo()
    entries = _read_index()
    new_entries = []

    for e in entries:
        if e["接口名"] == api:
            collections = [c.strip() for c in e["所属集合"].split(",")]
            if collection in collections:
                if len(collections) > 1:
                    # 场景2：多个集合，仅移除指定集合
                    collections.remove(collection)
                    e["所属集合"] = ", ".join(collections)
                    new_entries.append(e)
                else:
                    # 场景1：单个集合，移除整条记录并删除文件
                    file_path = os.path.join(REPO_DIR, e["映射文件"])
                    if os.path.exists(file_path):
                        os.remove(file_path)
                    continue
            else:
                new_entries.append(e)
        else:
            new_entries.append(e)

    _write_index(new_entries)
    print(json.dumps({"status": "ok", "action": "remove", "api": api, "collection": collection}, ensure_ascii=False))


def main():
    parser = argparse.ArgumentParser(description="API Repository Manager")
    subparsers = parser.add_subparsers(dest="command", help="操作命令")

    # add_new
    p_add = subparsers.add_parser("add_new", help="新增接口")
    p_add.add_argument("--api", required=True, help="接口名")
    p_add.add_argument("--collection", required=True, help="所属集合")
    p_add.add_argument("--source", required=True, help="映射文件源文件路径")

    # update
    p_update = subparsers.add_parser("update", help="更新接口")
    p_update.add_argument("--api", required=True, help="接口名")
    p_update.add_argument("--collection", required=True, help="所属集合")
    p_update.add_argument("--source", help="映射文件源文件路径（可选）")

    # query
    p_query = subparsers.add_parser("query", help="查询接口")
    p_query.add_argument("--api", required=True, help="接口名")

    # remove
    p_remove = subparsers.add_parser("remove", help="删除接口")
    p_remove.add_argument("--api", required=True, help="接口名")
    p_remove.add_argument("--collection", required=True, help="所属集合")

    args = parser.parse_args()

    if args.command == "add_new":
        add_new(args.api, args.collection, args.source)
    elif args.command == "update":
        update(args.api, args.collection, args.source)
    elif args.command == "query":
        query(args.api)
    elif args.command == "remove":
        remove(args.api, args.collection)
    else:
        parser.print_help()


if __name__ == "__main__":
    main()
