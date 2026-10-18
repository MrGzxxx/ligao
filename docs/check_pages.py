#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""静态自检：新页面 JSON-LD / 图片 / emoji / 标题 / canonical。"""
import json
import os
import re
import sys

ROOT = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
PAGES = ["suspended-door.html", "telescopic-door.html"]

for page in PAGES:
    path = os.path.join(ROOT, page)
    h = open(path, encoding="utf-8").read()
    print("==", page, len(h) // 1024, "KB")
    blocks = re.findall(r'<script type="application/ld\+json">(.*?)</script>', h, re.S)
    for b in blocks:
        d = json.loads(b)
        items = d if isinstance(d, list) else [d]
        print("  JSON-LD:", [i.get("@type") for i in items], "ok")
    imgs = re.findall(r'<img[^>]+src="([^"]+)"', h)
    missing = [i for i in imgs if not os.path.exists(os.path.join(ROOT, i))]
    print("  imgs:", len(imgs), "缺失:", missing or "无")
    emo = set(re.findall(r"[\U0001F300-\U0001FAFF\u2600-\u27BF]", h))
    print("  emoji:", emo or "无")
    print("  svg 数:", h.count("<svg"))
    print("  title:", re.search(r"<title>(.*?)</title>", h).group(1))
    print("  canonical:", re.search(r'rel="canonical" href="([^"]+)"', h).group(1))
    print("  h2 数:", len(re.findall(r"<h2>", h)), " faq 数:", h.count("<details>"))
