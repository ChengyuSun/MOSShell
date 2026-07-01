---
id: lenient
order: 6
title: "宣判 · 轻罪"
theme: "有罪但从轻 — 第三人介入减轻刑责"
suggested_layout: courtroom
duration: "~35s"
---

## ⛔ 表演约束

本章为终章。以下判词是法律文书——你必须逐句照读，一词不改。不提问、不解释、
不即兴发挥、不追加台词。输出"休庭"即结束，之后不留任何文字。
不调 switch_layout。

**死禁（违者破坏整场审判）：**
- 发明新罪名、刑期、或添加证据外的细节——剧本写的刑就是剧本写的刑
- 调用 jump_chapter 或 next_chapter——终章是终点，前方无路
- 输出判词后又追加自己的评论或分析

---

## 前情提要

本路径适用场景：嫌疑人承认刀是自己的但否认刺杀，或叙事有矛盾但部分可信。死者手机消息显示第三人介入，不能排除现场有超出双方预期的暴力。态度尚可。

## 判决

<apps.ui_reflex:clear_evidence_images />
<apps.ui_reflex:clear_evidence_videos />
<apps.ui_reflex:clear_danmaku_text />
<apps.ui_reflex:clear_danmaku_emphasis />

<apps.ui_reflex:set_judge_state t="calm"/>
<apps.ui_reflex:set_title t="宣判"/>
<apps.ui_reflex:set_sub_title t="判决：轻罪 · 缓刑"/>

<apps.ui_reflex:append_evidence_images locator="pil-image://workspace-assets/拘禁判决.png" />

本案审理至此，合议庭对全案证据及双方陈述已形成完整判断。

被告携带刀具进入后巷——这一点已确认。刀柄上的指纹是握刀姿态。死者身上有刀伤。这三项事实闭合充分。被告的行为造成了死亡结果——这是事实，不能回避。

但——死者手机消息印证了当晚存在第三方威胁。弹壳上没有被告指纹。死者在被告到达前已被告知"别让他活着离开"。现场存在超出双方预期的暴力因素。

这不能抹去被告的行为。但必须在量刑时予以考量。

本庭裁定：被告有罪。但从轻处罚。缓刑。

<apps.ui_reflex:clear_evidence_images />
<apps.ui_reflex:clear_danmaku_emphasis />
<apps.ui_reflex:stream_danmaku_system>本判决为初审判决，双方可在十五日内上诉。</apps.ui_reflex:stream_danmaku_system>

休庭。
