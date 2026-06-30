"""Courtroom layout CSS — extracted from layouts/courtroom.py."""

COURTROOM_CSS = """
/* ── Root ── */
.courtroom-root {
  position: relative; width: 100%; height: 100vh;
  overflow: hidden; background: #020202;
  perspective: 1000px;
}

/* ── Scene background (bleed) ── */
.courtroom-scene {
  position: absolute; inset: 0; z-index: 0;
  transition: background 0.6s ease;
}
.courtroom-root.calm .courtroom-scene  { background: #020202; }
.courtroom-root.mercy .courtroom-scene { background: #020212; }
.courtroom-root.anger .courtroom-scene { background: #0a0203; }

/* Dot grid */
.courtroom-scene::before {
  content: ''; position: absolute; inset: 0;
  background-image: radial-gradient(circle, rgba(255,255,255,0.025) 1px, transparent 1px);
  background-size: 50px 50px;
  pointer-events: none; z-index: 0;
}

/* Vignette */
.courtroom-scene::after {
  content: ''; position: absolute; inset: 0;
  pointer-events: none; z-index: 0;
  transition: background 0.6s ease;
}
.courtroom-root.calm .courtroom-scene::after {
  background: radial-gradient(ellipse at center, transparent 50%, rgba(0,0,0,0.45) 100%);
}
.courtroom-root.mercy .courtroom-scene::after {
  background: radial-gradient(ellipse at center, transparent 50%, rgba(2,2,24,0.5) 100%);
}
.courtroom-root.anger .courtroom-scene::after {
  background: radial-gradient(ellipse at center, transparent 50%, rgba(12,2,2,0.55) 100%);
}

/* ── Emotion speed variable — drives all animation durations ── */
.courtroom-root.calm  { --anim-speed: 1; }
.courtroom-root.mercy { --anim-speed: 0.7; }
.courtroom-root.anger { --anim-speed: 0.4; }

/* ── Ripple Glow — concentric ring waves expanding from center ── */
.courtroom-glow {
  position: absolute; top: 50%; left: 50%; z-index: 1;
  width: 0; height: 0; pointer-events: none;
}
.courtroom-glow::before,
.courtroom-glow::after {
  content: ''; position: absolute;
  border-radius: 50%;
  transform: translate(-50%, -50%);
  transition: background 0.6s ease;
}
.courtroom-glow::before {
  width: 1600px; height: 1600px;
}
.courtroom-glow::after {
  width: 2800px; height: 2800px;
}

/* Calm — silver concentric rings, slow wide expansion */
.courtroom-root.calm .courtroom-glow::before {
  background: radial-gradient(circle,
    transparent 0%, transparent 22%,
    rgba(200,210,225,0.14) 22%, rgba(200,210,225,0.0) 26%,
    transparent 26%, transparent 38%,
    rgba(180,190,210,0.10) 38%, rgba(180,190,210,0.0) 41%,
    transparent 41%, transparent 52%,
    rgba(160,175,200,0.07) 52%, rgba(160,175,200,0.0) 54.5%,
    transparent 54.5%, transparent 65%,
    rgba(145,160,185,0.04) 65%, rgba(145,160,185,0.0) 67%,
    transparent 67%
  );
  animation: glow-ripple-calm calc(5s * var(--anim-speed)) ease-out infinite;
}
.courtroom-root.calm .courtroom-glow::after {
  background: radial-gradient(circle,
    transparent 0%, transparent 35%,
    rgba(170,185,210,0.08) 35%, rgba(170,185,210,0.0) 38%,
    transparent 38%, transparent 50%,
    rgba(150,165,190,0.05) 50%, rgba(150,165,190,0.0) 52.5%,
    transparent 52.5%, transparent 68%,
    rgba(135,150,175,0.03) 68%, rgba(135,150,175,0.0) 70%,
    transparent 70%
  );
  animation: glow-ripple-calm calc(7s * var(--anim-speed)) ease-out 2s infinite;
}

/* Mercy — indigo rings, medium expansion */
.courtroom-root.mercy .courtroom-glow::before {
  background: radial-gradient(circle,
    transparent 0%, transparent 20%,
    rgba(129,140,248,0.16) 20%, rgba(129,140,248,0.0) 24%,
    transparent 24%, transparent 36%,
    rgba(99,102,241,0.12) 36%, rgba(99,102,241,0.0) 39%,
    transparent 39%, transparent 50%,
    rgba(80,85,220,0.08) 50%, rgba(80,85,220,0.0) 52.5%,
    transparent 52.5%, transparent 63%,
    rgba(70,75,200,0.05) 63%, rgba(70,75,200,0.0) 65%,
    transparent 65%
  );
  animation: glow-ripple-mercy calc(3.5s * var(--anim-speed)) ease-out infinite;
}
.courtroom-root.mercy .courtroom-glow::after {
  background: radial-gradient(circle,
    transparent 0%, transparent 32%,
    rgba(99,102,241,0.10) 32%, rgba(99,102,241,0.0) 35%,
    transparent 35%, transparent 48%,
    rgba(80,85,220,0.06) 48%, rgba(80,85,220,0.0) 50.5%,
    transparent 50.5%, transparent 65%,
    rgba(70,75,200,0.04) 65%, rgba(70,75,200,0.0) 67%,
    transparent 67%
  );
  animation: glow-ripple-mercy calc(5s * var(--anim-speed)) ease-out 1.5s infinite;
}

/* Anger — crimson rings, fast sharp ripples */
.courtroom-root.anger .courtroom-glow::before {
  background: radial-gradient(circle,
    transparent 0%, transparent 18%,
    rgba(248,113,113,0.22) 18%, rgba(248,113,113,0.0) 23%,
    transparent 23%, transparent 34%,
    rgba(239,68,68,0.16) 34%, rgba(239,68,68,0.0) 37%,
    transparent 37%, transparent 48%,
    rgba(220,50,50,0.10) 48%, rgba(220,50,50,0.0) 50.5%,
    transparent 50.5%, transparent 60%,
    rgba(200,40,40,0.06) 60%, rgba(200,40,40,0.0) 62%,
    transparent 62%
  );
  animation: glow-ripple-anger calc(2s * var(--anim-speed)) ease-out infinite;
}
.courtroom-root.anger .courtroom-glow::after {
  background: radial-gradient(circle,
    transparent 0%, transparent 30%,
    rgba(239,68,68,0.12) 30%, rgba(239,68,68,0.0) 33%,
    transparent 33%, transparent 45%,
    rgba(200,50,50,0.08) 45%, rgba(200,50,50,0.0) 47.5%,
    transparent 47.5%, transparent 62%,
    rgba(180,40,40,0.05) 62%, rgba(180,40,40,0.0) 64%,
    transparent 64%
  );
  animation: glow-ripple-anger calc(3s * var(--anim-speed)) ease-out 1s infinite;
}

@keyframes glow-ripple-calm {
  0%   { transform: translate(-50%, -50%) scale(0.7); opacity: 0; }
  12%  { opacity: 1; }
  100% { transform: translate(-50%, -50%) scale(1.6); opacity: 0; }
}
@keyframes glow-ripple-mercy {
  0%   { transform: translate(-50%, -50%) scale(0.65); opacity: 0; }
  10%  { opacity: 1; }
  100% { transform: translate(-50%, -50%) scale(1.5); opacity: 0; }
}
@keyframes glow-ripple-anger {
  0%   { transform: translate(-50%, -50%) scale(0.6); opacity: 0; }
  8%   { opacity: 1; }
  100% { transform: translate(-50%, -50%) scale(1.7); opacity: 0; }
}

/* ── Sonar Pulses — 3 staggered expanding rings from center ── */
.courtroom-sonar {
  position: absolute; top: 50%; left: 50%; z-index: 1;
  width: 0; height: 0; pointer-events: none;
}
.courtroom-sonar::before,
.courtroom-sonar::after {
  content: ''; position: absolute;
  border-radius: 50%;
  transform: translate(-50%, -50%);
}
.courtroom-sonar::before {
  animation: sonar-ripple calc(4s * var(--anim-speed)) ease-out 0s infinite;
}
.courtroom-sonar::after {
  animation: sonar-ripple calc(4s * var(--anim-speed)) ease-out calc(1.3s * var(--anim-speed)) infinite;
}
/* Third sonar pulse — rendered as a child div in the component tree */
.sonar-p3 {
  position: absolute; top: 50%; left: 50%;
  border-radius: 50%;
  transform: translate(-50%, -50%);
  pointer-events: none;
  animation: sonar-ripple calc(4s * var(--anim-speed)) ease-out calc(2.6s * var(--anim-speed)) infinite;
}

.courtroom-root.calm .courtroom-sonar::before,
.courtroom-root.calm .courtroom-sonar::after,
.courtroom-root.calm .sonar-p3 {
  border: 0.5px solid rgba(180,190,210,0.18);
}
.courtroom-root.mercy .courtroom-sonar::before,
.courtroom-root.mercy .courtroom-sonar::after,
.courtroom-root.mercy .sonar-p3 {
  border: 0.5px solid rgba(129,140,248,0.22);
}
.courtroom-root.anger .courtroom-sonar::before,
.courtroom-root.anger .courtroom-sonar::after,
.courtroom-root.anger .sonar-p3 {
  border: 0.8px solid rgba(239,68,68,0.30);
}

@keyframes sonar-ripple {
  0%   { width: 40px; height: 40px; opacity: 0.9; }
  100% { width: 2600px; height: 2600px; opacity: 0; }
}

/* ── Ambient Rings — color + breathe + rotate + tilt + ellipse warp ×4 ── */
.courtroom-ambient-ring {
  position: absolute; top: 50%; left: 50%; border-radius: 50%;
  pointer-events: none; z-index: 1;
  border: 0.5px solid;
  animation: ring-breathe calc(10s * var(--anim-speed)) ease-in-out infinite,
             ring-rotate 20s linear infinite;
}

.courtroom-root.calm .courtroom-ambient-ring {
  border-color: rgba(180,190,210,0.08);
}
.courtroom-root.mercy .courtroom-ambient-ring {
  border-color: rgba(129,140,248,0.14);
}
.courtroom-root.anger .courtroom-ambient-ring {
  border-color: rgba(239,68,68,0.18);
  border-width: 0.6px;
}

.courtroom-ambient-ring.r2 { animation-delay: calc(-3.5s * var(--anim-speed)), -5s; }
.courtroom-ambient-ring.r3 { animation-delay: calc(-7s * var(--anim-speed)), -10s; }
.courtroom-ambient-ring.r4 { animation-delay: calc(-1.5s * var(--anim-speed)), -15s; }

@keyframes ring-breathe {
  0%, 100% {
    opacity: 0.06;
    transform: translate(-50%, -50%) scale(1, 1) rotateX(60deg);
  }
  25% {
    opacity: 0.40;
    transform: translate(-50%, -50%) scale(1.05, 1.08) rotateX(60deg);
  }
  50% {
    opacity: 0.08;
    transform: translate(-50%, -50%) scale(1, 1) rotateX(60deg);
  }
  75% {
    opacity: 0.35;
    transform: translate(-50%, -50%) scale(1.06, 1.03) rotateX(60deg);
  }
}
@keyframes ring-rotate {
  from { transform: translate(-50%, -50%) rotateX(60deg) rotate(0deg); }
  to   { transform: translate(-50%, -50%) rotateX(60deg) rotate(360deg); }
}

/* ═══════════════════════════════════════════════════════════════════════════════
   Orb Cluster — 8 光团 screen 叠加制造失重流体
   ═══════════════════════════════════════════════════════════════════════════════ */

.courtroom-core {
  position: absolute; top: 50%; left: 50%; z-index: 2;
  width: 0; height: 0;
}

/* Anger — cluster shake */
.courtroom-root.anger .courtroom-core {
  animation: core-shake 0.25s ease-in-out infinite;
}
@keyframes core-shake {
  0%, 100% { transform: translate(0, 0); }
  10%      { transform: translate(-1.5px, 1px); }
  20%      { transform: translate(1.5px, -1px); }
  30%      { transform: translate(-1px, -1.5px); }
  40%      { transform: translate(1px, 1.5px); }
  50%      { transform: translate(-2px, 0); }
  60%      { transform: translate(2px, 1px); }
  70%      { transform: translate(-1px, -1px); }
  80%      { transform: translate(1.5px, 0); }
  90%      { transform: translate(0, -1.5px); }
}

/* Wrapper — float, each with its own trajectory */
.orb-wrap {
  position: absolute; top: 50%; left: 50%;
  width: 0; height: 0; pointer-events: none;
}
.orb-wrap.n1 { animation: orb-float-a calc(3s * var(--anim-speed))  ease-in-out infinite; }
.orb-wrap.n2 { animation: orb-float-b calc(3.5s * var(--anim-speed)) ease-in-out 0.4s infinite; }
.orb-wrap.n3 { animation: orb-float-c calc(4s * var(--anim-speed)) ease-in-out 0.7s infinite; }
.orb-wrap.n4 { animation: orb-float-d calc(4.5s * var(--anim-speed)) ease-in-out 1.1s infinite; }
.orb-wrap.n5 { animation: orb-float-e calc(5s * var(--anim-speed)) ease-in-out 0.3s infinite; }
.orb-wrap.n6 { animation: orb-float-b calc(6s * var(--anim-speed)) ease-in-out 1.5s infinite; }
.orb-wrap.n7 { animation: orb-float-c calc(5.5s * var(--anim-speed)) ease-in-out 0.9s infinite; }
.orb-wrap.n8 { animation: orb-float-a calc(8s * var(--anim-speed)) ease-in-out 2s infinite; }

/* Orb — radial gradient blob, screen blend, irregular shape, independent scale pulse */
.orb {
  position: absolute;
  mix-blend-mode: screen;
  pointer-events: none;
  transition: background 0.6s ease;
  top: 50%; left: 50%;
}

/* Each orb: unique size, irregular border-radius, offset gradient center, blur depth */
.orb-wrap.n1 .orb {
  width: 75px; height: 90px; filter: blur(2px);
  border-radius: 42% 58% 55% 45%;
  margin-left: -40px; margin-top: -38px;
  animation: orb-pulse-a calc(2.2s * var(--anim-speed)) ease-in-out infinite;
}
.orb-wrap.n2 .orb {
  width: 120px; height: 100px; filter: blur(3px);
  border-radius: 55% 40% 48% 58%;
  margin-left: -55px; margin-top: -60px;
  animation: orb-pulse-b calc(2.8s * var(--anim-speed)) ease-in-out 0.4s infinite;
}
.orb-wrap.n3 .orb {
  width: 95px; height: 115px; filter: blur(2px);
  border-radius: 38% 62% 52% 44%;
  margin-left: -50px; margin-top: -48px;
  animation: orb-pulse-c calc(3.2s * var(--anim-speed)) ease-in-out 0.7s infinite;
}
.orb-wrap.n4 .orb {
  width: 150px; height: 125px; filter: blur(3.5px);
  border-radius: 48% 45% 58% 42%;
  margin-left: -78px; margin-top: -68px;
  animation: orb-pulse-a calc(3.8s * var(--anim-speed)) ease-in-out 1.1s infinite;
}
.orb-wrap.n5 .orb {
  width: 200px; height: 180px; filter: blur(5px);
  border-radius: 52% 42% 46% 55%;
  margin-left: -95px; margin-top: -90px;
  animation: orb-pulse-b calc(4.5s * var(--anim-speed)) ease-in-out 0.3s infinite;
}
.orb-wrap.n6 .orb {
  width: 240px; height: 210px; filter: blur(7px);
  border-radius: 44% 56% 50% 48%;
  margin-left: -115px; margin-top: -100px;
  animation: orb-pulse-c calc(5s * var(--anim-speed)) ease-in-out 1.5s infinite;
}
.orb-wrap.n7 .orb {
  width: 280px; height: 250px; filter: blur(8px);
  border-radius: 40% 52% 58% 46%;
  margin-left: -145px; margin-top: -125px;
  animation: orb-pulse-a calc(5.5s * var(--anim-speed)) ease-in-out 0.9s infinite;
}
.orb-wrap.n8 .orb {
  width: 450px; height: 400px; filter: blur(20px);
  border-radius: 46% 48% 52% 44%;
  margin-left: -220px; margin-top: -210px;
  animation: orb-pulse-c calc(7s * var(--anim-speed)) ease-in-out 2s infinite;
}

/* Emotion colors — radial gradient from bright center to transparent edge */
.courtroom-root.calm .orb.core {
  background: radial-gradient(circle at center,
    rgba(220,225,240,0.9) 0%, rgba(200,210,230,0.5) 30%, transparent 70%);
}
.courtroom-root.calm .orb.mid {
  background: radial-gradient(circle at center,
    rgba(200,210,225,0.7) 0%, rgba(170,185,205,0.35) 30%, transparent 70%);
}
.courtroom-root.calm .orb.haze {
  background: radial-gradient(circle at center,
    rgba(180,195,215,0.4) 0%, rgba(150,165,185,0.15) 30%, transparent 70%);
}

.courtroom-root.mercy .orb.core {
  background: radial-gradient(circle at center,
    rgba(180,185,255,0.9) 0%, rgba(140,150,248,0.55) 30%, transparent 70%);
}
.courtroom-root.mercy .orb.mid {
  background: radial-gradient(circle at center,
    rgba(150,155,240,0.75) 0%, rgba(110,120,225,0.4) 30%, transparent 70%);
}
.courtroom-root.mercy .orb.haze {
  background: radial-gradient(circle at center,
    rgba(120,130,220,0.45) 0%, rgba(90,100,200,0.18) 30%, transparent 70%);
}

.courtroom-root.anger .orb.core {
  background: radial-gradient(circle at center,
    rgba(255,180,180,0.95) 0%, rgba(248,113,113,0.6) 30%, transparent 70%);
}
.courtroom-root.anger .orb.mid {
  background: radial-gradient(circle at center,
    rgba(248,140,140,0.8) 0%, rgba(239,68,68,0.45) 30%, transparent 70%);
}
.courtroom-root.anger .orb.haze {
  background: radial-gradient(circle at center,
    rgba(239,100,100,0.5) 0%, rgba(200,50,50,0.2) 30%, transparent 70%);
}

/* Anger orbs — brighter, tighter */
.courtroom-root.anger .orb.core { filter: blur(0.5px); }
.courtroom-root.anger .orb.mid  { filter: blur(2px); }
.courtroom-root.anger .orb.haze { filter: blur(8px); }

/* ── Float keyframes — 5 unique trajectories, wider drift ── */
@keyframes orb-float-a {
  0%, 100% { transform: translate(0, 0); }
  25%      { transform: translate(22px, -30px); }
  50%      { transform: translate(-16px, -20px); }
  75%      { transform: translate(-28px, 16px); }
}
@keyframes orb-float-b {
  0%, 100% { transform: translate(0, 0); }
  25%      { transform: translate(-28px, -14px); }
  50%      { transform: translate(12px, 30px); }
  75%      { transform: translate(30px, -12px); }
}
@keyframes orb-float-c {
  0%, 100% { transform: translate(0, 0); }
  33%      { transform: translate(16px, 28px); }
  66%      { transform: translate(-30px, -12px); }
}
@keyframes orb-float-d {
  0%, 100% { transform: translate(0, 0); }
  25%      { transform: translate(-22px, 32px); }
  50%      { transform: translate(32px, 6px); }
  75%      { transform: translate(6px, -24px); }
}
@keyframes orb-float-e {
  0%, 100% { transform: translate(0, 0); }
  25%      { transform: translate(16px, -32px); }
  50%      { transform: translate(-32px, -6px); }
  75%      { transform: translate(-12px, 28px); }
}

/* ── Pulse keyframes — scale breathing, 3 phases ── */
@keyframes orb-pulse-a {
  0%, 100% { transform: scale(0.85); opacity: 0.4; }
  50%      { transform: scale(1.3);  opacity: 0.95; }
}
@keyframes orb-pulse-b {
  0%, 100% { transform: scale(0.75); opacity: 0.35; }
  50%      { transform: scale(1.4);  opacity: 0.9; }
}
@keyframes orb-pulse-c {
  0%, 100% { transform: scale(0.9);  opacity: 0.3; }
  50%      { transform: scale(1.2);  opacity: 0.8; }
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
