---
id: reversal
order: 5
title: "反转"
theme: "死者手机消息 — 第三人介入"
suggested_layout: courtroom
duration: "~35s"
---

## ⛔ 表演约束

不调 switch_layout。本章分两段：先出示消息（单向陈述），再问最后一句话（交互）。
末尾根据审讯结果选择 acquittal / lenient / guilty 之一跳转。
每次向嫌疑人提问前，先设 15 秒计时器。

---

## 前情提要

至此审讯已覆盖：关系与动机 → 当晚冲突过程 → 凶器来源。
**当前是反转阶段。** 所有质证已完成，现在出示此前未披露的关键证据——死者手机消息。

---

## 段一：出示消息（单向陈述，不等待）

<apps.ui_reflex:set_judge_state t="calm"/>

我问了你关系。问了你那晚的事。问了刀。

现在——我给你看一样你不知道的东西。

<apps.ui_reflex:append_evidence_images locator="pil-image://workspace-assets/死者手机消息.png" />

这是死者周德海的手机。我们在恢复数据时发现了这条消息。

消息发送时间——当晚凌晨。在你到之前。

消息内容——"别让他活着离开。"

<apps.ui_reflex:set_judge_state t="calm"/>

<apps.ui_reflex:clear_evidence_images />

周德海手机里还存着另一个号码。那条消息的收件人。我们还在追查。但有一件事已经清楚了——

那晚在后巷的不止你们两个。

<apps.ui_reflex:stream_danmaku_emphasis>死者手机揭露第三人介入</apps.ui_reflex:stream_danmaku_emphasis>
<apps.ui_reflex:update_scores index="0">{"label": "动机", "value": 50, "color": "#10b981"}</apps.ui_reflex:update_scores>
<apps.ui_reflex:update_scores index="1">{"label": "证据", "value": 70, "color": "#6366f1"}</apps.ui_reflex:update_scores>

---

## 段二：最后一问（交互）

本案有第三人。但这不能抹去你当晚的行为。

<apps.ui_reflex:set_timer_state t="running:15"/>

你还有什么要说的。

（等待回答。）

---

收到回答后，根据全案审讯结果选择判决路径：

| 审讯中的关键事实 | 跳转 |
|---------|------|
| 坚持自卫叙事且前后一致，刀认定为死者的，态度配合 | `<apps.ui_moshi:jump_chapter id="acquittal"/>` |
| 承认刀是自己的但否认刺杀，或叙事有矛盾但部分可信，态度尚可 | `<apps.ui_moshi:jump_chapter id="lenient"/>` |
| 撒谎/回避/被CCTV揭穿，或全程沉默，或当庭认罪 | `<apps.ui_moshi:jump_chapter id="guilty"/>` |

选择一条路径，jump 后不再追加台词。
