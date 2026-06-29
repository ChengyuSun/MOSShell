---
created: 2026-06-29
depends:
- moshi
description: 基于 moshi 导演体系的第三门课程。以《桃花源记》为叙事蓝本，验证连续动画引擎 与交互式讲解在流式演示中的可行性——粒子系统叙景、光灵角色动画、五层统一舞台、
  字段级命令自动生成、用户可随时打断提问或要求回退。单一 peach_blossom_stage 布局 承载全部 6 章，不切换布局。
milestone: null
priority: P1
status: in-progress
status_note: 设计方案完善：确定交互打断模型、自由发挥型剧本格式、砍掉segment、素材只区分背景/浮层不区分内容类型、字段级命令起步10/11字段自动生成
title: 桃花源记 — 连续动画引擎驱动的流式叙事演示
updated: '2026-06-29'
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

---

## 章节结构

| 章 | 标题 | 情绪 | 粒子态 | 核心动效 | 知识锚点（示例） |
|---|---|---|---|---|---|
| 01 | 缘溪行 | serene 宁静 | 水流 | 光灵沿溪 gliding | 武陵人、缘溪行、忘路之远近 |
| 02 | 桃花林 | enchanted 惊艳 | 花瓣 | 粉色花瓣涌入、桃树渐显 | 夹岸数百步、中无杂树、芳草鲜美 |
| 03 | 山洞 | tense 紧张 | 水流（收束） | 暗角收紧、单束光缝 | 山有小口、仿佛若有光、初极狭才通人 |
| 04 | 豁然 | released 释放 | 金涌 | 三段式爆炸展开 | 豁然开朗、土地平旷、屋舍俨然 |
| 05 | 桃花源 | tranquil 恬静 | 花瓣 | 全景铺展、屋舍炊烟 | 阡陌交通、鸡犬相闻、黄发垂髫 |
| 06 | 归来 | wistful 怅然 | 水流 | 粒子消散、画面闭合 | 便扶向路、处处志之、不复得路 |

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
    background_image: Image.Image = None   # 背景层图片，在光灵后
    background_video: VideoLocator = ""    # 背景层视频，在光灵后
    overlay_image: Image.Image = None      # 浮层图片，在光灵前
    overlay_video: VideoLocator = ""       # 浮层视频，在光灵前

    # 过渡
    transition: str = ""                # constrict | expand | dissolve | ""

    # 字幕
    subtitles: list[str] = []

    # HUD
    chapter_title: str = ""
    chapter_index: int = 0              # 0-5
```

### 字段 → 命令映射

| 字段 | 类型 | Ghost 使用的命令 | 命令来源 |
|---|---|---|---|
| `atmosphere` | str | `set_atmosphere` `clear_atmosphere` | 自动（str） |
| `sigil_position` | str | `set_sigil_position` | 自动（str） |
| `sigil_gesture` | str | `set_sigil_gesture` `clear_sigil_gesture` | 自动（str） |
| `background_image` | Image.Image | `set_background_image` `clear_background_image` | 自动（Image.Image） |
| `background_video` | VideoLocator | `set_background_video` `clear_background_video` | 自动（VideoLocator） |
| `overlay_image` | Image.Image | `set_overlay_image` `clear_overlay_image` | 自动（Image.Image） |
| `overlay_video` | VideoLocator | `set_overlay_video` `clear_overlay_video` | 自动（VideoLocator） |
| `transition` | str | `set_transition` `clear_transition` | 自动（str） |
| `subtitles` | list[str] | `stream_subtitles` `clear_subtitles` | 自动（list[str]） |
| `chapter_title` | str | `set_chapter_title` `clear_chapter_title` | 自动（str） |
| `chapter_index` | int | `set_chapter_index` | **手动注册** |

Image.Image 和 VideoLocator 复用现有 `event_generator` 的命令生成逻辑——
locator→资源转换在命令函数内部完成，命令参数是 locator 字符串，入队时已是 PIL Image / HTTP URL。
`chapter_index: int` 是唯一需要手动注册命令的字段。

---

## moshi 导演端：零改动

课程导航（load_course / next_chapter / jump_chapter）原样复用。
所有 UI 操作由 Ghost 通过字段级 reflex 命令直接控制，10/11 字段自动生成。

moshi 的 `next_chapter` 推进章节，Ghost 在章节首自行调用 `set_chapter_title` +
`set_atmosphere` 设定新章节的视觉基调。

---

## Implementation Plan

### Phase 1: Canvas 粒子引擎 + 光灵

1. `peach_blossom_stage` 布局骨架 — 五层 CSS 结构 + ComponentState
2. Canvas IIFE 注入 — 粒子场基础渲染（三态：水流/花瓣/金涌）
3. Canvas IIFE — 光灵绘制 + idle 呼吸动画
4. 全局变量桥接 — `window.__PEACH_*__` 读写
5. 注册 `config.show_moshi.yaml`

**验证**：打开页面看到暗空间 + 光灵呼吸 + 粒子漂浮。调整 `__PEACH_PARTICLE_CONFIG__`
粒子态切换。

### Phase 2: 光灵运动 + 过渡动画

6. 光灵 gliding 动画 — `set_sigil_position` 驱动，Canvas JS 侧 lerp 到目标位置
7. 光束手势 — `set_sigil_gesture` 驱动光灵向指定方向伸出光束
8. 暗角 + 光缝 — CSS clip-path / box-shadow 动态、光缝呼吸
9. 三段式"豁然开朗"动画 — constrict → 临界 → expand，`set_transition` 触发

**验证**：光灵在舞台上移动，发射手势。`set_transition` 触发三段式展开。

### Phase 3: 内容面板

10. 背景层图片/视频渲染 — 在光灵后，支持 set/clear，带入场/退场动画
11. 浮层图片/视频渲染 — 在光灵前，支持 set/clear，带入场/退场动画
12. 资源 locator 转换复用 Image.Image / VideoLocator 类型，零新代码

**验证**：素材从边缘滑入，背景和浮层正确分层。

### Phase 4: 课程剧本 + 端到端

13. 编写 `.meta.md` — 课程元信息 + interaction 字段，复用现有 `context_messages`
    Layer 2 管道
14. 编写 6 章剧本 — 每章 YAML frontmatter + 知识锚点 + 口播锚点 + 建议 CTML 序列
    （自由发挥型，不写死台词。Ghost 照口播锚点即兴展开）
15. 素材整理 — 山水画/书法贴图/视频素材，导入 resource storage
16. 端到端集成 — Ghost + moshi 导演 + peach_blossom_stage + 字幕
17. 交互测试 — 验证打断提问、回答后继续、jump_chapter 回退、章间自然过渡

**验证**：完整跑通 6 章（~4 分钟）。

---

## 改动文件清单

| 文件 | 改动 | 状态 |
|---|---|---|
| `layouts/peach_blossom_stage.py` | 新增布局 — 五层舞台 + Canvas IIFE | ⬜ |
| `moss_in_reflex.py` | 注册 peach_blossom_stage 布局 | ⬜ |
| `framework/events.py` | 无需改动（复用现有 StreamEvent/SetEvent 等） | — |
| `framework/runtime/event_generator.py` | 为 int 字段补充命令生成（`chapter_index`） | ⬜ |
| `config.show_moshi.yaml` | 注册 peach_blossom_stage | ⬜ |
| `assets/moshi_courses/桃花源记/` | 6 章剧本 + .meta.md + 素材 | ⬜ |

不改 `moshi/main.py`。不改现有 11 个布局。10/11 字段自动生成命令，仅 `chapter_index: int` 需手动注册。

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