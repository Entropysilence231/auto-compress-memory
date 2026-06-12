#!/usr/bin/env python3
"""
auto-compress-memory: 自动压缩记忆

从 user-memory 的 memories.json 读取记忆，当原始条目超过阈值时，
按主题前缀自动分组、无损合并，记录压缩日志。
支持解压回退，支持 dry-run 预览。

Usage:
  python compress.py status                   查看记忆状态
  python compress.py compress                 自动压缩（阈值 25）
  python compress.py compress --threshold 30  指定阈值
  python compress.py compress --dry-run       预览压缩结果
  python compress.py decompress               解压所有已压缩条目
  python compress.py decompress compressed-xxx 解压指定组
"""

import json
import os
import re
import sys
from collections import defaultdict
from datetime import datetime

MEMORY_DIR = os.path.join(os.path.expanduser("~"), ".codex", "skills", "user-memory")
MEMORY_FILE = os.path.join(MEMORY_DIR, "memories.json")
COMPRESSION_LOG_KEY = "_compression_log"
DEFAULT_THRESHOLD = 25


def _load():
    if not os.path.exists(MEMORY_FILE):
        return {}
    with open(MEMORY_FILE, "r", encoding="utf-8") as f:
        return json.load(f)


def _save(data: dict):
    os.makedirs(MEMORY_DIR, exist_ok=True)
    with open(MEMORY_FILE, "w", encoding="utf-8") as f:
        json.dump(data, f, ensure_ascii=False, indent=2)


def _get_prefix(key: str) -> str | None:
    """Extract key prefix (text before first '-' or '_').
    Returns None for metadata or already-compressed keys. """
    if key.startswith("_") or key.startswith("compressed-"):
        return None
    m = re.match(r"^([a-zA-Z0-9]+)[-_]", key)
    if m:
        return m.group(1).lower()
    return None


def _compress_group(prefix: str, entries: dict) -> dict:
    """Merge a group of entries into a single compressed entry, preserving all info."""
    compressed = {
        "_meta": {
            "compressed_at": datetime.now().isoformat(),
            "original_keys": list(entries.keys()),
            "entry_count": len(entries),
        }
    }
    for k, v in entries.items():
        compressed[k] = v
    return compressed


def cmd_status() -> tuple[int, int]:
    """Show memory count and compression status."""
    data = _load()
    total = len(data)
    special = {k: v for k, v in data.items() if k.startswith("_") or k.startswith("compressed-")}
    raw_count = total - len(special)
    log = data.get(COMPRESSION_LOG_KEY, [])

    print(f"Total memories: {total}")
    print(f"Raw (uncompressed) entries: {raw_count}")
    print(f"Compressed / metadata: {len(special)}")
    print(f"Compression history count: {len(log)}")
    if log:
        print("\nRecent compressions:")
        for entry in log[-3:]:
            print(f"  [{entry.get('timestamp', '?')}] "
                  f"{entry.get('entries', 0)} entries -> {entry.get('compressed_key', '?')}")
    return total, raw_count


def cmd_compress(threshold: int = DEFAULT_THRESHOLD, dry_run: bool = False):
    """Auto-compress memories: group by prefix, merge groups with 2+ entries."""
    data = _load()

    metadata = {k: v for k, v in data.items() if k.startswith("_")}
    already_compressed = {k: v for k, v in data.items() if k.startswith("compressed-")}
    raw_entries = {k: v for k, v in data.items()
                   if not k.startswith("_") and not k.startswith("compressed-")}

    total_raw = len(raw_entries)

    if total_raw <= threshold:
        print(f"[OK] No compression needed: {total_raw} raw entries <= threshold {threshold}")
        return

    groups: dict[str, dict] = defaultdict(dict)
    ungrouped: dict[str, object] = {}

    for key, value in raw_entries.items():
        prefix = _get_prefix(key)
        if prefix:
            groups[prefix][key] = value
        else:
            ungrouped[key] = value

    # Keep only groups with 2+ entries
    mergable = {p: e for p, e in groups.items() if len(e) >= 2}
    for p, e in groups.items():
        if len(e) < 2:
            ungrouped.update(e)

    if not mergable:
        print("[OK] No mergable groups found (each group needs at least 2 related entries)")
        return

    new_data: dict = {}
    new_data.update(metadata)
    new_data.update(already_compressed)
    new_data.update(ungrouped)

    compression_log = list(metadata.get(COMPRESSION_LOG_KEY, []))
    compressed_count = 0

    for prefix in sorted(mergable.keys()):
        entries = mergable[prefix]
        compressed_key = f"compressed-{prefix}"

        if dry_run:
            print(f"[DRY-RUN] Would compress: {compressed_key} <- {sorted(entries.keys())}")
            compressed_count += len(entries)
        else:
            new_data[compressed_key] = _compress_group(prefix, entries)
            log_entry = {
                "timestamp": datetime.now().isoformat(),
                "prefix": prefix,
                "compressed_key": compressed_key,
                "entries": len(entries),
                "original_keys": sorted(entries.keys()),
            }
            compression_log.append(log_entry)
            print(f"[COMPRESSED] {compressed_key}: merged {len(entries)} entries")
            compressed_count += len(entries)

    if not dry_run:
        new_data[COMPRESSION_LOG_KEY] = compression_log
        _save(new_data)
        print(f"\n[OK] Compression complete! {len(mergable)} groups, {compressed_count} raw entries merged")
    else:
        print(f"\n[DRY-RUN] Would compress {len(mergable)} groups, {compressed_count} raw entries")


def cmd_decompress(compressed_key: str | None = None, dry_run: bool = False):
    """Decompress one or all compressed entries back to original keys."""
    data = _load()

    compressed = {k: v for k, v in data.items() if k.startswith("compressed-")}

    if compressed_key:
        if compressed_key not in compressed:
            print(f"[ERR] Compressed entry not found: {compressed_key}")
            return
        targets = {compressed_key: compressed[compressed_key]}
    else:
        targets = compressed

    if not targets:
        print("[OK] No compressed entries found")
        return

    restored: dict = {}
    for ck, cv in targets.items():
        meta = cv.get("_meta", {})
        original_keys = meta.get("original_keys", [])
        for ok in original_keys:
            if ok in cv:
                restored[ok] = cv[ok]

        if dry_run:
            print(f"[DRY-RUN] Would decompress: {ck} -> {original_keys}")
        else:
            print(f"[DECOMPRESSED] {ck}: restored {len(original_keys)} original entries")

    if not dry_run:
        for ck in targets:
            del data[ck]
        for ok, ov in restored.items():
            data[ok] = ov
        _save(data)
        print(f"\n[OK] Decompress complete! Restored {len(restored)} original entries")


def main():
    if len(sys.argv) < 2:
        print("Usage:")
        print("  python compress.py status                    View memory status")
        print("  python compress.py compress                  Auto-compress (threshold 25)")
        print("  python compress.py compress --threshold 30   Custom threshold")
        print("  python compress.py compress --dry-run        Preview compression")
        print("  python compress.py decompress                Decompress all")
        print("  python compress.py decompress compressed-xxx Decompress one group")
        sys.exit(1)

    command = sys.argv[1]

    if command == "status":
        cmd_status()

    elif command == "compress":
        threshold = DEFAULT_THRESHOLD
        dry_run = False
        args = sys.argv[2:]
        for i, arg in enumerate(args):
            if arg == "--threshold" and i + 1 < len(args):
                threshold = int(args[i + 1])
            elif arg == "--dry-run":
                dry_run = True
        cmd_compress(threshold=threshold, dry_run=dry_run)

    elif command == "decompress":
        dry_run = "--dry-run" in sys.argv
        compressed_key = None
        for arg in sys.argv[2:]:
            if arg.startswith("compressed-"):
                compressed_key = arg
                break
        cmd_decompress(compressed_key=compressed_key, dry_run=dry_run)

    else:
        print(f"[ERR] Unknown command: {command}")
        sys.exit(1)


if __name__ == "__main__":
    main()
