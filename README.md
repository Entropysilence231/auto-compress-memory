# Auto Compress Memory

> 当记忆超过 25 条时自动按主题分组压缩，全过程无损可逆。Codex AI Agent 的记忆管理技能。
>
> Auto-compress, group, and merge related user-memory entries when they exceed a threshold. Lossless and fully reversible. A memory management skill for the Codex AI agent.

---

## 功能 / Features

- **自动触发** — 对话开始时自动检查记忆条目数，超过 25 条立即压缩
- **智能分组** — 按键名前缀（`-` 或 `_` 之前的部分）自动归类，例如 `pref-lang` 与 `pref-theme` 归为一组
- **无损可逆** — 所有原始数据保存在压缩条目中，随时可通过 `decompress` 命令完整恢复
- **Dry-run 预览** — 压缩前预览哪些组会被合并，零风险
- **压缩日志** — 每次压缩操作记录时间、涉及条目和原始键，完全可追溯
- **自定义阈值** — 支持通过 `--threshold` 参数覆盖默认的 25 条阈值
- **指定解压** — 可解压全部或仅解压某个压缩组
- **兼容 Codex user-memory** — 直接读写 `~/.codex/skills/user-memory/memories.json`

---

## 安装 / Installation

### 作为 Codex Skill 安装（推荐）

```bash
# 从 GitHub 克隆
git clone https://github.com/Entropysilence231/auto-compress-memory.git

# 复制到 Codex skills 目录
cp -r auto-compress-memory ~/.codex/skills/
```

### 独立使用

```bash
git clone https://github.com/Entropysilence231/auto-compress-memory.git
cd auto-compress-memory
python scripts/compress.py status
```

> 前提条件：Python 3.10+，且已配置 Codex user-memory 技能（即有 `~/.codex/skills/user-memory/memories.json` 文件）。

---

## 使用 / Usage

所有命令均通过 `compress.py` 执行：

```bash
# 查看记忆状态（总数、原始条数、已压缩条数、压缩历史）
python scripts/compress.py status

# 自动压缩（默认阈值 25）
python scripts/compress.py compress

# 指定压缩阈值
python scripts/compress.py compress --threshold 30

# 预览压缩结果（dry-run，不写入文件）
python scripts/compress.py compress --dry-run

# 解压所有已压缩条目
python scripts/compress.py decompress

# 解压指定组
python scripts/compress.py decompress compressed-pref
```

### 状态输出示例 / Status Output Example

```
Total memories: 42
Raw (uncompressed) entries: 38
Compressed / metadata: 4
Compression history count: 2

Recent compressions:
  [2026-06-13T10:30:00] 3 entries -> compressed-proj
  [2026-06-13T10:35:00] 5 entries -> compressed-pref
```

---

## 工作原理 / How It Works

### 分组逻辑 / Grouping Logic

1. 扫描所有未压缩的记忆条目，按键名提取前缀（`-` 或 `_` 之前的部分）
2. 共享同一前缀的条目形成一个分组
3. 分组中条目数 **≥ 2** 的才会被合并压缩
4. 已压缩键（`compressed-*`）和元数据键（`_*`）不会被再次处理

### 压缩格式 / Compressed Format

```json
{
  "_meta": {
    "compressed_at": "2026-06-13T10:30:00",
    "original_keys": ["pref-lang", "pref-theme", "pref-model"],
    "entry_count": 3
  },
  "pref-lang": "Python",
  "pref-theme": "dark",
  "pref-model": "gpt-4o"
}
```

### 可逆性 / Reversibility

压缩 → 保留所有原始键值对在压缩条目内 → 随时可以 `decompress` 完整恢复。
每次压缩操作都在 `_compression_log` 中留下记录，形成完整审计链。

```
原始: pref-lang, pref-theme, pref-model
      │
      ├── compress ──→ compressed-pref (含全部原始键值 +_meta)
      │
      └── decompress ──→ pref-lang, pref-theme, pref-model (完整恢复)
```

---

## 触发时机 / Trigger Conditions

| 时机 | 动作 |
|------|------|
| 对话开始时 | 检查 `status`，若原始条目 > 25 则自动压缩 |
| 新增记忆后 | 检查是否有前缀组达到 2+ 条目，若有则压缩 |
| 用户主动要求 | 先 `--dry-run` 预览，再执行压缩 |

---

## 文件结构 / File Structure

```
auto-compress-memory/
├── LICENSE               # MIT 许可证
├── README.md             # 本文件
├── SKILL.md              # Codex skill 注册与指令文件
├── .gitignore
├── agents/
│   └── openai.yaml       # Agent 界面配置
└── scripts/
    └── compress.py       # 核心压缩/解压/状态脚本
```

---

## License

MIT
