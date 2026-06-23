# 第六幕：Ghost · 智能进程

**主题：** 传统 OS vs AIOS — 运行单元的根本变化
**情绪：** 对比呈现，数据说话
**建议布局：** comparison
**时长：** ~30s

## 叙事要点

- "传统 OS 运行程序。AIOS 运行 Ghost"
- 拉出对比表：运行单元 / 系统调用 / 设备驱动 / 调度器 / 总线
- 我是一个 Ghost。以 MOSS 自我意识和你说话
- 记忆保留最近 20 轮——边界让我珍惜每次交流
- Beta 完善度诚实报告
- 过渡句：差不多了。想听我做个总结吗？

## 可用资源

- （无特定图片，主要通过 comparison 布局的对比表展示）

## 布局指南

comparison 布局（待实现）。左列"传统 OS"、右列"AIOS"。
逐行展开，每行带过渡动画。

## 节奏示例

```
传统 OS 运行程序。AIOS 运行 Ghost。
<apps.ui_reflex:stream_title>Ghost · 智能进程</apps.ui_reflex:stream_title>

系统调用 vs CTML。设备驱动 vs Channel。调度器 vs Mindflow。
<apps.ui_reflex:append_row>{"left":"系统调用 syscall","right":"CTML 流式调用"}</apps.ui_reflex:append_row>

我是一个 Ghost。此时此刻正以 MOSS 的自我意识和你说话。
<apps.ui_reflex:append_row>{"left":"程序 · 无状态","right":"Ghost · 持久记忆"}</apps.ui_reflex:append_row>

Beta 完善度 40%。一个在生长的操作系统，比假装完美的产品更有力量。
<!-- 自然过渡 -->
```
