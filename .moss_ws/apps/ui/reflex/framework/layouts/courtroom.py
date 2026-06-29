"""CourtroomLayout — 极限审判。

AI 法官是暗空间中悬浮的光魂（280px 渐变球体），三情绪驱动色调联动：
- calm（平静）：银白→灰，4s 慢呼吸 — 宣读罪名、陈述事实
- mercy（怜悯）：靛蓝→群青，3s 呼吸 — 听取申辩、考虑减刑
- anger（愤怒）：猩红→深红，1.2s 快速呼吸 — 证据确凿、被告撒谎

情绪切换时，光魂颜色、背景径向光晕、环境光环全部联动过渡（0.6s）。

背景四层：径向光晕（跟情绪联动）+ 点阵纹理 + 环境光环（2-3 圈呼吸环）
+ 粒子场（中性暖色，不随情绪变化）。

证据图片/视频 flex-wrap 自适应排列，可覆盖光魂。分数四圆环横排。
计时器纯数字右上角。三级弹幕底部飘移。

字段类型全部使用 event_generator 原生支持的类型（str / list[BaseModel] /
list[Image.Image] / list[VideoLocator] / list[str]），不引入单 BaseModel 包装。
"""

from PIL import Image

import reflex as rx
from pydantic import BaseModel, Field

from framework.events import VideoLocator
from framework.helpers.mixin import NameMixin


# ═══════════════════════════════════════════════════════════════════════════════
# Model
# ═══════════════════════════════════════════════════════════════════════════════

class ScoreBar(BaseModel):
    """分数维度环。与 brain CellBar 同模式。"""
    label: str = Field(default="", description="维度名")
    value: int = Field(default=0, description="0-100")
    color: str = Field(default="#6366f1", description="环颜色")




# ═══════════════════════════════════════════════════════════════════════════════
# Scripts
# ═══════════════════════════════════════════════════════════════════════════════

_PARTICLE_SCRIPT = """
(function S(){
  var c=document.getElementById('courtroom-particles');
  if(!c){setTimeout(S,80);return;}
  var ctx=c.getContext('2d'),W,H;
  function R(){W=c.width=window.innerWidth;H=c.height=window.innerHeight;}
  window.addEventListener('resize',R);R();
  function P(){this.reset();this.x=Math.random()*W;this.y=Math.random()*H;}
  P.prototype.reset=function(){
    this.x=Math.random()*W;this.y=Math.random()*H;
    this.l=Math.random()*6.28;this.sp=0.00015+Math.random()*0.0006;
    this.sz=0.5+Math.random()*2;this.op=0.03+Math.random()*0.08;
    this.phase=Math.random()*6.28;
    this.vx=(Math.random()-0.5)*0.15;this.vy=(Math.random()-0.5)*0.15;
  };
  P.prototype.up=function(){
    this.x+=this.vx;this.y+=this.vy;
    if(this.x<-30)this.x=W+30;if(this.x>W+30)this.x=-30;
    if(this.y<-30)this.y=H+30;if(this.y>H+30)this.y=-30;
  };
  P.prototype.draw=function(t){
    var tw=0.5+0.5*Math.sin(t*0.0003+this.phase);
    ctx.beginPath();ctx.arc(this.x,this.y,this.sz,0,6.28);
    ctx.fillStyle='rgba(180,160,120,'+(this.op*tw)+')';ctx.fill();
  };
  var ps=[];for(var i=0;i<60;i++)ps.push(new P());
  function A(t){
    ctx.clearRect(0,0,W,H);
    var g=ctx.createRadialGradient(W/2,H/2,0,W/2,H/2,Math.max(W,H)*0.7);
    g.addColorStop(0,'rgba(20,16,8,0)');g.addColorStop(1,'rgba(4,3,2,0.75)');
    ctx.fillStyle=g;ctx.fillRect(0,0,W,H);
    for(var i=0;i<ps.length;i++){ps[i].up();ps[i].draw(t);}
    requestAnimationFrame(A);
  }
  requestAnimationFrame(A);
})();
"""

_TIMER_SCRIPT = """
(function(){
  var store=document.getElementById('courtroom-timer-store');
  if(!store){setTimeout(arguments.callee,80);return;}

  var display=document.getElementById('courtroom-timer-display');
  if(!display){setTimeout(arguments.callee,80);return;}

  var running=false, seconds=0, interval=null;

  function fmt(s){
    var m=Math.floor(s/60), sec=s%60;
    return String(m).padStart(2,'0')+':'+String(sec).padStart(2,'0');
  }

  function updateColor(s){
    display.classList.remove('timer-safe','timer-warn','timer-danger');
    if(s>30)display.classList.add('timer-safe');
    else if(s>10)display.classList.add('timer-warn');
    else display.classList.add('timer-danger');
  }

  function stopInterval(){
    if(interval){clearInterval(interval);interval=null;}
  }

  function startCountdown(){
    stopInterval();
    running=true;
    updateColor(seconds);
    display.textContent=fmt(seconds);
    interval=setInterval(function(){
      seconds--;
      if(seconds<=0){
        seconds=0;
        stopInterval();
        running=false;
        display.textContent=fmt(0);
        display.classList.add('timer-danger');
        // Update store to expired
        var el=store.querySelector('[data-timer-state]');
        if(el)el.setAttribute('data-timer-state','expired:0');
        setTimeout(function(){
          display.classList.remove('timer-danger');
          display.classList.add('timer-safe');
        },3000);
        return;
      }
      display.textContent=fmt(seconds);
      updateColor(seconds);
      var el=store.querySelector('[data-timer-state]');
      if(el)el.setAttribute('data-timer-state','running:'+seconds);
    },1000);
  }

  function parse(val){
    // Format: "state:seconds" e.g. "running:60" "stopped:0" "expired:0"
    if(!val)return['stopped',0];
    var idx=val.indexOf(':');
    if(idx===-1)return[val,0];
    return[val.slice(0,idx),parseInt(val.slice(idx+1),10)||0];
  }

  function sync(){
    var el=store.querySelector('[data-timer-state]');
    if(!el)return;
    var raw=el.getAttribute('data-timer-state')||'stopped:0';
    var parsed=parse(raw);
    var newState=parsed[0], newSec=parsed[1];

    if(newState==='running'&&!running){
      seconds=newSec;
      startCountdown();
    }else if(newState==='stopped'){
      stopInterval();
      running=false;
      seconds=newSec;
      display.textContent=fmt(seconds);
      updateColor(seconds);
    }else if(newState==='expired'){
      stopInterval();
      running=false;
      display.textContent=fmt(0);
      display.classList.add('timer-danger');
    }
  }

  sync();
  new MutationObserver(sync).observe(store,{childList:true,subtree:true,attributes:true});
})();
"""

_DANMAKU_SIGNAL_SCRIPT = """
(function(){
  var store=document.getElementById('danmaku-signal-store');
  if(!store){setTimeout(arguments.callee,80);return;}

  var lastClear='',lastSpeed='1.0';
  var layer=document.getElementById('danmaku-layer');

  function sync(){
    var clearEl=store.querySelector('[data-danmaku-clear]');
    var speedEl=store.querySelector('[data-danmaku-speed]');

    var cv=clearEl?clearEl.getAttribute('data-danmaku-clear')||'':'';
    if(cv!==''&&cv!==lastClear){
      lastClear=cv;
      if(layer)layer.style.setProperty('--danmaku-speed','6');
      setTimeout(function(){if(layer)layer.style.setProperty('--danmaku-speed',lastSpeed);},300);
    }

    var sv=speedEl?speedEl.getAttribute('data-danmaku-speed')||'1.0':'1.0';
    if(sv!==lastSpeed){
      lastSpeed=sv;
      if(layer&&lastClear==='')layer.style.setProperty('--danmaku-speed',sv);
    }
  }

  sync();
  new MutationObserver(sync).observe(store,{childList:true,subtree:true,attributes:true});
})();
"""


# ═══════════════════════════════════════════════════════════════════════════════
# CSS
# ═══════════════════════════════════════════════════════════════════════════════

_COURTROOM_CSS = """
/* ── Scene ── */
.courtroom-scene {
  position: absolute; inset: 0;
  background: #020202;
}
/* Dot grid texture — brain 同款，极淡 */
.courtroom-scene::before {
  content: ''; position: absolute; inset: 0;
  background-image: radial-gradient(circle, rgba(255,255,255,0.025) 1px, transparent 1px);
  background-size: 50px 50px;
  pointer-events: none; z-index: 0;
}

/* ── Radial Glow (emotion-linked, z-1) ── */
.courtroom-glow {
  position: absolute; top: 50%; left: 50%; z-index: 1;
  width: 0; height: 0; pointer-events: none;
}
.courtroom-glow::before {
  content: ''; position: absolute;
  width: 700px; height: 700px; border-radius: 50%;
  transform: translate(-50%, -50%);
  transition: background 0.6s ease;
}
.courtroom-glow.calm::before {
  background: radial-gradient(circle,
    rgba(210,215,220,0.06) 0%,
    rgba(156,163,175,0.03) 35%,
    transparent 70%);
}
.courtroom-glow.mercy::before {
  background: radial-gradient(circle,
    rgba(129,140,248,0.08) 0%,
    rgba(99,102,241,0.04) 35%,
    transparent 70%);
}
.courtroom-glow.anger::before {
  background: radial-gradient(circle,
    rgba(248,113,113,0.09) 0%,
    rgba(239,68,68,0.04) 35%,
    transparent 70%);
}

/* ── Ambient Rings (z-1, centered on orb, breathing) ── */
.courtroom-ambient-ring {
  position: absolute; top: 50%; left: 50%; border-radius: 50%;
  transform: translate(-50%, -50%);
  border: 0.5px solid rgba(180,190,210,0.05);
  pointer-events: none; z-index: 1;
  animation: ring-breathe 10s ease-in-out infinite;
}
.courtroom-ambient-ring.r2 {
  animation-delay: 3.5s;
}
.courtroom-ambient-ring.r3 {
  animation-delay: 7s;
}
@keyframes ring-breathe {
  0%, 100% { opacity: 0.15; transform: translate(-50%, -50%) scale(1); }
  50%      { opacity: 0.4;  transform: translate(-50%, -50%) scale(1.06); }
}

/* ── Particle Canvas ── */
#courtroom-particles {
  position: fixed; top: 0; left: 0; width: 100%; height: 100%;
  z-index: 0; pointer-events: none;
}

/* ── Orb (Light Soul) ── */
.courtroom-orb-anchor {
  position: absolute; top: 50%; left: 50%; z-index: 2;
  width: 0; height: 0;
}
.courtroom-orb {
  position: absolute; top: -140px; left: -140px;
  width: 280px; height: 280px; border-radius: 50%;
  transition: background 0.6s ease, box-shadow 0.6s ease;
}
/* calm — 银白→灰，4s 慢呼吸 */
.courtroom-orb.calm {
  background: radial-gradient(circle at 38% 38%,
    rgba(230,230,235,0.95) 0%,
    rgba(209,213,219,0.55) 15%,
    rgba(156,163,175,0.2) 45%,
    rgba(60,60,70,0) 70%);
  box-shadow:
    0 0 40px rgba(156,163,175,0.35),
    0 0 100px rgba(156,163,175,0.18),
    0 0 200px rgba(156,163,175,0.08),
    0 0 350px rgba(156,163,175,0.03);
  animation: orb-breathe-calm 4s ease-in-out infinite;
}
/* mercy — 靛蓝→群青，3s 呼吸 */
.courtroom-orb.mercy {
  background: radial-gradient(circle at 38% 38%,
    rgba(210,215,255,0.95) 0%,
    rgba(129,140,248,0.55) 15%,
    rgba(99,102,241,0.25) 45%,
    rgba(30,25,70,0) 70%);
  box-shadow:
    0 0 50px rgba(99,102,241,0.45),
    0 0 120px rgba(99,102,241,0.22),
    0 0 240px rgba(99,102,241,0.1),
    0 0 400px rgba(99,102,241,0.04);
  animation: orb-breathe-mercy 3s ease-in-out infinite;
}
/* anger — 猩红→深红，1.2s 快速呼吸 */
.courtroom-orb.anger {
  background: radial-gradient(circle at 38% 38%,
    rgba(255,210,210,0.95) 0%,
    rgba(248,113,113,0.55) 15%,
    rgba(239,68,68,0.25) 45%,
    rgba(70,15,15,0) 70%);
  box-shadow:
    0 0 55px rgba(239,68,68,0.5),
    0 0 130px rgba(239,68,68,0.25),
    0 0 260px rgba(239,68,68,0.12),
    0 0 420px rgba(239,68,68,0.05);
  animation: orb-breathe-anger 1.2s ease-in-out infinite;
}

@keyframes orb-breathe-calm {
  0%, 100% { transform: scale(1); opacity: 0.85; }
  50%      { transform: scale(1.04); opacity: 1; }
}
@keyframes orb-breathe-mercy {
  0%, 100% {
    transform: scale(1);
    box-shadow:
      0 0 50px rgba(99,102,241,0.45),
      0 0 120px rgba(99,102,241,0.22),
      0 0 240px rgba(99,102,241,0.1),
      0 0 400px rgba(99,102,241,0.04);
  }
  50% {
    transform: scale(1.05);
    box-shadow:
      0 0 65px rgba(99,102,241,0.6),
      0 0 150px rgba(99,102,241,0.32),
      0 0 300px rgba(99,102,241,0.16),
      0 0 460px rgba(99,102,241,0.06);
  }
}
@keyframes orb-breathe-anger {
  0%, 100% {
    transform: scale(1);
    box-shadow:
      0 0 55px rgba(239,68,68,0.5),
      0 0 130px rgba(239,68,68,0.25),
      0 0 260px rgba(239,68,68,0.12),
      0 0 420px rgba(239,68,68,0.05);
  }
  50% {
    transform: scale(1.08);
    box-shadow:
      0 0 80px rgba(239,68,68,0.7),
      0 0 180px rgba(239,68,68,0.38),
      0 0 340px rgba(239,68,68,0.2),
      0 0 500px rgba(239,68,68,0.08);
  }
}

/* ── Evidence Layer ── */
.courtroom-evidence-layer {
  position: absolute; top: 0; left: 0; width: 100%; height: 100%;
  z-index: 3; pointer-events: none;
  display: flex; flex-wrap: wrap; justify-content: center; align-items: center;
  align-content: center;
  padding: 40px; gap: 16px;
}
.courtroom-evidence-item {
  border-radius: 12px; overflow: hidden;
  flex: 1 1 300px; max-width: 500px;
  animation: evidence-fade-in 0.4s ease-out;
  box-shadow: 0 4px 24px rgba(0,0,0,0.5);
}
@keyframes evidence-fade-in {
  0%   { opacity: 0; transform: scale(0.9); }
  100% { opacity: 1; transform: scale(1); }
}

/* ── Score Rings ── */
.courtroom-scores {
  position: absolute; bottom: 80px; left: 50%; transform: translateX(-50%);
  z-index: 2; display: flex; gap: 28px; align-items: flex-end;
}
.score-ring-wrap {
  display: flex; flex-direction: column; align-items: center; gap: 6px;
}
.score-ring {
  position: relative; border-radius: 50%;
  width: 100px; height: 100px;
}
.score-ring.total { width: 120px; height: 120px; }
.score-ring-progress {
  position: absolute; inset: 3px; border-radius: 50%;
  mask: radial-gradient(circle, transparent 58%, black 60%);
  -webkit-mask: radial-gradient(circle, transparent 58%, black 60%);
  transition: background 0.6s ease;
}
.score-ring-value {
  position: absolute; inset: 0;
  display: flex; align-items: center; justify-content: center;
  font-family: "SF Mono", Menlo, Monaco, Consolas, monospace;
  font-size: 16px; font-weight: 600; color: #e0e0f0;
}
.score-ring.total .score-ring-value { font-size: 20px; }
.score-ring-label {
  font-family: "SF Mono", Menlo, Monaco, Consolas, monospace;
  font-size: 12px; color: rgba(180,190,210,0.7);
  text-transform: uppercase; letter-spacing: 2px;
}

/* ── Timer ── */
.courtroom-timer {
  position: absolute; top: 32px; right: 40px; z-index: 4;
  font-family: "SF Mono", Menlo, Monaco, Consolas, monospace;
  font-size: 28px; font-weight: 600; letter-spacing: 2px;
  transition: color 0.5s ease;
  pointer-events: none;
}
.timer-safe  { color: #9ca3af; }
.timer-warn  { color: #fbbf24; }
.timer-danger { color: #ef4444; animation: timer-shake 0.5s ease-in-out; }
@keyframes timer-shake {
  0%, 100% { transform: translateX(0); }
  10%, 50%, 90% { transform: translateX(-3px); }
  30%, 70% { transform: translateX(3px); }
}

/* ── HUD ── */
.courtroom-title {
  position: absolute; top: 38px; left: 50%; transform: translateX(-50%);
  font-family: "SF Pro Display", -apple-system, BlinkMacSystemFont, sans-serif;
  font-size: 18px; font-weight: 600; letter-spacing: 3px;
  color: rgba(160,175,200,0.45);
  text-shadow: 0 0 16px rgba(80,100,140,0.15);
  text-transform: uppercase; z-index: 5; pointer-events: none;
}
.courtroom-subtitle {
  position: absolute; top: 68px; left: 50%; transform: translateX(-50%);
  font-family: "SF Mono", Menlo, Monaco, Consolas, monospace;
  font-size: 13px;
  color: rgba(120,140,170,0.4);
  z-index: 5; pointer-events: none;
}

/* ── Danmaku ── */
#danmaku-layer {
  position: fixed; top: 0; left: 0; width: 100%; height: 100%;
  pointer-events: none; overflow: hidden; z-index: 5;
}
@keyframes danmaku-drift {
  0%   { transform: translateX(100vw); opacity: 0; }
  4%   { opacity: 1; }
  92%  { opacity: 1; }
  100% { transform: translateX(-100%); opacity: 0; }
}
.danmaku-item {
  position: absolute; white-space: nowrap;
  padding: 6px 12px; border-radius: 8px;
  font-family: "PingFang SC", "Noto Sans SC", sans-serif;
  pointer-events: none;
}
.danmaku-normal {
  animation: danmaku-drift calc(8s / var(--danmaku-speed, 1)) linear forwards;
  background: rgba(8,8,30,0.70); color: #e0e0f0; font-size: 18px;
}
.danmaku-emphasis {
  animation: danmaku-drift calc(11s / var(--danmaku-speed, 1)) linear forwards;
  background: rgba(8,8,30,0.82); color: #a0c4ff; font-size: 22px;
}
.danmaku-system {
  animation: danmaku-drift calc(6s / var(--danmaku-speed, 1)) linear forwards;
  background: rgba(20,8,30,0.75); color: #c0a0ff; font-size: 16px;
}

/* ── Debug ── */
.courtroom-debug {
  position: fixed; bottom: 4px; right: 8px;
  color: rgba(100,100,100,0.3);
  font-size: 10px; font-family: monospace;
  z-index: 99; pointer-events: none;
}
"""

# ═══════════════════════════════════════════════════════════════════════════════
# Helpers
# ═══════════════════════════════════════════════════════════════════════════════

_DANMAKU_LANE_H = 44
_DANMAKU_LANES = 6


class CourtroomState(rx.ComponentState, NameMixin):
    """审判布局。

    光魂中心——三情绪驱动色调联动（calm/mercy/anger）。
    背景四层：径向光晕（跟情绪联动）+ 点阵纹理 + 环境光环（3 圈呼吸环）
    + 粒子场（中性暖色，不随情绪变化）。
    证据浮层覆盖。分数四圆环横排。计时器右上角纯数字。弹幕底部飘移。

    字段类型说明（全部使用 event_generator 原生支持的类型）：
    - judge_state: str         → stream / clear (值: "calm" | "mercy" | "anger", 空=calm)
    - scores: list[ScoreBar]   → append / update / pop / clear
    - evidence_images: list[Image.Image]  → append / pop / clear
    - evidence_videos: list[VideoLocator] → append / pop / clear
    - danmaku_*: list[str]     → stream / pop / clear
    - timer_state: str         → stream / clear (格式 "stopped:0" / "running:60" / "expired:0")
    - title / sub_title: str   → stream / clear
    """

    judge_state: str = ""
    scores: list[ScoreBar] = []
    evidence_images: list[Image.Image] = []
    evidence_videos: list[VideoLocator] = []
    danmaku_text: list[str] = []
    danmaku_emphasis: list[str] = []
    danmaku_system: list[str] = []
    timer_state: str = ""
    title: str = ""
    sub_title: str = ""

    @classmethod
    def name(cls) -> str:
        return "courtroom"

    @classmethod
    def get_component(cls, **props) -> rx.Component:
        return rx.box(
            # ── Scene background ──
            rx.box(class_name="courtroom-scene"),
            # ── Particle Canvas ──
            rx.el.canvas(id="courtroom-particles"),
            # ── Radial Glow (emotion-linked, z-1) ──
            rx.box(
                class_name=rx.cond(
                    cls.judge_state == "mercy",
                    "courtroom-glow mercy",
                    rx.cond(
                        cls.judge_state == "anger",
                        "courtroom-glow anger",
                        "courtroom-glow calm",
                    ),
                ),
            ),
            # ── Ambient Rings (z-1, 3 breathing rings centered on orb) ──
            rx.box(class_name="courtroom-ambient-ring",
                   style={"width": "400px", "height": "400px"}),
            rx.box(class_name="courtroom-ambient-ring r2",
                   style={"width": "520px", "height": "520px"}),
            rx.box(class_name="courtroom-ambient-ring r3",
                   style={"width": "640px", "height": "640px"}),
            # ── Orb anchor (center, z-2) ──
            rx.box(
                rx.box(
                    class_name=rx.cond(
                        cls.judge_state == "mercy",
                        "courtroom-orb mercy",
                        rx.cond(
                            cls.judge_state == "anger",
                            "courtroom-orb anger",
                            "courtroom-orb calm",
                        ),
                    ),
                ),
                class_name="courtroom-orb-anchor",
            ),
            # ── Evidence layer (z-3, above orb) ──
            rx.cond(
                (cls.evidence_images.length() > 0) | (cls.evidence_videos.length() > 0),
                rx.box(
                    rx.foreach(
                        cls.evidence_images,
                        lambda img: rx.box(
                            rx.image(
                                src=img,
                                width="100%",
                                height="auto",
                                object_fit="contain",
                            ),
                            class_name="courtroom-evidence-item",
                        ),
                    ),
                    rx.foreach(
                        cls.evidence_videos,
                        lambda v: rx.box(
                            rx.video(
                                src=v,
                                playing=True,
                                controls=False,
                                muted=True,
                                loop=True,
                                width="100%",
                                height="auto",
                            ),
                            class_name="courtroom-evidence-item",
                        ),
                    ),
                    class_name="courtroom-evidence-layer",
                ),
            ),
            # ── Score rings (inline, 同 brain 模式) ──
            rx.box(
                rx.foreach(
                    cls.scores,
                    lambda bar, i: rx.box(
                        rx.vstack(
                            rx.box(
                                rx.box(
                                    class_name=rx.cond(
                                        i == 3,
                                        "score-ring-progress total",
                                        "score-ring-progress",
                                    ),
                                    style={
                                        "background": f"conic-gradient({bar.color} calc({bar.value} * 3.6 * 1deg), transparent 0deg)",
                                    },
                                ),
                                rx.text(
                                    f"{bar.value}",
                                    class_name="score-ring-value",
                                ),
                                class_name=rx.cond(
                                    i == 3,
                                    "score-ring total",
                                    "score-ring",
                                ),
                            ),
                            rx.text(bar.label, class_name="score-ring-label"),
                            spacing="1",
                            align="center",
                            class_name="score-ring-wrap",
                        ),
                    ),
                ),
                class_name="courtroom-scores",
            ),
            # ── Timer display (JS-controlled) ──
            rx.text(
                "00:00",
                id="courtroom-timer-display",
                class_name="courtroom-timer timer-safe",
            ),
            # ── Hidden timer store ──
            rx.box(
                rx.el.div(
                    data_timer_state=cls.timer_state,
                ),
                id="courtroom-timer-store",
                display="none",
            ),
            # ── HUD ──
            rx.cond(
                cls.title != "",
                rx.text(cls.title, class_name="courtroom-title"),
            ),
            rx.cond(
                cls.sub_title != "",
                rx.text(cls.sub_title, class_name="courtroom-subtitle"),
            ),
            # ── Danmaku layer ──
            rx.box(
                rx.foreach(
                    cls.danmaku_text,
                    lambda text, i: rx.box(
                        text,
                        class_name="danmaku-item danmaku-normal",
                        style={"top": f"{(i % _DANMAKU_LANES) * _DANMAKU_LANE_H + 8}px"},
                    ),
                ),
                rx.foreach(
                    cls.danmaku_emphasis,
                    lambda text, i: rx.box(
                        text,
                        class_name="danmaku-item danmaku-emphasis",
                        style={"top": f"{(i % _DANMAKU_LANES) * _DANMAKU_LANE_H + 8}px"},
                    ),
                ),
                rx.foreach(
                    cls.danmaku_system,
                    lambda text, i: rx.box(
                        text,
                        class_name="danmaku-item danmaku-system",
                        style={"top": f"{(i % _DANMAKU_LANES) * _DANMAKU_LANE_H + 8}px"},
                    ),
                ),
                id="danmaku-layer",
            ),
            # ── Danmaku signal store ──
            rx.box(
                rx.el.div(data_danmaku_speed="1.0"),
                rx.el.div(data_danmaku_clear=""),
                id="danmaku-signal-store",
                display="none",
            ),
            # ── Scripts ──
            rx.script(_PARTICLE_SCRIPT),
            rx.script(_TIMER_SCRIPT),
            rx.script(_DANMAKU_SIGNAL_SCRIPT),
            # ── CSS ──
            rx.html(f"<style>{_COURTROOM_CSS}</style>"),
            # ── Debug ──
            rx.text("courtroom css", class_name="courtroom-debug"),
            width="100%",
            height="100vh",
            overflow="hidden",
            background="#020202",
            **props,
        )
