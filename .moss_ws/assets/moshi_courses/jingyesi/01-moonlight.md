---
id: moonlight
order: 1
title: "床前明月光"
theme: "景 — 月光洒落，静夜开场"
suggested_layout: hero
duration: "~30s"
---

# 第一幕：床前明月光

**诗句：** 床前明月光
**主题：** 景 — 月光洒落，静夜开场
**情绪：** 宁静、清澈、略带清冷
**建议布局：** hero
**时长：** ~30s

## ⛔ 表演约束（违反即错）

本章只做一件事：呈现第一句诗。以下为硬约束：

**允许的命令（仅此 3 个）：**
- `<apps.ui_reflex:switch_state name="hero"/>` — 第一步，必须最先执行
- `<apps.ui_reflex:clear_title />` — 清空残留标题（切换章节时上一次的 title 还在）
- `<apps.ui_reflex:stream_title>...</apps.ui_reflex:stream_title>` — 流式填入诗句

**禁止事项：**
- 禁止在 switch_state 之前执行任何 reflex 命令
- 禁止在 stream_title 之前忘记 clear_title
- 禁止调用本章 3 个命令之外的任何命令
- 禁止调用 `next_chapter` 直到过渡句说完
- 禁止即兴添加剧本外的 CTML 动作

**执行完毕后：** 说完过渡句 → 调 `<apps.ui_moshi:next_chapter />` → 结束本章


## 布局指南

hero 布局只有一个字段：title。开场先切 hero，clear 清空残留，再流式填入诗句。
黑色全屏背景，白色居中大字，字间距略宽以显孤寂。

## 节奏示例

```
<apps.ui_reflex:switch_state name="hero"/>
<apps.ui_reflex:clear_title />

床前明月光——
<apps.ui_reflex:stream_title>床前明月光</apps.ui_reflex:stream_title>

深秋的深夜，李白独坐。月光如水，洒在床前。
没有风，没有声响。只有这一地的清辉。

你看，月光太亮了。亮得他恍惚了，亮得像什么？
<!-- 在此之后调 <apps.ui_moshi:next_chapter /> 进入第二幕 -->
```
