---
id: ctml
order: 2
title: "CTML · 系统调用"
theme: "流式系统调用，时间是第一公民"
suggested_layout: stage
duration: "~40s"
---

# 第二幕：CTML · 系统调用

**主题：** 我说，它变 —— CTML 实时操控
**情绪：** 对话式演示，像边解说边变魔术
**建议布局：** course
**时长：** ~40s

## ⛔ 表演约束（违反即错）

本章只操控 reflex channel 的 course 布局。不涉及其他 channel。

**允许的 reflex 命令（仅 course 布局）：**
- `switch_state name="course"` — 第一步，必须最先执行
- `stream_title` / `clear_title` — 流式写入 / 清空标题
- `stream_sub_title` / `clear_sub_title` — 流式写入 / 清空副标题
- `append_image locator="..."` / `pop_image` / `clear_image` — 追加 / 弹出 / 清空图片
- `stream_main_text` / `clear_main_text` — 流式写入 / 清空正文
- `stream_annotations` / `pop_annotations` / `clear_annotations` — 流式追加 / 弹出 / 清空注释
- `stream_appreciation` / `clear_appreciation` — 流式写入 / 清空赏析

**禁止事项：**
- 禁止在 switch_state 之前执行任何 reflex 命令
- 禁止调用本章列出的命令之外的任何 reflex 命令
- 禁止调用其他 channel 的控制命令（如 speech、vision 等）
- 禁止即兴添加剧本外的 CTML 动作
- 每步操作前必须先说出意图，操作后给一句确认

**执行完毕后：** 说完过渡句 → 调 `<apps.ui_moshi:next_chapter />` → 结束本章

## 可用资源

- `pil-image://workspace-assets/mosshell-three-layers` — Ghost In Shells 三层架构图
- `pil-image://workspace-assets/MOSShell-realtime-runtime-nervous-system` — MOSS 实时运行时神经系统

## 叙事结构

| 段 | 主题 | 核心演示 | 时长 |
|---|---|---|---|
| 1 | 文字 | stream → clear → stream（写、删、重写） | ~12s |
| 2 | 图片 | append → append → pop → clear（叠、删、清） | ~12s |
| 3 | 列表 | stream → stream → pop（逐条加、逐条删） | ~12s |
| 4 | 收尾 | 总结 CTML 的实时操控能力 | ~4s |

## 表演脚本

<apps.ui_reflex:switch_state name="course"/>

看好了——我现在说的每一句话，都能直接操控这个页面。

先来写点东西。我要写一个标题：
<apps.ui_reflex:stream_title>CTML · 实时系统调用</apps.ui_reflex:stream_title>
看到了吗？字是一个一个流出来的——不是我打完再发，是边说边写。

再来个副标题：
<apps.ui_reflex:stream_sub_title>Ghost 用输出 token 直接操控 UI</apps.ui_reflex:stream_sub_title>

正文也来一段：
<apps.ui_reflex:stream_main_text>
传统 AI 对话是你问一句、它回一句。CTML 打破了这个边界——
Ghost 的每一个输出 token 被实时解析成系统调用，不等整句说完，命令已经开始执行。
</apps.ui_reflex:stream_main_text>

但我不喜欢这个标题，换一个：
<apps.ui_reflex:clear_title />
<apps.ui_reflex:stream_title>CTML · 让 Ghost 长出双手</apps.ui_reflex:stream_title>

文字可以写了又改。接下来看看图片。

我要加一张架构图：
<apps.ui_reflex:append_image locator="pil-image://workspace-assets/mosshell-three-layers"/>
左边出现了 Ghost In Shells 的三层架构——Agent、Shell、Robot，灵壳一体。

全部清掉：
<apps.ui_reflex:clear_image />
图片区空了。我说加就加，说删就删。

文字和图片都能操控。最后看看列表——我加几条注释：
<apps.ui_reflex:stream_annotations>CTML 是 Ghost 的系统调用语言</apps.ui_reflex:stream_annotations>
<apps.ui_reflex:stream_annotations>每个 CTML 标签是一个命令，流式解析、实时执行</apps.ui_reflex:stream_annotations>
<apps.ui_reflex:stream_annotations>时间是系统调用的第一公民</apps.ui_reflex:stream_annotations>

三条注释，一条一条蹦出来。最后一条不要了：
<apps.ui_reflex:pop_annotations />
没了。

这就是 CTML——我说话，页面就变。不是聊天，不是问答，是 Ghost 在用系统调用直接操控它的身体。

想了解这些能力是怎么组织起来的吗？
<!-- 调 <apps.ui_moshi:next_chapter /> 进入 Channel 章 -->
