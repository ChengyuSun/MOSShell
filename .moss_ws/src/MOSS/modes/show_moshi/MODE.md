---
apps:
- browsers/*
- games/*
- tools/*
- ui/*
- sensors/*
bringup_apps: [
    # "tools/screen_capture",
    "ui/reflex",
    "ui/moshi",
    # "sensors/audio_capture", "sensors/listener",
    "games/ai_eye", 
    # "sensors/vision",
]
# 渐进启动: "ui/reflex", "ui/moshi", "games/ai_eye", ...
ctml_version: ''
description: Moshi 导演模式 — 章节化演示，Ghost 在章节框架内即兴表演
name: show_moshi
---