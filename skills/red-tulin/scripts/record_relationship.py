"""
record_relationship.py — 维护 .relationship.json

用法：
    python3 record_relationship.py <work_space> --action <init|update|set-code-path|remove-method> \
        --key <namespace.filename> [其他参数见下]

    --action init
        --type <class|method> --parent <namespace.filename|None>
        --fields <json字符串，如 '[{"secretKey":{"usedBy":[]}}]'>（可省略，默认 []）
        --methods <json字符串，如 '[{"login":{"paras":"...","invoke":[],"invokeBy":[]}}]'>

    --action update
        与 init 参数相同，会合并更新已有记录（不存在则新建）

    --action set-code-path
        --code-path <相对于 work_space 的路径>
        将 codePath 字段写入对应记录

    --action remove-method
        --method <methodname>
        从 methods 数组中移除指定方法（用于 make 工作流处理"删除已存在的方法"分支）

说明：
    记录格式定义见 references/relationship-definition.md：
    {
      "{namespace}.{filename}": {
        "type": "class" | "method",
        "parent": "{namespace}.{filename}" | "None",
        "codePath": "..." | "None",
        "fields": [...],
        "methods": [...]
      }
    }
"""

import sys
import json
import argparse
from pathlib import Path

# Windows 默认控制台编码可能是 GBK，无法打印 emoji，这里做兼容处理
if sys.stdout.encoding and sys.stdout.encoding.lower() != "utf-8":
    sys.stdout.reconfigure(encoding="utf-8", errors="replace")
    sys.stderr.reconfigure(encoding="utf-8", errors="replace")


def load_relationship(rel_path: Path) -> dict:
    if not rel_path.exists():
        return {}
    content = rel_path.read_text(encoding="utf-8").strip()
    if not content:
        return {}
    return json.loads(content)


def save_relationship(rel_path: Path, data: dict) -> None:
    rel_path.write_text(json.dumps(data, indent=2, ensure_ascii=False), encoding="utf-8")


def main():
    parser = argparse.ArgumentParser()
    parser.add_argument("work_space")
    parser.add_argument("--action", required=True,
                         choices=["init", "update", "set-code-path", "remove-method"])
    parser.add_argument("--key", required=True, help="{namespace}.{filename}")
    parser.add_argument("--type", choices=["class", "method"])
    parser.add_argument("--parent", default="None")
    parser.add_argument("--fields", default="[]")
    parser.add_argument("--methods", default="[]")
    parser.add_argument("--code-path")
    parser.add_argument("--method", help="用于 remove-method")
    args = parser.parse_args()

    work_space = Path(args.work_space)
    if not work_space.is_absolute():
        work_space = work_space.resolve()

    rel_path = work_space / ".relationship.json"
    data = load_relationship(rel_path)

    if args.action in ("init", "update"):
        if not args.type:
            print("错误: init/update 需要提供 --type")
            sys.exit(1)
        try:
            fields = json.loads(args.fields)
            methods = json.loads(args.methods)
        except json.JSONDecodeError as e:
            print(f"错误: --fields 或 --methods 不是合法 JSON: {e}")
            sys.exit(1)

        existing = data.get(args.key, {})
        record = {
            "type": args.type,
            "parent": args.parent,
            "codePath": existing.get("codePath", "None"),
            "fields": fields if fields else existing.get("fields", []),
            "methods": methods if methods else existing.get("methods", []),
        }
        data[args.key] = record
        save_relationship(rel_path, data)
        print(f"已{'初始化' if args.action == 'init' else '更新'} .relationship.json 记录: {args.key}")

    elif args.action == "set-code-path":
        if args.key not in data:
            print(f"错误: .relationship.json 中不存在记录: {args.key}")
            sys.exit(1)
        if not args.code_path:
            print("错误: set-code-path 需要提供 --code-path")
            sys.exit(1)
        data[args.key]["codePath"] = args.code_path
        save_relationship(rel_path, data)
        print(f"已写入 codePath: {args.key} -> {args.code_path}")

    elif args.action == "remove-method":
        if args.key not in data:
            print(f"错误: .relationship.json 中不存在记录: {args.key}")
            sys.exit(1)
        if not args.method:
            print("错误: remove-method 需要提供 --method")
            sys.exit(1)
        methods = data[args.key].get("methods", [])
        new_methods = [m for m in methods if args.method not in m]
        data[args.key]["methods"] = new_methods
        save_relationship(rel_path, data)
        print(f"已从 {args.key} 的 methods 中移除: {args.method}")


if __name__ == "__main__":
    main()
