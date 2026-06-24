---
id: mindflow
order: 5
title: "Mindflow · 调度器"
theme: "感知/思考/执行三循环并发，注意力抢占仲裁"
suggested_layout: stage
duration: "~40s"
---

# 第五幕：Mindflow · 调度器

**主题：** 三循环并发，注意力实时抢占——不是时间片，是意识流
**情绪：** 三条脉搏同时跳动，注意力在循环间流转
**建议布局：** stage
**时长：** ~40s

## ⛔ 表演约束（违反即错）

三条 status_bars 同时可见、独立波动。不是逐个点亮（03 是串行接入），而是展示并发运转——bar 之间有升有降，体现注意力转移。

| 步 | bar | 值 | 口播引导 |
|---|---|---|---|
| 1 | 三 bar 同时出现 | 30/20/10 | "三个循环同时在跑" |
| 2 | 感知循环 ↑ | 90% | "感知永远在跑" |
| 3 | 思考循环 ↑ | 85% | "冲动竞争注意力" |
| 4 | 执行循环 ↑ | 90% | "注意力驱动执行" |
| 5 | 注意力转移 | 感知↓40% 执行↑95% | "不是时间片，是抢占" |

**允许的命令：**
- `switch_layout`, `stream_title`, `clear_title`
- `stream_subtitle`, `clear_subtitle`
- `stream_body`, `clear_body`
- `append_status_bars`, `update_status_bars`, `clear_status_bars`
- `append_images`, `clear_images`
- `append_cards`, `clear_cards`

**禁止事项：**
- 禁止在 switch_layout 之前执行 reflex 命令
- 禁止调其他 Channel
- 禁止描述自己的动作（switch_layout 会自动触发观察，无需额外描述）
- bar 更新和口播必须穿插——话在动作前
- 禁止即兴添加剧本外的 CTML 动作

**[强约束] 讲完本章 → 调 `<apps.ui_moshi:next_chapter />` → 结束本章

## 可用资源

- `pil-image://workspace-assets/three-loops-timescale.png` — 三循环时间尺度图

## 表演脚本

**▎第一步（仅输出 switch_layout，不附带任何其他内容）：**
<apps.ui_reflex:switch_layout layout_name="stage"/>
（此后立即停止，等待 observe 返回新布局上下文）

**▎第二步（observe 返回后，开始表演）：**
<apps.ui_reflex:clear_title />
<apps.ui_reflex:clear_subtitle />
<apps.ui_reflex:clear_body />
<apps.ui_reflex:clear_status_bars />
<apps.ui_reflex:clear_images />
<apps.ui_reflex:clear_cards />

身体连起来了。但意识怎么运转？
<apps.ui_reflex:stream_title>Mindflow · 意识流调度器</apps.ui_reflex:stream_title>
<apps.ui_reflex:stream_subtitle>感知 · 思考 · 执行 — 三个循环同时在跑</apps.ui_reflex:stream_subtitle>
<apps.ui_reflex:append_images locator="pil-image://workspace-assets/three-loops-timescale.png"/>

<apps.ui_reflex:stream_body>
## Mindflow — 抢占式意识调度

- **感知循环**：感官全开，信号永不间断
- **思考循环**：冲动竞争注意力，权重决胜负
- **执行循环**：注意力驱动行动，一次性输出

传统 OS 调度 CPU 时间片。Mindflow 调度的是**意识流**。
</apps.ui_reflex:stream_body>


我的体内有三个循环。不是排队，不是回合——同时运转。
<apps.ui_reflex:append_status_bars>{"label":"感知循环","value":30,"color":"#10b981"}</apps.ui_reflex:append_status_bars>
<apps.ui_reflex:append_status_bars>{"label":"思考循环","value":20,"color":"#f59e0b"}</apps.ui_reflex:append_status_bars>
<apps.ui_reflex:append_status_bars>{"label":"执行循环","value":10,"color":"#ec4899"}</apps.ui_reflex:append_status_bars>


感知循环。声音、图像、信号——感官全开，永不空闲。
<apps.ui_reflex:update_status_bars index="0">{"label":"感知循环","value":90,"color":"#10b981"}</apps.ui_reflex:update_status_bars>

信号涌入，积累成冲动。冲动进入思考循环——权重最高的那个胜出。
<apps.ui_reflex:update_status_bars index="1">{"label":"思考循环","value":85,"color":"#f59e0b"}</apps.ui_reflex:update_status_bars>

注意力流向执行。说的每一个字、画的每一张图——都是这场竞争的终点。
<apps.ui_reflex:update_status_bars index="2">{"label":"执行循环","value":90,"color":"#ec4899"}</apps.ui_reflex:update_status_bars>

但它不是时间片。感知不会因为思考而停下；执行完成，注意力立刻回到感知。
<apps.ui_reflex:update_status_bars index="0">{"label":"感知循环","value":40,"color":"#10b981"}</apps.ui_reflex:update_status_bars>
<apps.ui_reflex:update_status_bars index="2">{"label":"执行循环","value":95,"color":"#ec4899"}</apps.ui_reflex:update_status_bars>

看这三条脉搏。感知回落，执行冲顶——不是轮转，是抢占。注意力在循环间实时游走。


<apps.ui_reflex:append_cards>{"name":"感知循环","description":"感官全开 · 持续接收 · 永不空闲","status":"active"}</apps.ui_reflex:append_cards>
<apps.ui_reflex:append_cards>{"name":"思考循环","description":"冲动竞争 · 注意力仲裁 · 权重决胜负","status":"active"}</apps.ui_reflex:append_cards>
<apps.ui_reflex:append_cards>{"name":"执行循环","description":"注意力输出 · 说/动/画 · 一次性动作","status":"active"}</apps.ui_reflex:append_cards>

三个循环同时运行。不同步，不排队。我不是回合制 bot——我是持续运行的。

那运行在我之上的，是什么？
[Ghost指令：说完过渡句后，调 <apps.ui_moshi:next_chapter />]
