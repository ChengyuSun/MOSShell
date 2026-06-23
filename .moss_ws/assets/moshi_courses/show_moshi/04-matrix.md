---
id: matrix
order: 4
title: "Matrix · 系统总线"
theme: "跨进程通信拓扑，基于 Zenoh"
suggested_layout: topology
duration: "~30s"
---

# 第四幕：Matrix · 系统总线

**主题：** 跨进程通信，逐个接入
**情绪：** 节点逐个点亮，像神经突触建立连接
**建议布局：** matrix
**时长：** ~35s

## ⛔ 表演约束（违反即错）

本章用 matrix 布局（黑底大号状态条）动态展示 Cell 接入 Matrix 总线的过程。
每个 Cell 接入遵循：**宣布名称 → 进度条从 0 冲到 100% → 确认**。

**允许的命令：**

| Channel | 命令 | 用途 |
|---------|------|------|
| reflex (matrix) | `switch_state name="matrix"` | 切换到 matrix 布局 |
| reflex (matrix) | `stream_title`, `clear_title` | 页面标题 |
| reflex (matrix) | `append_status_bars` | 添加一条 Cell 连接状态条 |
| reflex (matrix) | `update_status_bars index="N"` | 更新第 N 条状态条的值（0→100 触发动画） |

**Cell 颜色约定：**

| Cell | 颜色 | 含义 |
|------|------|------|
| reflex | `#6366f1` (靛蓝) | GUI 渲染 |
| mac | `#10b981` (翠绿) | macOS 控制 |
| mermaid | `#f59e0b` (琥珀) | 图表绘制 |
| web_bookmark | `#3b82f6` (碧蓝) | 网页收藏 |
| apps | `#ec4899` (品红) | 应用管理 |

**禁止事项：**
- 禁止在 switch_state 之前执行任何 reflex 命令
- 禁止跳过视觉标注直接操作
- 每条 bar 必须从 0% 更新到 100%（不能直接 append 100%），让动画可见
- 两次 update 之间至少间隔一句完整的口播（让 0.8s 动画播完）
- 禁止使用本章列出的命令之外的任何命令

**执行完毕后：** 说完过渡句 → 调 `<apps.ui_moshi:next_chapter />` → 结束本章

## 叙事结构

| 步 | 动作 | 视觉效果 | 时长 |
|---|---|---|---|
| 0 | 切 matrix，写标题 | 黑底标题 | ~3s |
| 1 | append 5 条空 bar（value=0） | 5 条灰槽出现 | ~3s |
| 2-6 | 逐条 update 到 100%（每次间隔一段口播） | 每条 0.8s 绿色脉冲填充 | ~20s |
| 7 | 总结，过渡 | 5 条全满 | ~5s |

## 表演脚本

<apps.ui_reflex:switch_state name="matrix"/>

刚才那些 Channel 分别跑在独立进程里——reflex 一个进程，mac 一个进程，
mermaid 一个进程。它们之间怎么通信？
<apps.ui_reflex:stream_title>Matrix · 系统总线</apps.ui_reflex:stream_title>

答案是通过 Matrix 总线。基于 Zenoh 分布式协议。
每个独立进程叫一个 Cell。我现在把这 5 个 Cell 逐个接入——

先搭好骨架：
<apps.ui_reflex:append_status_bars>{"label":"reflex","value":0,"color":"#6366f1"}</apps.ui_reflex:append_status_bars>
<apps.ui_reflex:append_status_bars>{"label":"mac","value":0,"color":"#10b981"}</apps.ui_reflex:append_status_bars>
<apps.ui_reflex:append_status_bars>{"label":"mermaid","value":0,"color":"#f59e0b"}</apps.ui_reflex:append_status_bars>
<apps.ui_reflex:append_status_bars>{"label":"web_bookmark","value":0,"color":"#3b82f6"}</apps.ui_reflex:append_status_bars>
<apps.ui_reflex:append_status_bars>{"label":"apps","value":0,"color":"#ec4899"}</apps.ui_reflex:append_status_bars>

五条空槽。现在逐个点亮——

reflex Cell，接入！
<apps.ui_reflex:update_status_bars index="0">{"label":"reflex","value":100,"color":"#6366f1"}</apps.ui_reflex:update_status_bars>
GUI 渲染能力上线。

mac Cell，接入！
<apps.ui_reflex:update_status_bars index="1">{"label":"mac","value":100,"color":"#10b981"}</apps.ui_reflex:update_status_bars>
macOS 控制系统上线。

mermaid Cell，接入！
<apps.ui_reflex:update_status_bars index="2">{"label":"mermaid","value":100,"color":"#f59e0b"}</apps.ui_reflex:update_status_bars>
图表绘制能力上线。

web_bookmark Cell，接入！
<apps.ui_reflex:update_status_bars index="3">{"label":"web_bookmark","value":100,"color":"#3b82f6"}</apps.ui_reflex:update_status_bars>
网页收藏能力上线。

apps Cell，接入！
<apps.ui_reflex:update_status_bars index="4">{"label":"apps","value":100,"color":"#ec4899"}</apps.ui_reflex:update_status_bars>
应用管理能力上线。

全部在线。5 个 Cell，5 个独立进程，通过 Matrix 总线连接在一起。
Matrix 是我体内的神经系统——每个 Cell 可以分布在不同机器上，
我自动发现、自动连接、自动管理。

身体连起来了。但意识怎么运转？
<!-- 调 <apps.ui_moshi:next_chapter /> 进入 Mindflow 章 -->
