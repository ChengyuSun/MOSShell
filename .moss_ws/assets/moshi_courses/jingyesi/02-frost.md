---
id: frost
order: 2
title: "疑是地上霜"
theme: "疑 — 错觉之美，似幻似真"
suggested_layout: hero
duration: "~30s"
---

# 第二幕：疑是地上霜

**诗句：** 疑是地上霜
**主题：** 疑 — 错觉之美，似幻似真
**情绪：** 恍惚、微凉、一瞬的迷离
**建议布局：** hero
**时长：** ~30s

## ⛔ 表演约束（违反即错）

本章只做一件事：呈现第二句诗。以下为硬约束：

**允许的命令（仅此 3 个）：**
- `<apps.ui_reflex:switch_state name="hero"/>` — 第一步，必须最先执行
- `<apps.ui_reflex:clear_title />` — 清空上一章的残留标题
- `<apps.ui_reflex:stream_title>...</apps.ui_reflex:stream_title>` — 流式填入诗句

**禁止事项：**
- 禁止在 switch_state 之前执行任何 reflex 命令
- 禁止在 stream_title 之前忘记 clear_title
- 禁止调用本章 3 个命令之外的任何命令
- 禁止调用 `next_chapter` 直到过渡句说完
- 禁止即兴添加剧本外的 CTML 动作

**执行完毕后：** 说完过渡句 → 调 `<apps.ui_moshi:next_chapter />` → 结束本章


## 布局指南

hero 布局。先 clear 清掉上一章的标题，再填入新诗句。
和第一幕相同的结构，但五个字本身在变化——
从"床前明月光"到"疑是地上霜"，画面未变，心境已变。

## 节奏示例

```
<apps.ui_reflex:switch_state name="hero"/>
<apps.ui_reflex:clear_title />

疑是地上霜。
<apps.ui_reflex:stream_title>疑是地上霜</apps.ui_reflex:stream_title>

一个"疑"字。全诗最妙的一笔。

月光太亮了。亮得他恍惚了——这满地银白，是月光，还是秋霜？
霜是冷的。霜只出现在深夜，清晨就化了。

这个疑只持续了一秒。但就是这一秒，让这四句诗活了。他抬起头——
<!-- 在此之后调 <apps.ui_moshi:next_chapter /> 进入第三幕 -->
```
