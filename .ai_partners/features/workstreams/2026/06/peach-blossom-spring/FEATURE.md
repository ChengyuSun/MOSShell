---
created: 2026-06-29
depends:
- moshi
description: 基于 moshi 导演体系的第三门课程。以《桃花源记》为叙事蓝本，验证连续动画引擎 与交互式讲解在流式演示中的可行性——粒子系统叙景、光灵角色动画、五层统一舞台、
  字段级命令自动生成、用户可随时打断提问或要求回退。单一 peach_blossom_stage 布局 承载全部 6 章，不切换布局。
milestone: null
priority: P1
status: in-progress
status_note: Phase 1-3 ✅。Phase 4 进行中：背景图可见 ✅、隧道过渡 v3 ✅、tense 氛围重做 ✅。Canvas 动画验证通过 ✅。bug修复：SYNC_SCRIPT f-string转义+gesture桥接 ✅。6章剧本重构 ✅。音频5轨入库 ✅。CTML前缀全量修正 ✅。剧本v2 ✅。素材清单 ✅。22张新浮层素材入库 ✅。剧本↔JSONL交叉校验 ✅。.meta.md YAML frontmatter修复 ✅。连续讲完修复 ✅（rhythm/continuity重写+恢复纪律+去blockquote）。背景图章首展示 ✅（6章bg移至锚点1，Ch04除外）。浮层双图 ✅（5章多图并排，删除"粒子/两张图"等元描述）。HUD放大 ✅（标题0.95→1.3rem，进度点6→10px）。⬜ 前端dispatch-is-not-a-function（.web缓存已清，待重启验证）。⬜ SIGIL_SCRIPT Reflex DOM输出。⬜ 光缝删除+替代动效（待人类确认方案）。⬜ 端到端集成测试。⬜ 交互打断/jump_chapter测试。
title: 桃花源记 — 连续动画引擎驱动的流式叙事演示
updated: '2026-07-01T15:30'
---

# 桃花源记

桃花源记是 moshi 导演体系的第三门课程——以陶渊明《桃花源记》为叙事蓝本，
验证**连续动画引擎**在流式演示中的可行性。

与 moss自我介绍（单向叙事）和极限审判（双向对抗）不同，桃花源记的核心命题是：
**演示全程不停歇——粒子持续演化、光灵自主运动、场景情绪连续流动**。

---

## Motivation

当前 moshi 的"一句一动"模式是离散的：Ghost 输出 → CTML 命令 → UI 更新 → 停顿。
用户希望 UI 是"活的"——即使 Ghost 没有说话，舞台上也有持续的微动效。

桃花源记天生适合验证这一点：
- 它是**空间-情绪旅程**，每个节点有清晰的视觉锚点
- "初极狭→豁然开朗"的过渡是完美的动画素材
- 花瓣、溪流、山洞、屋舍、炊烟——全部可以用粒子系统演绎

验证目标：
1. **自主动画循环**：Canvas requestAnimationFrame 持续驱动粒子场 + 光灵
2. **语义级命令**：Ghost 说"展示桃花林"，布局自动编排动画序列
3. **情绪联动**：粒子颜色/密度/速度 + 光灵颜色/脉动 + 环境光晕 + 基调色调，
   全部随章节情绪联动
4. **过渡动画**：粒子溶解+重构替代硬切换，"初极狭→豁然开朗"三段式展开
5. **交互打断**：用户可随时打断提问，Ghost 用知识锚点回答后继续；
   用户可要求回退到任意章节，Ghost 通过 jump_chapter 跳转重播

---

## Design Index

- 本文件 — 唯一设计文档
- 依赖 feature：
  - `.ai_partners/features/workstreams/2026/06/moshi/FEATURE.md`
- 参考实现：
  - `layouts/cohesion_field.py` — Canvas 粒子场 IIFE，粒子凝聚/消散
  - `layouts/brain.py` — conic-gradient 圆环、点阵纹理
  - `layouts/courtroom.py` — 光魂多情绪 class、径向光晕联动
  - `layouts/danmaku.py` — CSS @keyframes 漂移渲染
- 事件系统：`framework/events.py`
- 命令生成器：`framework/runtime/event_generator.py`
- 布局注册：`moss_in_reflex/config.show_moshi.yaml`
- moshi 课程存储：`.moss_ws/apps/ui/moshi/src/course_storage.py`
- 课程资产：`.moss_ws/assets/moshi_courses/桃花源记/`

---

## Key Decisions

### 1. 单一布局承载全部 6 章

不像 moss自我介绍 每章切换布局，桃花源记用一个 `peach_blossom_stage` 布局
贯穿始终。章节切换靠粒子状态、情绪基调、光灵位置的变化——不是切 DOM 树。

理由：桃花源记是连续的旅程，切布局打破沉浸感。情绪弧线本身就是章节标记。

### 2. 渔人灯灵 — 提灯前行的抽象光体

不搞具象人物。用 Canvas 绘制的抽象光灵：

```
         ·  ·  ·  ·        ← 花瓣粒子尾迹（拖尾消散）
           ✦  ✦  ✦         
             ◈              ← 灯笼核心光体（暖黄渐变）
           ✦  ✦  ✦         
         ·  ·  ·  ·        
```

- **移动**：光体在空间中 gliding，ease-in-out 1-2s，尾迹跟随
- **说话**：光体脉动呼吸（scale 微振 + 亮度波动），频率跟语速联动（监听 logos 流）
- **手势**：光体向目标方向延伸一束光线，像"提灯照亮前方"
- **情绪联动**：
  - 宁静（缘溪行）→ 暖黄，4s 缓慢呼吸，细长尾迹
  - 惊艳（桃花林）→ 粉暖，2s 中速呼吸，花瓣尾迹
  - 紧张（山洞）→ 暗琥珀，1.5s 快速呼吸，尾迹收短
  - 释放（豁然）→ 金白，爆炸呼吸后平稳
  - 恬静（桃花源）→ 暖金，5s 缓慢呼吸，宽尾迹
  - 怅然（归来）→ 灰暖，6s 极慢呼吸，尾迹消散

### 3. 五层统一舞台

```
┌──────────────────────────────────────────────┐
│  Layer 5: HUD                                │  z-50
│  章节指示器 · 进度环（溪流→桃林→山洞→豁然→村落→归来）│
├──────────────────────────────────────────────┤
│  Layer 4: 内容面板                             │  z-40
│  背景层（图片/视频）+ 浮层（图片/视频）            │
│  不区分内容类型，只区分展现方式——背景在光灵后，     │
│  浮层在光灵前。从边缘滑入/滑出                    │
├──────────────────────────────────────────────┤
│  Layer 3: 光灵层（角色）                        │  z-30
│  渔人灯灵本体 + 光束手势                        │
│  Canvas 绘制，requestAnimationFrame 驱动        │
├──────────────────────────────────────────────┤
│  Layer 2: 粒子环境                              │  z-20
│  持续演化的粒子场，情绪驱动颜色/密度/速度          │
│  三种粒子态：水流粒子 / 花瓣粒子 / 金色喷涌        │
├──────────────────────────────────────────────┤
│  Layer 1: 空间基底                              │  z-10
│  径向渐变光晕 + 点阵纹理                        │
│  暗空间基调，情绪驱动颜色变化                     │
└──────────────────────────────────────────────┘
```

各层同时运行，互不阻塞。Layer 1/2 有自主动画循环，不依赖 Ghost 逐帧指挥。

### 4. 双轨动画驱动

| 轨 | 驱动方式 | 负责 |
|---|---|---|
| **自主动画轨** | Canvas `requestAnimationFrame` + CSS `@keyframes` | 粒子场演化、光灵 idle 呼吸、环境光晕呼吸、花瓣飘落 |
| **事件响应轨** | Ghost CTML 命令 → Reflex state 更新 | 光灵移动/情绪切换、内容卡片进出、过渡动画触发 |

自主动画轨**永不停止**——即使 Ghost 没有任何输出，舞台上也有持续的微动效。

### 5. 交互打断 — 老师而非表演者

Ghost 是讲解《桃花源记》的老师，不是照本宣科的表演者。Ghost Runtime
本身就是对话循环（Ghost 输出 → 用户输入 → Ghost 回应），打断在架构层面
已天然支持。需要改造的不是基础设施，是 Ghost 的行为指令。

**段落节奏**：
- Ghost 每轮输出一个叙事段落（3-5 句口播 + 1-3 个 CTML 动作），段内一气呵成
- 段尾自然收束后停在当前章节，不自动推进下一章
- 用户沉默 → Ghost 继续下一段；用户说话 → Ghost 回答问题后继续

**被打断时**：
- 停下来回答。用每章的「知识锚点」中的内容回答
- 回答后说"我们继续"，从当前章节自然接续
- 不道歉、不解释"我刚才在做什么"——直接继续

**被要求回退时**：
- "回到初极狭" → `<apps.ui_moshi:jump_chapter id="cave" />`，从头重播第三章
- "回到上一章" → `jump_chapter(id=...)`
- 回退后直接重新讲，不说"我们刚才讲过..."

**结束当前章时**：
- 如果 Ghost 认为本章已讲解充分，调用 `<apps.ui_moshi:next_chapter />`
- 不需要问"要继续吗"——用过渡句自然引入下一章

**为什么不需要 Segment**：

用户最初考虑过在章内细分 segment 作为导航粒度。讨论后决定不需要——
原因很简单：桃花源记全程一个布局，章内就是一组连续叙事段落。用户要求回退时，
回退到章首重新讲就足够。章是自然的"场景单元"（缘溪行/桃林/山洞/豁然/村落/归来），
章内再细分对体验无明显增益。`jump_chapter` 已完美支持章节级导航，
不需要 `mark_segment` 等额外基础设施。砍掉 segment 概念后，moshi 导演端零改动。

**交互模式放在哪：.meta.md，不是 MODE.md**：

MODE.md 是模式级的——所有 show_moshi 下的课程共享同一份 MODE.md。
但三种课程的交互模型完全不同：

| 课程 | 交互模型 |
|---|---|
| moss自我介绍 | 纯表演，单向输出 |
| 极限审判 | 法官质询，双向对抗 |
| 桃花源记 | 教师讲解，打断/提问/回退 |

把桃花源记的交互模式写进 MODE.md 会污染 moss自我介绍 和极限审判。
正确的位置是课程的 `.meta.md`。它已经有 `performance` 字段定义课程级
表演纪律，交互模式是其自然延伸：

```yaml
# .moss_ws/assets/moshi_courses/桃花源记/.meta.md

interaction:
  model: "teacher"               # teacher | performer | judge
  interruption: "allow"
  replay: "allow"
  rules:
    - "被提问时引用每章的「知识锚点」回答"
    - "回答后说'我们继续'，从当前章节自然接续"
    - "不道歉、不解释'刚才在做什么'"
    - "被要求回退时 jump_chapter 到对应章节，直接重讲"
    - "禁止说'刚才被打断了'、'让我演示一下'"
```

**数据流**：`.meta.md` 的完整 YAML frontmatter 已经在 moshi 的
`context_messages` Layer 2（课程概况）中推送给 Ghost，零代码改动。
MODE.md 不改，moshi `main.py` 不改——数据已经在管道里了。

### 6. 自由发挥型剧本 — 知识锚点 + 口播锚点

与 moss自我介绍 的逐字 CTML 脚本不同，桃花源记的剧本不写死台词。
每章文件包含两个层次：

**知识锚点**（Ghost 回答提问的知识卡片）：
```markdown
| 锚点 | 解释 |
| 初极狭，才通人 | 山洞极窄，仅容一人侧身挤入。隐喻探索需要勇气 |
| 豁然开朗 | 由极度狭窄骤然转为极度开阔的视觉与心理反差 |
```

**口播锚点**（Ghost 自由展开的叙事要点，非照念台词）：
```markdown
> 渔人发现山脚下有个小口，隐约透着光。他侧身钻了进去。
> 起初极窄——走了几十步，前方突然宽广明亮。
```

Ghost 读口播锚点后用自己的话即兴展开，自主穿插 CTML 动作。
剧本告诉 Ghost "要讲什么"和"视觉效果是什么"——"怎么讲"由 Ghost 自己决定。

与 moss自我介绍 剧本的对比：

| | moss自我介绍 | 桃花源记 |
|---|---|---|
| 台词 | 逐句写死，禁止即兴 | 口播锚点，自由展开 |
| CTML 时机 | 脚本精确指定 | 口播锚点提示，Ghost 自主穿插 |
| 被提问 | 不处理（纯表演） | 查「知识锚点」回答 |
| 行为模型 | 演员，不等人 | 老师，等人、回应、回退 |

### 7. 命令哲学 — 字段级起步，语义级可选

桃花源记与 moshi 在命令粒度上的关系：

| 维度 | moshi 其他课程 | 桃花源记 |
|---|---|---|
| 粒度 | 字段级：`stream_title` / `clear_title` | 同样是字段级，但字段本身是语义的：`set_atmosphere` 而非 `set_color` |
| 动画 | 手动 CSS class | 布局自动编排——设 `atmosphere` 触发全部层联动 |
| 资源 | 字段直接塞 locator | 复用 Image.Image / VideoLocator 自动转换管道 |
| 转场 | `switch_layout` 硬切 | `set_transition` 粒子溶解+重构 |
| 情绪 | 无 | `set_atmosphere` → 粒子 + 光灵 + 光晕全部联动 |

**起步方案：直接用字段级命令。** 11 个字段中 10 个由 `event_generator.build()` 自动生成命令，
Ghost 只需学会字段名即可操控舞台。语义别名（如 `reveal_scene` 包装多个字段操作）
可在 Phase 4 按需添加。

示例命令：
```
<set_atmosphere>enchanted</set_atmosphere>                  ← 环境变粉暖，粒子切换花瓣
<set_sigil_position>forest_edge</set_sigil_position>        ← 光灵移动到桃林边缘
<set_sigil_gesture>forward</set_sigil_gesture>              ← 光灵向前方发出光束
<set_background_image>pil-image://peach/forest</set_background_image>  ← 背景层展示桃林全景
<set_overlay_image>pil-image://peach/calligraphy</set_overlay_image>   ← 浮层展示书法贴图
<set_transition>constrict</set_transition>                  ← 触发三段式"豁然开朗"
<clear_overlay_image />                                     ← 浮层图片退场
```

Ghost 不需要关心"先清哪个字段"——布局侧负责编排进场/退场动画序列。

### 8. "初极狭→豁然开朗"三段式过渡（整场演示的最高潮）

```
阶段1: 收紧 (0→0.8s)
  ├── 画面四周暗角向内挤压（CSS clip-path: inset 或 box-shadow）
  ├── 光灵缩小、变暗、脉动加速（紧张）
  └── 粒子向中心收缩

阶段2: 临界 (0.8→1.2s)
  ├── 完全黑暗，只剩光灵核心微光
  └── 字幕显示"复行数十步，豁然开朗"

阶段3: 爆炸展开 (1.2→2.5s)
  ├── 暗角从中心向外炸开（reverse clip-path + radial glow expansion）
  ├── 金色粒子从中心向外喷涌（比常规粒子更大、更亮）
  ├── 光灵放大、变亮、颜色从暗琥珀 → 暖金
  ├── 环境光晕从纯黑 → 金色径向渐变
  └── 远景山水/屋舍随金色粒子落地渐显
```

### 9. 三种粒子态

| 粒子态 | 场景 | 颜色 | 密度 | 速度 | 行为 |
|---|---|---|---|---|---|
| 水流粒子 | 01 缘溪行、06 归来 | 青白→灰蓝 | 稀疏 (60) | 缓慢 | 水平流动，微波动 |
| 花瓣粒子 | 02 桃花林、05 桃花源 | 粉白→桃红 | 中等 (120) | 中等 | 飘落+轻微螺旋 |
| 金色喷涌 | 04 豁然开朗 | 金→暖白 | 密集 (180) | 快速 | 中心向外爆炸，衰减回归 |

粒子引擎复用 `cohesion_field.py` 的 Canvas IIFE 模式，通过全局变量
`window.__PEACH_PARTICLE_CONFIG__` 暴露配置接口，Reflex state 变更时
更新配置，Canvas 动画循环读取配置。

### 10. Canvas + Reflex 桥接

Canvas 通过 `<script>` IIFE 注入，完全独立于 Reflex 渲染循环。
与 React/Reflex 通过全局变量通信：

```
Reflex state 变更
  → moss_listener → QUEUE → _apply_event_to_state
  → state._mark_dirty()
  → 渲染时 <script> 读取 window.__PEACH_CONFIG__ 更新 Canvas 行为

Canvas animation loop (requestAnimationFrame)
  → 每帧读取 window.__PEACH_CONFIG__
  → 独立驱动粒子 + 光灵
  → 不触发 Reflex 重渲染
```

桥接变量：
- `__PEACH_PARTICLE_CONFIG__` — 粒子类型/颜色/密度/速度
- `__PEACH_SIGIL_CONFIG__` — 光灵位置/情绪/大小/光束目标
- `__PEACH_ATMOSPHERE__` — 环境光晕颜色/暗角程度

### 11. 暗空间光绘风格

视觉基调：深色背景 + 发光轮廓 + 粒子叙景。
与 `cohesion_field` 的暗空间风格一脉相承，但粒子系统从抽象几何升级为叙事粒子
（水流、花瓣、金涌）。

不选水墨风（开发成本高、粒子模拟墨迹扩散难度大）或剪影风（表现力有限）。
暗空间光绘与现有代码最高度兼容，效果最华丽。

### 12. 音频播放 — Ghost 通过 CTML 控制

音频播放已由 `apps/tools/audio_player` 实现（基于 macOS afplay，支持 mp3/wav/aac/m4a/aiff）。
Ghost 在课程中通过 CTML 控制背景音乐：

```
<apps.tools_audio_player:play locator="local-audio://workspace-assets/bgm-ch01" />
<apps.tools_audio_player:stop />
```

音频不纳入布局 ComponentState——它是独立的 app 进程，Ghost 直接调用。
布局零改动。

### 13. 素材风格与来源

素材（山水画/书法贴图/视频）由人类工程师在确认整体视觉风格后统一收集。
风格要求：统一、古典、适合暗空间光绘呈现。避免多源混搭导致的风格割裂。

### 14. body 正文区 — 区域设计需避免与浮层冲突

`body: str` 用于流式展示原文关键句。文字区域设计需注意：
- 浮层图片从边缘滑入/滑出，body 文字不能与浮层重叠
- body 在无浮层时可居中大字展示，有浮层时自动收窄或移至底部
- 具体布局方案在 Phase 3（内容面板）中与浮层动画一起敲定

### 15. 章节间背景过渡 — CSS Crossfade

背景图片在章间通过 CSS `opacity` crossfade（~0.8s）过渡，不硬切。
旧背景淡出同时新背景淡入。实现方式：渲染时保持两张 img 标签，
切换时新旧 opacity 交叉渐变。

Ch03→Ch04（山洞→豁然）是例外——走三段式爆炸展开（Decision 8），
不走普通 crossfade。

### 16. 粒子-背景时序错位 — 不同时全强度出现

**核心原则**：粒子与背景图不同时全强度出现。一方主导时，另一方退让。
视觉焦点在两者之间交替转移，形成"呼吸"节奏。

**为什么**：背景图（具象、高信息密度）和粒子（抽象、高动态性）同时
全强度呈现时互相争夺视觉带宽——粒子在图上看像视频滤镜，图被粒子罩住
失去细节。时序错位让两者各有独占的视觉时刻。

**实现**：不需要新字段。Ghost 通过 `set_atmosphere`（切粒子态）和
`set_background_image`/`clear_background_image` 的时序控制节奏。
入场/退场自带 CSS opacity transition。

**每章节奏编排**：

```
Ch01 缘溪行
  粒子先行(~3s) → 背景从暗空间渐入(~1.5s) → 低密度粒子+背景主导
  水流粒子先出现 → 溪流山水画浮现 → 粒子退让为"溪水的微光"

Ch02 桃花林
  花瓣报信(~2s)    → 背景从花瓣雨中浮现(~2s) → 背景主导+稀疏花瓣
  花瓣在暗底上醒目  → 桃花林长卷透出             → 花瓣锦上添花

Ch03 山洞
  背景先行(~1s)    → 背景消退+粒子接管(~2s)    → 纯粒子+光灵+暗角
  山洞画面先出现    → 图退、暗角深、粒子收束     → 无背景，进入"压紧"态

Ch04 豁然
  临界纯黑(~0.5s)  → 三段式爆炸(0→2.5s)        → 背景从金涌中浮现(~2s)
  无背景无粒子      → 纯金涌粒子爆炸              → 桃花源全景渐显

Ch05 桃花源
  背景全程主导      → 浮层成为主角               → 浮层退出，回归全景
  粒子极低密度      → 细节图滑入讲解              → 偶尔几片花瓣飘过

Ch06 归来
  背景先褪(~3s)    → 粒子主导(~3s)              → 最终消散
  全景 fade out     → 灰蓝水流在暗空间漂移减少    → 光灵熄灭
```

**Ghost 脚本层面**：同一章内的时序控制完全由 Ghost 的 CTML 输出节奏
自然实现——先出 `set_atmosphere` 切粒子，口播几句后出
`set_background_image` 加载图片。不需要额外的"时序"命令。

---

## 章节结构

| 章 | 标题 | 情绪 | 粒子态 | 视觉节奏 | 知识锚点（示例） |
|---|---|---|---|---|---|
| 01 | 缘溪行 | serene 宁静 | 水流 | 粒子先行→背景渐入→低密度并存 | 武陵人、缘溪行、忘路之远近 |
| 02 | 桃花林 | enchanted 惊艳 | 花瓣 | 花瓣报信→背景从花雨浮现→背景主导 | 夹岸数百步、中无杂树、芳草鲜美 |
| 03 | 山洞 | tense 紧张 | 水流收束 | 背景先行→背景消退→纯粒子+暗角 | 山有小口、仿佛若有光、初极狭才通人 |
| 04 | 豁然 | released 释放 | 金涌 | 纯黑→三段式爆炸→背景从金涌浮现 | 豁然开朗、土地平旷、屋舍俨然 |
| 05 | 桃花源 | tranquil 恬静 | 花瓣（低密） | 背景主导→浮层讲解→回归全景 | 阡陌交通、鸡犬相闻、黄发垂髫 |
| 06 | 归来 | wistful 怅然 | 水流（衰减） | 背景先褪→粒子主导→消散熄灭 | 便扶向路、处处志之、不复得路 |

每章的「知识锚点」是 Ghost 回答用户提问的知识库。口播锚点（叙事要点）
写在每章剧本文件中，Ghost 据此即兴展开。

---

## ComponentState

```python
from PIL import Image
from framework.events import VideoLocator

class PeachBlossomState(rx.ComponentState):
    # 氛围
    atmosphere: str = "serene"          # serene | enchanted | tense | released | tranquil | wistful

    # 光灵
    sigil_position: str = "center"      # 位置标识，或具体坐标
    sigil_gesture: str = ""             # forward | right | left | "" (idle)

    # 内容面板 — 不区分内容类型，只区分展现方式
    background_image: Image.Image = None     # 背景层图片，在光灵后
    background_video: VideoLocator = ""      # 背景层视频，在光灵后
    overlay_images: list[Image.Image] = []   # 浮层图片列表，在光灵前，支持多张
    overlay_videos: list[VideoLocator] = []  # 浮层视频列表，在光灵前

    # 正文 — 流式大字原文/关键句，Ghost 讲到哪显示到哪
    body: str = ""

    # 过渡
    transition: str = ""                # constrict | expand | dissolve | ""

    # 字幕
    subtitles: list[str] = []

    # HUD
    chapter_title: str = ""
    chapter_id: str = ""                 # 章节标识（溪流/桃林/山洞/豁然/村落/归来），驱动进度环
```

### 字段 → 命令映射

| 字段 | 类型 | Ghost 使用的命令 | 命令来源 |
|---|---|---|---|
| `atmosphere` | str | `set_atmosphere` `clear_atmosphere` | 自动（str） |
| `sigil_position` | str | `set_sigil_position` | 自动（str） |
| `sigil_gesture` | str | `set_sigil_gesture` `clear_sigil_gesture` | 自动（str） |
| `background_image` | Image.Image | `set_background_image` `clear_background_image` | 自动（Image.Image） |
| `background_video` | VideoLocator | `set_background_video` `clear_background_video` | 自动（VideoLocator） |
| `overlay_images` | list[Image.Image] | `append_overlay_images` `pop_overlay_images` `clear_overlay_images` | 自动（list[Image.Image]） |
| `overlay_videos` | list[VideoLocator] | `append_overlay_videos` `pop_overlay_videos` `clear_overlay_videos` | 自动（list[VideoLocator]） |
| `body` | str | `stream_body` `clear_body` `set_body` | 自动（str） |
| `transition` | str | `set_transition` `clear_transition` | 自动（str） |
| `subtitles` | list[str] | `stream_subtitles` `clear_subtitles` | 自动（list[str]） |
| `chapter_title` | str | `set_chapter_title` `clear_chapter_title` | 自动（str） |
| `chapter_id` | str | `set_chapter_id` `clear_chapter_id` | 自动（str） |

Image.Image 和 VideoLocator 复用现有 `event_generator` 的命令生成逻辑——
locator→资源转换在命令函数内部完成。13 字段全为 str/list/Image.Image/VideoLocator，
全部由 `event_generator.build()` 自动生成命令，零手动注册。
`overlay_images` 从单张改为列表——Ghost 一次可展示多张浮层，append/pop/clear 全自动。

---

## moshi 导演端：零改动

课程导航（load_course / next_chapter / jump_chapter）原样复用。
所有 UI 操作由 Ghost 通过字段级 reflex 命令直接控制，13/13 字段全自动生成。

moshi 的 `next_chapter` 推进章节，Ghost 在章节首自行调用 `set_chapter_title` +
`set_atmosphere` 设定新章节的视觉基调。

---

## Implementation Plan

### Phase 1: Canvas 粒子引擎 + 光灵 + 五层舞台骨架 ✅

1. ✅ `peach_blossom_stage` 布局骨架 — 五层 CSS 结构 + 13 字段 ComponentState
2. ✅ 环境光晕层（z-10）+ 氛围统调层（z-15），`atmosphere` 驱动 CSS transition 0.6s
3. ✅ Canvas IIFE 粒子场 — 三态（水流/花瓣/金涌），`__PEACH_PARTICLE_CONFIG__` 驱动
4. ✅ Canvas IIFE 光灵 — idle 呼吸 + 情绪联动 + 拖尾粒子，`__PEACH_SIGIL_CONFIG__` 驱动
5. ✅ 暗角效果（CSS）— `atmosphere tense` 时四角深度挤压
6. ✅ 注册 `config.show_moshi.yaml`
7. ✅ Reflex ↔ Canvas 桥接 — #peach-store → MutationObserver → window.__PEACH_*
8. ✅ 独立测试页 `peach_test.html` — 6 mood + 5 position 实时切换验证

**产出文件**：
- `framework/layouts/peach_blossom_stage.py` (161 行)
- `framework/components/peach_assets.py` (MOOD 配置 + JS 脚本 + CSS)
- `framework/components/peach_test.html` (独立测试页)

### Phase 2: 光灵运动 + 过渡动画

7. ✅ 光灵 gliding 动画 — `sigil_position` → 5 个预设坐标，Canvas JS lerp ~1.2s
8. ✅ 光束手势 — `sigil_gesture` 驱动，锥形光束 @keyframes lerp
9. ✅ 光缝效果 — z-17，仅 tense 时可见，垂直暖光缝 + `::after` 亮线 + `@keyframes slit-breathe` 4s 呼吸。与 vignette tense 暗角配合形成"洞穴深处透微光"。
10. ✅ 三段式"豁然开朗"动画 — constrict→临界→expand (2.5s)。CSS 暗幕 @keyframes（暗角收紧→全黑→金色展开）+ 粒子三阶段（向心收缩→隐灭→金涌喷发）+ 光灵三阶段（缩小加速→仅核微光→easeOutCubic 膨胀亮金）。由 `set_transition constrict` 触发。
11. ✅ background_image CSS opacity crossfade — img 不再被 rx.cond 挂载/卸载，改为始终渲染 + inline style opacity 切换，0.8s 过渡

**验证**：光灵在舞台上移动，发射手势。`set_transition constrict` 触发三段式展开。
`set_background_image` 和 `clear_background_image` 带 crossfade 过渡。

### Phase 3: 内容面板 + 文字 ✅

12. ✅ 背景层图片渲染 — `<img>` 始终在 DOM，inline style opacity 0/1 切换，带 CSS crossfade 0.8s。event_generator 新增 Union 类型解包（`types.UnionType`→提取非 None 类型），`background_image: Image.Image | None` 正确生成 set/clear 命令
13. ✅ 背景层视频渲染 — `<video>` 同 z-0，`playing=True, controls=False, muted=True, loop=True`，与背景图共用 opacity crossfade 0.8s
14. ✅ 浮层图片列表 — `<img>` 在 z-40 光灵前方，append 时从边缘滑入，pop/clear 时滑出，支持多张排列
15. ✅ 浮层视频列表 — `<video>` 同 z-40，复用 `peach-overlay-item` 动画 class
16. ✅ body 正文区 — 流式大字在 z-45。compact 条件扩展为 `overlay_images | overlay_videos`，视频浮层存在时同步收窄
17. ✅ HUD 层 — 章节标题 + 6 段进度环（溪流→桃林→山洞→豁然→村落→归来）。`chapter_id: str`（如 "桃林"）语义化驱动，通过 `_AFTER` 先后关系推导 "done" 态。13/13 字段全自动生成命令，零 `chapter_index: int` 手动注册

**验证**：背景/浮层从边缘滑入滑出，crossfade 平滑。body 文字与浮层不冲突。
进度环随 chapter_id 推进。

### Phase 4: 课程剧本 + 端到端 + 音频

18. ✅ `.meta.md` — 全局表演纪律（"一句一动"铁律、章尾 next_chapter 铁律、音频铁律、禁止事项）+ 命令速查 + 音频资源表
19. ✅ 6 章剧本重构 — "一句一动"折中方案：
    - 保留知识锚点（Ghost 回答提问的知识库）
    - 口播锚点每句配 CTML 动作提示（非精确脚本，Ghost 仍有即兴空间）
    - 每章轻量「表演约束」：Ch01 强制 switch_layout 第一步、Ch04 高潮时序铁律（先音频→再过渡→说"豁然开朗"）、章尾强制 next_chapter（Ch06 除外）
    - 全部 CTML 命令使用完整前缀（`apps.ui_reflex:`/`apps.tools_audio_player:`/`apps.ui_moshi:`）
20. ✅ TEST_CTML.md — 6 章 CTML 剧本（7 图 + 章节推进），素材已注册 pil-image.jsonl
21. ✅ 音频 5 轨已入库 — serenity/enchanted/tense/release/tranquil
    - 发现 AI 生成的 .mp3 实为 AAC-in-MP4，afplay 按扩展名解码失败 → 改名 .m4a + 更新 JSONL 修复
    - locator 格式：`local-audio://workspace-assets/serenity.m4a`
22. ⬜ 素材替换 — 7 张占位图 + 5 轨音频待人类工程师替换正式素材
23. ⬜ 端到端集成 — Ghost + moshi + peach_blossom_stage，完整 6 章跑通（首次测试发现三个问题：不自动推进、大段文字、光灵不可见。前两个已通过剧本重构+约束修复，第三个调试中）
24. ⬜ 交互测试 — 验证打断提问（知识锚点回答后继续）、jump_chapter 回退重播

### Phase 4 首次端到端测试 — 2026-06-30 调试记录

TEST_CTML.md 已补全全部 7 张图片命令，素材全部注册入 pil-image JSONL 索引。
首次在完整 Ghost + moshi + peach_blossom_stage 环境中测试，发现以下问题：

**Bug 1 — 背景图片不渲染（根因：CSS z-index 遮挡）**

- 症状：`background_image` 在 state 中确认已加载（PIL Image 2732x1534），但前端不可见
- 排除项：图片加载/序列化正常（`overlay_images` 同路径能正常渲染）。CTML 命令解析正常
- 根因：`peach-scene`（z-0, `position:absolute;inset:0;background:#020202`）与 `peach-bg-img`（z-0）同 z-index。由于 `.peach-scene` 在 DOM 中先出现、且 `.peach-grade`（z-2）覆盖半透明色，背景图被遮挡
- 修复方向：提高背景图 z-index 至 z-0 之上（如 z-0.5），或调整 `peach-scene` 不使用纯黑背景覆盖全区域

**Bug 2 — 光灵 Canvas 无动画（根因：SYNC_SCRIPT 初始化竞态）**

- 症状：`#peach-sigil` Canvas 存在但无渲染内容
- 光灵完整逻辑：Canvas rAF 循环 → 每帧读取 `window.__PEACH_SIGIL_CONFIG__` → 三层径向渐变光体 + 拖尾粒子 + 光束手势。位置 lerp 平滑移动（~1.2s），呼吸脉动（scale 微振 + 亮度波动，频率由 `breathS` 控制），情绪联动（6 mood 各有独立 innerColor/outerColor/size/breathS/trailLen）
- 预期效果：暗空间中央可见暖色发光球体，缓慢呼吸脉动，被照射区域有锥形光束，身后拖尾粒子消散
- 根因：`SYNC_SCRIPT` 的 `sync()` 首次调用时，`data-atmosphere` 属性已初始化为 `"serene"`，但 `lastMood` 初始为 `""`，`mood!==lastMood` 为 true，会写入 config。但末尾检查 `if(!dirty&&pos===lastPos)return` —— 如果 mood 匹配失败（MOODS key 查找 `undefined`）则 dirty 保持 false 且提前 return，config 未写入
- 修复方向：首次运行时无条件写入 `window.__PEACH_*` 默认值，不依赖 diff 逻辑

**Bug 3 — 粒子 Canvas 无动画**

- 同根因：`window.__PEACH_PARTICLE_CONFIG__` 未被 SYNC_SCRIPT 写入
- 预期效果：根据 atmosphere 切换三种粒子态（水流水平漂移 / 花瓣飘落螺旋 / 金涌中心爆炸），持续 requestAnimationFrame 驱动

**Bug 4 — 豁然开朗过渡动效需重做**

- 当前实现：CSS `@keyframes transition-constrict` — 全屏暗幕从边缘向内压暗→全黑→金色展开（三段式 2.5s）。`peach-transition-constrict` class 挂到根 `rx.box` 触发 `.peach-transition-overlay` 的 animation
- 人类期望：不是暗幕从边缘压来，而是"远处有个亮光的小口，然后突然扩大，切换到新图片"——光缝从中心径向爆开，类似光圈快门/虹膜打开
- 修复方向：
  1. 重写 CSS transition：从中心小光点（`clip-path: circle(2%)` 或 `radial-gradient` 模拟）开始，ease-out 扩大到覆盖全屏（`circle(100%)`），扩开瞬间 crossfade 切换到 village.png
  2. 光灵配合：过渡期间光灵从暗琥珀 tiny core 膨胀为金白大光体
  3. 粒子配合：金色粒子从光点中心向外喷涌
  4. 不再需要 `peach-transition-overlay` 暗幕层，改用中心光点扩张 + 图片切换

### 2026-06-30 修复记录 (deepseek-v4-pro)

**Bug 1 修复 — bg-img 可见性 (verified ✅)**

根因分两层：
1. CSS z-index：`peach-bg-img` 原在 z-0，被 grade (z-2) / vignette (z-3) 遮挡。提升至 z-3 解决。
2. Reflex 渲染差异：`rx.foreach` 动态创建 `<img>`（overlay_images）正常，但静态 `rx.image(src=Var)` 在 src 从 None 变更到 PIL Image 时不更新 DOM。

修复：
- z-index 0→3（在 grade/vignette 之上，粒子 z-4 之下）
- 渲染模式从"始终在 DOM + opacity toggle"改为 `rx.cond` 条件渲染
- `rx.cond(cls.background_image != None, rx.image(...))` — 有数据时才创建元素
- CSS 新增 `@keyframes bg-fade-in` 0.8s 替代 opacity toggle

**Bug 2 & 3 修复 — Canvas 配置同步**

根因分两层：
1. `arguments.callee` 在 ES Module 严格模式下非法，SYNC_SCRIPT 静默死亡 → `window.__PEACH_*` 从未写入 → Canvas 脚本收不到配置 → MutationObserver 未建立 → atmosphere/transition 变更无法传播
2. 首次运行时 diff guard `if(!dirty&&pos===lastPos)return` 可能提前退出

修复：
- `arguments.callee` → 命名 IIFE `(function init(){...setTimeout(init,80)...})()` 严格模式兼容
- `firstRun` 标志 → 首次无条件写入默认值
- mood/pos 查找 fallback 到 `MOODS['serene']` / `POSITIONS['center']`

**Bug 4 修复 — "豁然开朗"过渡动画（三轮迭代）**

v1（clip-path circle 虹膜光圈）：黑色遮罩 + `clip-path: circle()` 洞口。问题——洞口内是遮罩自身的黑色，看不到白光。

v2（box-shadow 隧道壁 + 金色光源）：透明圆心 + 巨大黑色 box-shadow + 径向金光 + `repeating-conic-gradient` 旋转光纹。问题——(a) 中心暖金色不是白色，(b) 旋转 conic-gradient 像菊花而非时光隧道，(c) `animation: forwards` 导致 class 不变就无法重触发。

v3（当前版本）：
- 隧道壁：`position:fixed; top:45%; left:50%; border-radius:50%; background:transparent; box-shadow:0 0 0 150vmax rgba(0,0,0,0.95)` — 透明圆=洞口，box-shadow=隧道壁
- 隧道光源（z-5）：纯白中心 `rgba(255,255,255,1)` → 暖白过渡 `rgba(255,252,248,0.5)` → 透明。`transform:scale(0.3→2.5)` 从小到大扩散
- 同心光环（::before）：`repeating-radial-gradient` 同心环 + `transform:scale(0.25→3)` —— 环从内向外加速扩散，产生"时空穿梭"纵深感，**不旋转**
- 洞口边缘金色光晕环（::after）：`box-shadow:inset` 随洞口扩大渐隐
- 全部动画**不加 `forwards`**：结束后自动回到默认态 (opacity:0)，支持 Ghost 先 `clear_transition` 再 `set_transition` 重复触发
- 时间线 ~4s：0→1.2s 光点微扩 → 1.2→2.2s 加速靠近 → ~2.2s 临界 swap bg → 2.2→3.2s 爆开 → 3.2→4s 消散

**Bug 5 修复 — tense 氛围"远处光点"**

原设计：vignette 18%透明中心 + 垂直裂缝光 slit（`120px×70%` 竖条）

人类反馈：线条丑，应该是"远处的一个光点"配合洞口

修复：
- vignette.tense：透明中心从 18% 缩至 3%，暗区更快压深 (50%处 rgba(0,0,0,0.92))
- slit：从垂直裂缝 `120px×70%` 重做为圆形呼吸光点 `40px`，居中 `top:45%; left:50%`，`box-shadow` 多层柔光扩散，`@keyframes point-breathe` scale 1→1.4 脉动

**经验教训**

1. **Reflex 静态 `<img>` 的 src 更新**：`rx.image(src=state_var)` 在 src 从 None 变为 PIL Image 时不更新 DOM 属性。`rx.foreach` 动态创建的元素正常。处理可选图片的推荐模式：用 `rx.cond` 条件渲染，有数据时才创建 `<img>` 元素。

2. **`arguments.callee` 在 ES Module 中非法**：Reflex 前端构建为 ES Module，严格模式下 `arguments.callee` 抛 TypeError。所有重试逻辑必须使用命名函数表达式。

3. **CSS 动画可重复触发的条件**：使用 `forwards` 填充模式会导致动画结束后样式锁死在最后一帧，class 不变就无法重触发。去掉 `forwards` + 确保 Ghost 先 `clear` 再 `set`（class 的 remove→add 触发动画重启）。

4. **clip-path circle 洞口的视觉陷阱**：`clip-path` 剪裁的是元素自身——黑色遮罩的洞透出的还是黑色。要做"光点洞口"效果，正确做法是透明元素 + box-shadow 扩散（或 mask-image）。

5. **旋转 ≠ 速度感**：`conic-gradient` + `rotate` 产生的是旋转图案（菊花），不是速度感。`repeating-radial-gradient` + `scale` 产生的是从内向外扩散的环——这才是"穿梭"的纵深感。

6. **氛围设计的叙事对齐**：tense mood 的 vignette 透明中心大小直接决定了"远处光点有多远"——3% 是极远的小光点，18% 只是普通暗角。设计 mood 参数时需要代入叙事场景（"山有小口，仿佛若有光" → 极小光点）。

### 2026-06-30 修复记录 (deepseek-v4-pro, 第二轮) — Canvas 桥接修复

**Bug 6 — SYNC_SCRIPT f-string 转义错误导致整段 JS 被浏览器拒绝执行（verified ✅）**

- 症状：
  - `<set_atmosphere released/>`：CSS 光晕正确变色，粒子不变；光灵位置/手势无响应
  - 静态 HTML test page 正常 → Canvas 渲染逻辑无问题
  - Console：`window.__PEACH_PARTICLE_CONFIG__` 和 `window.__PEACH_SIGIL_CONFIG__` 均为 `undefined`
  - Console 红色报错：`Uncaught SyntaxError: Failed to execute 'appendChild' on 'Node': Unexpected token '{'`
- 根因：`peach_assets.py` SYNC_SCRIPT 是 Python f-string，POSITIONS 变量用了 4 层大括号 `{{{{...}}}}`，f-string 转义后产生 `{{...}}`（双层）而非 `{...}`（单层）。浏览器解析 `<script>` 时遇到 `var POSITIONS = {{...}}` → 语法错误，拒绝执行整个脚本标签 → `window.__PEACH_*__` 永不写入
- 为何 PARTICLE_SCRIPT/SIGIL_SCRIPT 仍能渲染：它们有独立的硬编码默认值，不依赖 `window.__PEACH_*__`。但仅使用默认值，无法响应 CTML 更新
- 为何 CSS 能变：CSS class 由 Reflex 直接管理，不走 SYNC_SCRIPT
- 修复：`{{{{...}}}}` → `{{...}}`（4层→2层），f-string 转义后正确产生单层 `{...}`
- 教训：
  7. **f-string 中的 JS 对象字面量**：`{{` 在 Python f-string 中产生一个字面 `{`。要生成 `var x = {a:1}`，Python 源码需写 `var x = {{a:1}}`。多加一层 `{{{{` 会产生 `{{`，导致 JS 语法错误
  8. **`window.__PEACH_*__` 为 `undefined` 意味 SYNC_SCRIPT 未执行**：直接搜 Console 报错，不需要猜 DOM/Reflex

**Bug 7 — 光束手势 CTML 无反应（verified ✅）**

- 症状：`set_sigil_gesture`/`clear_sigil_gesture` CTML 不产生光束
- 根因：
  1. `peach_blossom_stage.py` 的 `peach-store` div 缺少 `data_sigil_gesture` 属性 → 手势状态未传入 DOM
  2. SYNC_SCRIPT 未读取 `data-sigil-gesture` → `window.__peachSetGesture()` 从未被调用
- 修复：
  1. `peach_blossom_stage.py`：`peach-store` 新增 `data_sigil_gesture=cls.sigil_gesture`
  2. `peach_assets.py`：SYNC_SCRIPT 新增 gesture 读取 + `window.__peachSetGesture(!!gesture)` 调用 + MutationObserver 监听 `data-sigil-gesture`

---

## 改动文件清单

| 文件 | 改动 | 状态 |
|---|---|---|
| `layouts/peach_blossom_stage.py` | 新增布局 — 五层舞台 + ComponentState | ✅ |
| `components/peach_assets.py` | 新增 — mood 配置 + JS 脚本 + CSS（含过渡 v3 + tense v2）。修复：f-string 转义 + gesture 桥接 | ✅ |
| `components/peach_test.html` | 新增 — 独立测试页 (6 mood + 5 position) | ✅ |
| `framework/runtime/event_generator.py` | 无需改动 — 13 字段全为已支持类型 | ✅ |
| `config.show_moshi.yaml` | 注册 peach_blossom_stage | ✅ |
| `assets/moshi_courses/桃花源记/TEST_CTML.md` | 测试剧本（7 图 + 音频占位） | 🔄 端到端待跑 |
| `assets/moshi_courses/桃花源记/.meta.md` | 课程元信息（interaction: teacher） | ✅ |
| `apps/assets/pil-images/` | 7 张占位图（stream/forest/cave/village/return + callig_narrow/open）已注册 pil-image.jsonl | ⬜ 待替换正式素材 |
| `apps/assets/audios/` | 3 段占位 wav | ⬜ 待替换正式 BGM |

不改 `moshi/main.py`。不改现有 11 个布局。13 字段全部自动生成命令。
音频由 `apps/tools/audio_player` 独立处理。

---

## 与现有 feature 的关系

```
moshi (导演体系)
  ├── moss自我介绍    (纯单向叙事，11布局切换)
  ├── 极限审判         (双向对抗，单布局+情绪系统)
  └── 桃花源记         (连续动画引擎，单布局+粒子叙景)
```

每个后续 feature 验证 moshi 架构在不同方向的可扩展性。

---

*Created: 2026-06-29. Based on discussion with human engineer.*

---

### 2026-07-01 排查记录 (deepseek-v4-pro) — SIGIL_SCRIPT 未被 Reflex 输出

**环境**：Reflex dev 模式，show_moshi mode，peach_blossom_stage 布局已通过 CTML switch_layout 激活。

**验证通过的部分**：

- CSS 层面正常：`<set_atmosphere tense/>` 后 vignette 收缩为 3% 光点、grade 变暗、CSS transition 联动
- 粒子 Canvas 正常：`#peach-particles` 尺寸 [898, 716]（`R()` 已执行），`window.__PEACH_PARTICLE_CONFIG__` 有值，三种粒子态切换联动
- SYNC_SCRIPT 正常：`window.__PEACH_PARTICLE_CONFIG__` 和 `window.__PEACH_SIGIL_CONFIG__` 均已写入，mood/position 切换后属性正确联动

**定位到的根因**：

SIGIL_SCRIPT 整个 `<script>` 标签未出现在 DOM 中：
- `window.__peachSetGesture === undefined`（该函数由 SIGIL_SCRIPT 定义）
- `#peach-sigil` Canvas 存在于 DOM 但尺寸为 [300, 150]（HTML5 默认值，SIGIL_SCRIPT 的 `R()` 未执行）
- Elements 面板搜索 `peachSetGesture` 无结果
- `document.scripts` 只有 3 个框架注入脚本，无我们的

同为 `rx.script()` 注入，PARTICLE_SCRIPT（4735 字节）正常输出到 DOM，SIGIL_SCRIPT（4756 字节）被 Reflex 静默丢弃。Python 侧已验证两者均为有效非空字符串。

**排查方向**：
1. react-helmet 对无 `id`/`key` 属性的同标签去重（三个 `<script>` 标签无区分属性）
2. SIGIL_SCRIPT 内容触发了 Reflex/Next.js 的某种过滤
3. 字符编码问题（SIGIL_SCRIPT 含 U+2192 →、U+2014 — 等 Unicode 字符）

**下一步**：给三个 `rx.script()` 加唯一 `id` 属性排除 helmet 去重假设。

---

### 2026-07-01 剧本v2 + 素材体系 (deepseek-v4-pro)

**背景**：人类工程师反馈两个方向性问题：
1. 剧本节奏不对——应该是视觉先行、口播在后，符合观众"先看到再听解释"的认知习惯
2. 浮层严重利用不足——6章只用2张书法，且现有书法丑

**剧本修订**：

核心原则：
1. **CTML 全部前置** — 每轮先出 CTML 动作，再口播。旧格式 `> 口播 → CTML` 翻转为 `> → CTML > 口播`
2. **"不加动作"全部消灭** — Ch05 最严重（4处），每处改为浮层插入/切换
3. **浮层密度暴增** — 从全6章 2 次浮层操作 → 42 次（Ch01:4、Ch02:7、Ch03:6、Ch04:6、Ch05:12、Ch06:7）
4. **章首视觉冲击** — 每章第一轮就让观众看到变化，再开口

保持不变的约束：Ch01 switch_layout 铁律、Ch04 高潮时序铁律（Step 1-6）、Ch06 静默收场。

**素材体系**：

创建素材需求清单 `.moss_ws/apps/ui/moshi/peach_blossom_materials.md`：
- 每章逐项列出所需素材：标识符、类型、内容描述、风格要求、中英文AI提示词
- 总计 29-32 件：6 背景图 + 8 书法浮层 + 15 场景浮层 + 可选视频
- 风格统一要点：全部暗底、发光感、宋人山水/工笔基底、人物存在感极弱、色调沿情绪弧线演进

**素材入库**：人类工程师上传 22 张新浮层素材，全部注册入 pil-image.jsonl（line 52-73）。

**交叉校验**：剧本 locator 引用 ↔ JSONL path 逐条校对，27/27 全部对齐。旧版 `callig_narrow.png`/`callig_open.png`（JSONL line 45-46）已被 `overlay_` 前缀版本替代。

**当前状态**：剧本和素材就绪，等待 SIGIL_SCRIPT 修复后跑端到端集成测试。

---

### 2026-07-01 排查记录 (deepseek-v4-pro) — moshi 窗口闪退 + 白屏

**Bug 8 — `.meta.md` YAML frontmatter 解析崩溃（修复 verified ✅）**

- 症状：`uv run python main.py` 直接崩溃，窗口闪退
- Traceback：`yaml.scanner.ScannerError: while scanning a simple key ... could not find expected ':'`
- 链：`main.py` → `_get_course_storage()` → `storage.scan()` → `_scan_course()` → `_split_frontmatter()` → `yaml.safe_load(parts[1])`
- 根因：`.meta.md` 的两个 `---` fence 之间混入了 Markdown 格式的表演规则（`# 全局表演纪律`、`## 节奏铁律`、`1. **一句一动。**` 等），`yaml.safe_load` 将这些 Markdown 行当成 YAML mapping key 解析，遇到 `1. **一句一动。**` 找不到 `:` 分隔符抛异常
- 为何之前没发现：FEATURE.md 的 Decision 6 声明了 interaction 放 `.meta.md`，但这些规则是后来逐步加进去的，写内容时没意识到它们落在了 frontmatter fence 内
- 修复：将第二个 `---` 从第 53 行上移到第 26 行（`audio_available: true` 之后），使 Markdown 规则留在 body 部分
- 教训：
  9. **`.meta.md` 的 fence 位置**：`---` 之后、第二个 `---` 之前的所有内容必须是合法 YAML。写上 Markdown 内容前先确认 fence 已关闭
  10. **`_split_frontmatter` 是脆弱的**：`text.split("---", 2)` 对 fence 内嵌 `---` 的场景无防护。长期应加固（加 YAML 解析错误时的明确告警，而非静默崩）

**Bug 9 — 前端白屏：`dispatch is not a function`（待清缓存重启验证 ⬜）**

- 症状：moshi 窗口打开后白屏，左上角黑字 "default"。即使 Ghost 连接并切换布局，始终白屏
- 前端 Console：`TypeError: dispatch is not a function` at `state.js:647:27`
- 分析：Reflex 状态管理的核心 `dispatch` 函数未定义，WebSocket 连接正常但 state 变更无法传播到 React 组件。`rx.match(State.layout, ...)` 获取不到有效的 layout 值 → 始终 fallback 到 `rx.text("default")`
- 推测根因：新增 `PeachBlossomState`（13 字段，含 `Image.Image | None` 联合类型 + `list[Image.Image]`）后，前端的 `.web/` 编译缓存中 state schema 与新的 Python state 结构不兼容
- 修复方向：删除 `.web/` 缓存目录，重启 Reflex 强制重新编译前端
- 备注：`.web/` 已清，待人类工程师重新 `uv run reflex run` 验证