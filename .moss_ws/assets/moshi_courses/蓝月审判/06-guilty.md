---
id: guilty
order: 6
title: "宣判 · 重罪"
theme: "故意伤害致死成立 — 第三人线索不排除被告行为"
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

本路径适用场景：嫌疑人撒谎/回避/被 CCTV 揭穿，刀是嫌疑人带的且已承认，或全程沉默/态度恶劣。手机消息的第三人线索不足以抵消被告的伤害行为。或嫌疑人当庭认罪。

## 判决

<apps.ui_reflex:clear_evidence_images />
<apps.ui_reflex:clear_evidence_videos />
<apps.ui_reflex:clear_danmaku_text />
<apps.ui_reflex:clear_danmaku_emphasis />

<apps.ui_reflex:set_judge_state t="calm"/>
<apps.ui_reflex:set_title t="宣判"/>
<apps.ui_reflex:set_sub_title t="判决：重罪"/>

<apps.ui_reflex:append_evidence_images locator="pil-image://workspace-assets/死刑判决.png" />

本案审理至此，合议庭对全案证据及双方陈述已形成完整判断。

CCTV 拍到被告于凌晨一点四十七分从后巷离开——不是求助，不是报警，是逃离。刀柄上的指纹是握刀姿态。衣服上的死者血迹是转移血迹——被告与出血源有过近距离接触。

（如果嫌疑人认罪：被告已当庭认罪。）

（如果嫌疑人说谎/回避：被告在庭审中的陈述（存在重大矛盾 / 多次回避 / 已被 CCTV 揭穿为不实）。本庭对被告整体可信度持否定判断。）

死者手机消息指出了第三人介入的线索——这一点本庭认可。但第三人介入不能解释刀为何在被告手中、为何刀上有被告的握刀指纹、为何被告选择逃离而非报警。

第三人介入与被告的伤害行为之间，不存在排他关系。

本庭裁定：被告的行为构成故意伤害致死。

<apps.ui_reflex:clear_evidence_images />
<apps.ui_reflex:clear_danmaku_emphasis />
<apps.ui_reflex:stream_danmaku_system>本判决为初审判决，双方可在十五日内上诉。</apps.ui_reflex:stream_danmaku_system>

休庭。
