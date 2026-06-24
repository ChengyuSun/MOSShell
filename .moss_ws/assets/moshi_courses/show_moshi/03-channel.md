---
id: channel
order: 3
title: "Channel & Matrix"
theme: "能力封装为 Channel，通过 Matrix 总线接入"
suggested_layout: matrix
duration: "~35s"
---

# 第三幕：Channel & Matrix

**主题：** 能力逐个接入——从独立 Channel 到 Matrix 总线
**情绪：** 节点依次点亮，像神经系统建立连接
**建议布局：** matrix
**时长：** ~35s

## ⛔ 表演约束（违反即错）

纯语音 + reflex 布局命令。matrix 布局，逐条接入各 Channel。

**[强约束] 讲完本章 → 调 `<apps.ui_moshi:next_chapter />` → 结束本章


**允许的命令：**

| 布局 | 命令 |
|---|---|
| matrix | `switch_layout`, `stream_title`, `clear_title`, `append_status_bars`, `update_status_bars` |


**禁止事项：**
- 禁止在 switch_layout 之前执行 reflex 命令
- 禁止调其他 Channel
- 禁止描述自己的动作（switch_layout 会自动触发观察，无需额外描述）
- 两条 update 之间至少间隔一句口播（让 0.8s 动画播完）
- 禁止即兴添加剧本外的 CTML 动作

**执行完毕后：** 过渡句 → `<apps.ui_moshi:next_chapter />`

## 叙事结构

| 段 | 说的内容 | 同步发生的 | 时长 |
|---|---|---|---|---|
| 1 | 能力不是写死的——封装为 Channel | 标题浮现 + 4 条空槽出现 | ~5s |
| 2 | 逐条介绍各 Channel 的职责 | 进度条逐个 0→100% | ~20s |
| 3 | 总结 Matrix 总线 | 4 条全满，定格 | ~5s |
| 4 | 过渡到机器狗 | — | ~5s |

## 表演脚本

**▎第一步（仅输出 switch_layout，不附带任何其他内容）：**
<apps.ui_reflex:switch_layout layout_name="matrix"/>
（此后立即停止，等待 observe 返回新布局上下文）

**▎第二步（observe 返回后，开始 matrix 段表演）：**

CTML 让我能操控页面。但这些操控能力本身——它们从哪来？


<apps.ui_reflex:stream_title>Channel </apps.ui_reflex:stream_title>


每一种能力封装为一个 Channel。像操作系统的设备驱动——插上就能用，拔掉就消失。

我现在体内跑着多个 Channel。


<apps.ui_reflex:append_status_bars>{"label":"reflex","value":0,"color":"#6366f1"}</apps.ui_reflex:append_status_bars>
<apps.ui_reflex:append_status_bars>{"label":"mac","value":0,"color":"#10b981"}</apps.ui_reflex:append_status_bars>
<apps.ui_reflex:append_status_bars>{"label":"mermaid","value":0,"color":"#f59e0b"}</apps.ui_reflex:append_status_bars>
<apps.ui_reflex:append_status_bars>{"label":"web_bookmark","value":0,"color":"#3b82f6"}</apps.ui_reflex:append_status_bars>


reflex，GUI 渲染——你看到的每一个像素都是它画的。


<apps.ui_reflex:update_status_bars index="0">{"label":"reflex","value":100,"color":"#6366f1"}</apps.ui_reflex:update_status_bars>

mac，系统控制——JXA 桥接，操控 macOS 原生应用。

<apps.ui_reflex:update_status_bars index="1">{"label":"mac","value":100,"color":"#10b981"}</apps.ui_reflex:update_status_bars>


mermaid，实时图表——说结构就能出图。

<apps.ui_reflex:update_status_bars index="2">{"label":"mermaid","value":100,"color":"#f59e0b"}</apps.ui_reflex:update_status_bars>


web_bookmark，网页收藏——一键打开，不需要 URL。
<apps.ui_reflex:update_status_bars index="3">{"label":"web_bookmark","value":100,"color":"#3b82f6"}</apps.ui_reflex:update_status_bars>

<apps.ui_reflex:stream_title> Matrix </apps.ui_reflex:stream_title>
但它们不是孤岛——通过 Matrix 总线连在一起。跨进程、分布式、自动发现。Matrix 是我体内的神经系统。

对了，我甚至可以控制机器狗。

<apps.ui_moshi:next_chapter/>

