---
title: Moshi — show_moshi 模式导演与演示布局体系
status: in-progress
priority: P1
created: 2026-06-23
updated: 2026-06-23
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

- 设计文档：`.moss_ws/apps/ui/moshi/DESIGN.md`
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

---

## 新布局规划

| 布局 | 用途 | 关键字段 | 对应章节 | 状态 |
|---|---|---|---|---|
| `hero` | 全屏开场/收束 | title, subtitle, background | 01 Awakening, 07 Finale | ✅ 完成 |
| `code_split` | 代码 + 执行结果分屏 | code_block, result_block, caption | 02 CTML | ❌ 待实现 |
| `capability_grid` | 能力卡片网格 + 树形展开 | items, active_item, tree_mode | 03 Channel | ❌ 待实现 |
| `topology` | 节点拓扑图 + 连线动画 | nodes, edges, active_path | 04 Matrix, 05 Mindflow | ❌ 待实现 |
| `comparison` | 左右对比表 | left_header, right_header, rows, stats | 06 Ghost | ❌ 待实现 |

### 各布局难点

**code_split**（中等）：代码语法高亮——Reflex 无内置方案，首版可用纯色等宽终端风格，后续嵌入 highlight.js。打字机逐字效果已有 stream 事件支撑。

**capability_grid**（中高）：卡片逐个点亮（CSS animation-delay 编排）；树形视图切换（`tree_mode` 字段切换平铺网格 ↔ 递归树形组件）。

**topology**（最难）：Reflex 无 Canvas API，需手写 SVG（circle/text/line/path）；节点布局算法（首版硬编码坐标或圆形布局）；连线脉冲动画（SVG animateMotion 或 stroke-dashoffset）；Mindflow 章复用（三循环旋转环 + ai_eye 联动），与 Matrix 章星形拓扑的视觉需求完全不同。

**comparison**（中低）：逐行动画展开；左右列对齐；可选 stats 统计卡片。相对最友好。

---

## moshi App 职责

### 做
- 管理章节状态（当前第几章）
- 提供章节上下文（主题、可用资源列表、建议布局）
- 章节推进（next / jump / list）
- 资源按章节归属登记

### 不做
- 不直接切换 reflex 布局
- 不直接过滤 reflex 的 context_messages
- 不感知 reflex 的存在
- 不干预 Ghost 的表演决策

### 暴露给 Ghost 的命令

```
<apps.ui_moshi:get_context />     → 返回当前章节上下文
<apps.ui_moshi:next_chapter />    → 推进到下一章
<apps.ui_moshi:jump_chapter id /> → 跳转到指定章节
<apps.ui_moshi:list_chapters />   → 列出全部章节
```

---

## Implementation Notes

### 已完成

- [x] hero 布局（`framework/layouts/hero.py`，全屏开场，背景图 + 标题/副标题）
- [x] 7 章内容资产（`assets/moshi_courses/`，含 `_meta.md` YAML 索引 + 7 个章节 md）
- [x] MODE.md（Ghost 身份 + 表演纪律 + moshi 协议）
- [x] Reflex 事件系统（`events.py`：LayoutEvent / StreamEvent / SetEvent / AppendEvent / UpdateEvent / PopEvent / ClearEvent）
- [x] 命令生成器（`event_generator.py`：365 行，按类型注解自动生成全套 CTML 命令，覆盖 str / list[str] / list[Image] / list[BaseModel] / list[dict] / BaseModel / Image 全部 7 种类型）
- [x] Layout 快照系统（`layout_snapshot.py`：119 行，通过 Reflex get_state() 读取 ComponentState 字段值，类型感知摘要压缩，支持 JSON 持久化）
- [x] show_moshi mode manifests（8 文件齐全：channels 导入了 AppStoreChannel + mac + mermaid + web_bookmark；nuclei 声明了 AudioNucleusMeta；configs/providers/resources/topics 继承全局；contracts 预留空文件）

### 待完成

- [ ] 实现 moshi channel 逻辑（`main.py`）：章节状态管理 + `get_context` / `next_chapter` / `jump_chapter` / `list_chapters` 四个命令
- [ ] 实现 `comparison` 布局
- [ ] 实现 `code_split` 布局
- [ ] 实现 `capability_grid` 布局
- [ ] 实现 `topology` 布局（Matrix + Mindflow 两章复用）
- [ ] 创建 `config.show_moshi.yaml`（注册全部 5 个布局到 show_moshi mode）
- [ ] 端到端集成测试

### 跨布局共同难点

- **动画与 Reflex 的摩擦**：Reflex 声明式模型下，动画靠 CSS transition/animation。组件挂载/卸载动画（enter/exit）在 Reflex 中不好做——没有 React 的 `<Transition>` 组件。每个布局需要独立设计 CSS 动画策略。
- **事件系统够用但不够优雅**：对于"添加节点 + 添加连线 + 设置脉冲"这种复合操作，Ghost 需连续发多个命令，增加了编排负担。
- **测试困境**：布局是纯视觉的，单元测试只能验证 ComponentState 字段更新，不能验证渲染效果。

---

*Created: 2026-06-23. Based on `.moss_ws/apps/ui/moshi/DESIGN.md`.*
