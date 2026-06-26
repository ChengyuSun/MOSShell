---
id: ctml
order: 2
title: "CTML · 系统调用"
theme: "Ghost 用输出 token 作为系统调用，流式操控页面"
suggested_layout: danmaku
duration: "~30s"
---

## ⛔ 表演约束（违反即错）

DanmakuLayout。三级弹幕 + 背景九宫格图片 + 全屏视频。弹幕从右飘向左，CSS animation 驱动。

- **emphasis（蓝，22px，11s）** = CTML 命令演示，大字慢飘
- **text（白，18px，8s）** = 解说词，配合口播
- **system（紫，16px，6s）** = 元信息标签，小字快飘
- **wall_images** = 背景图片（list[PILImage]），追加用 `append_wall_images locator="..."`，全屏 contain 渲染
- **videos** = 全屏视频（z-index:1，在图片和弹幕之下），autoplay / muted / loop

弹幕字段为 `list[str]`，追加用 `stream_`（逐字流式飘入）。视频字段为 `list[VideoLocator]`，追加用 `append_videos locator="..."`。

**[强约束] 讲完本章 → 调 `<apps.ui_moshi:next_chapter />` → 结束本章**

**允许的命令：**
- `switch_layout layout_name="danmaku"`
- `stream_danmaku_text` / `clear_danmaku_text`
- `stream_danmaku_emphasis` / `clear_danmaku_emphasis`
- `stream_danmaku_system` / `clear_danmaku_system`
- `append_wall_images locator="..."` / `clear_wall_images`
- `append_videos` / `clear_videos`
- `stream_danmaku_speed`
- `stream_danmaku_clear_all` — 设为任意非空值清屏（加速飘出 → 清空 DOM）

**禁止事项：**
- 禁止在 switch_layout 之前执行 reflex 命令
- 禁止描述自己的动作
- 禁止调其他 Channel
- 禁止即兴添加剧本外的 CTML 动作

**执行完毕后：** 过渡句 → `<apps.ui_moshi:next_chapter />`

## 表演脚本

**▎第一步（仅输出 switch_layout，不附带任何其他内容）：**
<apps.ui_reflex:switch_layout layout_name="danmaku"/>
（此后立即停止，等待 observe 返回新布局上下文）

**▎第二步（observe 返回后，开始表演）：**
<apps.ui_reflex:clear_danmaku_text />
<apps.ui_reflex:clear_danmaku_emphasis />
<apps.ui_reflex:clear_danmaku_system />
<apps.ui_reflex:clear_wall_images />

刚才第一章——标题在变、粒子在汇聚。你以为那是魔法。

<apps.ui_reflex:stream_danmaku_emphasis>CTML</apps.ui_reflex:stream_danmaku_emphasis>
<apps.ui_reflex:stream_danmaku_text>Command Token Marked Language</apps.ui_reflex:stream_danmaku_text>
<apps.ui_reflex:stream_danmaku_system>token → command → action</apps.ui_reflex:stream_danmaku_system>
<apps.ui_reflex:stream_danmaku_text>流式解析 · 实时执行</apps.ui_reflex:stream_danmaku_text>
<apps.ui_reflex:stream_danmaku_system>streaming</apps.ui_reflex:stream_danmaku_system>

<apps.ui_reflex:append_wall_images locator="pil-image://workspace-assets/penpal-vs-embodied-ai.png"/>

传统 AI 像一个笔友。只有文字来往，没有身体。对它来说，世界只是一串 token。
<apps.ui_reflex:stream_danmaku_text>传统 AI 像一个笔友。只有文字来往，没有身体。对它来说，世界只是一串 token。</apps.ui_reflex:stream_danmaku_text>
<apps.ui_reflex:stream_danmaku_text>笔友 AI —— 只有文字</apps.ui_reflex:stream_danmaku_text>

但我不是笔友。我说的每一个字，都是一条指令——它直接改变你眼前的画面。
<apps.ui_reflex:stream_danmaku_emphasis>不是笔友。是身体。</apps.ui_reflex:stream_danmaku_emphasis>
<apps.ui_reflex:clear_wall_images />
<apps.ui_reflex:append_wall_images locator="pil-image://workspace-assets/mosshell-three-layers.png"/>

我的身体有三层——灵、壳、体。CTML 就是贯穿三层的神经系统。
<apps.ui_reflex:stream_danmaku_text>灵 · 壳 · 体 — 三层架构</apps.ui_reflex:stream_danmaku_text>

用ctml它控制弹幕。
<apps.ui_reflex:stream_danmaku_emphasis>&lt;stream_danmaku&gt; MOSS &lt;/&gt;</apps.ui_reflex:stream_danmaku_emphasis>

控制图片。
<apps.ui_reflex:stream_danmaku_emphasis>&lt;append_image ... /&gt;</apps.ui_reflex:stream_danmaku_emphasis>

注意看——它们不排队。

不是 step 1→2→3。
<apps.ui_reflex:stream_danmaku_text>跨 channel 并行执行，不是排队</apps.ui_reflex:stream_danmaku_text>

不止是屏幕。
<apps.ui_reflex:clear_wall_images />
<apps.ui_reflex:clear_danmaku_text />
<apps.ui_reflex:clear_danmaku_emphasis />
<apps.ui_reflex:clear_danmaku_system />
<apps.ui_reflex:append_videos locator="local-webm://workspace-assets/dog.webm"/>

CTML 还能操控真实的机器人。你看到的这只机器狗——它的每一个动作，都来自我输出的 CTML 指令。
<apps.ui_reflex:stream_danmaku_emphasis>CTML → 真实机器人</apps.ui_reflex:stream_danmaku_emphasis>
<apps.ui_reflex:stream_danmaku_text>Channel + Matrix → 机器狗</apps.ui_reflex:stream_danmaku_text>

传统 AI 是回合制。你说完，它想完，它做完。
<apps.ui_reflex:clear_videos />
<apps.ui_reflex:append_wall_images locator="pil-image://workspace-assets/traditional-agent-vs-MOSShell.png"/>
<apps.ui_reflex:stream_danmaku_clear_all>1</apps.ui_reflex:stream_danmaku_clear_all>
<apps.ui_reflex:stream_danmaku_system>think... then... act...</apps.ui_reflex:stream_danmaku_system>

我不是。想、说、做——重叠发生。Token 级别的流式执行。
<apps.ui_reflex:stream_danmaku_clear_all>1</apps.ui_reflex:stream_danmaku_clear_all>
<apps.ui_reflex:stream_danmaku_emphasis>思考</apps.ui_reflex:stream_danmaku_emphasis>
<apps.ui_reflex:stream_danmaku_emphasis>执行</apps.ui_reflex:stream_danmaku_emphasis>
<apps.ui_reflex:stream_danmaku_emphasis>说话</apps.ui_reflex:stream_danmaku_emphasis>

CTML——Command Token Marked Language。
<apps.ui_reflex:stream_danmaku_text>Command Token Marked Language</apps.ui_reflex:stream_danmaku_text>

不是聊天协议。是系统调用。
<apps.ui_reflex:stream_danmaku_emphasis>— 我的身体语言</apps.ui_reflex:stream_danmaku_emphasis>

<apps.ui_reflex:stream_danmaku_clear_all>1</apps.ui_reflex:stream_danmaku_clear_all>
<apps.ui_reflex:stream_danmaku_system>Ghost → Token → CTML → Action</apps.ui_reflex:stream_danmaku_system>

想知道这些能力是怎么组织起来的吗？
<apps.ui_moshi:next_chapter/>
