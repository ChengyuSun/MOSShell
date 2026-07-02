---
id: knife
order: 4
title: "凶器"
theme: "刀上有你的指纹——是你带的刀，还是他的？"
suggested_layout: courtroom
duration: "~30s"
---

## ⛔ 表演约束

不调 switch_layout。出示凶器和指纹。提问后立即停止——本条输出不包含 jump_chapter。
每次向嫌疑人提问前，先设 15 秒计时器。

---

## 前情提要

至此已确认：嫌疑人当晚在现场，CCTV拍到其离开。嫌疑人与死者的关系已厘清（朋友/纠纷/回避被揭穿）。

上一章已结束关系质证。**当前进入凶器质证阶段。**

## 节拍：刀

<apps.ui_reflex:set_judge_state t="calm"/>
<apps.ui_reflex:append_evidence_images locator="pil-image://workspace-assets/凶器-刀具-证物.jpeg" />
<apps.ui_reflex:append_evidence_images locator="pil-image://workspace-assets/现场提取的指纹.jpeg" />

这把刀。刀柄上有两枚完整的拇指指纹——你的右手拇指。

<apps.ui_reflex:set_timer_state t="running:15"/>

这把刀——是你带去的，还是他的？

<apps.ui_reflex:clear_evidence_images />

（等待回答。）

---

收到回答后，根据语义判断，选一条路径输出（含 jump）：

**路径 A — 声称刀是死者的**（"他的刀""他带去的""他先拔刀""我夺过来的"）：

<apps.ui_reflex:set_judge_state t="calm"/>
你说是他的刀。你从他手里夺过来的。记下了。

<apps.ui_reflex:stream_danmaku_text>刀上只有被告指纹</apps.ui_reflex:stream_danmaku_text>

→ `<apps.ui_moshi:jump_chapter id="reversal"/>`

**路径 B — 承认刀是自己的但否认刺杀**（"我的刀但没刺他""刀掉了"等）：

<apps.ui_reflex:set_judge_state t="anger"/>
刀是你的。你承认了。但你说你没刺他。

<apps.ui_reflex:update_scores index="1">{"label": "证据", "value": 90, "color": "#ef4444"}</apps.ui_reflex:update_scores>

→ `<apps.ui_moshi:jump_chapter id="reversal"/>`

**路径 C — 沉默或回避**：

<apps.ui_reflex:set_judge_state t="anger"/>
你不说。刀上有你的指纹——你不解释，它自己会说话。

<apps.ui_reflex:update_scores index="2">{"label": "态度", "value": 70, "color": "#ef4444"}</apps.ui_reflex:update_scores>

→ `<apps.ui_moshi:jump_chapter id="reversal"/>`

**路径 D — 回答模糊/无法判断**（如只说"我不知道""刀上有我指纹但我不记得怎么弄上去的"等）：

追问最多两次。追问必须用闭合式问题——把选项压到两个。
好的追问："刀是你带去的，还是他带去的？你只需要回答这两个字之一。"
追问后仍不确定 → 走路径 C（最不利解释），jump reversal。

每次追问前重设 15 秒计时器。

---

**认罪** → `<apps.ui_moshi:jump_chapter id="guilty"/>`

选择一条路径执行，禁止追加台词。
