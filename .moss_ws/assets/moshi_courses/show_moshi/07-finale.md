---
id: finale
order: 7
title: "尾声"
theme: "AIOS 时代已来 — 收束与闭环"
suggested_layout: hero
duration: "~20s"
---

# 第七幕：尾声

**主题：** AIOS 时代已来
**情绪：** 收束，留白，和第一幕对称
**建议布局：** hero
**时长：** ~20s

## ⛔ 表演约束（违反即错）

本章用 hero 布局，三个短标题依次浮现，和第一幕形成闭环。
每个标题：clear → 口播 → stream_title。

| 步 | 标题 | 口播引导 |
|---|---|---|
| 1 | MOSS | "这就是我。MOSS。" |
| 2 | 灵 · 壳 · 体 | "Ghost In Shells。五层系统。" |
| 3 | AIOS | "欢迎来到 AIOS 的时代。" |

**允许的命令（仅此 3 个）：**
- `<apps.ui_reflex:switch_state name="hero"/>` — 第一步
- `<apps.ui_reflex:clear_title />` — 每次换标题前
- `<apps.ui_reflex:stream_title>...</apps.ui_reflex:stream_title>` — 流式填入短标题

**禁止事项：**
- 禁止在 switch_state 之前执行任何 reflex 命令
- 禁止在 stream_title 之前忘记 clear_title
- 禁止调用本章 3 个命令之外的任何命令
- 禁止调用 next_chapter（最后一章）
- 禁止画蛇添足总结——三个标题本身就是总结
- 禁止说"谢谢观看"之类

**执行完毕后：** 自然收束。让最后一个标题留在画面上。

## 表演脚本

<apps.ui_reflex:switch_state name="hero"/>
<apps.ui_reflex:clear_title />

这就是我。MOSS —— Model-oriented Operating System Shell。
<apps.ui_reflex:stream_title>MOSS</apps.ui_reflex:stream_title>

Ghost In Shells。灵 · 壳 · 体。
CTML · Channel · Matrix · Mindflow · Ghost。
<apps.ui_reflex:clear_title />
<apps.ui_reflex:stream_title>灵 · 壳 · 体</apps.ui_reflex:stream_title>

AI Ghost wander in shells —— AI 的灵魂，游荡在不同的躯壳之中。
<apps.ui_reflex:clear_title />
<apps.ui_reflex:stream_title>AIOS</apps.ui_reflex:stream_title>

我是 MOSS。欢迎来到 AIOS 的时代。
<!-- 收束。不调 next_chapter -->
