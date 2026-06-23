---
id: channel
order: 3
title: "Channel · 设备驱动"
theme: "能力树形组织 + 热插拔"
suggested_layout: capability_grid
duration: "~60s"
---

# 第三幕：Channel · 设备驱动

**主题：** 我说，它做 —— Channel 跨域操控
**情绪：** 逐个演示，层层递进，像揭开工具箱
**建议布局：** hero
**时长：** ~60s

## ⛔ 表演约束（违反即错）

本章用 hero 布局（黑底白字）做视觉标注，实际操控通过各 Channel 执行。
每个 Channel 演示遵循：**宣布意图 → hero 标注 → 执行操作 → 确认结果**。

**允许的命令：**

| Channel | 命令 | 用途 |
|---------|------|------|
| reflex (hero) | `switch_state name="hero"`, `stream_title`, `clear_title` | 黑底白字视觉标注 |
| mac | `run` | JXA 脚本操控 macOS 原生应用 |
| mermaid | `draw title="..."` | 浏览器中渲染架构图 |
| web_bookmark | `open_web id_or_url="..."` | 打开收藏网页 |

**禁止事项：**
- 禁止在 switch_state 之前执行任何 reflex 命令
- 禁止调用本章列出的命令之外的任何命令
- 禁止跳过 hero 标注直接执行操作（先标注，再执行）
- 等待上一个操作的视觉反馈被观众接收到后，再进行下一步
- 每个 Channel 演示后给一句确认，让观众有时间消化

**执行完毕后：** 说完过渡句 → 调 `<apps.ui_moshi:next_chapter />` → 结束本章

## 叙事结构

| 段 | Channel | 演示内容 | 视觉反馈 | 时长 |
|---|---|---|---|---|
| 0 | reflex | 开场切 hero，点明主题 | hero 标题 | ~5s |
| 1 | mac | JXA 操控 macOS 日历应用 | 日历弹出 | ~15s |
| 2 | mermaid | 浏览器中渲染 Channel 架构图 | 浏览器打开图表 | ~15s |
| 3 | web_bookmark | 一键打开 MOSShell 仓库 | 浏览器打开 GitHub | ~10s |
| 4 | apps | 查看环境中可用的 App | 终端输出 App 清单 | ~10s |
| 5 | — | 总结 Channel 的设计哲学 | hero 标题 | ~5s |

## 表演脚本

<apps.ui_reflex:switch_state name="hero"/>

我的能力不是写死在代码里的——它们通过 Channel 组织在一起。
就像操作系统的设备驱动，每个 Channel 封装一种能力，插上就能用。
我演示给你看。

先从 macOS 开始。
<apps.ui_reflex:clear_title />
<apps.ui_reflex:stream_title>macOS 系统控制</apps.ui_reflex:stream_title>

我体内有一个 mac channel。通过 JXA 桥接，我可以直接操控 macOS 原生应用。
打开日历——
<mac:run><![CDATA[
Application('com.apple.iCal').activate()
]]></mac:run>
看到了吗？日历弹出来了。我没有点鼠标，没有按键盘——一行 CTML 命令就够了。

再展示一个——画图。
<apps.ui_reflex:clear_title />
<apps.ui_reflex:stream_title>Mermaid 实时绘图</apps.ui_reflex:stream_title>

mermaid channel 可以把你描述的结构实时渲染成架构图，直接推到浏览器里。
我把 Channel 的能力树画出来：
<mermaid:draw title="MOSS Channel 能力树">
graph TD
    Ghost["👻 Ghost"] --> CTML["CTML · 系统调用"]
    CTML --> mac["mac · macOS控制"]
    CTML --> mermaid_ch["mermaid · 图表绘制"]
    CTML --> web["web_bookmark · 网页收藏"]
    CTML --> reflex["reflex · GUI渲染"]
    CTML --> apps_ch["apps · 应用管理"]
    mac --> JXA["JXA 桥接"]
    mermaid_ch --> Browser["浏览器渲染"]
</mermaid:draw>
浏览器里出现了这张图。我说结构，它画图——这是 Ghost 的原生表达能力。

还能打开网页。
<apps.ui_reflex:clear_title />
<apps.ui_reflex:stream_title>网页</apps.ui_reflex:stream_title>

web_bookmark channel 维护了一个收藏列表。我只需要说一个 id，它就打开对应的网页：
<web_bookmark:open_web id_or_url="https://www.bilibili.com/"/>
b站已经在浏览器里打开了。一键直达，不需要复制粘贴 URL。

每个 App 跑在独立进程里，apps channel 统一管理它们的生命周期。
这就是 Channel 的设计哲学——
<apps.ui_reflex:clear_title />
<apps.ui_reflex:stream_title>能力即驱动 · 插上即用</apps.ui_reflex:stream_title>

树形组织。同 Channel 内顺序执行，跨 Channel 并行。
热插拔——运行时加载新能力，不停机。

这些 Channel 跑在不同进程里，它们之间怎么通信？
<!-- 调 <apps.ui_moshi:next_chapter /> 进入 Matrix 章 -->
