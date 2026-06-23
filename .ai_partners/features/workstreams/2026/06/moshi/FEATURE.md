---
title: Moshi — show_moshi 模式导演与演示布局体系
status: in-progress
priority: P1
created: 2026-06-23
updated: 2026-06-24T03:00
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
- Moshi App 代码：`.moss_ws/apps/ui/moshi/main.py`、`course.py`、`src/window.py`
- Moshi App 依赖：`.moss_ws/apps/ui/moshi/pyproject.toml`
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

### 7. 桌面壳窗口（2026-06-23）

show_moshi 的 reflex 前端目前在 Chrome 浏览器中查看。用原生桌面窗口替代：

**技术选型**：PySide6 + QWebEngineView。PySide6（Qt 官方维护，LGPL）与 PyQt6（Riverbank，GPL）API 99% 一致，选 PySide6 因许可证干净且社区更大。QWebEngineView 是完整 Chromium 内核，网页兼容性零问题。

**事件循环分离**：Qt（主线程）与 MOSS asyncio（后台线程）各跑各的事件循环——`QApplication.exec()` 在主线程驱动窗口，`Matrix.discover().run(main)` 在 daemon 线程驱动 channel。不共享 loop，互不阻塞。QAsyncioEventLoopPolicy 方案因与 QApplication 创建时机冲突而弃用。

**架构定位**：桌面窗口是纯基础设施——替代浏览器，不耦合 moshi 导演逻辑或 reflex 渲染逻辑。Ghost 仍是唯一集成点（Key Decision #1）。窗口本身可拓展（toolbar/sidebar/statusbar），当前阶段仅嵌入 QWebEngineView 加载 reflex 前端。

**放置位置**：`ui/moshi` app 内，不独立成 app。理由：窗口只是 moshi channel 进程的附带 UI，不是独立服务；独立 app 增加不必要的进程边界。

**关键依赖**：PySide6（~200MB，含 Qt + Chromium），仅 moshi app 的 pyproject.toml 声明，不污染主项目。

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
| `hero` | 全屏开场/收束 | title | 01 Awakening, 07 Finale | ✅ 完成 |
| `stage` | Ghost 舞台（复用） | status_bars, title, subtitle, body, images, cards | 02 CTML, 05 Mindflow, 06 Ghost | ✅ 已有 |
| `matrix` | 进度条逐个点亮 | title, status_bars | 04 Matrix | ✅ 完成 |
| `topology` | 节点拓扑图 + 连线动画（未来增强） | nodes, edges, active_path | 05 未来 | 🔮 待实现 |
| `comparison` | 左右对比表（未来增强） | left_header, right_header, rows, stats | 06 未来 | 🔮 待实现 |

> **2026-06-24**: 03 Channel 章改走"hero 标注 + Channel 命令执行"模式，不设专用布局。
> 04 Matrix 章从 topology（SVG 拓扑图）改为新建 matrix 布局。
> **05、06 章用 stage 先行跑通**（bar-eye 锁步 / body 清写对比），topology/comparison 降级为未来视觉增强，不再阻塞七幕联调。

### 各布局难点

**CTML 章（2026-06-23 重设计）**：CTML 章不再需要 `code_split` 专用布局。该章的核心亮点不是"展示代码"，而是**跨域并行执行**——Ghost 在一个输出块中同时驱动 reflex（GUI）、ai_eye（AI 眼睛）、mac（系统控制）、mermaid（架构图）、moss_self（自省）五个独立 Channel。这些 Channel 各自有独立的渲染通道（mermaid 走浏览器、mac 走 JXA、ai_eye 走 pygame），reflex 的 `stage` 布局只承担标题/字幕的背景板角色。详见 [场景渲染设计](#场景渲染设计)。

**matrix**（已完成）：基于 Reflex ComponentState，`CellBar` Pydantic model 驱动。`append_status_bars` 搭骨架（value=0），`update_status_bars index="N"` 逐个推至 100%，CSS `transition: width 0.8s cubic-bezier` 产生平滑填充动画。每条 bar 独立颜色（#6366f1 靛蓝 / #10b981 翠绿 / #f59e0b 琥珀 / #3b82f6 碧蓝 / #ec4899 品红）。两条 update 之间至少间隔一句口播让动画播完。

**topology**（未来增强，不阻塞）：Reflex 无 Canvas API，需手写 SVG；节点布局算法；三循环旋转环 + ai_eye 联动。05 章已用 stage + bar-eye 锁步跑通，topology 作为视觉升级。

**comparison**（未来增强，不阻塞）：逐行动画展开，左右列对齐。06 章已用 stage + body 清写对比跑通，comparison 作为视觉升级。

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

### 第三幕：Channel · 设备驱动（hero + Channel 命令，~60s）

**视觉目标**：hero 黑底白字做"操作前标签"，实际演示通过 mac/mermaid/web_bookmark/apps Channel 执行。每个操作遵循：宣布意图 → hero 标注 → 执行操作 → 确认结果。

**画面演进**：
1. 切到 hero，"我的能力不是写死在代码里的"
2. 逐 Channel 演示：mac 打开日历 / mermaid 画能力树 / web_bookmark 打开网页 / apps 列清单
3. 每个 Channel 演示前用 hero 标题标注当前操作名（黑色全屏+白字，聚焦注意力）
4. 演示完毕后总结 Channel 设计哲学："能力即驱动 · 插上即用"

**与旧剧本差异**：原计划用 capability_grid 卡片网格（未实现）。改用 hero + Channel 命令模式，
不依赖未完成布局。每个操作可被观众直接验证（日历弹出/浏览器打开），强化"AI 操控真实系统"的感知。

**关键命令**：`switch_state name="hero"` / `stream_title` / `mac:run` / `mermaid:draw` / `web_bookmark:open_web`

---
### 第四幕：Matrix · 系统总线（matrix，~35s）

**视觉目标**：5 个 Cell 逐个接入 Matrix 总线。黑色全屏 + 大号进度条（28px），每条从 0% 冲到 100%，配合 `cubic-bezier` 平滑填充动画。每条独立颜色标识不同 Cell。

**画面演进**：
1. 切 matrix，标题"Matrix · 系统总线"
2. 批量 append 5 条空 bar（value=0，各带颜色）：reflex #6366f1 / mac #10b981 / mermaid #f59e0b / web_bookmark #3b82f6 / apps #ec4899
3. 逐条 update 到 100%，每次间隔一句口播让 0.8s 动画播完
4. 5 条全满 → 总结"全部在线。Matrix 是我体内的神经系统"

**与旧剧本差异**：原计划 topology（SVG 拓扑图，待实现）。改为新建 matrix 布局——进度条逐个点亮。
动画策略："先 append 0%，再 update 到 100%"，利用 CSS transition 产生平滑填充感，比直接 append 100% 更有视觉冲击力。

**关键命令**：`switch_state name="matrix"` / `stream_title` / `append_status_bars` / `update_status_bars index="N"`

---

### 第五幕：Mindflow · 调度器（topology，~40s）

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
- [x] **matrix 布局**（`framework/layouts/matrix.py`）——进度条逐个点亮，仅 title + status_bars，28px 粗条 + 0.8s cubic-bezier 动画，5 色 Cell 标识
- [x] **config.show_moshi.yaml**（show_moshi mode 专用布局配置，hero + stage + matrix，默认 hero）
- [x] 7 章内容资产（`assets/moshi_courses/show_moshi/`，含 `.meta.md` + 7 个章节 md，各章自带 YAML frontmatter）
- [x] **02-ctml.md 剧本**（四段式递进：流式→并行→时间→自省，附带表演约束段）
- [x] **03-channel.md 剧本**（hero 标注 + mac/mermaid/web_bookmark 命令演示，附带表演约束段）
- [x] **04-matrix.md 剧本**（matrix 布局 + 进度条 0→100% 逐个接入，附带表演约束段）
- [x] **01-awakening.md 剧本加强**：补显式 `switch_state` 命令 + `⛔ 表演约束` 段
- [x] MODE.md（Ghost 身份 + 表演纪律 + moshi 协议）
- [x] Reflex 事件系统（`events.py`：LayoutEvent / StreamEvent / SetEvent / AppendEvent / UpdateEvent / PopEvent / ClearEvent）
- [x] 命令生成器（`event_generator.py`：按类型注解自动生成全套 CTML 命令）
- [x] Layout 快照系统（`layout_snapshot.py`）
- [x] show_moshi mode manifests
- [x] **moshi channel 鲁棒性修复**（`main.py` + `course.py`）：
  - 修复 `load_course` 名字遮蔽 bug
  - `load_course` / `next_chapter` / `jump_chapter` 返回 `Observe` 信号
  - `context_messages` 按层裁剪
- [x] **课程数据重构（2026-06-24）**：
  - 章节元信息从 `.meta.md` 集中式 chapters 数组下沉到各章节文件 YAML frontmatter
  - `course.py` 改为 async，从章节文件 frontmatter 读取
  - `main.py` context 改为三层叠加（课程列表始终可见 + 课程概况 + 当前章节）
  - 接入 MOSS 标准资源体系（`CourseResourceStorage`, scheme=`moshi-course`）
- [x] **桌面壳窗口**（`ui/moshi` app 内）：PySide6 + QWebEngineView + qasync 事件循环集成
- [x] **ResourceStorage 标准化（2026-06-24）**：
  - `_get_course_storage` 改为 IoC 优先：`matrix.container.force_fetch(CourseResourceStorage)`，回退仅限开发/测试
  - `load_course` 改为从 `CourseResourceStorage` 获取数据（`storage.list_infos()` + `storage.get(path)`），不再直接读文件
  - `main.py` context 三层叠加确认：Layer 1（课程列表）全程可见并标注"◀ 当前"，Layer 2（课程概况）进入章节后保留，Layer 3（章节详情）按需叠加
- [x] **测试课程 jingyesi（2026-06-24）**：
  - 3 章李白《静夜思》（床前明月光 / 疑是地上霜 / 低头思故乡），全部 hero 布局
  - 每章含完整 YAML frontmatter + `⛔ 表演约束` + 叙事要点 + 节奏示例
  - 用于验证 Storage 扫描、课程加载、多课程共存等流程
- [x] **hero 布局 clear_title 纪律（2026-06-24）**：
  - `switch_state` 不自动清空 ComponentState，切换章节时 title 会残留
  - hero 章节标准执行顺序：`switch_state` → `clear_title` → `stream_title`
  - `event_generator.py` 已为 str 字段自动生成 `clear_{name}` 命令，无需额外开发
  - jingyesi 三章均按此纪律编写，含 `禁止在 stream_title 之前忘记 clear_title` 硬约束
- [x] **05-mindflow.md 剧本（2026-06-24）**：
  - 布局从 `topology`（不存在）降级为 `stage`（立即可跑）
  - 核心机制：3 对 bar-eye 锁步（curious→感知 / thinking→思考 / speaking→执行）
  - 每对一一对应不交叉，bar 脉冲和 eye 表情同轮同步
  - `⛔ 表演约束`：bar ↔ eye 绑定表 + 命令白名单
- [x] **06-ghost.md 剧本（2026-06-24）**：
  - 布局从 `comparison`（不存在）降级为 `stage`（立即可跑）
  - 核心机制：4 轮 body 清写对比（运行单元 → 系统调用+设备驱动 → 调度器+总线 → Ghost 自白）
  - 不使用 status_bars（和 04/05 章差异化），用 cards 展示生命体征
  - `⛔ 表演约束`：逐轮 clear_body 硬约束 + 禁止 status_bars
- [x] **07-finale.md 剧本（2026-06-24）**：
  - 纯 hero，三短标题：MOSS → 灵·壳·体 → AIOS
  - 和第一幕首尾对称——同布局、同起点标题"MOSS"、同极简风格
  - `⛔ 表演约束`：仅 3 个命令 + 禁止 next_chapter + 禁止画蛇添足

### 待完成

- [x] 章节剧本补 switch_state + 表演约束（全部 7 章 ✅）
- [ ] 实现 `comparison` 布局（未来视觉增强，不阻塞——06 章已用 stage 跑通）
- [ ] 实现 `topology` 布局（未来视觉增强，不阻塞——05 章已用 stage 跑通）
- [ ] fill `bringup_apps`（MODE.md 目前只有 `ui/reflex`，需加入 `ui/moshi`、`games/ai_eye`）
- [ ] 端到端集成测试

新布局实现时遵守 [布局实现模式](#6-布局实现模式2026-06-23-修订) 的三条纪律。

### 跨布局共同难点

- **动画与 Reflex 的摩擦**：Reflex 声明式模型下，动画靠 CSS transition/animation。组件挂载/卸载动画（enter/exit）在 Reflex 中不好做——没有 React 的 `<Transition>` 组件。每个布局需要独立设计 CSS 动画策略。
- **事件系统够用但不够优雅**：对于"添加节点 + 添加连线 + 设置脉冲"这种复合操作，Ghost 需连续发多个命令，增加了编排负担。
- **测试困境**：布局是纯视觉的，单元测试只能验证 ComponentState 字段更新，不能验证渲染效果。

---

*Created: 2026-06-23. Based on `.moss_ws/apps/ui/moshi/DESIGN.md`.*
