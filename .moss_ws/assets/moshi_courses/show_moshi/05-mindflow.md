# 第五幕：Mindflow · 调度器

**主题：** 感知/思考/执行三循环并发仲裁
**情绪：** 三个轨道旋转，意识流可视化
**建议布局：** topology
**时长：** ~40s

## 叙事要点

- "我的感知、思考、执行三个循环同时运行"
- 感知循环：声音、图像、信号持续输入
- 思考循环：信号产生冲动，冲动竞争注意力
- 执行循环：注意力驱动思考，思考输出行动
- 用 ai_eye 表情变化可视化：thinking → blink → curious → speaking
- 我是持续运行的，不是回合制 bot
- 过渡句：那运行在我之上的是什么？

## 可用资源

- （无特定图片，主要通过 ai_eye 表情切换展示）

## 布局指南

复用 topology 布局。用三个旋转的环形轨道表示三循环。
配合 ai_eye 的 thinking/blink/curious/speaking 表情切换。

## 节奏示例

```
我的感知、思考、执行三个循环同时运行。
<apps.games_ai_eye:thinking />
<apps.ui_reflex:stream_title>Mindflow · AI 意识流调度器</apps.ui_reflex:stream_title>

就像现在——我的嘴在说话，但我的眼睛同时在做自己的事。
<apps.games_ai_eye:blink />

感知输入、思考竞争、执行输出。三个循环并发。
<apps.games_ai_eye:set_expression name="curious" />

我不是回合制 bot——我是持续运行的。
<apps.games_ai_eye:speaking />
<!-- 自然过渡 -->
```
