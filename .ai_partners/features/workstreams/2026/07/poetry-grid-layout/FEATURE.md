---
created: 2026-07-02
depends:
- moshi
description: 诗文网格卡片布局 — 四/九宫格逐句填卡，浮层图/视频先居中再缩入格子，章节间卡片飞出转场。纯 CSS 动效，无 Canvas/JS。
milestone: null
priority: P2
status: in-progress
status_note: v2 布局完成（bounds-guard 修复渲染错误方块，章首清空策略替代章尾清空，body z-index=70 不再被 overlay 遮挡，字体 40px，四宫格 gap=36px 更舒展）。剧本三章完成（全视频素材，12 个 chX_Y.webm 逐句填格，配乐 serenity/enchanted/tense）。set_transition 移除。待端到端测试。
title: Poetry Grid Layout — 诗文网格卡片布局
updated: '2026-07-02T23:59'
---

# Poetry Grid Layout

> Use `moss features set-status poetry-grid-layout <status> -m "note"` to update state.

## Motivation

现有布局体系覆盖了多种叙事模式——`peach_blossom_stage` 的环境驱动连续舞台、
`living_document` 的线性手稿、`courtroom` 的交互式庭审——但缺少一种**网格分镜**式的
诗文展演布局。

核心体验：一首诗被逐句"吟出"，每句配一个场景图/视频（浮层先居中亮相，再缩入网格格子），
格子逐个填满屏幕。章节之间卡片飞出转场。像精心剪辑的诗文纪录片——有开场、有铺陈、有转场。

与 `古诗演示`（急板）的区别：急板用 `peach_blossom_stage` 引擎做快节奏单舞台炫技；
本布局是**新引擎**，核心机制是**网格逐格填充 + 浮层→格子动画**，纯 CSS 实现，复杂度远低于
peach_blossom_stage。

## Design Index

- 布局实现：`framework/layouts/poetry_grid.py`（✅ v2 已完成，~400行）
- 注册配置：`config.show_moshi.yaml:18`（⚠️ 行已写入但被注释，需手动激活）
- 上游 moshi 导演：`.moss_ws/apps/ui/moshi/main.py`（章节推进，布局只做转场动效）
- 同类布局参考：`peach_blossom_stage.py`（bg_video 始终渲染+opacity切换模式已采纳）
- Demo 原型：`framework/layouts/poetry_grid_demo.html`（桃花源记三章，图片+视频混排，用于验证视觉效果）
- 剧本：`.moss_ws/assets/moshi_courses/桃花源记-四宫格/`（.meta.md 已创建，三章待补全）

## Key Decisions

### 1. 章节切换由 moshi 管理，布局只管转场动效

Moshi 的 `next_chapter` 命令推进章节，context_messages 推送剧本内容给 Ghost。
布局不管理章节状态，只在 `transition` 字段被设为 `"next"` 时触发卡片飞出+黑幕动画。
Ghost 在转场黑暗期 clear 所有列表，准备下一章内容。

### 2. 浮层与格子数据源分离（v2 架构决策）

v1 设计用同一个列表（`overlay_images`）同时驱动浮层和格子——`:last-child` CSS
选择器控制浮层显隐，`overlay_images[i]` 直接映射到格子 #i 的配图。问题：浮层亮相和
格子填卡**同时发生**，无法做出"先亮相、再飞入"的时序差。

v2 拆分为独立字段：
- **浮层**：`active_overlay_image` / `active_overlay_video`（单张，非列表）
- **格子**：`card_images` / `card_videos`（列表，按索引对应 `lines`）

Ghost 操作节奏（每句两步）：
```
set_active_overlay_image locator="scene.png"   # 浮层居中淡入
# Ghost 等待 ~1.5s（LLM 自然延迟）
clear_active_overlay_image                     # 浮层消失
append_card_images locator="scene.png"         # 图落入格子 i
stream_lines "床前明月光，"                     # 文字墨迹浮现
```

浮层消失 + 格子卡 cardEnter 动画的时序重叠形成"飞入"错觉。不需要 JS。

### 3. 四宫格 / 九宫格

| 宫格 | 布局 | 适用 |
|------|------|------|
| 4 (2×2) | 绝句 4 句，每句一卡 |
| 9 (3×3) | 律诗 8 句 + 1 空，或填满 9 句 |

Grid size 由 `grid_size` 字段控制（`"4"` 或 `"9"`），默认 `"9"`。
格子填入顺序：左→右，上→下。

### 4. 视觉风格

| style | 背景色 | 卡片底色 | 文字色 | 适用 |
|-------|--------|---------|--------|------|
| `ink` | `#e8e0d0` | `#f5f0e8` | `#2c1810` | 古典诗词 |
| `warm` | `#ede4d2` | `#faf6f0` | `#3d2b1f` | 田园思乡 |
| `dark` | `#0d0d0d` | `#1a1a1a` | `#e0d8c8` | 边塞羁旅 |
| `fresh` | `#dce8dc` | `#f0f4f0` | `#1a2f1a` | 山水写景 |

### 5. 纯 CSS 动效策略

不引入 Canvas 粒子系统、不引入 JS bridge（与 peach_blossom_stage 的本质区别）。
所有动画用 CSS `@keyframes`：
- 浮层入场：`overlay-enter`（scale 0.8→1, opacity 0→1, 0.6s）
- 格子入场：`card-enter`（scale 0.7→1, translateY 30px→0, opacity 0→1, 0.5s）
- 格子文字：`ink-reveal`（blur 3px→0, translateY 14px→0, 0.8s，复用 living_document）
- 浮层→格子交叉淡化：`overlay-to-card`（overlay: opacity 1→0 scale 1→0.6; card-img: opacity 0→1 scale 1→1）
- 章节转场卡片飞出：`card-exit-*`（四方向飞出，rotate ±5deg）
- 章节转场黑幕：`transition-curtain`（opacity 0→1→0，0.8s）

### 6. State 字段（v2：13 个字段）

```
# 章节级
title: str                              → set / stream / clear
chapter_image: Image.Image | None       → set / clear   🆕 splash → badge
show_badge: str = ""                    → set / clear   🆕 "true"=缩略动画
style: str = "ink"                      → set / clear

# 背景
background_image: Image.Image | None    → set / clear
background_video: VideoLocator          → set / clear   (始终渲染+opacity切换)

# 浮层（单张，中央亮相）                  🔄 v2: 从 list 改为单张
active_overlay_image: Image.Image|None  → set / clear
active_overlay_video: VideoLocator      → set / clear

# 格子（列表，按索引对应）                🔄 v2: 与 overlay 分离
card_images: list[Image.Image]          → append / pop / clear
card_videos: list[VideoLocator]         → append / pop / clear
lines: list[str]                        → stream / pop / clear

# 字幕 / 转场                           🔄 v2: subtitle 移除
body: str                               → set / stream / clear  (屏幕中下 24px)
transition: str = ""                    → set / clear  ("next" 触发转场)
```

### 8. 章节开场：Splash → Badge 流（v2 新增）

每章开始时，章节图+标题在屏幕中央亮相（`splashEnter` animation），
然后缩到左上角成为 badge（`splashToBadge` animation）。纯 CSS 驱动，
通过 `show_badge` 字段触发。

CSS 动画链：
- `.poetry-root:not(.has-badge) .poetry-splash-img` — 居中 splashEnter (0.8s)
- `.poetry-root.has-badge .poetry-splash-img` — 缩到 80×80, top:24/left:32 (0.7s)
- `.poetry-root.has-badge .poetry-splash` — 动画结束后 opacity→0
- `.poetry-root.has-badge .poetry-badge` — 延迟 0.5s 后 opacity→1

Ghost 控制时序：`set_chapter_image` → 等待 → `set_show_badge "true"`。
不依赖 JS 回调，LLM 自然生成延迟即可。

### 9. 每张格子卡的内部结构

```
┌──────────────┐
│  [场景图/视频] │  ← 圆角 8px，object-fit: cover，占卡片 65% 高度
│  底部渐变遮罩  │  ← linear-gradient(transparent, rgba(bg, 0.8))
│  疑是地上霜。  │  ← 大字衬线体，居中偏下，占卡片 35% 高度
└──────────────┘
   border-radius: 12px
   box-shadow: 0 4px 24px rgba(0,0,0,0.3)
```

视频卡：autoplay muted loop。

## Implementation Notes

### 已完成（2026-07-02 Session）

- [x] **poetry_grid.py v2**（~400行）— overlay/card 数据源分离、splash→badge、body 字幕层
- [x] **_card() bounds-guard** — `length() > idx` 卫语句防止空列表越界导致渲染错误方块
- [x] **章首清空策略** — 清空从章尾移到章首，避免章尾残留（章名+overlay）
- [x] **CSS 调优** — overlay `78vw×72vh`、body `z-index:70` + `font-size:40px`、grid `gap:36px` + `max-width:420px`
- [x] **Demo HTML 原型** (`poetry_grid_demo.html`)
- [x] **config 已激活** (`config.show_moshi.yaml:18`)
- [x] **三章剧本完成** (`桃花源记-四宫格/`) — 全视频素材（12 个 chX_Y.webm），配乐 serenity/enchanted/tense
- [x] **set_transition 移除** — 章尾直接 `next_chapter`，章首 clear_all

### 待完成

- [ ] **端到端测试**：启动 moshi + reflex，完整跑完三章
- [ ] **九宫格 (3×3)**：`grid_size` 字段 + CSS grid-template 动态切换（暂缓）

### Ghost 操作序列（每章模板 — 当前版本）

```
# 章首（Ch2+ 先清空上一章）
clear_lines / clear_card_videos / clear_active_overlay_video / set_body "" / clear_chapter_image / set_show_badge ""
set_style "ink"
set_title "缘溪逢林"
set_chapter_image locator="pil-image://workspace-assets/stream.png"
set_show_badge "true"

# 每句（×4）— 三步，顺序即节奏
set_active_overlay_video locator="local-webm://workspace-assets/ch1_1-武陵人捕鱼.webm"
set_body t="武陵人捕鱼为业"
# 念诗文（视觉已领先）
clear_active_overlay_video
append_card_videos locator="local-webm://workspace-assets/ch1_1-武陵人捕鱼.webm"
stream_lines chunks__>武陵人捕鱼为业

# 章末
next_chapter
```