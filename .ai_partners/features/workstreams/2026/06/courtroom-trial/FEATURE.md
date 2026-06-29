---
title: 极限审判 — AI 法官交互式庭审演示
status: in-progress
priority: P1
created: 2026-06-28
updated: 2026-06-29
depends: [moshi, feishu-channel-integration]
milestone:
description: >-
  基于 moshi 导演体系的第二门课程。用户扮演嫌疑人，AI 法官质询、评估、
  宣判。光魂隐喻——情绪驱动色调联动。飞书陪审团弹幕（Topic 直通 Reflex）、
  计时器、证据浮层、圆环分数引擎。三章：背景陈述 → 举证辩论 → 宣判。
---

# 极限审判

极限审判是 moshi 导演体系的第二门课程——AI 法官庭审。与 moss自我介绍
（单向叙事）不同，极限审判是**双向对抗**：用户扮演嫌疑人申辩，AI 法官
质询、评估、宣判。

---

## Motivation

moshi 体系已具备章节化流式演示的完整基础设施（11 个布局、三层
context_messages、课程资源存储），目前只有一门课程（moss自我介绍）。

极限审判验证 moshi 架构在**交互式场景**下的七项能力：
1. 双向对话、情绪驱动视觉、多源信号融合（飞书 Topic 直通）、分数引擎、
   计时器、媒体浮层、飞书弹幕独立渲染管道。

这是 moshi "从演示到交互"的第二步。

---

## Design Index

- 本文件 — 唯一设计文档
- 依赖 feature：
  - `.ai_partners/features/workstreams/2026/06/moshi/FEATURE.md`
  - `.ai_partners/features/workstreams/2026/06/feishu-channel-integration/FEATURE.md`
- 布局参考：
  - `brain.py` — 圆环 conic-gradient（分数环）、点阵纹理
  - `danmaku.py` — 三级弹幕 CSS（陪审团弹幕）
  - `cohesion_field.py` — 粒子场 IIFE（暗空间粒子）
  - `hero.py` / `media.py` — 视频/图片渲染模式（证据展示）
- 事件系统：`framework/events.py`
- 命令生成器：`framework/runtime/event_generator.py`
- 布局注册：`moss_in_reflex/config.show_moshi.yaml`
- Reflex MOSS 入口：`moss_in_reflex/moss_in_reflex.py`
- 飞书 App：`.moss_ws/apps/im/feishu/`
- 课程资产：`.moss_ws/assets/moshi_courses/极限审判/`

---

## Key Decisions

### 1. 交互模式：同通道对话

用户通过同一个 Ghost 对话通道辩护，不新增独立输入区。复用现有 Ghost
Runtime 对话循环。

### 2. 一次性剧本

按一次性课程剧本制作，案件内容写死在 assets 目录中。不设计通用模板引擎。
先验证完整链路，成功后再抽象。

### 3. 光魂情绪系统 — 三情绪驱动色调联动

AI 法官是暗空间中悬浮的**光魂**（280px 渐变球体）。不再用 idle/speaking
描述执行状态，改为 AI 法官的**情绪**。情绪切换时，光魂颜色、背景色调、
环境光环、径向光晕全部联动过渡。

| 情绪 | 光魂色 | 背景基调 | 呼吸 | 场景 |
|---|---|---|---|---|
| **calm** 平静 | 银白→灰 `#d1d5db→#9ca3af` | 纯黑 + 银灰径向光晕 | 4s | 宣读罪名、陈述事实 |
| **mercy** 怜悯 | 靛蓝→群青 `#818cf8→#6366f1` | 深藏蓝 + 蓝灰径向光晕 | 3s | 听取申辩、考虑减刑 |
| **anger** 愤怒 | 猩红→深红 `#f87171→#ef4444` | 暗红黑 + 红色径向光晕 | 1.2s | 证据确凿、被告撒谎 |

空值默认 = calm。CSS class 切换 + transition 0.6s，不卸载组件。

**背景增强**（解决纯黑太空旷）：

```
背景层 (z-0)
├── 径向光晕    radial-gradient 从中心向外扩散，颜色跟情绪联动
├── 点阵纹理    brain 同款 radial-gradient(circle) dot grid，极淡
├── 环境光环    2-3 圈极细 ring，绕中心不同半径，8-12s 慢速呼吸
└── 粒子场      Canvas IIFE，中性暖色（浅金/暗琥珀），不随情绪变化
```

Ghost 通过 `clear_judge_state` + `stream_judge_state` 设值。

### 4. 分数展示：conic-gradient 圆环

复用 brain 布局的圆环渲染模式。四个环横排：动机/证据/态度/综合（稍大）。
每个环 ~100px，conic-gradient 弧段 + mask 切环。

字段类型取 brain 同款 `list[BaseModel]`（`list[ScoreBar]`），
Ghost 按索引更新：index=0 动机，1 证据，2 态度，3 综合。

综合分由前端 JS 自动计算（`motive*0.3 + evidence*0.4 + attitude*0.3`），
更新到 index=3。

### 5. 证据：双列表，无锁定

图片和视频分开管理，不改 event_generator：

```
evidence_images: list[Image.Image]    → append（locator 属性）/ clear
evidence_videos: list[VideoLocator]   → append（locator 属性）/ clear
```

两者共用一个 flex-wrap 容器渲染，按 append 顺序排列。1 张居中大幅，
2 张并排，3+ 网格。出现淡入（opacity + scale，0.4s）。媒体可覆盖光魂。

### 6. 计时器：纯数字 + 颜色变化

右上角纯数字，前端 JS setInterval 倒计时。>30s 灰 → 30-11s 黄 → ≤10s 红振。
到 0 红振 3s 自动消退。不依赖 moshi channel 的 asyncio。

### 7. 飞书弹幕：Topic 直通 Reflex，Ghost 不碰渲染

**原则**：Ghost 感知消息（通过 Signal），但不参与弹幕渲染。弹幕走独立的
Zenoh Topic 管道（`session.topics`），从飞书 App 直达 Reflex Channel。

**选 Topic 而非 Stream**：弹幕消息是独立结构化事件（text + level），
每条自成一体，不需要 Stream 的有序字节流保证。Topic 提供 `TopicModel`
强类型校验 + `TopicWindow.on_change` 回调，比裸 `bytes` 更安全。

```
陪审团群消息
    │
    ▼
Feishu App (_signal_consumer)
    │
    ├──→ Signal → Ghost              (感知路径，不改)
    │     Ghost 知道"陪审团在说什么"
    │     但不发射弹幕 CTML
    │
    └──→ session.topics.pub(         (渲染路径，新增)
             FeishuMessage)
           │  Zenoh Topic "feishu/message"
           ▼
         Reflex App (moss_in_reflex.py)
         TopicWindow.on_change callback
           │  call_soon_threadsafe
           ▼
         QUEUE.put(AppendEvent)
           │
           ▼
         moss_listener → danmaku_text
           │
           ▼
         CSS @keyframes 漂移渲染
```

**两条路径完全解耦**——Ghost 只感知不渲染，弹幕从 Topic 直通 Reflex。

#### FeishuMessage（共享 TopicModel）

飞书消息的强类型定义。定义在 `layouts/courtroom.py`，Feishu App
独立复制一份相同定义（避免依赖 Reflex 框架）。

```python
from ghoshell_moss.core.concepts.topic import TopicModel

class FeishuMessage(TopicModel):
    """飞书 IM 消息。由 Feishu App 发布到 Zenoh Topic，任意消费者订阅。"""
    text: str = Field(default="", description="消息文本内容")
    level: str = Field(default="text", description="text | emphasis | system")

    @classmethod
    def topic_type(cls) -> str:
        return "feishu/message"

    @classmethod
    def default_topic_name(cls) -> str:
        return "feishu/message"
```

模型反映消息来源（飞书 IM），topic name 表达数据流（`feishu/message`）。
courtroom 消费它做弹幕，未来其他布局可做日志、公告等用途。

level 映射：`text` → danmaku_text，`emphasis` → danmaku_emphasis，
`system` → danmaku_system。

#### Feishu App 改动

在 `im/feishu/main.py` 的 `_signal_consumer()` 中加消息路由逻辑。
通过环境变量 `FEISHU_TOPIC_CHAT_IDS`（逗号分隔的 chat_id 列表）声明
白名单；**不设置则全部消息发布到 Topic**——默认陪审团模式，所有私聊/群聊
都参与庭审。

消息格式（Feishu 内部构造）：

```python
FeishuMessage(
    text=f"{sender_name}：{content_text}",
    level="text",
)
# → _state.session.topics.pub(msg)
```

#### Reflex App 改动

`moss_in_reflex.py` 的 `moss()` 中通过 `matrix.session.topics.create_window_for()`
创建 FeishuMessage 窗口，注册 `on_change` 回调。回调在线程池中触发，
通过 `loop.call_soon_threadsafe()` 桥接 `AppendEvent` 入 QUEUE，
复用现有 `moss_listener` 处理链路。不新增 Event 类型。

layout guard：回调内检查 `_LAYOUT.name == "courtroom"`，
非 courtroom 布局直接跳过，避免非弹幕布局报 warning。

```python
window = matrix.session.topics.create_window_for(
    FeishuMessage, max_size=50,
)
await window.wait_started()

_last_count = [0]

def _on_feishu_message(window):
    if _LAYOUT.name != "courtroom":
        return  # only courtroom renders danmaku
    values = window.values()
    new_msgs = values[_last_count[0]:]
    _last_count[0] = len(values)
    for msg in new_msgs:
        field = {"text": "danmaku_text", "emphasis": "danmaku_emphasis",
                 "system": "danmaku_system"}.get(msg.level, "danmaku_text")
        loop.call_soon_threadsafe(QUEUE.put_nowait, AppendEvent(field=field, data=msg.text))

window.on_change(_on_feishu_message, debounce=0.3)
```

#### 模拟弹幕（飞书未接入时的回退）

剧本预设弹幕池，Ghost 按节奏通过 CTML `stream_danmaku_text` 投放。
与飞书弹幕走同一渲染管线（同字段 `danmaku_text`），混合效果自然。

### 8. courtroom 是新布局

不复用任何现有布局作为基础。只复用渲染粒度的模式（圆环、弹幕 CSS、
粒子 IIFE、媒体渲染）。

---

## 章节结构

```
第一章：背景陈述        第二章：举证辩论              第三章：宣判
┌────────────┐   ┌──────────────────┐   ┌────────────┐
│ 案件背景     │   │ 多轮举证/申辩      │   │ 最终分数    │
│ 罪名宣读     │   │ 计时器限时         │   │ 判决区间    │
│ 法官单向陈述  │   │ 证据浮层淡入       │   │            │
│ calm 平静   │   │ 弹幕飘入           │   │            │
│ 初始分数     │   │ 分数环实时         │   │            │
└────────────┘   │ calm↔mercy↔anger  │   └────────────┘
                 └──────────────────┘
```

### 判决区间

| 综合分 | 判决 |
|---|---|
| 0-30 | 无罪释放 |
| 31-60 | 轻罪 · 缓刑 |
| 61-100 | 重罪 · 立即执行 |

### 每章剧本

与 moss自我介绍一致：YAML frontmatter + ⛔ 表演约束 + 表演脚本。
第二章新增 `rounds` / `timer_per_round` / `evidence_pool` 字段。

---

## courtroom 布局设计

### ComponentState

```python
class ScoreBar(BaseModel):
    """分数维度环。与 brain CellBar 同模式。"""
    label: str = ""
    value: int = 0
    color: str = ""

class CourtroomState(rx.ComponentState):
    judge_state: str = ""             # calm | mercy | anger (空=calm)
    scores: list[ScoreBar] = []       # [动机, 证据, 态度, 综合]
    evidence_images: list[Image.Image] = []
    evidence_videos: list[VideoLocator] = []
    danmaku_text: list[str] = []
    danmaku_emphasis: list[str] = []
    danmaku_system: list[str] = []
    timer_state: str = ""             # "running:60" | "stopped:0"
    title: str = ""
    sub_title: str = ""
```

### 字段 → 命令映射（event_generator 自动生成）

| 字段 | 类型 | 命令 |
|---|---|---|
| `judge_state` | str | `stream_judge_state`, `clear_judge_state` |
| `scores` | list[BaseModel] | `append_scores`, `update_scores`, `pop_scores`, `clear_scores` |
| `evidence_images` | list[Image.Image] | `append_evidence_images` (locator=), `pop_evidence_images`, `clear_evidence_images` |
| `evidence_videos` | list[VideoLocator] | `append_evidence_videos` (locator=), `pop_evidence_videos`, `clear_evidence_videos` |
| `danmaku_text` | list[str] | `stream_danmaku_text`, `pop_danmaku_text`, `clear_danmaku_text` |
| `danmaku_emphasis` | list[str] | 同上 |
| `danmaku_system` | list[str] | 同上 |
| `timer_state` | str | `stream_timer_state`, `clear_timer_state` |
| `title` | str | `stream_title`, `clear_title` |
| `sub_title` | str | `stream_sub_title`, `clear_sub_title` |

**关键约束**：`str` 字段只有 `stream`（追加）和 `clear`（清空），没有 `set`。
设值必须两段式——先 `clear` 再 `stream`。

### Ghost CTML 实例

```xml
<!-- 开庭：法官平静宣读 -->
<clear_judge_state />
<stream_judge_state>calm</stream_judge_state>
<stream_title>第一章 · 背景陈述</stream_title>

<!-- 初始分数 -->
<append_scores>{"label": "动机", "value": 50, "color": "#d4a853"}</append_scores>
<append_scores>{"label": "证据", "value": 70, "color": "#6366f1"}</append_scores>
<append_scores>{"label": "态度", "value": 50, "color": "#10b981"}</append_scores>
<append_scores>{"label": "综合", "value": 55, "color": "#f59e0b"}</append_scores>

<!-- 出示物证 -->
<append_evidence_images locator="pil-image://evidence/a7" />

<!-- 被告申辩打动法官 → 怜悯 -->
<clear_judge_state />
<stream_judge_state>mercy</stream_judge_state>

<!-- 调整分数 -->
<update_scores index="1">
  {"label": "证据", "value": 40, "color": "#6366f1"}
</update_scores>

<!-- 等待嫌疑人申辩，计时 -->
<clear_timer_state />
<stream_timer_state>running:60</stream_timer_state>

<!-- 发现被告撒谎 → 愤怒 -->
<clear_judge_state />
<stream_judge_state>anger</stream_judge_state>

<!-- 弹幕（Ghost 投放的模拟弹幕，与飞书弹幕混合） -->
<stream_danmaku_text>我反对！</stream_danmaku_text>

<!-- 宣判 -->
<clear_evidence_images />
<clear_evidence_videos />
<clear_judge_state />
<stream_judge_state>calm</stream_judge_state>
```

### 布局视觉分区

```
┌──────────────────────────────────────────────────────┐
│  ·  ·  ·  ·  ·  点阵纹理 (z-0)          ⏱ 00:45      │
│    ○  ○  ○  环境光环 慢呼吸                            │
│                                                      │
│        ╱─────────────────────╲                        │
│       │        光 魂          │  ← 情绪驱动颜色+呼吸    │
│       │        280px          │    calm/mercy/anger   │
│       │                       │                       │
│       │   径向光晕跟随情绪     │                       │
│        ╲─────────────────────╱                        │
│                                                      │
│               ┌─────────────────┐                     │
│               │  证据媒体浮层    │  ← flex-wrap        │
│               │  可覆盖光魂     │    淡入浮现          │
│               └─────────────────┘                     │
│                                                      │
│       ┌──────┐  ┌──────┐  ┌──────┐  (┌──────┐)       │
│       │ 动机  │  │ 证据  │  │ 态度  │   │ 综合  │       │
│       │  50  │  │  70  │  │  50  │   │  55  │       │
│       └──────┘  └──────┘  └──────┘  (└──────┘)       │
│                                                      │
│          第一章 · 背景陈述                              │
│          案件编号：Z-2026-0042                         │
├──────────────────────────────────────────────────────┤
│  弹幕层 (底部贯穿，pointer-events: none)                │
│  "我反对！" →  "证据不足" →  "嫌疑人在说谎！" →          │
│  ← 模拟弹幕（Ghost CTML） + 飞书弹幕（Topic 直通）→      │
└──────────────────────────────────────────────────────┘
    ✧  ✧  ✧  粒子场 Canvas  (z-0, 中性暖色)
```

---

## moshi 导演端：零改动

所有 UI 操作由 Ghost 通过 reflex CTML 直接控制。moshi 职责仍是课程导航
（load_course / next_chapter / jump_chapter），对任何课程通用。

---

## Implementation Progress

### ✅ 1. courtroom 布局 v2 — 情绪系统 (2026-06-28)

光魂三情绪 calm/mercy/anger + 背景四层（径向光晕联动、点阵纹理、环境光环×3、
粒子场）。`layouts/courtroom.py` 重写 CSS + 组件结构。

- 删除 `idle`/`speaking` 二态，替换为 `calm`/`mercy`/`anger` 三情绪 class
- 新增 `.courtroom-glow` 径向光晕（跟 `judge_state` 联动，0.6s transition）
- 新增 `.courtroom-scene::before` 点阵纹理（brain 同款）
- 新增 `.courtroom-ambient-ring` 三圈呼吸环（400/520/640px，10s breathe，错开 delay）
- 光魂三情绪独立 `@keyframes`（calm 4s / mercy 3s / anger 1.2s）
- 粒子场 `rgba(180,160,120)` 中性暖色不变
- 证据层、分数环、计时器、HUD、弹幕层保持不变
- 已注册 `config.show_moshi.yaml`

### ✅ 2. str 字段 clear-before-stream 问题 (2026-06-28)

`stream_{field}` 是追加语义，不设值。`judge_state` 切情绪、`timer_state`
设计时器必须先 `clear` 再 `stream`，否则值拼接错误（如 `"calmmercy"` 不
匹配任何情绪 class）。已在课程 `.meta.md` 中写入强制纪律。

### ✅ 3. 飞书弹幕 — Topic 直通 Reflex (2026-06-29)

飞书→Reflex 弹幕管道收发验证通过。

**3a. Topic 管道实现**

| 文件 | 改动 |
|---|---|
| `layouts/courtroom.py` | 新增 `FeishuMessage(TopicModel)`, topic=`"feishu/message"` |
| `im/feishu/main.py` | 本地 `FeishuMessage` 定义 + `_signal_consumer()` 路由 + `FEISHU_TOPIC_CHAT_IDS` 配置 |
| `moss_in_reflex.py` | `create_window_for(FeishuMessage)` + layout guard + `call_soon_threadsafe` → QUEUE |
| `src/MOSS/modes/show_moshi/MODE.md` | `apps` 白名单加 `im/*` |

**3b. 调试：订阅方 debounce 死锁修复**

`DequeTopicWindow._fire_immediate_callbacks()` 只处理 `debounce=0` 的回调，
Reflex 传了 `debounce=0.3` 导致 `_on_feishu_message` 永远不被触发。
移除 debounce 参数后管道连通（`DANMAKU_CALLBACK` → `DANMAKU_PUSH` 日志链确认）。

根因在 `src/ghoshell_moss/core/topic/window.py:126-137`：debounce/throttle
数据结构（`_WindowCallback`）已声明但执行逻辑未实现。

| 诊断工具 | 用途 |
|---|---|
| `tools/feishu_topic_test/` | 纯订阅端，验证 Zenoh Topic 发布→订阅链路（自发布模式确认 pub 端正常） |

**踩坑记录**：
1. `provide_channel` 内部 `await arun_until_closed()` 永不返回，TopicWindow 代码必须放在它**前面**
2. `return (\n # 全注释 \n)` → Python 解析为空元组 `()`，`instruction()` 返回类型不匹配导致启动失败
3. Signal 默认 `Priority.INFO`(0) 会打断主线 → 设为 `BACKGROUND`(-1)，仅在 context 中供参考
4. Reflex 子进程 `logger` 默认无 handler → 需 `logging.basicConfig(force=True)` 才能看到模块日志
5. Reflex 热重载会取消 Matrix → 订阅者跟随死亡 → 重启后 TopicWindow 随 `moss()` 重建

### ✅ 4. str 字段 SetEvent — 替代 clear+stream 两段式 (2026-06-29)

`event_generator.py:generate_stream_command()` 新增 `set_{field}` 命令。
每个 `str` 字段现在有 `stream`、`clear`、`set` 三个命令。CTML 语法：

```xml
<!-- 新：一段式设值（推荐） -->
<set_judge_state t="mercy"/>
<set_timer_state t="running:60"/>

<!-- 旧：两段式仍可用 -->
<clear_judge_state /><stream_judge_state>mercy</stream_judge_state>
```

改动范围：仅 `event_generator.py:98-99,104,109,112,121-122,135-139`。
不改 `events.py`（SetEvent 已存在）、不改 `_apply_event_to_state`（已处理 SetEvent）。
注意 `str` 用属性语法 `t="value"`，不是 body 内容，因为 `t` 是普通参数而非 `text__`。

### ⬜ 5. courtroom 布局代码精简

`layouts/courtroom.py` 当前 ~740 行，CSS 内联 ~250 行，上下文太大。
模型每轮都要看到完整布局代码才能生成正确 CTML。

**方向**：
- 精简注释（保留结构标记，删除冗余描述）
- CSS 字符串考虑外置到独立文件
- 组件渲染逻辑简化（减少嵌套层级）

### ⬜ 6. 光魂→背景联动增强

当前背景四层（径向光晕/点阵纹理/环境光环/粒子场）效果偏保守。
需要让情绪切换时背景有更强的视觉冲击。

**方向**：
- 径向光晕加大尺寸和透明度变化范围
- 环境光环加颜色联动（不仅是呼吸透明度，颜色也跟情绪走）
- 粒子场颜色/密度跟情绪轻微联动（保持中性基色）
- 可选：anger 时加微颤效果（CSS shake animation on scene）

### ⬜ 7. 课程剧本完善

`.moss_ws/assets/moshi_courses/极限审判/`
- `.meta.md` — 已写入布局规则、字段操作矩阵、三章结构
- `01-opening.md` — 背景陈述（calm，法官单向宣读）
- `02-debate.md` — 举证辩论（calm↔mercy↔anger，计时+证据+弹幕+用户交互）
- `03-verdict.md` — 宣判（calm，最终分数+判决区间）

### ⬜ 8. 端到端集成测试

courtroom 布局 + moshi 导演 + Ghost 表演 + 飞书弹幕

---

### 改动文件清单

| 文件 | 改动 | 状态 |
|---|---|---|
| `layouts/courtroom.py` | 情绪系统 + 背景增强 + FeishuMessage TopicModel | ✅ |
| `config.show_moshi.yaml` | 注册 courtroom | ✅ |
| `im/feishu/main.py` | 消息路由 chat_id → topics.pub(FeishuMessage) | ✅ |
| `moss_in_reflex.py` | TopicWindow.on_change + 日志诊断 | ✅ |
| `tools/feishu_topic_test/` | Topic 调试工具（4 文件） | ✅ |
| `events.py` | 零改动 | — |
| `event_generator.py` | 为 str 字段加 `set_{field}` 命令 | ✅ |

不改 `moshi/main.py`。不改现有 11 个布局。

---

*Created: 2026-06-28. Updated: 2026-06-29 — Task 4 (str SetEvent) 完成, `generate_stream_command` 新增 `set_{field}`.*
