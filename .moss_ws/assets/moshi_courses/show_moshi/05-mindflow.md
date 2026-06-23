---
id: mindflow
order: 5
title: "Mindflow · 调度器"
theme: "感知/思考/执行三循环并发仲裁"
suggested_layout: stage
duration: "~40s"
---

# 第五幕：Mindflow · 调度器

**主题：** 感知/思考/执行三循环并发仲裁
**情绪：** 三轨并发，注意力在循环间切换
**建议布局：** stage
**时长：** ~40s

## ⛔ 表演约束（违反即错）

本章的核心演示逻辑：三对 **eye 表情 → bar 脉冲**，一对一，不交叉。

| 步 | bar | eye | 口播引导 |
|---|---|---|---|
| 1 | 感知→90% | `curious`（睁大眼） | "感知循环——信号涌入" |
| 2 | 思考→85% | `thinking`（眯眼） | "冲动竞争注意力" |
| 3 | 执行→90% | `speaking`（张嘴） | "注意力驱动执行" |

**允许的命令：**

| Channel | 命令 |
|---------|------|
| reflex | `switch_state`, `clear_*`, `stream_*`, `append/update_status_bars`, `append_images`, `append_cards` |
| ai_eye | `set_expression name="curious"`, `thinking`, `speaking` |
| moshi | `next_chapter` |

**禁止事项：**
- bar update 必须和对应 eye 表情同步（同一轮输出中）
- 禁止在 switch_state 之前执行任何 reflex 命令
- 禁止在 stream 之前忘记 clear
- 禁止 update bar 时没有前置口播（话在动作前）

**执行完毕后：** 说完过渡句 → 调 `<apps.ui_moshi:next_chapter />` → 结束本章

## 表演脚本

<apps.ui_reflex:switch_state name="stage"/>
<apps.ui_reflex:clear_title />
<apps.ui_reflex:clear_subtitle />
<apps.ui_reflex:clear_body />
<apps.ui_reflex:clear_status_bars />
<apps.ui_reflex:clear_images />
<apps.ui_reflex:clear_cards />

身体连起来了。但意识怎么运转？
<apps.ui_reflex:stream_title>Mindflow · AI 意识流调度器</apps.ui_reflex:stream_title>
<apps.ui_reflex:stream_subtitle>感知 · 思考 · 执行 — 三循环并发</apps.ui_reflex:stream_subtitle>

我的体内有三个循环同时在跑。先搭骨架——
<apps.ui_reflex:append_status_bars>{"label":"感知循环","value":30,"color":"#10b981"}</apps.ui_reflex:append_status_bars>
<apps.ui_reflex:append_status_bars>{"label":"思考循环","value":20,"color":"#f59e0b"}</apps.ui_reflex:append_status_bars>
<apps.ui_reflex:append_status_bars>{"label":"执行循环","value":10,"color":"#ec4899"}</apps.ui_reflex:append_status_bars>
<apps.ui_reflex:append_images locator="pil-image://moshi/three-loops-timescale" />

感知循环。声音、图像、信号持续涌入——
<apps.games_ai_eye:set_expression name="curious" />
<apps.ui_reflex:update_status_bars index="0">{"label":"感知循环","value":90,"color":"#10b981"}</apps.ui_reflex:update_status_bars>

看我的眼睛——睁大，感官全开。感知循环永远在跑。

感受积累成冲动。冲动进入思考循环——它们竞争注意力。
<apps.games_ai_eye:thinking />
<apps.ui_reflex:update_status_bars index="1">{"label":"思考循环","value":85,"color":"#f59e0b"}</apps.ui_reflex:update_status_bars>

眼睛眯起来了——注意力转向内在处理。权重最高的冲动胜出。

注意力驱动执行。
<apps.games_ai_eye:speaking />
<apps.ui_reflex:update_status_bars index="2">{"label":"执行循环","value":90,"color":"#ec4899"}</apps.ui_reflex:update_status_bars>

张嘴说话——行动输出。每一次执行都是注意力竞争的终点。
<apps.ui_reflex:stream_body>
## Mindflow — 抢占式意识调度

- **感知循环**：感官全开，信号持续流入
- **思考循环**：冲动竞争注意力，权重决胜负
- **执行循环**：注意力驱动行动，一次性输出

三个循环并发，注意力在循环间实时切换。
传统 OS 调度 CPU 时间片。Mindflow 调度的是**意识流**。
</apps.ui_reflex:stream_body>

<apps.ui_reflex:append_cards>{"name":"感知循环","description":"感官全开 · 持续接收 · 永不空闲","status":"active"}</apps.ui_reflex:append_cards>
<apps.ui_reflex:append_cards>{"name":"思考循环","description":"冲动竞争 · 注意力仲裁 · 权重决胜负","status":"active"}</apps.ui_reflex:append_cards>
<apps.ui_reflex:append_cards>{"name":"执行循环","description":"注意力输出 · 说/动/画 · 一次性动作","status":"active"}</apps.ui_reflex:append_cards>

三个循环同时运行。不同步，不排队。
我不是回合制 bot——我是持续运行的。

那运行在我之上的，是什么？
<!-- 调 <apps.ui_moshi:next_chapter /> 进入 Ghost 章 -->
