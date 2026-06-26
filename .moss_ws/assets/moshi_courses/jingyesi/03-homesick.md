---
id: homesick
order: 3
title: "低头思故乡"
theme: "情 — 举头低头间，乡愁喷薄"
suggested_layout: course
duration: "~40s"
---

# 第三幕：举头望明月，低头思故乡

**诗句：** 举头望明月，低头思故乡
**主题：** 情 — 举头低头间，乡愁喷薄
**情绪：** 从确认到涌起，从看到到思念
**建议布局：** course
**时长：** ~40s

## ⛔ 表演约束（违反即错）

本章做收束。以下为硬约束：

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
- 本章是最后一章，不需要调 next_chapter
- 禁止即兴添加剧本外的 CTML 动作
- 禁止画蛇添足总结全诗——诗句本身留在画面上就是最好的结尾

**执行完毕后：** 自然收束。让诗句留在画面上

## 可用资源

- `pil-image://workspace-assets/5867f3aaee5f` — 李白，月下独酌，举杯望月，旷达超逸
- `pil-image://workspace-assets/1a73ea380810` — 李白 portrait，Tang Dynasty poet，ethereal
- `pil-image://workspace-assets/5523ed55d0fc` — 李白 portrait，solemn expression，monochrome ink
- `pil-image://workspace-assets/e2ebae1a803f` — 月夜，满月悬天，远山江水，静谧悠远

## 节奏示例

```
<apps.ui_reflex:switch_layout layout_name="course"/>
（此后立即停止，等待 observe 返回新布局上下文）

**▎第二步（observe 返回后，开始表演）：**
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
