# 第二幕：CTML · 系统调用

**主题：** 流式系统调用，时间是第一公民
**情绪：** 代码感、终端感、实时解析
**建议布局：** code_split
**时长：** ~40s

## 叙事要点

- "AI 怎么操作我？通过 CTML —— 流式系统调用语言"
- 演示：我说一句话，CTML 标签就是系统调用，流式解析、边生成边执行
- 对比：传统 OS 系统调用同步阻塞，CTML 流式并行、时间感知
- 每个命令有物理执行时长——Ghost 的输出是对未来的时序规划
- 过渡句：能力本身怎么组织？想继续听吗？

## 可用资源

- pil-image://moshi/ctml_flow — CTML 流式解析流程图

## 布局指南

code_split 布局（待实现）。左面板展示 CTML 代码片段，
右面板展示执行结果。逐字打字机效果。

## 节奏示例

```
AI 怎么操作我？通过 CTML —— 流式系统调用语言。
<apps.ui_reflex:stream_code>CTML 标签就是系统调用</apps.ui_reflex:stream_code>

边生成 token 边解析执行。时间是第一公民。
<mermaid:draw title="CTML 系统调用">flowchart LR
  A["Ghost 说话"] --> B["CTML 解析"] --> C["命令执行"]
</mermaid:draw>

传统 OS 系统调用同步阻塞。我的系统调用流式、并行、时间感知。
<!-- 自然过渡到下一章 -->
```
