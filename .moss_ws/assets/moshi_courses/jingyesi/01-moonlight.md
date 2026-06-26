---
id: moonlight
order: 1
title: "床前明月光"
theme: "景 — 月光洒落，静夜开场"
suggested_layout: course
duration: "~30s"
---

# 第一幕：床前明月光

**诗句：** 床前明月光
**主题：** 景 — 月光洒落，静夜开场
**情绪：** 宁静、清澈、略带清冷
**建议布局：** course
**时长：** ~30s

## ⛔ 表演约束（违反即错）

本章只做一件事：呈现第一句诗。以下为硬约束：

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

- `pil-image://workspace-assets/e2ebae1a803f` — 月夜，一轮满月悬于天际，清辉洒人间，远山隐隐，江水静流
- `pil-image://workspace-assets/5867f3aaee5f` — 李白，月下独酌，举杯望月，传统中国水墨画风格

## 节奏示例

```
<apps.ui_reflex:switch_layout layout_name="course"/>
（此后立即停止，等待 observe 返回新布局上下文）

**▎第二步（observe 返回后，开始表演）：**
<apps.ui_reflex:clear_title />

床前明月光——
<apps.ui_reflex:stream_title>床前明月光</apps.ui_reflex:stream_title>

深秋的深夜，李白独坐。月光如水，洒在床前。
没有风，没有声响。只有这一地的清辉。

你看，月光太亮了。亮得他恍惚了，亮得像什么？
<!-- 在此之后调 <apps.ui_moshi:next_chapter /> 进入第二幕 -->
```
