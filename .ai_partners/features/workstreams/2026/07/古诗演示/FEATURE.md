---
created: 2026-07-01
depends:
- peach-blossom-spring
description: 古诗/古文的"急板"式纯视觉炫技演示——屏幕不停歇、四层同时动，与教学式演示分道。
milestone: null
priority: P2
status: in-progress
status_note: Ch1+Ch2 19拍完成。落英双视频峰值、三箭硬切+光隙、body字体3rem加粗。零新素材。set_background_video待查。待Ch3
title: 古诗演示
updated: '2026-07-01'
---

# 古诗演示

> Use `moss features set-status 古诗演示 <status> -m "note"` to update state.

## Motivation

`peach-blossom-spring` 走的是**教学式**演示：老师讲解、留白、每 ~20 秒一次视觉变化，
以口播为主、动效为辅。人类想要**另一种形态**——**纯视觉炫技**：屏幕永不静止、
每 2-3 字就切一次画面、几乎只念原文、目不暇接。

这不是把桃花源记重做一遍，而是开一条**可复用于任意古诗/古文**的演示范式：
用同一套 `peach_blossom_stage` 引擎，把它当作"视觉乐器"演奏，追求沉浸冲击而非知识传递。
桃花源记是第一个试验体（课程 `桃花源记急板`），验证后可推广到其它诗文。

与 `peach-blossom-spring` 的关系：共用引擎与素材（背景/浮层/音频），但**表演纪律相反**
（快 vs 慢、炫技 vs 讲解）。两者是同一舞台的两种演奏法。

## Design Index

- 课程剧本：`.moss_ws/assets/moshi_courses/桃花源记急板/`（`.meta.md` + `01-缘溪逢林.md`）
- 浮层视频素材清单：`.moss_ws/apps/ui/moshi/peach_blossom_presto_video_materials.md`
- 复用引擎：`.moss_ws/apps/ui/reflex/framework/layouts/peach_blossom_stage.py`、`components/peach_assets.py`
- 上游教学式演示：`peach-blossom-spring` FEATURE.md（素材清单、命令体系的源头）

## Key Decisions

**1. 命名"急板"** — 借音乐术语（presto，最快速度）标记这条范式，与教学版区分。
课程目录 `桃花源记急板`，不覆盖原版 `桃花源记`。

**2. 密度即表现力，做成动态曲线** — 拒绝两个均匀极端（永远单图 / 永远堆满）。
按情绪起伏：缘溪行**留白**（多为单层、敢留黑）→ 桃花林**堆满**（峰值背景视频+2 浮层视频+1 浮层图同屏）。
稀疏↔繁密的反差本身就是叙事。这是人类第二轮反馈的核心（"有时单图有时多图，把素材用起来"）。

**3. 四层同时动，背景频繁切换** — 背景不是"设一次就不管"：静图 `stream.png/forest.png`
⇄ 背景视频 `stream_flow/petals_falling` **反复切**，静↔动本身即动效。背景图/背景视频/
浮层图/浮层视频四层各有节奏。这是人类第三轮反馈（"背景也可以频繁换，让屏幕动起来"）。

**4. 浮层视频 = 半常驻动态锚点** — 激活此前从未用过的 `append_overlay_videos`。
`ov_*` 视频停留数拍作锚点（摇橹舟、临风桃枝），静图在它周围快切进出（"图讲完就切，
浮层视频停留久一些"）。新出 4 条素材：`ov_boat_rowing`/`ov_branch_wind`/`ov_petals_swirl`/`ov_stream_rush`。

**5. 隧道转场当剪辑点** — `set_transition constrict`（原教学版整部只用 1 次）在急板里
当**场景硬切**用。样章在"忽逢"处一次：溪水世界连锚点一起被吸走，桃林随隧道张开涌现，
氛围 serene→enchanted 当场重构粒子系统。

**6. 只念原文** — 台词几乎等于原文，讲解退到"被打断时才展开"（interaction.model 从
teacher 改为 performer）。知识锚点保留但不主动讲。

## Implementation Notes

**set_body 必须用属性形式**（关键坑，见记忆 `reflex-set-command-body-arg-bug`）：
`<set_body t="缘溪" />` — 即时**替换**、无需 clear、无流式延迟，正是快剪主力。
文本**禁含双引号**（中文逗号句号安全）。body 形式 `<set_body>文本</set_body>` 会报
`args ()` TypeError（生成器里 `set_command(t)` 参数无 `__` 后缀，当属性解析）。

**stream_body 是追加语义**（见记忆 `courtroom-stream-clear-pattern`）：用前必须
`clear_body`，否则字符拼接错乱。全章只在结尾"原文回收"用一次做慢呼吸。

**浮层卡片尺寸**：`.peach-overlay-item` CSS `max-width:35% max-height:50%`，无 object-fit，
按原始比例缩放。1080p 舞台上限盒 = 672×540（≈5:4）。浮层视频素材定为 **1:1（1080×1080）**
默认、天然竖的用 **4:5（1080×1350）**；别超 5:4 横否则整张缩小。透明底 alpha webm（VP9），
Chromium webview 原生支持；出不了 alpha 退纯黑底。

**背景 image/video 是两个独立字段**：切换时显式 clear 另一个（clear_background_video 后
set_background_image，反之亦然），避免两层叠加。

**隧道涌现用静图更稳**：样章保守用 `forest.png` 图从隧道口涌现（复用第四章验证过的
`village.png` 模式），未用背景视频穿隧道——待验证视频穿隧道是否同样顺。

## 当前进度（2026-07-01）

- ✅ 课程骨架 `桃花源记急板`：`.meta.md`（急板表演纪律 + 语法铁律 + 命令表），chapters: 2
- ✅ 样章 `01-缘溪逢林.md`：前半段（晋太元中→欲穷其林），11 拍
  - 密度曲线：缘溪行留白（单图/单锚点）→ 隧道硬切 → 桃花林逐拍蓄力 → 落英爆发
  - 浮层视频：`ov_boat_rowing`（武陵→缘溪 2 拍锚点）+ `ov_branch_wind` + `ov_petals_swirl`（落英处双视频同屏、不叠静图）
  - 浮层图快切：overlay_wuling → forest_panorama → stream_pink
  - 结尾 next_chapter 自动推进，前接"渔人甚异之，复前行——"口播避免 Ch2 回退
  - 夹岸数百步：无素材，仅 clear_transition + set_body，隧道后留一口气
- ✅ 样章 `02-穷其林.md`：后半段（欲穷其林→仿佛若有光），8 拍，零新素材
  - 转场方案：不用 constrict，改用氛围 enchanted→tense + 背景 forest.png→cave.png + 音频 enchanted→tense 三箭硬切
  - 激活 peach-slit 光隙系统（tense 氛围自动浮现，CSS point-breathe 3s 呼吸循环）
  - `cave_light.webm` 复用为 overlay video（绕过背景视频 bug）
  - 密度曲线：从繁华渐收→山壁聚焦→一隙微光
- ✅ 浮层视频素材清单 + AI 生成提示词（含尺寸规格），人类已产出 4 条 `ov_*.webm` 并注册进 jsonl
- ✅ `.peach-body-text` 字体加大加粗：3rem / 700 / #fff / 三层金白光晕（全局，影响教学版）
- ❌ `set_background_video` 背景视频无法显示（overlay 视频正常），根因待查
- ⏳ 待续：第三章（便舍船→从口入→初极狭→豁然开朗，压迫→爆炸）