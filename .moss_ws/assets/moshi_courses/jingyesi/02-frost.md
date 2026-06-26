---
id: frost
order: 2
title: "疑是地上霜"
theme: "疑 — 错觉之美，似幻似真"
suggested_layout: course
duration: "~30s"
---

# 第二幕：疑是地上霜

**诗句：** 疑是地上霜
**主题：** 疑 — 错觉之美，似幻似真
**情绪：** 恍惚、微凉、一瞬的迷离
**建议布局：** course
**时长：** ~30s

## ⛔ 表演约束（违反即错）

本章只做一件事：呈现第二句诗。以下为硬约束：

**允许的命令：**
- `<apps.ui_reflex:switch_layout layout_name="course"/>` — 第一步，仅此一条，不附带任何其他内容
- `stream_title` / `clear_title` — 诗句主体
- `stream_sub_title` / `clear_sub_title` — 可选副标题
- `stream_main_text` / `clear_main_text` — 赏析正文
- `append_annotations` / `clear_annotations` — 注释条目
- `stream_appreciation` / `clear_appreciation` — 鉴赏文字

**禁止事项：**
- 禁止在 switch_layout 之前执行任何 reflex 命令
- 禁止在 stream_title 之前忘记 clear_title
- 禁止调用 `next_chapter` 直到过渡句说完
- 禁止即兴添加剧本外的 CTML 动作

**执行完毕后：** 说完过渡句 → 调 `<apps.ui_moshi:next_chapter />` → 结束本章

## 可用资源

- `pil-image://workspace-assets/e2ebae1a803f` — 月夜，满月悬于天际，画面留白，意境静谧
- `pil-image://workspace-assets/747d53b80f54` — 李白 portrait，ethereal and free-spirited，传统水墨

## 节奏示例

```
<apps.ui_reflex:switch_layout layout_name="course"/>
（此后立即停止，等待 observe 返回新布局上下文）

**▎第二步（observe 返回后，开始表演）：**
<apps.ui_reflex:clear_title />

疑是地上霜。
<apps.ui_reflex:stream_title>疑是地上霜</apps.ui_reflex:stream_title>

一个"疑"字。全诗最妙的一笔。

月光太亮了。亮得他恍惚了——这满地银白，是月光，还是秋霜？
霜是冷的。霜只出现在深夜，清晨就化了。

这个疑只持续了一秒。但就是这一秒，让这四句诗活了。他抬起头——
<!-- 在此之后调 <apps.ui_moshi:next_chapter /> 进入第三幕 -->
```
