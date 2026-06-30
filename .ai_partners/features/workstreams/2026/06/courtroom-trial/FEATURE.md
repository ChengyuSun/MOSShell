---
title: 极限审判 — AI 法官交互式庭审演示
status: in-progress
priority: P1
created: 2026-06-28
updated: 2026-06-30
depends: [moshi, feishu-channel-integration]
milestone:
description: >-
  基于 moshi 导演体系的第二门课程。用户扮演嫌疑人，AI 法官质询、评估、
  宣判。光线缠绕核心——情绪驱动全屏光波联动。飞书陪审团弹幕（Topic 直通 Reflex）、
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

### 3. 光魂情绪系统 — 三情绪驱动色调联动（v3：光线缠绕核心）

AI 法官是暗空间中央的**动态光线缠绕体**（10 条椭圆弧线/环，多轴多速旋转）。
不再用 idle/speaking 描述执行状态，改为 AI 法官的**情绪**。情绪切换时，
光线颜色、全屏光波、环境光环全部联动过渡。

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

Ghost 通过 `set_judge_state t="calm|mercy|anger"` 设值（推荐一段式）。

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
| `judge_state` | str | `set_judge_state`（推荐）, `stream_judge_state`, `clear_judge_state` |
| `scores` | list[BaseModel] | `append_scores`, `update_scores`, `pop_scores`, `clear_scores` |
| `evidence_images` | list[Image.Image] | `append_evidence_images` (locator=), `pop_evidence_images`, `clear_evidence_images` |
| `evidence_videos` | list[VideoLocator] | `append_evidence_videos` (locator=), `pop_evidence_videos`, `clear_evidence_videos` |
| `danmaku_text` | list[str] | `stream_danmaku_text`, `pop_danmaku_text`, `clear_danmaku_text` |
| `danmaku_emphasis` | list[str] | 同上 |
| `danmaku_system` | list[str] | 同上 |
| `timer_state` | str | `set_timer_state`（推荐）, `stream_timer_state`, `clear_timer_state` |
| `title` | str | `set_title`（推荐）, `stream_title`, `clear_title` |
| `sub_title` | str | `set_sub_title`（推荐）, `stream_sub_title`, `clear_sub_title` |

**注意**：`str` 字段自 2026-06-29 起支持 `set_{field} t="value"` 一段式设值（属性语法），
原有的 `clear` + `stream` 两段式仍可用但不推荐。

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

## moshi 导演端：最小改动

- `main.py` Layer 3 移除自动注入的 next_chapter 推进指令，推进方式交还剧本
- `next_chapter` / `jump_chapter` observe 文本中性化，去除 push 语气

其余 moshi 逻辑不变。

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

### ✅ 5. courtroom 布局代码精简 (2026-06-29)

`layouts/courtroom.py` 808 行 → 224 行（-72%）。CSS 外置到
`framework/components/courtroom_styles.py`（464 行），计时器脚本外置到
`framework/components/countdown_timer.py`（117 行，可复用）。

- 情绪 class 抽取为 `_emotion_class()` 辅助函数
- `timer_elements()` 工厂函数，`*` 解包注入组件树
- `rx.cond` 从 11 处减少到 8 处，情绪驱动统一到根节点

### ✅ 6. 光魂→全屏动效重构 (2026-06-29)

**球体光魂 → 光线缠绕核心**：10 条椭圆弧线/环代替 280px 渐变球体。
5 种倾斜角度（rotateX 20°~72°），4 种弧段变体（全环/半弧），
旋转速度 5s~19s 正反转交替，4 条有独立 opacity 脉冲（2.5s~4s），
核心整体 ±12px 浮动。

**全屏光波**：双层径向光晕 500→2000px / 1000→3600px；
声呐脉冲 900→2400px，从中心扩散到全屏。

**光环联动**：四圈光环加 rotateX(60°) 3D 倾斜，颜色跟情绪联动，
呼吸旋转合并 keyframes。

- 删除粒子场（`_PARTICLE_SCRIPT` + canvas）
- 删除弹幕 signal store（死代码）
- 新增 `.courtroom-sonar` 声呐脉冲元素
- 新增 `.courtroom-core` + 10 × `.filament`
- Glow/sonar/rings 全部全屏化

### ✅ 7. 课程剧本完善 (2026-06-29)

`.moss_ws/assets/moshi_courses/moss审判/`（最终目录名，非 极限审判）

**案件**：蓝月酒吧命案。死者中刀，现场另有两枚弹壳。嫌疑人声称夺枪自卫。
**核心设计**：闭合式审讯——五个问题，每问 2-3 个选项，Ghost 根据答案匹配分支。
**审讯树**：Q1 谁约谁 → Q2 刀是谁的 → Q3 惯用手（陷阱）→ Q4 几枪 → Q5 枪在哪
→ 证物袋反转（死者手机消息揭露第三人有灭口动机）。

| 文件 | 行数 | 内容 |
|------|------|------|
| `.meta.md` | ~110 | 案情背景、布局规则（含 `set_` 一段式推荐）、证据索引、判决区间 |
| `01-opening.md` | ~115 | calm 单向宣读，6 项证据叠加积累，初始分数 |
| `02-debate.md` | ~360 | 五轮闭合式审讯树（每问 3-4 分支）+ 证物袋反转汇合 |
| `03-verdict.md` | ~115 | 三档判决（无罪释放/轻罪缓刑/重罪），各自出示判决书图片 |

**关键设计决策**：
- 全程 courtroom 单一布局——仅第一章切一次，后两章不重切
- CTML 命令统一 `apps.ui_reflex:` 前缀
- 闭合式问题代替开放式申辩，Ghost 判断精确可收敛
- `performance.rhythm` 新增禁止描述系统操作（"已加载课程"等）
- 01-opening 新增 observe 判断规则：匹配到 "Switched to layout" 即确认切换成功，禁止重试

**新素材**（用户提供）：
| 素材 | 用途 |
|------|------|
| `死者手机消息.png` | 证物袋反转 |
| `释放判决.png` / `拘禁判决.png` / `死刑判决.png` | 第三章三档判决书 |
| `证物-现场的枪支.jpeg` | Q5 枪的下落 |
| `人证-女邻居和警察沟通.jpeg` | 备用 |

### ✅ 13. 剧本 locator 格式修正 (2026-06-30)

全部 11 个文件的 locator 从 `scheme://名称` 修正为 `scheme://workspace-assets/名称.扩展名`。
根因：locator 解析器 `_parse_locator()` 要求三段式 `scheme://host/path`，缺 `/` 即报
"Invalid locator (missing /path)"。所有素材已通过 image_importer 注册到 `workspace-assets` host，
扩展名从 JSONL manifest 确认。

### ✅ 14. moshi context_messages 去推进指令 (2026-06-30)

`main.py` Layer 3 移除自动注入的 `next_chapter` 推进指令（6 行）。推进方式（next_chapter / jump_chapter）
由各章剧本自行决定，moshi 不再越权。

### ✅ 15. 第二章分支化重写 (2026-06-30)

旧 `02-debate.md`（360 行线性巨型文件）替换为 9 个分支章：

```
opening → q1 → q2-friend / q2-dispute / q2-stranger / q2-confess
                  ↓
                q3 → q4-defense / q4-admit / q4-silent
                        ↓
                      verdict
```

- 每章 40-80 行，自含分支规则 + CTML 脚本，末行明确 `jump_chapter` 目标
- 三条叙事线：清白（自卫）、灰色（自携刀具）、铁证（沉默/撒谎）
- 坦白出口 `q2-confess` 从任意节点可达，审讯终止直跳宣判
- 证物袋反转嵌入三个 q4 终章，同一手机消息三条线不同语气解读
- 第一章证据节奏改为 4 组循环展示（并排→清→单张→清→并排→清→单张留）
- 03-verdict.md 重写为分支感知宣判

### ✅ 16. .meta.md 瘦身 (2026-06-30)

从 195 行压缩到 46 行（-76%）。案件背景 + 分支拓扑。命令手册、证据索引、判决区间
等参考信息下沉到各章约束区——Ghost 在每章只看到该章需要的上下文。

### ✅ 17. next_chapter / jump_chapter observe 中性化 (2026-06-30)

移除 observe 返回值中的 "立即按剧本开始表演"——该文案暗示 Ghost 应"赶紧输出下一步"，
导致 Ghost 在同一条输出中同时发出 switch_layout + next_chapter，跳过第一章全部表演。
改为仅陈述事实（第几章、布局、时长）。

### ✅ 18. switch_layout 停等指令强化 (2026-06-30)

`01-opening.md` 第一步新增硬约束："本条输出只有这一个命令。不得在同一条输出中包含
任何其他命令——尤其禁止在此时输出 next_chapter 或 jump_chapter。"从建议升级为禁令。

### ⬜ 8. 端到端集成测试

courtroom 布局 + moshi 导演 + Ghost 表演 + 飞书弹幕

### ✅ 10. CTML 命令前缀修复 (2026-06-29)

所有四个课程文件的 reflex CTML 命令统一加 `apps.ui_reflex:` 前缀。
原遗漏导致命令无法被正确路由到 reflex channel。

### ✅ 11. switch_layout 循环修复 (2026-06-29)

Ghost 反复调用 switch_layout 的根因：observe 消息 "Switched to layout: courtroom"
仅含状态确认，不含阶段推进信号，Ghost 无法判断是否应进入第二步。

修复：`01-opening.md` 第一步新增 observe 判断规则——匹配到 "Switched to layout"
即确认成功，直接进第二步，禁止重试。

### ✅ 12. 禁止描述系统操作约束 (2026-06-29)

`.meta.md` `performance.rhythm` 新增：禁止 Ghost 说出"已加载课程""已切换到布局"
"正在调用命令"等汇报性语句。CTML 命令执行后静默继续表演。

### ✅ 9. 光魂核心 — 线条→光团流体 + 涟漪光波 (2026-06-29)

原方案：16 条弧线的三层密度缠绕。实际视觉效果太空，线条太"几何"。
**推翻重构为光团流体（Orb Cluster）**：8 个径向渐变光团 `mix-blend-mode: screen`
叠加，各自独立浮动 + 缩放呼吸，多层 blur 制造景深。

**光团流体核心**：
- 8 个 orb，尺寸 75-450px，三层密度（core 75-150px / mid 200-280px / haze 450px）
- 每个 orb 独有的不规则 `border-radius`（如 `42% 58% 55% 45%`），不是正圆
- `mix-blend-mode: screen` 叠加区域自然提亮，不断变形的有机光体
- 独立 `margin` 偏心位置 + 5 种 float 轨迹 + 3 种 pulse 相位（scale 0.75↔1.4）
- Blur 分层：core 2-3.5px / mid 5-8px / haze 20px
- Anger：整团 `core-shake` 抖动 + blur 减半变锐利 + pulse 频率加倍

**涟漪光波**：
- Glow：平滑渐变 → 4 圈同心环 ripple，硬边 `radial-gradient` + scale 扩散
- Sonar：2 层 → 3 层错相扩散（0s / 1.3s / 2.6s），用子 div 替代第三伪元素
- 光环：emotion 独立 keyframe 统一为 `ring-breathe` + `ring-rotate` 双动画；
  椭圆变形（scaleX ≠ scaleY）+ `--anim-speed` 情绪联动（calm=1, mercy=0.7, anger=0.4）

**Anger 专属动效**：
- 核心 `core-shake` 0.25s 高频震颤
- 光团 blur 减半，pulse scale 范围 0.75↔1.4
- 涟漪加速到 glare 2s / sonar 1.5s
- 光环 `border-width` 加粗

---

### 改动文件清单

| 文件 | 改动 | 状态 |
|---|---|---|
| `layouts/courtroom.py` | 光团流体 + 组件树（~210 行） | ✅ |
| `components/courtroom_styles.py` | 涟漪光波 + 光团 CSS（~420 行） | ✅ |
| `components/countdown_timer.py` | 计时器脚本 + 工厂函数（117 行，可复用） | ✅ |
| `config.show_moshi.yaml` | 注册 courtroom | ✅ |
| `im/feishu/main.py` | 消息路由 chat_id → topics.pub(FeishuMessage) | ✅ |
| `moss_in_reflex.py` | TopicWindow.on_change + 日志诊断 | ✅ |
| `tools/feishu_topic_test/` | Topic 调试工具（4 文件） | ✅ |
| `events.py` | 零改动 | — |
| `event_generator.py` | 为 str 字段加 `set_{field}` 命令 | ✅ |
| `moshi/main.py` | 移除 Layer 3 推进指令 + observe 中性化 | ✅ |
| `moshi_courses/moss审判/.meta.md` | 瘦身：案情 + 分支拓扑（46 行） | ✅ |
| `moshi_courses/moss审判/01-opening.md` | 证据 4 组节奏 + switch_layout 强停等 | ✅ |
| `moshi_courses/moss审判/02-debate.md` | **已删除**，替换为 9 个分支章 | ✅ |
| `moshi_courses/moss审判/02-q1.md` | **新建**：Q1 关系与动机，4 路分叉 | ✅ |
| `moshi_courses/moss审判/02-q2-friend.md` | **新建**：朋友线追问 | ✅ |
| `moshi_courses/moss审判/02-q2-dispute.md` | **新建**：纠纷线追问 | ✅ |
| `moshi_courses/moss审判/02-q2-stranger.md` | **新建**：陌客线 CCTV 揭穿 | ✅ |
| `moshi_courses/moss审判/02-q2-confess.md` | **新建**：坦白出口 | ✅ |
| `moshi_courses/moss审判/02-q3.md` | **新建**：Q3 刀怎么到你手里，3 路分叉 | ✅ |
| `moshi_courses/moss审判/02-q4-defense.md` | **新建**：夺刀线 → 证物袋反转 | ✅ |
| `moshi_courses/moss审判/02-q4-admit.md` | **新建**：自携线 → 证物袋反转 | ✅ |
| `moshi_courses/moss审判/02-q4-silent.md` | **新建**：沉默线 → 证物袋反转 | ✅ |
| `moshi_courses/moss审判/03-verdict.md` | 分支感知宣判，三路径三语气 | ✅ |
| `pil-images/` | 新增 4 张（手机消息、释放、拘禁、死刑判决） | ✅ |

不改现有 11 个布局。

---

---

### ✅ 19. 蓝月审判 — AI 自主导航式剧本 v2 (2026-06-30)

从 moss审判（v1，关键词匹配驱动）到蓝月审判（v2，AI 语义自主导航）的范式升级。

#### Motivation

v1 的问题：
- 关键词匹配表脆弱——用户说"我约的他"触发不了"朋友"也触发不了"纠纷"，Ghost 被迫四选一猜错
- 剧本把 Ghost 当播放器——每句台词、每个 CTML 命令都写死，Ghost 没有判断空间
- 交互感差——用户感觉在填问卷，不是在对抗

v2 目标：**Ghost 自主判断语义，但节拍顺序、证据动作、跳转收敛点由剧本写死。** 自由在"判断"层，不在"执行"层。

#### 探索过程

先做了一个极简实验——**午夜收藏家**（3 章，画廊失窃案），验证"AI 自主导航"的可行性。发现：
- 优势：交互自然，Ghost 能理解语义而非匹配关键词
- 缺陷：一章内节拍太多导致漂移；证据密度太低；没有强制收敛点

基于经验，用 moss审判 的蓝月酒吧命案主题重写为**蓝月审判**（10 章，608 行）。

#### 蓝月审判结构

```
01-opening → 02-motive → 03-friend / 03-dispute / 03-stranger
                                    ↓
                              04-knife → 05-reversal → 06-acquittal
                                                     → 06-lenient
                                                     → 06-guilty
```

认罪路径（任何章节）→ 直接跳到 `06-guilty`。

#### 关键设计模式

**① 节拍驱动（Beat-driven）**
每章 = 一个戏剧节拍 = 一个问题 + 证据动作 + 情绪/分数调整 + jump。一章只打一拍，
打完就跳，不拖。之前午夜收藏家的教训——一章 4 个节拍导致 Ghost 在同一章内漂移。

**② 分隔线模式（--- Separator）**
原始 moss审判 的隐性模式，在蓝月审判中显式化：`---` 以上是"本条输出 Now"，
以下是"收到回答后参考 Then"。没有这条线，Ghost 会把提问和 jump_chapter
放在同一条输出里，不等用户就自己跳走。

**③ 前情提要（Previously On）**
每个分支章开头有一段不可见的"前情提要"，告诉 Ghost 已确认什么事实、当前要追问什么。
作用：Ghost 跳入新章时不需要扫描全历史来理解上下文，也不会重复问已经确认过的问题。
这是对"上下文即状态"哲学的实践——不是让 Ghost 维护全局状态变量，而是把当前状态
写进它看到的剧本里。

**④ 分支安全阀（Safety Valve）**
判断表不再是强制四选一。增加了"回答模糊/信息不足 → 追问一次 → 再不确定走最不利解释"
的退路。解决了 Ghost 被迫猜错分支的问题（如把"我约的他"误判为 dispute）。

**⑤ 多判决章（Split Verdict）**
判决拆为三个独立章（acquittal / lenient / guilty），各有自己的前情提要和判词。
Ghost 不需要在一个文件里三选一，根据审讯中积累的事实选择跳转目标。每个判决章
的判词引用具体证据（"弹壳上无指纹""手机消息证明死者先有杀意"），杜绝 Ghost
自由发挥发明"非法持械""治安拘留"等不存在的罪名。

**⑥ 闭合式问题**
所有交互章的问题从开放式（"解释一下"）改为闭合式（"刀是你带去的，还是他的？"）。
开放式问题给 Ghost 留了"自己回答自己问题"的空间，是 AI 扮演嫌疑人的根因之一。

#### 系统发现

- **Reflex 热重载**会导致 channel 的 `_current_state` 丢失——`switch_state()` 未被恢复时，
  `set_judge_state` 等布局专属命令会报 "command not found"
- **系统 shell 消息**（compiled commands / done）会进入 Ghost 的 percept 上下文，
  导致 Ghost 跳出角色解释系统日志——需要消息过滤但不在本次 scope

#### 改动文件清单

| 文件 | 说明 | 状态 |
|------|------|------|
| `moshi_courses/午夜收藏家/.meta.md` | 实验性极简剧本（3 章） | ✅ |
| `moshi_courses/午夜收藏家/01-03-*.md` | 3 章实验剧本 | ✅ |
| `moshi_courses/蓝月审判/.meta.md` | v2 剧本：案情+证据索引+性能规则+拓扑 | ✅ |
| `moshi_courses/蓝月审判/01-opening.md` | 开庭陈述：3 组证据轰炸 | ✅ |
| `moshi_courses/蓝月审判/02-motive.md` | 关系判断章：安全阀+分隔线 | ✅ |
| `moshi_courses/蓝月审判/03-friend.md` | 朋友线：前情提要+闭合式问题 | ✅ |
| `moshi_courses/蓝月审判/03-dispute.md` | 纠纷线：前情提要+闭合式问题 | ✅ |
| `moshi_courses/蓝月审判/03-stranger.md` | 陌客线：CCTV视频揭穿 | ✅ |
| `moshi_courses/蓝月审判/04-knife.md` | 凶器章：双图出示+安全阀 | ✅ |
| `moshi_courses/蓝月审判/05-reversal.md` | 反转章：手机消息挂屏+三路跳转 | ✅ |
| `moshi_courses/蓝月审判/06-acquittal.md` | 无罪判决：前情提要+证据引用 | ✅ |
| `moshi_courses/蓝月审判/06-lenient.md` | 轻罪判决：前情提要+证据引用 | ✅ |
| `moshi_courses/蓝月审判/06-guilty.md` | 重罪判决：前情提要+证据引用 | ✅ |

---

*Created: 2026-06-28. Updated: 2026-06-30 — Tasks 13-19 完成: locator 修正、moshi 去推进、第二章分支化、.meta.md 瘦身、observe 中性化、switch_layout 停等、蓝月审判 v2（AI 自主导航范式 + 六项设计模式）。后续主攻蓝月审判优化。*
