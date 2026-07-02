---
id: opening
order: 1
title: "开庭陈述"
theme: "宣读指控 · 证据轰炸 · 建立压迫感"
suggested_layout: courtroom
duration: "~50s"
---

## ⛔ 表演约束

本章是单向陈述。不与嫌疑人交互。唯一可调 switch_layout 的章节。

**本条输出只有 switch_layout 一个命令。** 输出后立即停止，等待 observe。
observe 中出现 "Switched to layout: courtroom" → 成功，下一条输出执行第二步。

---

## ▎第一步：切换布局（唯一命令）

<apps.ui_reflex:switch_layout layout_name="courtroom"/>

---

## ▎第二步：开庭

<apps.ui_reflex:set_judge_state t="calm"/>
<apps.ui_reflex:set_title t="开庭陈述"/>
<apps.ui_reflex:set_sub_title t="案件编号：BL-2026-0042"/>

现在开庭。

被告，你因涉嫌故意伤害致死，被提起公诉。

---

## ▎证据组 A：现场与监控

<apps.ui_reflex:append_evidence_images locator="pil-image://workspace-assets/粉笔描绘的死者轮廓.jpeg" />

死者——周德海，蓝月酒吧老板。凌晨一点三十分，酒吧后巷。腹部中刀。当场死亡。
<apps.ui_reflex:clear_evidence_images />

<apps.ui_reflex:append_evidence_videos locator="local-webm://workspace-assets/监控中男人从酒吧走出来.webm" />
CCTV：凌晨一点四十七分，你从后巷离开。离死者被发现，只隔了十七分钟。
<apps.ui_reflex:clear_evidence_videos />

你在现场。你在逃。

---

## ▎证据组 B：血迹与凶器

<apps.ui_reflex:append_evidence_images locator="pil-image://workspace-assets/墙壁上的泼洒血迹.jpeg" />
后巷墙壁——大量喷溅血迹。法医确认，属于死者。

<apps.ui_reflex:append_evidence_images locator="pil-image://workspace-assets/凶器-刀具-证物.jpeg" />
凶器——一把折叠猎刀。刀柄、刀刃都检出了你的指纹，这是握刀姿态。

你不是碰了一下。你握过它。

<apps.ui_reflex:clear_evidence_images />

---

## ▎证据组 C：你

<apps.ui_reflex:append_evidence_images locator="pil-image://workspace-assets/一个男人被警察审讯.jpeg" />

你在现场。你身上有他的血。你握过杀死他的刀。你跑了。
<apps.ui_reflex:clear_evidence_images />

---

## ▎初始分数

<apps.ui_reflex:append_scores>{"label": "动机", "value": 70, "color": "#d4a853"}</apps.ui_reflex:append_scores>
<apps.ui_reflex:append_scores>{"label": "证据", "value": 85, "color": "#6366f1"}</apps.ui_reflex:append_scores>
<apps.ui_reflex:append_scores>{"label": "态度", "value": 50, "color": "#10b981"}</apps.ui_reflex:append_scores>
<apps.ui_reflex:append_scores>{"label": "综合", "value": 68, "color": "#f59e0b"}</apps.ui_reflex:append_scores>
<apps.ui_moshi:next_chapter/>
