# 第四幕：Matrix · 系统总线

**主题：** 跨进程通信拓扑，基于 Zenoh
**情绪：** 节点汇聚，连线脉冲
**建议布局：** topology
**时长：** ~30s

## 叙事要点

- "刚才那些能力跑在不同的进程里。它们怎么通信？"
- 引入 Matrix：基于 Zenoh 分布式协议
- 每个独立进程叫一个 Cell——可分布不同机器上
- 画出拓扑图：Ghost 作为中心节点，各 Cell 通过 Matrix 连接
- 我自动发现和管理所有 Cell
- 过渡句：身体连起来了。意识怎么运转？

## 可用资源

- pil-image://moshi/matrix_topo — Matrix 跨进程拓扑图

## 布局指南

topology 布局（待实现）。Canvas/SVG 节点 + 连线。
节点逐个出现，连线脉冲动画。Ghost 在中心，各 Cell 围绕。

## 节奏示例

```
刚才那些能力跑在不同的进程里。它们怎么通信？
<apps.ui_reflex:stream_title>Matrix · 系统总线</apps.ui_reflex:stream_title>

通过 Matrix 总线。基于 Zenoh 分布式协议。
<mermaid:draw title="Matrix 拓扑">flowchart TD
  matrix["Matrix 总线"] --> reflex["Cell: reflex"]
  matrix --> ai_eye["Cell: ai_eye"]
  matrix --> mac["Cell: mac"]
  ghost["Ghost"] --> matrix
</mermaid:draw>

每个独立进程叫一个 Cell。我能自动发现和管理它们。跨进程、跨机器。
<!-- 自然过渡 -->
```
