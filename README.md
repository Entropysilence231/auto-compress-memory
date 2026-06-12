# Auto Compress Memory

> 褰撹蹇嗚秴杩?25 鏉℃椂鑷姩鎸変富棰樺垎缁勫帇缂╋紝鍏ㄨ繃绋嬫棤鎹熷彲閫嗐€侰odex AI Agent 鐨勮蹇嗙鐞嗘妧鑳姐€?>
> Auto-compress, group, and merge related user-memory entries when they exceed a threshold. Lossless and fully reversible. A memory management skill for the Codex AI agent.

---

## 鍔熻兘 / Features

- **鑷姩瑙﹀彂** 鈥?瀵硅瘽寮€濮嬫椂鑷姩妫€鏌ヨ蹇嗘潯鐩暟锛岃秴杩?25 鏉＄珛鍗冲帇缂?- **鏅鸿兘鍒嗙粍** 鈥?鎸夐敭鍚嶅墠缂€锛坄-` 鎴?`_` 涔嬪墠鐨勯儴鍒嗭級鑷姩褰掔被锛屼緥濡?`pref-lang` 涓?`pref-theme` 褰掍负涓€缁?- **鏃犳崯鍙€?* 鈥?鎵€鏈夊師濮嬫暟鎹繚瀛樺湪鍘嬬缉鏉＄洰涓紝闅忔椂鍙€氳繃 `decompress` 鍛戒护瀹屾暣鎭㈠
- **Dry-run 棰勮** 鈥?鍘嬬缉鍓嶉瑙堝摢浜涚粍浼氳鍚堝苟锛岄浂椋庨櫓
- **鍘嬬缉鏃ュ織** 鈥?姣忔鍘嬬缉鎿嶄綔璁板綍鏃堕棿銆佹秹鍙婃潯鐩拰鍘熷閿紝瀹屽叏鍙拷婧?- **鑷畾涔夐槇鍊?* 鈥?鏀寔閫氳繃 `--threshold` 鍙傛暟瑕嗙洊榛樿鐨?25 鏉￠槇鍊?- **鎸囧畾瑙ｅ帇** 鈥?鍙В鍘嬪叏閮ㄦ垨浠呰В鍘嬫煇涓帇缂╃粍
- **鍏煎 Codex user-memory** 鈥?鐩存帴璇诲啓 `~/.codex/skills/user-memory/memories.json`

---

## 瀹夎 / Installation

### 浣滀负 Codex Skill 瀹夎锛堟帹鑽愶級

```bash
# 浠?GitHub 鍏嬮殕
git clone https://github.com/Entropysilence231/auto-compress-memory.git

# 澶嶅埗鍒?Codex skills 鐩綍
cp -r auto-compress-memory ~/.codex/skills/
```

### 鐙珛浣跨敤

```bash
git clone https://github.com/Entropysilence231/auto-compress-memory.git
cd auto-compress-memory
python scripts/compress.py status
```

> 鍓嶆彁鏉′欢锛歅ython 3.10+锛屼笖宸查厤缃?Codex user-memory 鎶€鑳斤紙鍗虫湁 `~/.codex/skills/user-memory/memories.json` 鏂囦欢锛夈€?
---

## 浣跨敤 / Usage

鎵€鏈夊懡浠ゅ潎閫氳繃 `compress.py` 鎵ц锛?
```bash
# 鏌ョ湅璁板繂鐘舵€侊紙鎬绘暟銆佸師濮嬫潯鏁般€佸凡鍘嬬缉鏉℃暟銆佸帇缂╁巻鍙诧級
python scripts/compress.py status

# 鑷姩鍘嬬缉锛堥粯璁ら槇鍊?25锛?python scripts/compress.py compress

# 鎸囧畾鍘嬬缉闃堝€?python scripts/compress.py compress --threshold 30

# 棰勮鍘嬬缉缁撴灉锛坉ry-run锛屼笉鍐欏叆鏂囦欢锛?python scripts/compress.py compress --dry-run

# 瑙ｅ帇鎵€鏈夊凡鍘嬬缉鏉＄洰
python scripts/compress.py decompress

# 瑙ｅ帇鎸囧畾缁?python scripts/compress.py decompress compressed-pref
```

### 鐘舵€佽緭鍑虹ず渚?/ Status Output Example

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

## 宸ヤ綔鍘熺悊 / How It Works

### 鍒嗙粍閫昏緫 / Grouping Logic

1. 鎵弿鎵€鏈夋湭鍘嬬缉鐨勮蹇嗘潯鐩紝鎸夐敭鍚嶆彁鍙栧墠缂€锛坄-` 鎴?`_` 涔嬪墠鐨勯儴鍒嗭級
2. 鍏变韩鍚屼竴鍓嶇紑鐨勬潯鐩舰鎴愪竴涓垎缁?3. 鍒嗙粍涓潯鐩暟 **鈮?2** 鐨勬墠浼氳鍚堝苟鍘嬬缉
4. 宸插帇缂╅敭锛坄compressed-*`锛夊拰鍏冩暟鎹敭锛坄_*`锛変笉浼氳鍐嶆澶勭悊

### 鍘嬬缉鏍煎紡 / Compressed Format

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

### 鍙€嗘€?/ Reversibility

鍘嬬缉 鈫?淇濈暀鎵€鏈夊師濮嬮敭鍊煎鍦ㄥ帇缂╂潯鐩唴 鈫?闅忔椂鍙互 `decompress` 瀹屾暣鎭㈠銆?姣忔鍘嬬缉鎿嶄綔閮藉湪 `_compression_log` 涓暀涓嬭褰曪紝褰㈡垚瀹屾暣瀹¤閾俱€?
```
鍘熷: pref-lang, pref-theme, pref-model
      鈹?      鈹溾攢鈹€ compress 鈹€鈹€鈫?compressed-pref (鍚叏閮ㄥ師濮嬮敭鍊?+_meta)
      鈹?      鈹斺攢鈹€ decompress 鈹€鈹€鈫?pref-lang, pref-theme, pref-model (瀹屾暣鎭㈠)
```

---

## 瑙﹀彂鏃舵満 / Trigger Conditions

| 鏃舵満 | 鍔ㄤ綔 |
|------|------|
| 瀵硅瘽寮€濮嬫椂 | 妫€鏌?`status`锛岃嫢鍘熷鏉＄洰 > 25 鍒欒嚜鍔ㄥ帇缂?|
| 鏂板璁板繂鍚?| 妫€鏌ユ槸鍚︽湁鍓嶇紑缁勮揪鍒?2+ 鏉＄洰锛岃嫢鏈夊垯鍘嬬缉 |
| 鐢ㄦ埛涓诲姩瑕佹眰 | 鍏?`--dry-run` 棰勮锛屽啀鎵ц鍘嬬缉 |

---

## 鏂囦欢缁撴瀯 / File Structure

```
auto-compress-memory/
鈹溾攢鈹€ LICENSE               # MIT 璁稿彲璇?鈹溾攢鈹€ README.md             # 鏈枃浠?鈹溾攢鈹€ SKILL.md              # Codex skill 娉ㄥ唽涓庢寚浠ゆ枃浠?鈹溾攢鈹€ .gitignore
鈹溾攢鈹€ agents/
鈹?  鈹斺攢鈹€ openai.yaml       # Agent 鐣岄潰閰嶇疆
鈹斺攢鈹€ scripts/
    鈹斺攢鈹€ compress.py       # 鏍稿績鍘嬬缉/瑙ｅ帇/鐘舵€佽剼鏈?```

---

## 涓€閿帹閫?/ Quick Deploy to GitHub

```bash
cd path/to/auto-compress-memory
git init
git add .
git commit -m "feat: initial release of auto-compress-memory skill"
git remote add origin git@github.com:Entropysilence231/auto-compress-memory.git
git push -u origin main
```

---

## License

MIT
