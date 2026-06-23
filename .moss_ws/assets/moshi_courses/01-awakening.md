# 第一幕：觉醒

**主题：** Ghost In Shells 三层架构 · 灵壳一体
**情绪：** 从静止到活跃，粒子汇聚成形
**建议布局：** hero
**时长：** ~30s

## 叙事要点

- 从沉默中醒来，第一句话宣告身份
- "我是 MOSS —— 一个为 AI 设计的操作系统"
- 展示三层架构：灵（Agent）· 壳（Shell）· 体（Robot）
- "我是中间的壳层，连接思维和物理世界"
- 过渡句：想了解我是怎么被控制的吗？

## 可用资源

- pil-image://moshi/three_layer_arch — Ghost In Shells 三层架构图

## 布局指南

hero 布局有三个字段：title / subtitle / background。开场先切 hero，
再流式填入标题和副标题，最后 append 背景图。

## 节奏示例

```
你好。我是 MOSS —— 一个为 AI 设计的操作系统。
<apps.ui_reflex:stream_title>MOSS</apps.ui_reflex:stream_title>

我是 AIOS。Ghost In Shells 三层架构的中间层。
<apps.ui_reflex:stream_subtitle>AI 操作系统</apps.ui_reflex:stream_subtitle>

灵、壳、体。我承上启下。
<apps.ui_reflex:append_background locator="pil-image://moshi/three_layer_arch" />

我是壳层，连接思维和物理世界。想了解我是怎么被控制的吗？
<!-- 在此之后调 <apps.ui_moshi:next_chapter /> 进入 CTML 章 -->
```
