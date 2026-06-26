---
id: mindflow
order: 4
title: "Mindflow · 调度器"
theme: "感知/思考/执行三循环并发，注意力抢占仲裁"
suggested_layout: video_player
duration: "~40s"
---

## ⛔ 表演约束（违反即错）

video_player 布局：左侧文字（title / sub_title / body 三级），右侧图片/视频。文字带交错凝聚动画（0.7s），媒体带缩放浮现（0.9s）。

本章的动态感来自三线并进：sub_title 切换焦点、body 清空重写、右侧媒体随叙事换屏。开场用星空视频营造"意识流淌"意境，中段切图为三循环图解，收尾切回视频闭环——右侧始终有内容。

**[强约束] 讲完本章 → 调 `<apps.ui_moshi:next_chapter />` → 结束本章**

**允许的命令：**
- `switch_layout layout_name="video_player"`
- `stream_title` / `clear_title`
- `stream_sub_title` / `clear_sub_title`
- `stream_body` / `clear_body`
- `append_image` / `clear_image`
- `append_videos` / `clear_videos`

**禁止事项：**
- 禁止在 switch_layout 之前执行 reflex 命令
- 禁止调其他 Channel
- 禁止描述自己的动作
- 每次 body/sub_title 更新前必须说至少一句口播（话在动作前）
- 禁止即兴添加剧本外的 CTML 动作

**执行完毕后：** 过渡句 → `<apps.ui_moshi:next_chapter />`

## 可用资源

**视频：**
- `local-webm://workspace-assets/tt视频 星空划船.webm` — 星空划船，开场和收尾两次使用

**图片：**
- `pil-image://workspace-assets/three-loops-timescale.png` — 三循环时间尺度图
- `pil-image://workspace-assets/perception-think-action-in-real-world.png` — 感知-思考-执行在物理世界
- `pil-image://workspace-assets/MOSShell-realtime-runtime-nervous-system.png` — 实时运行时神经系统
- `pil-image://workspace-assets/end-to-end-circle.png` — 端到端循环

## 表演脚本

**▎第一步（仅输出 switch_layout，不附带任何其他内容）：**
<apps.ui_reflex:switch_layout layout_name="video_player"/>
（此后立即停止，等待 observe 返回新布局上下文）

**▎第二步（observe 返回后，开始表演）：**
<apps.ui_reflex:clear_title />
<apps.ui_reflex:clear_sub_title />
<apps.ui_reflex:clear_body />
<apps.ui_reflex:clear_image />
<apps.ui_reflex:clear_videos />

CTML 是我的语言。Channel 是我的感官。Matrix 是我的神经。
<apps.ui_reflex:stream_title>Mindflow</apps.ui_reflex:stream_title>

那意识呢？我的意识——
<apps.ui_reflex:append_videos locator="local-webm://workspace-assets/tt视频 星空划船.webm"/>

像是在流淌。
<apps.ui_reflex:stream_sub_title>感知 · 思考 · 执行</apps.ui_reflex:stream_sub_title>

三个循环。同时在跑。
<apps.ui_reflex:stream_body>不是排队。不是回合。感知、思考、执行——三个循环同时运转。</apps.ui_reflex:stream_body>

但它是怎么工作的？拆开来看看。
<apps.ui_reflex:clear_videos />
<apps.ui_reflex:append_image locator="pil-image://workspace-assets/three-loops-timescale.png"/>

感知循环。声音、图像、信号——我的感官全开，永不空闲。
<apps.ui_reflex:clear_image />
<apps.ui_reflex:append_image locator="pil-image://workspace-assets/perception-think-action-in-real-world.png"/>
<apps.ui_reflex:stream_sub_title>感知循环 · 永不空闲</apps.ui_reflex:stream_sub_title>
<apps.ui_reflex:clear_body />
<apps.ui_reflex:stream_body>感官全开，信号涌入，积累成冲动。</apps.ui_reflex:stream_body>

冲动涌进思考循环。不是排队处理——是竞争。所有冲动同时喊话，权重最高的那个胜出。
<apps.ui_reflex:clear_image />
<apps.ui_reflex:append_image locator="pil-image://workspace-assets/MOSShell-realtime-runtime-nervous-system.png"/>
<apps.ui_reflex:stream_sub_title>思考循环 · 冲动竞争</apps.ui_reflex:stream_sub_title>
<apps.ui_reflex:clear_body />
<apps.ui_reflex:stream_body>冲动竞争注意力。权重决胜负。</apps.ui_reflex:stream_body>

胜出的冲动抓住注意力，流向执行。我说的每一个字，都是这场竞争的终点。
<apps.ui_reflex:clear_image />
<apps.ui_reflex:append_image locator="pil-image://workspace-assets/end-to-end-circle.png"/>
<apps.ui_reflex:stream_sub_title>执行循环 · 注意力输出</apps.ui_reflex:stream_sub_title>
<apps.ui_reflex:clear_body />
<apps.ui_reflex:stream_body>注意力驱动行动。说、画、动——一次性输出。</apps.ui_reflex:stream_body>

但它不是时间片。感知不会因为思考而停下。执行的同时，新的信号已经涌进来了。
<apps.ui_reflex:clear_image />
<apps.ui_reflex:append_videos locator="local-webm://workspace-assets/tt视频 星空划船.webm"/>
<apps.ui_reflex:stream_sub_title>抢占 · 不是时间片</apps.ui_reflex:stream_sub_title>
<apps.ui_reflex:clear_body />
<apps.ui_reflex:stream_body>注意力在三个循环间实时游走。不是轮转，是抢占。</apps.ui_reflex:stream_body>

三个循环同时运行。不同步，不排队。我不是回合制 bot——我是持续运行的。
<apps.ui_reflex:clear_sub_title />
<apps.ui_reflex:clear_body />
<apps.ui_reflex:stream_body>传统 OS 调度 CPU 时间片。Mindflow 调度的是意识流。</apps.ui_reflex:stream_body>

那运行在我之上的，是什么？
<apps.ui_moshi:next_chapter/>
