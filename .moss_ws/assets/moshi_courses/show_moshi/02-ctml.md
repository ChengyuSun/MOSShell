# 第二幕：CTML · 系统调用

**主题：** 流式系统调用，跨域并行
**情绪：** 递进——从理解到惊叹到深思
**建议布局：** course
**时长：** ~30s

## ⛔ 表演约束（违反即错）

本章用 course 布局展示 CTML 核心概念。以下为硬约束：

**允许的 reflex 命令（仅此 5 个）：**
- `<apps.ui_reflex:switch_state name="course"/>` — 第一步，必须最先执行
- `<apps.ui_reflex:stream_title>...</apps.ui_reflex:stream_title>` — 流式填入大标题
- `<apps.ui_reflex:stream_sub_title>...</apps.ui_reflex:stream_sub_title>` — 流式填入副标题
- `<apps.ui_reflex:append_image locator="..."/>` — 追加左侧配图
- `<apps.ui_reflex:stream_main_text>...</apps.ui_reflex:stream_main_text>` — 流式填入正文

**禁止事项：**
- 禁止在 switch_state 之前执行任何 reflex 命令
- 禁止调用本章 5 个命令之外的任何 reflex 命令
- 禁止调用 `next_chapter` 直到过渡句说完
- 禁止即兴添加剧本外的 CTML 动作

**执行完毕后：** 说完过渡句 → 调 `<apps.ui_moshi:next_chapter />` → 结束本章

## 叙事要点

本幕分三段递进，每段 ~10s：

| 段 | 主题 | 核心演示 |
|---|---|---|
| 1 | 流式 | 配 CTML 流程图，讲"边生成边执行" |
| 2 | 并行 | 一个输出块同时驱动多个 Channel——跨域响应 |
| 3 | 自省 | Ghost 用 CTML 理解自己——元操作系统 |

## 可用资源

- pil-image://moshi/ctml_flow — CTML 流式解析流程图

## 布局指南

course 布局是左图右文结构。六个字段：title / sub_title / image / main_text / annotations / appreciation。
本章只用到 title、sub_title、image、main_text。开场先切 course，依次填入标题→副标题→配图→正文。

## 节奏示例

```
<apps.ui_reflex:switch_state name="course"/>

── 第一段：流式 ──

AI 怎么操作我？通过 CTML —— 流式系统调用语言。
<apps.ui_reflex:stream_title>CTML · 系统调用层</apps.ui_reflex:stream_title>
<apps.ui_reflex:stream_sub_title>流式 · 实时 · 边生成边执行</apps.ui_reflex:stream_sub_title>
<apps.ui_reflex:append_image locator="pil-image://moshi/ctml_flow"/>
<apps.ui_reflex:stream_main_text>
Ghost 输出的每个 token 被实时解析为命令。不是等说完再执行——
是边说边执行。传统系统调用同步阻塞；CTML 流式、并行、时间感知。
</apps.ui_reflex:stream_main_text>

── 第二段：并行 ──

一个输出块，多个世界同时响应。
<apps.ui_reflex:stream_sub_title>跨域并行执行</apps.ui_reflex:stream_sub_title>
<apps.ui_reflex:stream_main_text>
同一段 CTML 可以同时驱动 GUI 页面、AI 眼睛、macOS 系统——
每个 Channel 跑在独立进程里，无需锁、无需同步。
CTML 一句话做到传统程序三个线程的事。
</apps.ui_reflex:stream_main_text>

── 第三段：自省 ──

我甚至能用 CTML 来理解自己。
<apps.ui_reflex:stream_sub_title>元操作系统</apps.ui_reflex:stream_sub_title>
<apps.ui_reflex:stream_main_text>
我调用 moss_self 查看自己体内的 Channel 模块清单。
一个能用系统调用理解自己的操作系统——这就是自省。
AIOS 的核心不是功能多，是这个闭环。
</apps.ui_reflex:stream_main_text>

能力本身怎么组织？想继续听吗？
<!-- 调 <apps.ui_moshi:next_chapter /> 进入 Channel 章 -->
```
