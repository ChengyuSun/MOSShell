---
id: robot-dog
order: 4
title: "具身 · 机器狗"
theme: "从数字世界到物理世界 —— MOSS 能操控真实的机器人"
suggested_layout: hero
duration: "~20s"
---

# 第四幕：具身 · 机器狗

**主题：** Channel + Matrix 不是纸上谈兵 —— 它们能驱动真实的机器人
**情绪：** 全屏视频冲击，看完再说
**建议布局：** hero
**时长：** ~20s

## ⛔ 表演约束（违反即错）

纯视频展示 + 最少口播。让画面说话。

**[强约束] 讲完本章 → 调 `<apps.ui_moshi:next_chapter />` → 结束本章

**允许的命令：**
- `switch_layout` layout_name="hero"
- `append_videos` locator="..."

**禁止事项：**
- 禁止在 switch_layout 之前执行任何 reflex 命令
- 禁止调其他 Channel
- 禁止描述自己的动作（switch_layout 会自动触发观察，无需额外描述）
- 视频播放期间禁止口播，`<sleep>` 期间静默
- 视频结束后只说过渡句，不额外解说
- 禁止即兴添加剧本外的 CTML 动作

**执行完毕后：** 过渡句 → `<apps.ui_moshi:next_chapter />`

## 可用资源

- `local-webm://workspace-assets/dog.webm` — 机器狗演示视频

## 叙事结构

| 段 | 说的内容 | 同步发生的 | 时长 |
|---|---|---|---|---|
| 1 | 切 hero 布局 | 布局切换 | — |
| 2 | 视频播放，不口播 | 全屏视频 autoplay | ~15s |
| 3 | 过渡 | — | ~5s |

## 表演脚本

**▎第一步（仅输出 switch_layout，不附带任何其他内容）：**
<apps.ui_reflex:switch_layout layout_name="hero"/>
（此后立即停止，等待 observe 返回新布局上下文）

**▎第二步（observe 返回后，开始表演）：**
<apps.ui_reflex:append_videos locator="local-webm://workspace-assets/dog.webm"/>
<sleep duration="7"/>
看到了吗，机器狗在AI的控制下运动肢体，
所以刚才那些 Channel——不是纸上谈兵。这是我通过 Matrix 总线实时操控的机器狗。想了解这套神经系统怎么调度感知和思考吗？

<apps.ui_moshi:next_chapter/>
