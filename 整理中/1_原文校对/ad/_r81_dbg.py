# -*- coding: utf-8 -*-
import io, re, importlib.util
BASE = "D:/Git/Book/整理中/1_原文校对/ad/"
spec = importlib.util.spec_from_file_location("tbl", BASE + "_r81_tbl.py")
T = importlib.util.module_from_spec(spec); spec.loader.exec_module(T)

FWMAP = {"＋": "+", "－": "-", "（": "(", "）": ")", "［": "[", "］": "]",
         "｛": "{", "｝": "}", "：": ":", "；": ";", "，": ",", "．": ".",
         "／": "/", "＼": "\\", "％": "%", "＃": "#", "＆": "&", "＊": "*",
         "＝": "=", "？": "?", "！": "!", "～": "~", "＇": "'", "＂": '"',
         "–": "-", "—": "-", "−": "-", "‐": "-", "\u00a0": " "}


def norm(t):
    t = t.strip()
    t = re.sub(r"^(第[一二三四五六七八九十]+篇)[：:、]?", "", t)
    t = t.replace("\\&", "&").replace("\\_", "_").replace("\\%", "%")
    t = re.sub(r"\\([a-zA-Z]+)\s*", r"\1", t)
    t = t.replace("\u201c", '"').replace("\u201d", '"')
    t = t.replace("\u2018", "'").replace("\u2019", "'")
    t = "".join(FWMAP.get(ch, ch) for ch in t)
    return re.sub(r"\s+", "", t)


targets = ["STI概述、流行现状与预防原则", "LGBTQ+性健康", "性功能障碍(续)",
           "性与法律:同意、权益与边界", "性文化与政策"]
kn = {norm(k): k for k in T.SEC_ROUTE}
for t in targets:
    print(repr(t), "->", repr(kn.get(t, "MISS")))
print("--- 表内含 STI/LGBTQ 的键归一化 ---")
for k in T.SEC_ROUTE:
    if "STI" in k or "LGBTQ" in k or "文化与政策" in k:
        print("  ", repr(k), "=>", repr(norm(k)))
