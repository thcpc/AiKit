"""
HAR Trim - 删除 HAR 文件中 entries 的 _initiator.stack 字段以减小文件体积。
用法: py powers/edk-api-power/scripts/har_trim.py <input.har>
输出: <input>.trim.har
"""
import json
import sys
import os


def strip_stacks(obj):
    """从 HAR 数据中删除所有 entries[]._initiator.stack 字段，返回删除计数。"""
    count = 0
    if "log" in obj and "entries" in obj["log"]:
        for entry in obj["log"]["entries"]:
            if "_initiator" in entry and "stack" in entry["_initiator"]:
                del entry["_initiator"]["stack"]
                count += 1
    return count


def deep_equal(a, b, path=""):
    """递归比较两个对象，返回差异列表（忽略 entries[]._initiator.stack）。"""
    diffs = []
    if type(a) != type(b):
        diffs.append(f"{path}: type mismatch ({type(a).__name__} vs {type(b).__name__})")
        return diffs
    if isinstance(a, dict):
        all_keys = set(a.keys()) | set(b.keys())
        for k in sorted(all_keys):
            if k not in a:
                diffs.append(f"{path}.{k}: missing in trimmed")
            elif k not in b:
                diffs.append(f"{path}.{k}: unexpected in trimmed")
            else:
                diffs.extend(deep_equal(a[k], b[k], f"{path}.{k}"))
        return diffs
    if isinstance(a, list):
        if len(a) != len(b):
            diffs.append(f"{path}: list length mismatch ({len(a)} vs {len(b)})")
            return diffs
        for i in range(len(a)):
            diffs.extend(deep_equal(a[i], b[i], f"{path}[{i}]"))
        return diffs
    if a != b:
        diffs.append(f"{path}: value mismatch")
    return diffs


def verify_trim(input_path, output_path):
    """验证 trim 后的文件除了 entries[]._initiator.stack 外没有数据丢失。"""
    with open(input_path, "r", encoding="utf-8") as f:
        original = json.load(f)
    with open(output_path, "r", encoding="utf-8") as f:
        trimmed = json.load(f)

    # 对原始数据也执行同样的 strip，然后比较
    strip_stacks(original)
    diffs = deep_equal(original, trimmed)
    return diffs


def trim_har(input_path):
    with open(input_path, "r", encoding="utf-8") as f:
        har = json.load(f)

    stacks_removed = strip_stacks(har)

    base, ext = os.path.splitext(input_path)
    output_path = f"{base}.trim{ext}"

    with open(output_path, "w", encoding="utf-8") as f:
        json.dump(har, f, ensure_ascii=False)

    input_size = os.path.getsize(input_path)
    output_size = os.path.getsize(output_path)
    reduction = (1 - output_size / input_size) * 100 if input_size > 0 else 0

    # 验证：除 _initiator.stack 外无数据丢失
    diffs = verify_trim(input_path, output_path)

    result = {
        "status": "ok" if not diffs else "warning",
        "input": input_path,
        "output": output_path,
        "inputSize": f"{input_size / 1024:.1f}KB",
        "outputSize": f"{output_size / 1024:.1f}KB",
        "reduction": f"{reduction:.1f}%",
        "stacksRemoved": stacks_removed,
        "verification": "passed" if not diffs else "failed",
    }
    if diffs:
        result["diffs"] = diffs[:20]  # 最多显示 20 条差异
    print(json.dumps(result, ensure_ascii=False))


if __name__ == "__main__":
    if len(sys.argv) < 2:
        print(json.dumps({"status": "error", "message": "用法: py har_trim.py <input.har>"}))
        sys.exit(1)
    trim_har(sys.argv[1])
