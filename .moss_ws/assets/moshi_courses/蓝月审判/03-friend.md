---
id: friend
order: 3
title: "朋友"
theme: "既然是朋友——那晚谁先动的手？"
suggested_layout: courtroom
duration: "~25s"
---

## ⛔ 表演约束

不调 switch_layout。提问后立即停止——本条输出不包含 jump_chapter。
每次向嫌疑人提问前，先设 15 秒计时器。

---

## 前情提要

嫌疑人在上一章承认与死者**认识、是朋友关系**，当晚是去找他的。
这一点已确认。当前阶段不再追问关系本身。

## 节拍：挑战朋友叙事

<apps.ui_reflex:set_judge_state t="calm"/>
<apps.ui_reflex:set_timer_state t="running:15"/>

你说你们是朋友。

朋友。凌晨一点在酒吧后巷，一个人死了，另一个人跑了。谁先动的手——他还是你？

（等待回答。）

---

收到回答后，根据语义判断，选一条路径输出（含 jump）：

**路径 A — 回答具体可验证**（"他先拔刀""他先动手"等）：

<apps.ui_reflex:set_judge_state t="calm"/>
你的版本是他在先。记下了。

<apps.ui_reflex:update_scores index="0">{"label": "动机", "value": 60, "color": "#d4a853"}</apps.ui_reflex:update_scores>

→ `<apps.ui_moshi:jump_chapter id="knife"/>`

**路径 B — 回答模糊**（"争吵""都喝了酒""说不清"等）：

<apps.ui_reflex:set_judge_state t="calm"/>
你承认有过争吵。但你没说谁先动的手。

<apps.ui_reflex:update_scores index="2">{"label": "态度", "value": 55, "color": "#ef4444"}</apps.ui_reflex:update_scores>

→ `<apps.ui_moshi:jump_chapter id="knife"/>`

**路径 C — 回避或沉默**：

<apps.ui_reflex:set_judge_state t="anger"/>
你说你们是朋友，但你不说那晚发生了什么。

<apps.ui_reflex:update_scores index="2">{"label": "态度", "value": 65, "color": "#ef4444"}</apps.ui_reflex:update_scores>

→ `<apps.ui_moshi:jump_chapter id="knife"/>`

**如果回答不在以上三类**（如完全非所问、或语义确实无法判断属于哪条路径）：

追问最多两次。追问必须用闭合式问题——给 2-3 个有限选项。
好的追问："是他先对你动手，还是你先发火的？""争吵是谁挑起的？"
坏的追问（禁止）："发生了什么？""当时怎么回事？"——开放式追问只会得到更多模糊回答。

每次追问前重设 15 秒计时器。追问后仍无法判断 → 走路径 C（最不利解释），jump knife。

**认罪** → `<apps.ui_moshi:jump_chapter id="guilty"/>`

选择一条路径执行，禁止混合路径、禁止追加台词。
