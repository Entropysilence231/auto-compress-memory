---
name: auto-compress-memory
description: "Auto-compress user-memory when memories exceed 25 entries. This skill automatically compresses, groups, and merges related memories in the user-memory system. Triggers when: (1) at conversation start, check if memory count exceeds 25 entries, (2) after adding new memories that could be merged with existing prefixed groups, (3) user explicitly asks to compress or clean up memories."
---

# Auto Compress Memory

## Overview

Keeps the user-memory store lean by auto-grouping related memories (same key prefix)
into compressed entries. All original data is preserved. Compression is lossless
and fully reversible.

## Usage (run from scripts/)

- `python compress.py status` -- Show memory count, raw vs compressed breakdown, and compression history.
- `python compress.py compress` -- Auto-compress if raw entries exceed threshold (25).
- `python compress.py compress --threshold 30` -- Use a custom threshold.
- `python compress.py compress --dry-run` -- Preview which groups would merge without writing.
- `python compress.py decompress` -- Restore all compressed entries to individual keys in one step.
- `python compress.py decompress compressed-xxx` -- Restore one specific compressed group.

## When and how to compress

1. **At conversation start**: Run `python compress.py status` first.
   If raw entries > 25, immediately run `python compress.py compress`.

2. **After adding memories**: When you save a new memory (via `memory.py add`),
   check if a prefix group now has 2+ entries. If so, run compress.

3. **User request**: The user may explicitly ask you to clean up or compress memories.
   Run `python compress.py compress --dry-run` first to preview, then compress.

## How grouping works

- Keys sharing a prefix before `-` or `_` (e.g. `pref-lang`, `pref-theme`) form a group.
- Groups with fewer than 2 entries are left as-is.
- Already-compressed keys (`compressed-*`) and metadata keys (`_*`) are never re-processed.
- Each group is merged into one `compressed-<prefix>` entry. The compressed entry contains
  all original key-value pairs plus a `_meta` field tracking source keys and timestamp.
- A `_compression_log` entry records every compression operation for full traceability.

## Decompression

`decompress` reads the `_meta.original_keys` field and restores each entry to its
original key, removing the compressed container. Run with `--dry-run` to preview.
