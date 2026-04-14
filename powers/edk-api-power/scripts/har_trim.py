"""
HAR Trim - 删除 HAR 文件中 entries 的 _initiator.stack 字段以减小文件体积。
用法: py powers/edk-api-power/scripts/har_trim.py <input.har>
输出: <input>.trim.har
"""
import json
import sys
import os


def trim_har(input_path):
    with open(input_path, "r", encoding="utf-8") as f:
        har = json.load(f)

    if "log" in har and "entries" in har["log"]:
        for entry in har["log"]["entries"]:
            if "_initiator" in entry and "stack" in entry["_initiator"]:
                del entry["_initiator"]["stack"]

    base, ext = os.path.splitext(input_path)
    output_path = f"{base}.trim{ext}"

    with open(output_path, "w", encoding="utf-8") as f:
        json.dump(har, f, ensure_ascii=False)

    input_size = os.path.getsize(input_path)
    output_size = os.path.getsize(output_path)
    reduction = (1 - output_size / input_size) * 100 if input_size > 0 else 0

    print(json.dumps({
        "status": "ok",
        "input": input_path,
        "output": output_path,
        "inputSize": f"{input_size / 1024:.1f}KB",
        "outputSize": f"{output_size / 1024:.1f}KB",
        "reduction": f"{reduction:.1f}%"
    }))


if __name__ == "__main__":
    if len(sys.argv) < 2:
        print(json.dumps({"status": "error", "message": "用法: py har_trim.py <input.har>"}))
        sys.exit(1)
    trim_har(sys.argv[1])
