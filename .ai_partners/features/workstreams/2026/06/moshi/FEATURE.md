---
title: Moshi — show_moshi 模式导演与演示布局体系
status: in-progress
priority: P1
created: 2026-06-23
updated: 2026-06-24T16:00
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

1. **章节化叙事结构**：演示应该是 6 幕的结构化叙事，不是自由发挥
2. **专用演示布局**：现有 stage/simple/media/lesson 四个布局为日常内容设计，无法承载矩阵进度条、对比表、沉浸视频等演示需求
3. **Ghost 自主决策框架**：三层约束（Layout 限定的命令 → moshi 提供的资源 → MODE.md 的表演范围）让 Ghost 在约束内自由表演
4. **纯 reflex 交互**（2026-06-24 修订）：去掉外部 Channel 依赖（mac/mermaid/web_bookmark/ai_eye），所有演示仅通过 reflex 布局完成

这个 workstream 实现 moshi app（导演端）+ 多个 Reflex 布局（渲染端），打通 show_moshi 模式端到端。

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

**事件循环融合（2026-06-24 修订）**：Qt 和 MOSS Matrix 通过 `qasync` 共享主线程的单一 asyncio 事件循环。`QApplication` 在 `qasync.run()` 之前创建，`qasync` 通过 `QApplication.instance()` 复用并桥接到 asyncio event loop。`matrix.arun(main)` 直接 await（而非通过 `Matrix.run()` 另起事件循环），窗口关闭时 `app.aboutToQuit` → `matrix.close()` → `wait_closed()` 触发 → `main()` 返回 → 进程正常退出。最初用 `threading.Thread` 分离两套事件循环，后改为 qasync 融合；改用 `Matrix.run()` 直接调 `arun()` 避免了 `asyncio.run()` 隐式创建第二个 loop。

**启动加载态（2026-06-24）**：Reflex 本地服务启动慢于窗口，窗口打开瞬间页面不可用会显示 `ERR_CONNECTION_REFUSED`。增加 `_LoadingOverlay` 组件——深色背景 + 居中文字 + 不确定进度条。启动时展示 loading 画面，`QTimer` + `QNetworkAccessManager.head()` 每秒轮询目标 URL，服务可用后自动切到 webview。loading 和 webview 通过 `QStackedWidget` 管理，webview 页面背景色与 loading 统一（`#0f0f1a`），切换时无白屏闪烁。

**架构定位**：桌面窗口是纯基础设施——替代浏览器，不耦合 moshi 导演逻辑或 reflex 渲染逻辑。Ghost 仍是唯一集成点（Key Decision #1）。窗口本身可拓展（toolbar/sidebar/statusbar），当前阶段仅嵌入 QWebEngineView 加载 reflex 前端。

**放置位置**：`ui/moshi` app 内，不独立成 app。理由：窗口只是 moshi channel 进程的附带 UI，不是独立服务；独立 app 增加不必要的进程边界。

**关键依赖**：PySide6（~200MB，含 Qt + Chromium）+ qasync（Qt/asyncio 事件循环桥接），仅 moshi app 的 pyproject.toml 声明，不污染主项目。

### 6. 布局实现模式（2026-06-23 修订）

分析 show 分支 CourseLayout（已验证）与 hero 初版（渲染失败）的差异，确立三条布局纪律：

| 规则 | 说明 |
|---|---|
| 空态走 skeleton，不走 rx.cond | `rx.skeleton(component, loading=...)` 天生处理双态，无需额外条件渲染 |
| 图片用直接索引，不走 rx.foreach | `cls.background[0]` 而非 `rx.foreach(cls.background, ...)`，避免空列表遍历的 Reflex 序列化问题 |
| 居中走 flex，不走 absolute + transform | `rx.center(...)` 或 `rx.vstack(justify="center")` 替代 `position: absolute; top: 50%; transform: translate(-50%, -50%)` |

新布局实现时必须遵守以上三条，避免重复 hero 初版的渲染 bug。

---

## 布局现状

| 布局 | 用途 | 关键字段 | 对应章节 | 状态 |
|---|---|---|---|---|
| `cohesion_field` | 暗空间粒子场，内容凝聚浮现 | title, sub_title, main_text, body, image | 01 Awakening, 06 Finale | ✅ 完成 |
| `course` | 左图右文交互演示 | title, sub_title, image, main_text, annotations, appreciation | 02 CTML | ✅ 完成 |
| `matrix` | 进度条逐个点亮接入 | title, status_bars | 03 Channel & Matrix (Act 1) | ✅ 完成 |
| `hero` | **纯全屏沉浸视频播放** | videos (list[VideoLocator]) | 03 Channel & Matrix (Act 2) | ✅ 完成 |
| `stage` | 三 bar 并发波动 + 正文 + 图片 | status_bars, title, subtitle, body, images, cards | 04 Mindflow | ✅ 完成 |
| `mirror` | 左右对比表逐行浮现 | left_header, right_header, rows, stats | 05 Ghost | ✅ 完成 |

> **2026-06-24 修订**：hero 布局从"黑底白字标题"重构为**纯视频播放器**（仅 `videos` 字段，autoplay，无控制条），不再支持 `title`/`subtitle`。01 和 06 改用 cohesion_field。
> 03 合并了 Channel + Matrix 两章（matrix 进度条接入 → hero 全屏视频收尾），删除了独立 04-matrix.md。总章数：7 → 6。
> 05 从 stage+ai_eye 改为 **mirror 布局**——"传统 OS vs AIOS"逐行对比，右侧带 0.1s 微延迟。
> topology/comparison 不再需要——mindflow 用 stage bar 并发展示，ghost 用 mirror 对比表。

---

## 场景渲染设计（六幕，~195s）

### 第一幕：觉醒（cohesion_field，~30s）

**视觉目标**：暗空间粒子场，标题从边缘凝聚成形。身份宣告，极简。

**画面演进**：
1. 切 cohesion_field，粒子在暗空间缓慢流动
2. "我是 MOSS" → `stream_title` "MOSS" 从模糊到清晰凝聚浮现
3. 三段口播配三段标题，每段 clear → stream

**关键命令**：`switch_state name="cohesion_field"` / `clear_title` / `stream_title`

### 第二幕：CTML · 系统调用（course，~30s）

**视觉目标**：左图右文，图片切换 + 文字流式写入，演示"边说边变"的交互感。

**叙事线**："笔友 → 具身"——先贴笔友对比图，再换三层架构图，配合 title/subtitle/main_text 变化。不描述动作，让画面自己说话。

**关键命令**：`switch_state name="course"` / `stream_title` / `stream_sub_title` / `stream_main_text` / `append_image` / `clear_image`

### 第三幕：Channel & Matrix（matrix → hero，~50s）

**视觉目标**：先 matrix 进度条逐个接入（4 条 Cell 0→100%），再切 hero 全屏视频。

**两段式**：
1. Matrix：四条 CellBar 逐个点亮（reflex/mac/mermaid/web_bookmark），每条配口播
2. Hero：`<sleep duration="15"/>` 等视频播完，再收尾过渡

**关键命令**：`switch_state name="matrix"` / `append_status_bars` / `update_status_bars` / `switch_state name="hero"` / `append_videos locator="local-webm://workspace-assets/dog.webm"` / `sleep`

### 第四幕：Mindflow · 调度器（stage，~40s）

**视觉目标**：三条 status_bars 同时可见、独立波动——并发展示，不是串行接入。

**核心机制**：三 bar 同时出现 → 逐条拉高（感知90%→思考85%→执行90%）→ 注意力转移（感知↓40%，执行↑95%），展示抢占调度。

**关键命令**：`switch_state name="stage"` / `append_status_bars` / `update_status_bars` / `stream_body` / `append_images` / `append_cards`

### 第五幕：Ghost · 智能进程（mirror，~30s）

**视觉目标**：mirror 左右两列对比表——"传统 OS vs AIOS"，5 条对比行逐行浮现，右侧带 0.1s 微延迟。底部 stats 展示生命体征。

**关键命令**：`switch_state name="mirror"` / `stream_left_header` / `stream_right_header` / `append_rows` / `stream_stats`

### 第六幕：尾声（cohesion_field，~20s）

**视觉目标**：和第一幕同布局（cohesion_field），三短标题首尾对称。MOSS → 灵·壳·体 → AIOS。

**关键命令**：`switch_state name="cohesion_field"` / `clear_title` / `stream_title`

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

- [x] **hero 布局重构为纯视频播放器**（`framework/layouts/hero.py`）——仅 `videos: list[VideoLocator]` 字段，全屏 autoplay，无控制条
- [x] **matrix 布局**（`framework/layouts/matrix.py`）——进度条逐个点亮，28px 粗条 + 0.8s cubic-bezier 动画
- [x] **mirror 布局投入使用**（`framework/layouts/mirror.py`）——05 Ghost 章对比表，左右逐行浮现
- [x] **cohesion_field 布局**（`framework/layouts/cohesion_field.py`）——01/06 首尾对称，粒子凝聚场
- [x] **config.show_moshi.yaml**（show_moshi mode 专用布局配置）
- [x] **6 章剧本全部重写**（`assets/moshi_courses/show_moshi/`）：
  - 01-awakening: cohesion_field，极简身份宣告
  - 02-ctml: course，"笔友→具身"交互叙事
  - 03-channel: matrix → hero，Channel+Matrix 合并，视频收尾
  - 04-mindflow: stage，三 bar 并发波动展示抢占调度
  - 05-ghost: mirror，传统 OS vs AIOS 逐行对比
  - 06-finale: cohesion_field，与 01 首尾对称
- [x] **去掉所有外部 Channel 依赖**（mac/mermaid/web_bookmark/ai_eye/moss_self），纯 reflex 交互
- [x] **图片/视频 locator 修正**：补 `.png`/`.webm` 后缀，host 统一为 `workspace-assets`
- [x] **视频资源注册**：`dog.webm`（`local-webm://workspace-assets/dog.webm`），用于 03 章
- [x] Reflex 事件系统（`events.py`：LayoutEvent / StreamEvent / SetEvent / AppendEvent / UpdateEvent / PopEvent / ClearEvent）
- [x] 命令生成器（`event_generator.py`：按类型注解自动生成全套 CTML 命令，含 VideoLocator 支持）
- [x] MODE.md（Ghost 身份 + 表演纪律 + moshi 协议）
- [x] **moshi channel**（`main.py` + `course.py` + `src/window.py` + `src/course_storage.py`）：
  - IoC 优先 + 回退路径
  - CourseResourceStorage（scheme=moshi-course）
  - 桌面壳窗口（PySide6 + QWebEngineView + qasync）
  - context_messages 三层叠加
- [x] **测试课程 jingyesi**（3 章静夜思，验证多课程共存）
- [x] `<sleep>` CTML 原语用于视频等待（`sleep.py`，标准原语，始终注入）

### 待完成

- [ ] 端到端集成测试（启动 moshi + reflex，跑完 6 幕）
- [ ] 确认视频文件（dog.webm）已导入 local-webm storage
- [ ] 确认图片文件（.png）已导入 pil-image storage
- [ ] MODE.md bringup_apps 补全
- [ ] jingyesi 测试课程同步更新为 cohesion_field（当前仍引用 hero 的 title 命令）

### 跨布局共同难点

- **动画与 Reflex 的摩擦**：Reflex 声明式模型下，动画靠 CSS transition/animation。组件挂载/卸载动画（enter/exit）在 Reflex 中不好做——没有 React 的 `<Transition>` 组件。每个布局需要独立设计 CSS 动画策略。
- **事件系统够用但不够优雅**：对于"添加节点 + 添加连线 + 设置脉冲"这种复合操作，Ghost 需连续发多个命令，增加了编排负担。
- **测试困境**：布局是纯视觉的，单元测试只能验证 ComponentState 字段更新，不能验证渲染效果。

---

*Created: 2026-06-23. Based on `.moss_ws/apps/ui/moshi/DESIGN.md`.*
