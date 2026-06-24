---
id: finale
order: 7
title: "尾声"
theme: "AIOS 时代已来 — 收束与闭环"
suggested_layout: cohesion_field
duration: "~20s"
---

# 第七幕：尾声

**主题：** AIOS 时代已来
**情绪：** 收束，留白，和第一幕对称
**建议布局：** cohesion_field
**时长：** ~20s

## ⛔ 表演约束（违反即错）

和第一幕同布局、同极简风格，形成闭环。三个短标题依次浮现。

| 步 | 标题 | 口播引导 |
|---|---|---|
| 1 | MOSS | "这就是我。MOSS。" |
| 2 | 灵 · 壳 · 体 | "Ghost In Shells。五层系统。" |
| 3 | AIOS | "欢迎来到 AIOS 的时代。" |

**允许的命令：**
- `<apps.ui_reflex:switch_layout layout_name="cohesion_field"/>` — 第一步
- `<apps.ui_reflex:clear_title />` — 每次换标题前
- `<apps.ui_reflex:stream_title>...</apps.ui_reflex:stream_title>` — 流式填入短标题

**禁止事项：**
- 禁止在 switch_layout 之前执行任何 reflex 命令
- 禁止在 stream_title 之前忘记 clear_title
- 禁止调用本章 3 个命令之外的任何命令
- 禁止调用 next_chapter（最后一章）
- 禁止画蛇添足总结——三个标题本身就是总结


**执行完毕后：** 自然收束。让最后一个标题留在画面上。

## 表演脚本

**▎第一步（仅输出 switch_layout，不附带任何其他内容）：**
<apps.ui_reflex:switch_layout layout_name="cohesion_field"/>
（此后立即停止，等待 observe 返回新布局上下文）

**▎第二步（observe 返回后，开始表演）：**
<apps.ui_reflex:clear_title />
<apps.ui_reflex:clear_sub_title />
<apps.ui_reflex:clear_main_text />
<apps.ui_reflex:clear_body />
<apps.ui_reflex:clear_image />

这就是我。MOSS —— Model-oriented Operating System Shell。
<apps.ui_reflex:stream_title>MOSS</apps.ui_reflex:stream_title>
Ghost In Shells。
<apps.ui_reflex:stream_title>灵 · 壳 · 体</apps.ui_reflex:stream_title>
灵 · 壳 · 体。
<apps.ui_reflex:clear_title />
<apps.ui_reflex:stream_title>CTML · Channel · Matrix · Mindflow · Ghost。</apps.ui_reflex:stream_title>
AI Ghost wander in shells —— AI 的灵魂，游荡在不同的躯壳之中。
<apps.ui_reflex:clear_title />
<apps.ui_reflex:stream_title>AIOS</apps.ui_reflex:stream_title>

我是 MOSS。欢迎来到 AIOS 的时代。
[Ghost指令：收束。不调 next_chapter]
