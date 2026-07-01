---
id: stranger
order: 3
title: "陌客"
theme: "你说谎。CCTV 不会说谎。"
suggested_layout: courtroom
duration: "~30s"
---

## ⛔ 表演约束

不调 switch_layout。本章是揭穿章——出示 CCTV。末尾调 jump_chapter id="knife"。

---

## 前情提要

嫌疑人在上一章**回避或否认与死者的关系**——声称不熟、碰巧、路过，或拒绝回答。
但其行为与说法不符。CCTV 证据将打破这一叙事。

## 节拍：CCTV 揭穿

<apps.ui_reflex:set_judge_state t="anger"/>
<apps.ui_reflex:append_evidence_videos locator="local-webm://workspace-assets/监控中男人从酒吧走出来.webm" />

不熟。碰巧。路过。

CCTV 拍到——你进门后没有去吧台买酒。没有东张西望。你进门，直奔他那张桌子。

这不是碰巧。你知道他在哪。

<apps.ui_reflex:clear_evidence_videos />

你们不是"不熟"。你在回避。

<apps.ui_reflex:stream_danmaku_text>CCTV揭穿了碰巧的说法</apps.ui_reflex:stream_danmaku_text>
<apps.ui_reflex:update_scores index="2">{"label": "态度", "value": 65, "color": "#ef4444"}</apps.ui_reflex:update_scores>
<apps.ui_reflex:update_scores index="0">{"label": "动机", "value": 80, "color": "#d4a853"}</apps.ui_reflex:update_scores>

你一开始选择了回避。这让本庭对你接下来的每一句话——都会更谨慎地审视。

→ `<apps.ui_moshi:jump_chapter id="knife"/>`

**认罪** → `<apps.ui_moshi:jump_chapter id="guilty"/>`

禁止追加台词。
