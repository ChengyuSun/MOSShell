# moshi — Show Director

Moshi 是 show_moshi 模式的导演。管理章节状态，为 Ghost 提供上下文，但不干预渲染层。

---

## 架构原则

**Ghost 是唯一集成点。** 两个工具互不知道对方存在。

```
┌──────────────┐     ┌──────────────┐
│    moshi     │     │    reflex    │
│              │     │              │
│ 章节状态管理  │     │ 多布局渲染    │
│ 资源归属登记  │     │ 流式事件路由  │
│              │     │              │
│ 不知道 reflex │     │ 不知道 moshi  │
└──────┬───────┘     └──────┬───────┘
       │                    │
       │  context_messages  │  context_messages
       │  "当前是第X章"     │  "当前 layout 是 Y，
       │  "可用资源是[...]" │   可用命令是 [...]"
       │                    │
       └────────┬───────────┘
                │
                ▼
         ┌─────────────┐
         │    Ghost     │
         │             │
         │ 读取双方上下文│
         │ 自主决策：    │
         │  用什么布局   │
         │  展示什么资源 │
         │  说什么话     │
         └─────────────┘
```

---

## moshi 职责边界

### 做
- 管理章节状态（当前第几章）
- 提供章节上下文（主题、可用资源列表、建议布局）
- 章节推进（next / jump）
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

## 三层约束机制

| 约束类型 | 实现方式 | 说明 |
|---|---|---|
| 可用 CTML 命令 | **Layout 自动限定** | 布局有多少字段，就自动生成多少 stream/set/append/clear 命令 |
| 可用资源 | **moshi context + Ghost 决策** | moshi 列出当前章节资源，Ghost 自主选择使用 |
| 表演范围 | **MODE.md 章节描述** | Ghost 读章节主题，在约束内自由发挥 |

---

## 章节数据

章节数据存储在 `.moss_ws/assets/moshi_courses/`，与 moshi app 代码解耦：

```
.moss_ws/assets/moshi_courses/
├── _meta.md             ← frontmatter 章节索引 + body 知识背景
├── 01-awakening.md
├── 02-ctml.md
├── 03-channel.md
├── 04-matrix.md
├── 05-mindflow.md
├── 06-ghost.md
└── 07-finale.md
```

**MODE.md** 只保留 Ghost 身份 + 表演纪律 + moshi 协议（~70行）。
章节结构和细则由 moshi 从 assets 目录加载，通过 `get_context()` 暴露给 Ghost。

---

## 新布局规划

现有 4 个布局（stage / simple / media / lesson）为日常内容设计，不适用于演示场景。计划新建 5 个：

| 布局 | 用途 | 关键字段 |
|---|---|---|
| `hero` | 全屏开场/收束 | title, subtitle, background_image, particle_theme |
| `code_split` | 代码 + 执行结果分屏 | code_block, result_block, caption |
| `capability_grid` | 能力卡片网格 + 树形展开 | items, active_item, tree_mode |
| `topology` | 节点拓扑图 + 连线动画 | nodes, edges, active_path |
| `comparison` | 左右对比表 | left_header, right_header, rows, stats |

每个布局定义一个 `ComponentState` 子类，字段自动生成全套 CTML 命令。

---

## 流式渲染节奏

保持 show mode 的 **一句一动** 节奏：

```
Ghost 说话（TTS）         CTML 动作                    reflex 渲染
─────────────────────    ──────────────────────    ─────────────────
"你好，我是 MOSS。"    →  <stream_title>MOSS</>    →  标题逐字浮现
"一个为 AI 设计的 OS。" →  <stream_subtitle>...</> →  副标题跟上
"看，三层架构。"        →  <append_images .../>    →  架构图淡入
```

moshi 不介入表演节奏，只在章节边界提供上下文。

---

## 待完成

- [ ] 确定最终章节结构和各章资源清单
- [ ] 设计 5 个新布局的字段规范
- [ ] 实现 moshi channel（章节状态 + context_messages）
- [ ] 创建 show_moshi MODE.md（Ghost 表演指令）
- [ ] reflex config.show_moshi.yaml（多布局注册）
- [ ] 端到端集成测试

---

*Created: 2026-06-23. This file tracks the ongoing design of moshi + show_moshi.*
