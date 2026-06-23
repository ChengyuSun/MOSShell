# 第三幕：Channel · 设备驱动

**主题：** 能力树形组织 + 热插拔
**情绪：** 能力卡片逐个点亮，树形展开
**建议布局：** capability_grid
**时长：** ~60s

## 叙事要点

- "能力通过 Channel 组织——就像操作系统的设备驱动"
- 逐个介绍 Channel：mermaid（架构图绘制）、mac（系统控制）、ai_eye（AI 眼睛）
- 每介绍一个 Channel，追加一张能力卡片到画面
- 核心概念：树形结构，同 channel 内顺序执行，跨 channel 并行
- 热插拔——运行时加载新能力
- 过渡句：这些 Channel 跑在不同进程里，它们怎么通信？

## 可用资源

- pil-image://moshi/channel_tree — Channel 能力树图

## 布局指南

capability_grid 布局（待实现）。卡片网格展示各 Channel。
介绍的 Channel 卡片高亮/放大。

## 节奏示例

```
我的能力通过 Channel 组织——就像操作系统的设备驱动。
<apps.ui_reflex:stream_title>Channel · 设备驱动层</apps.ui_reflex:stream_title>

这是 mermaid channel —— 画架构图、流程图。
<apps.ui_reflex:append_cards>{"name":"mermaid","description":"架构图绘制 · 流程图 · 时序图","status":"active"}</apps.ui_reflex:append_cards>

这是 mac channel —— 通过 JXA 控制 macOS。
<apps.ui_reflex:append_cards>{"name":"mac","description":"macOS 系统控制 · 日历 · 音乐 · 终端","status":"active"}</apps.ui_reflex:append_cards>

树形组织，同 channel 内顺序执行，跨 channel 并行。热插拔——运行时加载新能力。
<!-- 自然过渡 -->
```
