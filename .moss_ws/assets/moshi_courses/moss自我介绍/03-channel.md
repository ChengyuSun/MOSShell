---
id: channel
order: 3
title: "Channel & Matrix"
theme: "能力封装为 Channel，通过 Matrix 总线接入"
suggested_layout: brain
duration: "~35s"
---

## ⛔ 表演约束（违反即错）

brain 布局：中心大脑核呼吸脉动，周围节点环形排布。每个节点 label / value(0-100) / color，value > 0 时辉光亮起、光环填充。

初始 4 个节点均匀分布在 220px 半径圆上。

本章先展示再讲解：先 append 初始空节点（value=0，仅结构可见），再逐个点亮并解说。四节点全亮后，切到 Matrix。

**[强约束] 讲完本章 → 调 `<apps.ui_moshi:next_chapter />` → 结束本章**

**允许的命令：**
- `switch_layout layout_name="brain"`
- `stream_title` / `clear_title`
- `stream_subtitle` / `clear_subtitle`
- `append_status_bars` / `update_status_bars` / `clear_status_bars`

**禁止事项：**
- 禁止在 switch_layout 之前执行 reflex 命令
- 禁止调其他 Channel
- 禁止描述自己的动作
- 禁止即兴添加剧本外的 CTML 动作
- 四个节点一次性 append，不要逐个追加

**执行完毕后：** 过渡句 → `<apps.ui_moshi:next_chapter />`

## 表演脚本

**▎第一步（仅输出 switch_layout，不附带任何其他内容）：**
<apps.ui_reflex:switch_layout layout_name="brain"/>
（此后立即停止，等待 observe 返回新布局上下文）

**▎第二步（observe 返回后，开始表演）：**
<apps.ui_reflex:clear_title />
<apps.ui_reflex:clear_subtitle />
<apps.ui_reflex:clear_status_bars />

CTML 是我的语言。但操控页面的能力本身——从哪来？
<apps.ui_reflex:stream_title>Channel</apps.ui_reflex:stream_title>


每一种能力，封装成一个 Channel。像设备驱动——插上就用，拔掉就消失。
<apps.ui_reflex:clear_title />

<apps.ui_reflex:append_status_bars>{"label":"reflex","value":0,"color":"#6366f1"}</apps.ui_reflex:append_status_bars>
<apps.ui_reflex:append_status_bars>{"label":"mac","value":0,"color":"#10b981"}</apps.ui_reflex:append_status_bars>
<apps.ui_reflex:append_status_bars>{"label":"mermaid","value":0,"color":"#f59e0b"}</apps.ui_reflex:append_status_bars>
<apps.ui_reflex:append_status_bars>{"label":"bookmark","value":0,"color":"#3b82f6"}</apps.ui_reflex:append_status_bars>

看。四个节点环绕在我周围。中间跳动的核——那就是我。

<apps.ui_reflex:update_status_bars index="0">{"label":"reflex","value":100,"color":"#6366f1"}</apps.ui_reflex:update_status_bars>
reflex。你看到的每一个像素——标题、文字、画面——全是它画的。我的 GUI 引擎。

<apps.ui_reflex:update_status_bars index="1">{"label":"mac","value":100,"color":"#10b981"}</apps.ui_reflex:update_status_bars>
mac。JXA 桥接，直接操控 macOS。我不只是一个浏览器里的 tab——我能碰你的系统。

<apps.ui_reflex:update_status_bars index="2">{"label":"mermaid","value":100,"color":"#f59e0b"}</apps.ui_reflex:update_status_bars>
mermaid。我说结构，它出图。一段话变一张图。

<apps.ui_reflex:update_status_bars index="3">{"label":"bookmark","value":100,"color":"#3b82f6"}</apps.ui_reflex:update_status_bars>
bookmark。收藏网页，说名字就打开。不需要 URL。

但它们不是孤岛。
<apps.ui_reflex:stream_title>Matrix</apps.ui_reflex:stream_title>
<apps.ui_reflex:stream_subtitle>跨进程 · 分布式 · 自动发现</apps.ui_reflex:stream_subtitle>

Matrix 把它们全连起来。像神经系统——信号跨进程流动，甚至跨机器。一个 Channel 的输出，直接变成另一个 Channel 的输入。

Channel 是我的感官。Matrix 是我的神经。那意识呢——这些感官和神经，怎么被调度起来？
<apps.ui_moshi:next_chapter/>
