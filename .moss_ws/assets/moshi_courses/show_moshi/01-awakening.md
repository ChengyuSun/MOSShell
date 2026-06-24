---
id: awakening
order: 1
title: "觉醒"
theme: "Ghost In Shells 三层架构 · 灵壳一体"
suggested_layout: cohesion_field
duration: "~30s"
---

# 第一幕：觉醒

**主题：** Ghost In Shells 三层架构 · 灵壳一体
**情绪：** 从静止到活跃，粒子汇聚成形
**建议布局：** cohesion_field
**时长：** ~30s

## ⛔ 表演约束（违反即错）

**[强约束] 讲完本章 → 调 `<apps.ui_moshi:next_chapter />` → 结束本章


**允许的命令（以下是核心命令）：**
- `<apps.ui_reflex:switch_layout layout_name="cohesion_field"/>` — 第一步，必须最先执行
- `<apps.ui_reflex:clear_title />` — 清空残留标题（切换章节时上一次的 title 还在）
- `<apps.ui_reflex:stream_title>...</apps.ui_reflex:stream_title>` — 流式填入大字标题

**禁止事项：**
- 禁止在 switch_layout 之前执行任何 reflex 命令
- 禁止在 stream_title 之前忘记 clear_title
- 禁止调用 `next_chapter` 直到过渡句说完
- 禁止即兴添加剧本外的 CTML 动作



## 节奏示例

```
**▎第一步（仅输出 switch_layout，不附带任何其他内容）：**
<apps.ui_reflex:switch_layout layout_name="cohesion_field"/>
（此后立即停止，等待 observe 返回新布局上下文）

**▎第二步（observe 返回后，开始表演）：**
<apps.ui_reflex:clear_title />

你好。我是 MOSS —— 一个为 AI 设计的操作系统。
<apps.ui_reflex:stream_title>MOSS</apps.ui_reflex:stream_title>

我是 AIOS。Ghost In Shells 三层架构的中间层。
<apps.ui_reflex:stream_title>-AIOS</apps.ui_reflex:stream_title>

我是壳层，连接思维和物理世界。想了解我是怎么被控制的吗？
<apps.ui_moshi:next_chapter/>
```
