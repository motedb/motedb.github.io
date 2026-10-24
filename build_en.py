#!/usr/bin/env python3
"""从中文源页 index.html 生成英文独立页 en/index.html。

用法: 改完 index.html 后在仓库根目录运行  python3 build_en.py  然后两份一起提交。
原则: index.html 是唯一事实源; en/ 是构建产物, 不要手改。
"""
import re, pathlib, sys

ROOT = pathlib.Path(__file__).resolve().parent
src = (ROOT / 'index.html').read_text(encoding='utf-8')
out = src

def rep(old, new, n=1):
    global out
    c = out.count(old)
    if c != n:
        sys.exit(f"build_en: expected {n} hit(s) but got {c} for:\n  {old[:90]}")
    out = out.replace(old, new)

# ── 1. 提取 en 字典 ────────────────────────────────────────────────
m = re.search(r"\n  en: \{(.*?)\n  \}", src, re.S)
if not m: sys.exit("build_en: en dict not found")
body = m.group(1)
if "\\'" in body: sys.exit("build_en: escaped quote in en dict — extend the parser")
EN = dict(re.findall(r"'([^']+)'\s*:\s*'([^']*)'", body))

# ── 2. 静态替换所有 data-i18n 叶子元素的内容 ─────────────────────
hits = 0
def swap(mo):
    global hits
    tag, attrs, key = mo.group(1), mo.group(2), mo.group(3)
    if key not in EN: sys.exit(f"build_en: en dict missing key {key!r}")
    hits += 1
    return f"<{tag}{attrs}>{EN[key]}</{tag}>"
out = re.sub(r'<(\w+)([^>]*?\sdata-i18n="([^"]+)"[^>]*)>.*?</\1>', swap, out, flags=re.S)
expected = len(re.findall(r'data-i18n="', src))
if hits != expected:
    sys.exit(f"build_en: replaced {hits} i18n nodes but source has {expected} (nested data-i18n?)")

# ── 3. <head> 语言相关字段 ───────────────────────────────────────
rep('<html lang="zh-CN">', '<html lang="en">')
rep('<title>MoteDB — 嵌入式多模态数据库 · 为具身智能与机器人而生 | Rust 开源</title>',
    '<title>MoteDB — Embedded Multimodal Database for Embodied AI &amp; Robotics | Rust, MIT</title>')
rep('<meta name="description" content="MoteDB 是面向具身智能与机器人的开源嵌入式多模态数据库：一个 SQL 引擎原生承载向量、时序、全文与二进制数据。Rust 编写、零运维，支持 MCAP 导入、单文件快照与只读容器分发，提供 Rust / Python / Node.js SDK。MIT 协议。">',
    '<meta name="description" content="MoteDB is an open-source embedded multimodal database for embodied AI and robotics: one SQL engine natively carrying vectors, time series, full text and binary. Written in Rust, zero-ops — MCAP import, single-file snapshots, read-only container distribution; Rust, Python and Node.js SDKs. MIT licensed.">')
rep('<link rel="canonical" href="https://motedb.github.io/">', '<link rel="canonical" href="https://motedb.github.io/en/">')
rep('<meta property="og:url" content="https://motedb.github.io/">', '<meta property="og:url" content="https://motedb.github.io/en/">')
rep('<meta property="og:locale" content="zh_CN">\n<meta property="og:locale:alternate" content="en_US">',
    '<meta property="og:locale" content="en_US">\n<meta property="og:locale:alternate" content="zh_CN">')
rep('<meta property="og:title" content="MoteDB — 嵌入式多模态数据库 · 为具身智能与机器人而生">',
    '<meta property="og:title" content="MoteDB — Embedded Multimodal Database for Embodied AI &amp; Robotics">')
rep('<meta property="og:description" content="面向具身智能与机器人的开源嵌入式多模态数据库：向量、时序、全文、二进制，一个 SQL 引擎。Rust 编写，零运维，MIT 协议。">',
    '<meta property="og:description" content="Open-source embedded multimodal database for embodied AI and robotics — vectors, time series, full text and binary in one SQL engine. Rust, zero-ops, MIT.">')
rep('<meta name="twitter:title" content="MoteDB — The multimodal embedded database for embodied intelligence">',
    '<meta name="twitter:title" content="MoteDB — Embedded Multimodal Database for Embodied AI &amp; Robotics">')
rep('  "url": "https://motedb.github.io/",\n  "inLanguage": "zh-CN",',
    '  "url": "https://motedb.github.io/en/",\n  "inLanguage": "en",')

# ── 3.5 视频资源切英文（中文页 /media/motedb-promo.mp4，英文页 …-en.mp4）──
rep('/media/motedb-promo.mp4', '/media/motedb-promo-en.mp4', 2)
rep('aria-label="MoteDB 宣传片"', 'aria-label="MoteDB promo video"')

# ── 4. 复制按钮静态文案 ─────────────────────────────────────────
rep('https://motedb.github.io/og-zh.png', 'https://motedb.github.io/og-en.png', 3)
rep('<meta property="og:image:alt" content="MoteDB — 具身智能的嵌入式多模态数据库">',
    '<meta property="og:image:alt" content="MoteDB — Embedded multimodal database for embodied AI &amp; robotics">')
rep('aria-label="菜单"', 'aria-label="Menu"')
rep('data-copy="复制" data-ok="✓">复制</button>', 'data-copy="Copy" data-ok="✓">Copy</button>', 6)

dst = ROOT / 'en' / 'index.html'
dst.parent.mkdir(exist_ok=True)
dst.write_text(out, encoding='utf-8')
print(f"build_en: wrote {dst.relative_to(ROOT)} ({len(out)} bytes, {hits} i18n nodes, {len(EN)} en keys)")
