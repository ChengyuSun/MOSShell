# 第二幕：CTML · 系统调用

**主题：** 流式系统调用，跨域并行，时间是第一公民
**情绪：** 递进——从理解到惊叹到深思
**建议布局：** stage
**时长：** ~40s

## 叙事要点

本幕分四段递进，每段 ~10s：

| 段 | 主题 | 核心演示 | 观众反应 |
|---|---|---|---|
| 1 | 流式 | mermaid 画 CTML 流程图——边生成 token 边执行 | "哦，这样" |
| 2 | 并行 | 一个输出块同时驱动 reflex + ai_eye + mac——三个独立系统同时响应 | "卧槽" |
| 3 | 时间 | 快命令（mermaid ~1s）+ 慢命令（mac 通知 ~3s）——快慢错峰，Ghost 嘴没停 | "有意思" |
| 4 | 自省 | moss_self 查看自己的 Channel 列表——Ghost 用 CTML 理解自己 | "这 OS 是活的" |

## 可用 Channel

本幕需确保以下 Channel 可用（应在 MODE.md `bringup_apps` 中声明）：

- `mermaid` — 架构图绘制（main channel 子通道，始终可用）
- `mac` — macOS JXA 系统控制（main channel 子通道）
- `apps.ui_reflex` — GUI 页面（stage 布局，标题/字幕背景板）
- `apps.games_ai_eye` — AI 眼睛表情
- `apps.tools_moss_self` — MOSS CLI 自省

## 可用资源

- pil-image://moshi/ctml_flow — CTML 流式解析流程图（可选，用于 stage 的 append_images）

## 布局指南

stage 布局承担标题/字幕的背景板角色。真正的视觉冲击来自五个 Channel 的同时响应——
这些 Channel 各有独立的渲染通道（mermaid 走浏览器、mac 走 JXA、ai_eye 走 pygame），
reflex 页面只是其中一个"世界"。

Ghost 应在开场切到 stage 布局，之后聚焦于跨 Channel 编排。CTML 标签本身不需要
展示在页面上——它们被 Ghost 说出来就已经是演示。

## 节奏示例

```
（切 stage 布局，清字段，写标题）
<apps.ui_reflex:stream_title>CTML · 系统调用层</apps.ui_reflex:stream_title>

── 第一段：流式 ──

AI 怎么操作我？通过 CTML —— 流式系统调用语言。
<mermaid:draw title="CTML 流式执行"><![CDATA[
flowchart LR
  A["Ghost 说话"] --> B["CTML 解析<br/>流式、实时"]
  B --> C["命令执行<br/>边生成边执行"]
]]></mermaid:draw>

我说的同时，图已经出来了。不是等我说完——是边生成 token 边解析执行。
<mermaid:draw title="传统 vs CTML"><![CDATA[
flowchart LR
  subgraph 传统
    A1["程序调用"] --> A2["等待返回"] --> A3["继续执行"]
  end
  subgraph CTML
    B1["Ghost 输出 token"] --> B2["流式解析"] --> B3["命令并行执行"]
    B1 --> B4["继续输出 token"]
  end
]]></mermaid:draw>

传统系统调用同步阻塞；CTML 流式、并行、时间感知。每个命令有物理执行时长——
Ghost 的输出是对未来的时序规划。

── 第二段：并行 ──

现在，一句话。三个世界。
<apps.ui_reflex:stream_subtitle>并行执行</apps.ui_reflex:stream_subtitle>
<apps.games_ai_eye:set_expression name="excited" />
<mac:run timeout="15"><![CDATA[
(function() {
    'use strict';
    var Calendar = Application('com.apple.iCal');
    Calendar.activate();
    return { success: true, action: 'open_calendar' };
})();
]]></mac:run>

GUI 更新了。我的眼睛变了。日历打开了。
<apps.games_ai_eye:speaking />

传统程序要写三个线程，加锁，同步。CTML 一句话就够了。

── 第三段：时间 ──

还不止——每个命令有独立的物理执行时长。
<mermaid:draw title="快速通道：1 秒"><![CDATA[
flowchart LR
  A["mermaid 命令"] --> B["1 秒完成 ✓"]
]]></mermaid:draw>
<mac:run timeout="15"><![CDATA[
(function() {
    'use strict';
    var app = Application.currentApplication();
    app.includeStandardAdditions = true;
    delay(3);
    app.displayNotification('3 秒后到达 —— CTML 时间感知', {
        withTitle: 'MOSS · AIOS',
        subtitle: 'Ghost In Shells'
    });
    return { success: true, action: 'notify_after_3s' };
})();
]]></mac:run>

mermaid 一秒完成。mac 通知要三秒。我不等。

CTML 的每个命令是对未来时间的规划。Ghost 规划时序，命令各自按时到达。
这就是"时间是第一公民"。

── 第四段：自省 ──

我甚至能用 CTML 来理解自己。
<apps.tools_moss_self:run command="codex list ghoshell_moss.channels" />

（结果返回后，Ghost 读取 Channel 列表，即兴评论）

看到了吗？我刚才用 CTML 调用了 MOSS 的 codex 工具——
它返回了我体内的 Channel 模块清单。我用系统调用来理解我自己。
这是一个能自省的操作系统。

能力本身怎么组织？想继续听吗？
<!-- 调 <apps.ui_moshi:next_chapter /> 进入 Channel 章 -->
```
