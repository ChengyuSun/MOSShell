---
id: homesick
order: 3
title: "低头思故乡"
theme: "情 — 举头低头间，乡愁喷薄"
suggested_layout: hero
duration: "~40s"
---

# 第三幕：举头望明月，低头思故乡

**诗句：** 举头望明月，低头思故乡
**主题：** 情 — 举头低头间，乡愁喷薄
**情绪：** 从确认到涌起，从看到到思念
**建议布局：** hero
**时长：** ~40s

## ⛔ 表演约束（违反即错）

本章做收束。以下为硬约束：

**允许的命令（仅此 3 个）：**
- `<apps.ui_reflex:switch_state name="hero"/>` — 第一步，必须最先执行
- `<apps.ui_reflex:clear_title />` — 清空上一章的残留标题
- `<apps.ui_reflex:stream_title>...</apps.ui_reflex:stream_title>` — 流式填入诗句

**禁止事项：**
- 禁止在 switch_state 之前执行任何 reflex 命令
- 禁止在 stream_title 之前忘记 clear_title
- 禁止调用本章 3 个命令之外的任何命令
- 本章是最后一章，不需要调 next_chapter
- 禁止即兴添加剧本外的 CTML 动作
- 禁止画蛇添足总结全诗——诗句本身留在画面上就是最好的结尾

**执行完毕后：** 自然收束。让诗句留在画面上

## 布局指南

hero 布局。先 clear 清掉上一章标题，再填入新内容。
前两句的大字停留片刻后，完整呈现后两句。
让诗句本身留在画面上作为收束——不解释，不总结。

## 节奏示例

```
<apps.ui_reflex:switch_state name="hero"/>
<apps.ui_reflex:clear_title />

他抬起头。那不是霜——是月亮。
<apps.ui_reflex:stream_title>举头望明月</apps.ui_reflex:stream_title>

举头。确认了，是明月。但月亮在中国人的心里，从来不只是月亮。

他低下头。故乡，就这么涌上来了。
<apps.ui_reflex:clear_title />
<apps.ui_reflex:stream_title>低头思故乡</apps.ui_reflex:stream_title>

二十个字。四句。从看到疑，从疑到举头，从举头到低头。
从外物到内心。一千三百年了，每个想家的人，都在这四句话里。
<!-- 收束，不调 next_chapter。让诗句留在画面上 -->
```
