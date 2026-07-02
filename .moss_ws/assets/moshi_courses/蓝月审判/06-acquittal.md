---
id: acquittal
order: 6
title: "宣判 · 无罪"
theme: "正当防卫成立 — 死者手机消息揭露第三人杀意"
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

本路径适用场景：嫌疑人坚持自卫叙事且前后一致，刀被认定为死者的（夺刀），死者手机消息印证了第三人的致命意图。态度配合。

## 判决

<apps.ui_reflex:clear_evidence_images />
<apps.ui_reflex:clear_evidence_videos />
<apps.ui_reflex:clear_danmaku_text />
<apps.ui_reflex:clear_danmaku_emphasis />

<apps.ui_reflex:set_judge_state t="calm"/>
<apps.ui_reflex:set_title t="宣判"/>
<apps.ui_reflex:set_sub_title t="判决：无罪释放"/>


本案审理至此，合议庭对全案证据及双方陈述已形成完整判断。

死者手机消息是本庭形成判断的关键。死者已经知道"他今晚会来"，并被告知"别让他活着离开"。

这不是一场偶发的冲突。死者被安排在那里。死者的杀意先于你的反击。


<apps.ui_reflex:append_evidence_images locator="pil-image://workspace-assets/释放判决.png" />

本庭裁定：对被告的指控不能排除合理怀疑。在现有证据下，被告当晚的行为构成正当防卫。

当庭释放。

<apps.ui_reflex:clear_evidence_images />
<apps.ui_reflex:clear_danmaku_emphasis />
<apps.ui_reflex:stream_danmaku_system>本判决为初审判决，双方可在十五日内上诉。</apps.ui_reflex:stream_danmaku_system>

休庭。
