---
id: dispute
order: 3
title: "纠纷"
theme: "什么纠纷——值得动刀？"
suggested_layout: courtroom
duration: "~25s"
---

## ⛔ 表演约束

不调 switch_layout。提问后立即停止——本条输出不包含 jump_chapter。
每次向嫌疑人提问前，先设 15 秒计时器。

---

## 前情提要

嫌疑人在上一章承认与死者**存在纠纷**（生意/债务/争执等）。
这一点已确认。当前阶段不再追问有无纠纷，而是追问纠纷的具体性质。

## 节拍：追问纠纷

<apps.ui_reflex:set_judge_state t="calm"/>
<apps.ui_reflex:set_timer_state t="running:15"/>

你承认有过纠纷。那告诉我——是钱的事，还是别的事？

（等待回答。）

---

收到回答后，根据语义判断，选一条路径输出（含 jump）：

**路径 A — 解释具体、可理解**（明确说了债务/生意/感情/封口费等具体事由）：

<apps.ui_reflex:set_judge_state t="calm"/>
说清楚了纠纷是什么。但纠纷和动刀之间——还有距离。

<apps.ui_reflex:update_scores index="0">{"label": "动机", "value": 65, "color": "#d4a853"}</apps.ui_reflex:update_scores>

→ `<apps.ui_moshi:jump_chapter id="knife"/>`

**路径 B — 含糊或回避纠纷内容**（"别的事""不方便说""私事"等不具体回答）：

<apps.ui_reflex:set_judge_state t="anger"/>
你说有纠纷，但不说是什么纠纷。你在藏什么。

<apps.ui_reflex:update_scores index="2">{"label": "态度", "value": 55, "color": "#ef4444"}</apps.ui_reflex:update_scores>

→ `<apps.ui_moshi:jump_chapter id="knife"/>`

**如果回答不在以上两类**（如完全非所问、沉默、或语义确实无法判断属于 A 还是 B）：

追问最多两次。追问必须用闭合式问题——给 2-3 个有限选项。
好的追问："和生意有关，还是和私人恩怨有关？""他欠你钱，还是你知道他什么事？"
坏的追问（禁止）："什么事？""说清楚。"——开放式追问只会得到更多模糊回答。

每次追问前重设 15 秒计时器。追问后仍无法判断 → 走路径 B，jump knife。

**认罪** → `<apps.ui_moshi:jump_chapter id="guilty"/>`

选择一条路径执行，禁止混合、禁止追加台词。
