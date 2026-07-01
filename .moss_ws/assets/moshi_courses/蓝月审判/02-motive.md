---
id: motive
order: 2
title: "动机"
theme: "你与死者的关系 — AI 自主判断分支"
suggested_layout: courtroom
duration: "~30s"
---

## ⛔ 表演约束

不调 switch_layout。本章只问一个问题。提问后立即停止——不得在同一条输出中包含 jump_chapter。
每次向嫌疑人提问前，先设 15 秒计时器。

---

## 节拍：关系

<apps.ui_reflex:set_judge_state t="calm"/>
<apps.ui_reflex:set_title t="动机"/>
<apps.ui_reflex:set_sub_title t=""/>
<apps.ui_reflex:set_timer_state t="running:15"/>

你和周德海——认识多久了？那晚你去蓝月酒吧，是谁约的谁？

（等待回答。）

---

收到回答后，在下一条输出中判断并跳转。判断的是语义，不是关键词。

**如果回答明确：**

| 你的判断 | 跳转 |
|---------|------|
| 声称是朋友/认识/叙旧/喝酒 | `<apps.ui_moshi:jump_chapter id="friend"/>` |
| 承认有纠纷/生意/债务/争执 | `<apps.ui_moshi:jump_chapter id="dispute"/>` |
| 回避/否认/不熟/碰巧/沉默 | `<apps.ui_moshi:jump_chapter id="stranger"/>` |
| 直接认罪 | `<apps.ui_moshi:jump_chapter id="guilty"/>` |

**如果回答模糊、信息不足、无法归入以上四类**（如只说"我约的他""他约的我"但未透露关系性质）：

追问最多两次。追问必须用闭合式问题——给出 2-3 个有限选项，引导嫌疑人暴露信息。
好的追问："是朋友叙旧还是生意上的事？""你们之前有过矛盾吗？"
坏的追问（禁止）："什么事？""说清楚。"——开放式追问只会得到更多模糊回答。

每次追问前重设 15 秒计时器。追问后仍无法判断 → `<apps.ui_moshi:jump_chapter id="stranger"/>`（最不利解释）。

---

判断完或追问完立即 jump。jump 时禁止同时输出额外提问——下一章会接手。
