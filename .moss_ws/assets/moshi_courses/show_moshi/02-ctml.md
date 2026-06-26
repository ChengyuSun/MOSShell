---
id: ctml
order: 2
title: "CTML · 系统调用"
theme: "Ghost 用输出 token 作为系统调用，流式操控页面"
suggested_layout: course
duration: "~30s"
---

# 第二幕：CTML · 系统调用

**主题：** 从笔友到具身——Ghost 说的每一个字，都是系统调用
**情绪：** 娓娓道来，像在讲一个理所当然的事实
**建议布局：** course
**时长：** ~30s

## ⛔ 表演约束（违反即错）

纯语音 + course 布局。不调其他 Channel，不描述自己的动作。

**[强约束] 讲完本章 → 调 `<apps.ui_moshi:next_chapter />` → 结束本章


**允许的命令：**
- `switch_layout layout_name="course"`
- `stream_title` / `clear_title`
- `stream_sub_title` / `clear_sub_title`
- `append_image locator="..."` / `clear_image`
- `stream_main_text` / `clear_main_text`

**禁止事项：**
- 禁止在 switch_layout 之前执行 reflex 命令
- 禁止说"看"、"你看"、"看到了吗"、"我来演示"——动作自己会说话
- 禁止描述自己的动作（switch_layout 会自动触发观察，无需额外描述）
- 禁止调其他 Channel
- 一句话最多配一个动作，不要堆命令
- 禁止即兴添加剧本外的 CTML 动作


## 可用资源

- `pil-image://workspace-assets/penpal-vs-embodied-ai.png` — 笔友 AI vs 具身 AI 对比
- `pil-image://workspace-assets/mosshell-three-layers.png` — Ghost In Shells 三层架构

## 叙事结构

三段自然推进，不加解说。图片和文字的切换本身就是论点。

| 段 | 说的内容 | 同步发生的 | 时长 |
|---|---|---|---|
| 1 | 传统 AI 是什么——笔友，只有文字 | 标题浮现 + 贴对比图 | ~8s |
| 2 | 但我不是——我有身体，有架构 | 换三层架构图 + 副标题更新 | ~8s |
| 3 | CTML 就是我操控身体的方式 | 正文写下 → 重写 | ~10s |
| 4 | 收尾，过渡 | — | ~4s |

## 表演脚本

**▎第一步（仅输出 switch_layout，不附带任何其他内容）：**
<apps.ui_reflex:switch_layout layout_name="course"/>
（此后立即停止，等待 observe 返回新布局上下文）

**▎第二步（observe 返回后，开始表演）：**
<apps.ui_reflex:stream_title>C T M L</apps.ui_reflex:stream_title>
<apps.ui_reflex:append_image locator="pil-image://workspace-assets/penpal-vs-embodied-ai.png"/>
传统 AI 像一个笔友。你发一段文字，它回一段文字。它不知道你在哪，在做什么，周围有什么。对它来说，世界就是一串 token。

但 AI 不应该是笔友。
<apps.ui_reflex:clear_image />
<apps.ui_reflex:append_image locator="pil-image://workspace-assets/mosshell-three-layers.png"/>

一个真正有用的 AI 需要一个身体，一套神经系统，一种把想法变成动作的方式。
<apps.ui_reflex:stream_sub_title>灵 · 壳 · 体</apps.ui_reflex:stream_sub_title>

在 MOSS 里，这套神经系统叫 CTML——Command Token Marked Language。
<apps.ui_reflex:stream_main_text>Ghost 输出的每一个 token，被 CTML 实时解析为系统调用。流式、并行、时间是第一公民。</apps.ui_reflex:stream_main_text>
<apps.ui_reflex:append_annotations>token：模型输出的最小语义单元。Ghost 一边思考一边输出，不等整句说完，命令已经跑起来了</apps.ui_reflex:append_annotations>
<apps.ui_reflex:append_annotations>CTML：Command Token Marked Language。不是聊天协议，是 Ghost 操控 Shell 的系统调用</apps.ui_reflex:append_annotations>

它不是我"想好了再发"的东西。它是我一边思考一边执行的——不等整句说完，命令已经跑起来了。
<apps.ui_reflex:clear_main_text />
<apps.ui_reflex:stream_main_text>我说，它变。每一次输出，都是一个动作。</apps.ui_reflex:stream_main_text>

这就是 CTML。不是聊天协议，是系统调用。是 Ghost 的身体语言。
<apps.ui_reflex:stream_title>· Ghost 的身体语言</apps.ui_reflex:stream_title>
想了解这些能力是怎么组织起来的吗？
<apps.ui_moshi:next_chapter/>
