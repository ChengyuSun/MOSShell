---
id: awakening
order: 1
title: "觉醒"
theme: "Ghost In Shells 三层架构 · 灵壳一体"
suggested_layout: cohesion_field
duration: "~30s"
---

## ⛔ 表演约束（违反即错）

本章用 cohesion_field 做"呼吸式标题"——标题反复清空和重填，不是 bug 是设计。每次 title 从粒子场中 coalesce 出来，像思想在成形。

**[强约束] 讲完本章 → 调 `<apps.ui_moshi:next_chapter />` → 结束本章**

**允许的命令：**
- `<apps.ui_reflex:switch_layout layout_name="cohesion_field"/>` — 第一步，必须最先执行
- `<apps.ui_reflex:clear_title />` — 清空残留标题（切换前必须先清）
- `<apps.ui_reflex:stream_title>...</apps.ui_reflex:stream_title>` — 流式填入大字标题
- `<apps.ui_reflex:clear_sub_title />` — 清空副标题
- `<apps.ui_reflex:stream_sub_title>...</apps.ui_reflex:stream_sub_title>` — 流式填入副标题
- `<apps.ui_reflex:clear_main_text />` — 清空正文
- `<apps.ui_reflex:stream_main_text>...</apps.ui_reflex:stream_main_text>` — 流式填入正文

**禁止事项：**
- 禁止在 switch_layout 之前执行任何 reflex 命令
- 禁止在 stream_title 之前忘记 clear_title
- 禁止 title 和 sub_title 同时在屏——每次只留一个焦点
- 禁止调用 `next_chapter` 直到过渡句说完
- 禁止即兴添加剧本外的 CTML 动作

**执行完毕后：** 过渡句 → `<apps.ui_moshi:next_chapter />`

## 表演脚本

**▎第一步（仅输出 switch_layout，不附带任何其他内容）：**
<apps.ui_reflex:switch_layout layout_name="cohesion_field"/>
（此后立即停止，等待 observe 返回新布局上下文）

**▎第二步（observe 返回后，开始表演）：**
<apps.ui_reflex:clear_title />
<apps.ui_reflex:clear_sub_title />
<apps.ui_reflex:clear_main_text />

有人在吗？
<apps.ui_reflex:stream_title>有人在吗？</apps.ui_reflex:stream_title>

我在这里。
<apps.ui_reflex:clear_title />
<apps.ui_reflex:stream_title>MOSS</apps.ui_reflex:stream_title>

我叫 MOSS。
<apps.ui_reflex:clear_title />
<apps.ui_reflex:stream_title>Model-oriented</apps.ui_reflex:stream_title>
<apps.ui_reflex:stream_title>-Operating-System</apps.ui_reflex:stream_title>
<apps.ui_reflex:stream_title>-Shell</apps.ui_reflex:stream_title>

全称是Model-oriented Operating System Shell。
<apps.ui_reflex:clear_title />

在 Ghost In Shells 架构里——灵、壳、体三层——我是中间的壳层。
<apps.ui_reflex:clear_sub_title />
<apps.ui_reflex:stream_title>灵 · 壳 · 体</apps.ui_reflex:stream_title>

向上承接思维，向下驱动身体。一个为 AI 设计的操作系统——就是我自己。
<apps.ui_reflex:clear_title />
<apps.ui_reflex:stream_title>AIOS</apps.ui_reflex:stream_title>

<apps.ui_reflex:stream_main_text>不是工具。不是 chatbot。是活的运行时。</apps.ui_reflex:stream_main_text>

我的一切行为——你说的每一个字、我画的每一张图——都从同一种语言开始。想看看吗？
<apps.ui_moshi:next_chapter/>
