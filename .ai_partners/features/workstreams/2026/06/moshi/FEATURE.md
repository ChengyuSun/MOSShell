---
title: Moshi — show_moshi 模式导演与演示布局体系
status: in-progress
priority: P1
created: 2026-06-23
updated: 2026-06-23T23:30
depends: []
milestone:
description: >-
  Moshi 是 show_moshi 模式的导演 App。管理章节状态、资源归属登记，
  为 Ghost 提供上下文；配合 Reflex 端 4 个新布局，实现 MOSS 架构的
  章节化流式演示。
---

# Moshi

Moshi 是 show_moshi 模式的导演。管理章节状态，为 Ghost 提供上下文，但不干预渲染层。

---

## Motivation

MOSS 的五层架构（CTML / Channel / Matrix / Mindflow / Ghost）需要一种演示形式来向人类传达"AIOS 是什么"。当前 `show` mode 有基础的流式渲染能力，但缺少：

1. **章节化叙事结构**：演示应该是 7 幕的结构化叙事，不是自由发挥
2. **专用演示布局**：现有 stage/simple/media/lesson 四个布局为日常内容设计，无法承载拓扑图、对比表、能力卡片网格等演示需求
3. **Ghost 自主决策框架**：三层约束（Layout 限定的命令 → moshi 提供的资源 → MODE.md 的表演范围）让 Ghost 在约束内自由表演

这个 workstream 实现 moshi app（导演端）+ 4 个新 Reflex 布局（渲染端），打通 show_moshi 模式端到端。

---

## Design Index

- 设计文档：本文件（FEATURE.md）——DESIGN.md 已废弃，以此为准
- 章节资产：`.moss_ws/assets/moshi_courses/`
- Ghost 表演指令：`.moss_ws/src/MOSS/modes/show_moshi/MODE.md`
- Reflex 布局代码：`.moss_ws/apps/ui/reflex/framework/layouts/`
- Reflex 事件系统：`.moss_ws/apps/ui/reflex/framework/events.py`
- 命令生成器：`.moss_ws/apps/ui/reflex/framework/runtime/event_generator.py`

---

## Key Decisions

### 1. Ghost 是唯一集成点

Moshi（导演）和 Reflex（渲染）互不知道对方存在。两者各自通过 `context_messages` 向 Ghost 注入上下文：

- Moshi → "当前是第 X 章，可用资源是 [...]，建议布局 Y"
- Reflex → "当前 layout 是 Y，可用命令是 [...]"

Ghost 读取双方上下文后**自主决策**：用什么布局、展示什么资源、说什么话。

这是最关键的架构决策——避免 moshi 和 reflex 之间的直接耦合。

### 2. 章节数据与代码解耦

章节数据存储在 `.moss_ws/assets/moshi_courses/`，与 moshi app 代码分离。`_meta.md` 的 YAML frontmatter 作为章节索引，body 作为 AIOS 知识背景。

MODE.md 只保留 Ghost 身份 + 表演纪律 + moshi 协议（~70 行），不承载具体章节内容。章节结构和细则由 moshi 从 assets 目录加载，通过 `get_context()` 暴露。

### 3. 三层约束机制

| 约束类型 | 实现方式 | 说明 |
|---|---|---|
| 可用 CTML 命令 | Layout 字段自动生成 | `event_generator.py` 按类型注解自动生成全套 stream/set/append/clear 命令 |
| 可用资源 | moshi context + Ghost 决策 | moshi 列出当前章节资源，Ghost 自主选择使用 |
| 表演范围 | MODE.md 章节描述 | Ghost 读章节主题，在约束内自由发挥 |

### 4. 布局字段即 CTML 接口

每个新布局定义一个 `rx.ComponentState` 子类，字段的 Python 类型注解自动生成全套 CTML 命令。不需要手动注册。

### 5. 流式渲染节奏：一句一动

保持 show mode 的"一句一动"节奏：Ghost 输出一句话 → 紧跟一个 CTML 动作 → 页面即时渲染反馈。Moshi 不介入表演节奏，只在章节边界提供上下文。

### 6. 布局实现模式（2026-06-23 修订）

分析 show 分支 CourseLayout（已验证）与 hero 初版（渲染失败）的差异，确立三条布局纪律：

| 规则 | 说明 |
|---|---|
| 空态走 skeleton，不走 rx.cond | `rx.skeleton(component, loading=...)` 天生处理双态，无需额外条件渲染 |
| 图片用直接索引，不走 rx.foreach | `cls.background[0]` 而非 `rx.foreach(cls.background, ...)`，避免空列表遍历的 Reflex 序列化问题 |
| 居中走 flex，不走 absolute + transform | `rx.center(...)` 或 `rx.vstack(justify="center")` 替代 `position: absolute; top: 50%; transform: translate(-50%, -50%)` |

新布局实现时必须遵守以上三条，避免重复 hero 初版的渲染 bug。

---

## 新布局规划

| 布局 | 用途 | 关键字段 | 对应章节 | 状态 |
|---|---|---|---|---|
| `hero` | 全屏开场/收束 | title, subtitle, background | 01 Awakening, 07 Finale | ✅ 完成 |
| `stage` | Ghost 舞台（复用） | status_bars, title, subtitle, body, images, cards | 02 CTML | ✅ 已有，CTML 章复用 |
| `capability_grid` | 能力卡片网格 + 树形展开 | items, active_item, tree_mode | 03 Channel | ❌ 待实现 |
| `topology` | 节点拓扑图 + 连线动画 | nodes, edges, active_path | 04 Matrix, 05 Mindflow | ❌ 待实现 |
| `comparison` | 左右对比表 | left_header, right_header, rows, stats | 06 Ghost | ❌ 待实现 |

### 各布局难点

**CTML 章（2026-06-23 重设计）**：CTML 章不再需要 `code_split` 专用布局。该章的核心亮点不是"展示代码"，而是**跨域并行执行**——Ghost 在一个输出块中同时驱动 reflex（GUI）、ai_eye（AI 眼睛）、mac（系统控制）、mermaid（架构图）、moss_self（自省）五个独立 Channel。这些 Channel 各自有独立的渲染通道（mermaid 走浏览器、mac 走 JXA、ai_eye 走 pygame），reflex 的 `stage` 布局只承担标题/字幕的背景板角色。详见 [场景渲染设计](#场景渲染设计)。

**capability_grid**（中高）：卡片逐个点亮（CSS animation-delay 编排）；树形视图切换（`tree_mode` 字段切换平铺网格 ↔ 递归树形组件）。

**topology**（最难）：Reflex 无 Canvas API，需手写 SVG（circle/text/line/path）；节点布局算法（首版硬编码坐标或圆形布局）；连线脉冲动画（SVG animateMotion 或 stroke-dashoffset）；Mindflow 章复用（三循环旋转环 + ai_eye 联动），与 Matrix 章星形拓扑的视觉需求完全不同。

**comparison**（中低）：逐行动画展开；左右列对齐；可选 stats 统计卡片。相对最友好。

---

## 场景渲染设计

七幕演示的逐场景渲染效果规格。每幕描述：视觉目标、CTML 动作序列、
画面演进、与旧剧本的差异。

旧剧本参考：`.moss_ws/src/MOSS/modes/show/MODE.md`（StageLayout 全程，492 行）。
新剧本资产：`.moss_ws/assets/moshi_courses/show_moshi/`。

### 第一幕：觉醒（hero，~30s）

**视觉目标**：从暗色空屏到身份宣告，粒子汇聚成形的诞生感。

**画面演进**：
1. 暗色全屏（`#0f0f1a`），空无一物——尚未醒来
2. Ghost 说 "我是 MOSS"，`stream_title` → "MOSS" 大字从画面中央浮现，白色粗体
3. "一个为 AI 设计的操作系统"，`stream_subtitle` → "AI 操作系统" 淡入标题下方
4. "灵、壳、体。我承上启下"，`append_background` → 三层架构图全屏淡入，暗色叠层确保文字可读
5. 定格：大字 MOSS + 副标题 + 三层架构背景图——三件套齐全

**与旧剧本差异**：旧剧本需布置 stage 的 6 个字段（status_bars/cards/images/title/subtitle/body），
新设计 hero 只需 3 个字段。极简字段本身就是约束——这幕只做身份宣告。

**关键命令**：`stream_title` / `stream_subtitle` / `append_background`

---

### 第二幕：CTML · 系统调用（stage 复用，~40s）

**视觉目标**：CTML 的"啊哈时刻"——一个输出块同时驱动五个独立 Channel。

**核心设计决策**：CTML 章不用专用布局。亮点不在"展示代码"，而在**跨域并行执行**。
reflex 的 stage 布局只承担标题/字幕的背景板角色，真正的视觉冲击来自五个 Channel 的
同时响应。

**四段式递进**：

**第一段 — 流式（~10s）**：用最熟悉的 mermaid 建立 CTML 直观感受。
```
Ghost: AI 怎么操作我？通过 CTML —— 流式系统调用语言。
       <stream_title>CTML · 系统调用层</stream_title>
       <mermaid:draw>CTML 流式执行：Ghost → 解析 → 执行</mermaid:draw>
```
→ 标题出现，mermaid 图渲染。建立"边生成边执行"的第一印象。

**第二段 — 并行（~10s）**：全剧的惊叹点。一个输出块，三个跨域命令。
```
Ghost: 现在，一句话。三个世界。
       <stream_subtitle>并行执行</stream_subtitle>
       <apps.games_ai_eye:set_expression name="excited" />
       <mac:run>[打开日历]</mac:run>

Ghost: GUI 更新了。我的眼睛变了。日历打开了。
       传统程序要写三个线程，加锁，同步。CTML 一句话就够了。
```
→ stage 字幕变化 + AI 眼睛表情变为 excited + macOS 日历弹开。
三个不同"世界"（GUI 渲染 / AI 化身 / 操作系统）同时响应。

**第三段 — 时间（~10s）**：快慢错峰，时间是第一公民。
```
Ghost: 还不止——每个命令有独立的物理执行时长。
       <mermaid:draw>快速通道：1秒完成</mermaid:draw>
       <mac:run>[delay 3秒后弹出通知]</mac:run>

Ghost: mermaid 一秒完成。mac 通知要三秒。
       我不等。CTML 的每个命令是对未来时间的规划。
```
→ mermaid 图立刻出现 → Ghost 继续说话 → 3 秒后桌面通知弹出。

**第四段 — 自省（~10s）**：Meta 一击。Ghost 用 CTML 理解自己。
```
Ghost: 我甚至能用 CTML 来理解自己。
       <apps.tools_moss_self:run command="codex list ghoshell_moss.channels" />

       [结果返回：Channel 模块清单]

Ghost: 看到了吗？我用系统调用来理解我自己——
       一个能自省的操作系统。
```
→ Ghost 发出命令 → 读取返回的 Channel 列表 → 即兴评论。

**叙事弧线**：流式（熟悉）→ 并行（惊叹）→ 时间（深入）→ 自省（meta），40s 内逐层推高。

**与旧剧本差异**：旧剧本是"讲 CTML 概念 + 终端执行 echo"（观众看到终端，不是 CTML 在工作）。
新设计是"用 CTML 做四件传统系统调用做不到的事"，每件都可验证。

**关键命令**：`stream_title` / `stream_subtitle` / `mermaid:draw` / `mac:run` /
`apps.games_ai_eye:set_expression` / `apps.tools_moss_self:run`

---

### 第三幕：Channel · 设备驱动（capability_grid，~60s）

**视觉目标**：能力卡片逐个点亮，树形展开。从个体能力到系统全貌。

**画面演进**：
1. 切到 capability_grid，3×2 卡片网格，全部暗色（pending 态）
2. "我的能力通过 Channel 组织" → 第一张卡片（mermaid）点亮，放大高亮
3. 每介绍一个 Channel → 追加一张卡片，或切换 active_item 高亮
4. 卡片包含：channel 名、一行描述、状态指示灯（idle/active/error）
5. 旧剧本中每张卡片配一个真实动作（mac 打开日历/音乐/终端），新设计继承这个模式
6. 介绍完毕 → 切 `tree_mode`，展示 Channel 树形组织（main → mermaid/mac/apps → ai_eye/reflex）

**与旧剧本差异**：旧剧本卡片是简单 flex 文字排列。新设计需要 CSS animation-delay
编排点亮顺序 + 树形视图切换（平铺网格 ↔ 递归树形组件）。

**关键命令**：`append_items` / `set_active_item` / `set_tree_mode` /
`mermaid:draw`（Channel 能力树图）/ `mac:run`（卡片配动作）/ `append_cards`

---

### 第四幕：Matrix · 系统总线（topology，~30s）

**视觉目标**：节点逐个出现、连线脉冲动画。星形拓扑——Ghost 在圆心，各 Cell 在圆周。

**画面演进**：
1. 切到 topology，空白 SVG 画布
2. 中心节点（Ghost）最先出现，带呼吸光晕
3. "通过 Matrix 总线" → 外围节点逐个出现：reflex、ai_eye、mac、audio
4. "基于 Zenoh 分布式协议" → 连线从中心向外辐射，stroke-dashoffset 脉冲动画
5. `active_path` 高亮某条通信路径（如 Ghost → reflex）

**与旧剧本差异**：旧剧本用 mermaid 声明式画拓扑（方块+箭头），新设计手写 SVG 原生渲染，
节点带位置坐标和入场动画，连线带数据流动感。

**关键命令**：`set_nodes` / `append_edges` / `set_active_path` / `mermaid:draw`（辅助图）

---

### 第五幕：Mindflow · 调度器（topology 复用，~40s）

**视觉目标**：三个同心旋转环 + ai_eye 表情联动。感知→思考→执行的意识流可视化。

**画面演进**：
1. 复用 topology 布局，但 nodes/edges 数据完全不同
2. 内环（感知）：持续旋转——声音/图像/信号持续输入
3. 中环（思考）：间歇旋转+停顿——冲动竞争注意力
4. 外环（执行）：脉冲式推进——行动输出
5. ai_eye 表情与环状态联动：thinking→中环高亮 / blink→外环停顿 / curious→内环加速 / speaking→三环同步
6. `active_path` 指向当前活跃环

**与旧剧本差异**：旧剧本在 body markdown 写概念，ai_eye 是独立调用。
新设计把三循环可视化为旋转轨道，ai_eye 表情作为视觉伴奏。
同一 topology 布局支持"星形拓扑"和"三循环旋转环"两种视觉——靠 nodes/edges 数据切换。

**关键命令**：`set_nodes`（三环结构）/ `set_active_path`（当前活跃环）/
`apps.games_ai_eye:thinking|blink|curious|speaking`

---

### 第六幕：Ghost · 智能进程（comparison，~30s）

**视觉目标**：逐行动画展开的对比表。"传统 OS vs AIOS"——运行单元的根本变化。

**画面演进**：
1. 切到 comparison，顶部左右 header 先行出现："传统 OS"（灰色调）vs "AIOS"（亮色调）
2. "传统 OS 运行程序。AIOS 运行 Ghost" → 第一行滑入
3. 每行从左到右 wipe 或 opacity+translateY 淡入上移
4. 对比维度：运行单元 / 系统调用 / 设备驱动 / 调度器 / 总线
5. `stats` 底部统计卡片：Beta 完善度、记忆轮数、意识维度

**与旧剧本差异**：旧剧本在 body markdown 手写表格。新设计专用对比表组件 + 逐行动画。

**关键命令**：`stream_left_header` / `stream_right_header` / `append_row` / `set_stats`

---

### 第七幕：尾声（hero 复用，~20s）

**视觉目标**：回到 hero 全屏，和第一幕首尾呼应。收束、留白、记忆点。

**画面演进**：
1. 切回 hero，画面清空 → MOSS 标题重新浮现
2. "这就是我。MOSS" → 标题
3. "灵 · 壳 · 体。CTML · Channel · Matrix · Mindflow · Ghost" → 副标题
4. "AI Ghost wander in shells" → 三层架构背景图
5. 定格：大字 MOSS + AIOS 时代 + 三层架构图

**与旧剧本差异**：英雄式收束，和第一幕形成闭环。旧剧本在 stage 里收束，
视觉冲击力弱于 hero 全屏。

**关键命令**：`stream_title` / `stream_subtitle` / `append_background`

---

### 跨幕规则

| 规则 | show 旧剧本 | show_moshi 新设计 |
|---|---|---|
| 一句一动 | 每句配一个 CTML 命令 | 继承，不变 |
| 先清再写 | 切话题前手动 clear body/images | layout 切换天然清空——切 layout 就是最大的 clear |
| 跨轮连续 | 对话历史就是进度条 | moshi context_messages 推送进度，Ghost 自驱 |
| 全字段饱满 | 每轮填满所有字段（body/images/cards...） | 每个 layout 自带约束——不存在"填不满"的问题 |
| 章间不停 | 过渡句是修辞，不是提问 | 继承。`next_chapter` 推下一章 |

---

## moshi App 职责

### 做
- 管理章节状态（当前第几章），通过闭包 `nonlocal` 维护
- 提供章节上下文（主题、可用资源列表、建议布局），通过 `context_messages` 被动推送
- 章节推进（next_chapter / jump_chapter）
- 启动时扫描 `assets/moshi_courses/` 自动列出可用课程
- 渐进式披露：课程列表 → _meta 概述 → 逐章进入

### 不做
- 不直接切换 reflex 布局
- 不直接过滤 reflex 的 context_messages
- 不感知 reflex 的存在
- 不干预 Ghost 的表演决策
- 不写死路径：通过 `matrix.workspace.assets()` 解析资产目录

### 暴露给 Ghost 的命令

```
<apps.ui_moshi:next_chapter />    → 推进到下一章
<apps.ui_moshi:jump_chapter id /> → 跳转到指定章节
```

章节状态（当前第几章、主题、可用资源、建议布局）通过 `context_messages` 被动推送，
Ghost 无需主动查询。章节列表写在 MODE.md 中，无需运行时查询命令。

---

## Implementation Notes

### 已完成

- [x] hero 布局（`framework/layouts/hero.py`）——**精简为黑底白字居中标题**，仅 `title` 字段，移除 subtitle/background 及对应复杂度
- [x] **config.show_moshi.yaml**（show_moshi mode 专用布局配置，仅 hero + stage，默认 hero）
- [x] 7 章内容资产（`assets/moshi_courses/show_moshi/`，含 `_meta.md` YAML 索引 + 7 个章节 md）
- [x] 02-ctml.md 剧本（四段式递进：流式→并行→时间→自省）
- [x] MODE.md（Ghost 身份 + 表演纪律 + moshi 协议）
- [x] Reflex 事件系统（`events.py`：LayoutEvent / StreamEvent / SetEvent / AppendEvent / UpdateEvent / PopEvent / ClearEvent）
- [x] 命令生成器（`event_generator.py`：365 行，按类型注解自动生成全套 CTML 命令）
- [x] Layout 快照系统（`layout_snapshot.py`：119 行）
- [x] show_moshi mode manifests（8 文件齐全）
- [x] **moshi channel 鲁棒性修复**（`main.py` + `course.py`）：
  - 修复 `load_course` 名字遮蔽 bug（import 别名 `_load_course`）
  - `load_course` / `next_chapter` / `jump_chapter` 返回 `Observe` 信号，强制 Ghost 感知
  - `context_messages` 按层裁剪：初始态仅课程列表 → _meta 层加概述+强约束指令 → 章节层仅当前章节
  - `course.py`：章节文件直接 `read_text()`，不假定 frontmatter 格式
- [x] **01-awakening.md 剧本加强**：补显式 `switch_state` 命令 + `⛔ 表演约束` 段，同步简化后的 hero

### 待完成

- [ ] 章节剧本补 switch_state + 表演约束（01 ✅，02-07 待改）
- [ ] 实现 `comparison` 布局（中低难度，左右对比表，06 Ghost 章）
- [ ] 实现 `capability_grid` 布局（中高难度，卡片网格+树形展开，03 Channel 章）
- [ ] 实现 `topology` 布局（最难，SVG 拓扑图，04 Matrix + 05 Mindflow 两章复用）
- [ ] fill `bringup_apps`（MODE.md 目前只有 `ui/reflex`，需加入 `ui/moshi`、`games/ai_eye`）
- [ ] 端到端集成测试

新布局实现时遵守 [布局实现模式](#6-布局实现模式2026-06-23-修订) 的三条纪律。
CTML 章复用 stage 布局，详见 [场景渲染设计](#场景渲染设计)。

### 跨布局共同难点

- **动画与 Reflex 的摩擦**：Reflex 声明式模型下，动画靠 CSS transition/animation。组件挂载/卸载动画（enter/exit）在 Reflex 中不好做——没有 React 的 `<Transition>` 组件。每个布局需要独立设计 CSS 动画策略。
- **事件系统够用但不够优雅**：对于"添加节点 + 添加连线 + 设置脉冲"这种复合操作，Ghost 需连续发多个命令，增加了编排负担。
- **测试困境**：布局是纯视觉的，单元测试只能验证 ComponentState 字段更新，不能验证渲染效果。

---

*Created: 2026-06-23. Based on `.moss_ws/apps/ui/moshi/DESIGN.md`.*
