"""PeachBlossomStage 资产：mood 配置、JS 脚本、CSS。

私有模块，由 peach_blossom_stage.py 导入。不与 Reflex 生命周期耦合。
"""

# ═══════════════════════════════════════════════════════════════════════════════
# Atmosphere → 各层配置（Python 侧用于 CSS，JS 侧用于 Canvas）
# ═══════════════════════════════════════════════════════════════════════════════

MOOD = {
    "serene": {
        "label": "宁静",
        "particle_type": "water",
        "particle_count": 60,
        "particle_colors": [
            "rgba(200,220,248,0.5)",
            "rgba(138,180,224,0.3)",
            "rgba(180,200,230,0.25)",
        ],
        "particle_speed": 0.3,
    },
    "enchanted": {
        "label": "惊艳",
        "particle_type": "petal",
        "particle_count": 120,
        "particle_colors": [
            "rgba(248,208,220,0.55)",
            "rgba(232,168,192,0.35)",
            "rgba(255,220,235,0.4)",
        ],
        "particle_speed": 0.6,
    },
    "tense": {
        "label": "紧张",
        "particle_type": "water",
        "particle_count": 40,
        "particle_colors": [
            "rgba(140,150,170,0.4)",
            "rgba(100,110,130,0.25)",
            "rgba(120,130,150,0.2)",
        ],
        "particle_speed": 0.15,
    },
    "released": {
        "label": "释放",
        "particle_type": "gold_burst",
        "particle_count": 180,
        "particle_colors": [
            "rgba(248,224,128,0.7)",
            "rgba(240,208,64,0.5)",
            "rgba(255,240,180,0.6)",
        ],
        "particle_speed": 1.0,
    },
    "tranquil": {
        "label": "恬静",
        "particle_type": "petal",
        "particle_count": 80,
        "particle_colors": [
            "rgba(240,220,160,0.4)",
            "rgba(220,200,140,0.25)",
            "rgba(245,225,170,0.3)",
        ],
        "particle_speed": 0.35,
    },
    "wistful": {
        "label": "怅然",
        "particle_type": "water",
        "particle_count": 50,
        "particle_colors": [
            "rgba(160,155,150,0.35)",
            "rgba(130,125,120,0.2)",
            "rgba(150,145,140,0.18)",
        ],
        "particle_speed": 0.2,
    },
}

DEFAULT_MOOD = "serene"


def mood_js_config() -> str:
    """Generate JS mood config object string."""
    entries = []
    for key, cfg in MOOD.items():
        parts = [
            f"type:'{cfg['particle_type']}'",
            f"count:{cfg['particle_count']}",
            f"colors:{cfg['particle_colors']}",
            f"speed:{cfg['particle_speed']}",
        ]
        entries.append(f"{key}:{{{','.join(parts)}}}")
    return "{" + ",".join(entries) + "}"


# ═══════════════════════════════════════════════════════════════════════════════
# JS Scripts — Reflex → Canvas 桥接 + Canvas 动画
# ═══════════════════════════════════════════════════════════════════════════════

SYNC_SCRIPT = f"""
(function init(){{
  var store=document.getElementById('peach-store');
  if(!store){{setTimeout(init,80);return;}}
  var MOODS={mood_js_config()};
  var lastMood='',lastTrans='',firstRun=true;
  function sync(){{
    var mood=store.getAttribute('data-atmosphere')||'';
    var trans=store.getAttribute('data-transition')||'';
    var dirty=false;

    if(mood&&(mood!==lastMood||firstRun)){{
      lastMood=mood;
      var cfg=MOODS[mood]||MOODS['serene'];
      window.__PEACH_PARTICLE_CONFIG__={{type:cfg.type,count:cfg.count,colors:cfg.colors,speed:cfg.speed}};
      dirty=true;
    }}

    if(trans!==lastTrans){{
      lastTrans=trans;
      if(trans==='constrict'){{
        window.__PEACH_TRANSITION__={{state:trans,startTime:performance.now()}};
      }}else{{
        window.__PEACH_TRANSITION__=null;
      }}
    }}

    firstRun=false;
    if(!dirty)return;
  }}
  sync();
  new MutationObserver(sync).observe(store,{{attributes:true,attributeFilter:['data-atmosphere','data-transition']}});
}})();
"""

PARTICLE_SCRIPT = r"""
(function S(){
  var c=document.getElementById('peach-particles');
  if(!c){setTimeout(S,80);return;}
  var ctx=c.getContext('2d'),W,H;
  function R(){W=c.width=window.innerWidth;H=c.height=window.innerHeight;}
  window.addEventListener('resize',R);R();
  var CFG=window.__PEACH_PARTICLE_CONFIG__||{type:'water',count:60,colors:['rgba(200,220,248,0.5)','rgba(138,180,224,0.3)'],speed:0.3};
  var pool=[];

  function P(){
    this.bursting=false; // true only during one-shot burst window
    this.reset=function(mode){
      if(mode==='petal'){
        this.x=Math.random()*W; this.y=-20-Math.random()*H*0.5;
        this.sway=Math.random()*6.28; this.swaySp=0.015+Math.random()*0.025;
        this.fallSp=0.5+Math.random()*0.6; this.size=1.5+Math.random()*2.5;
        this.bursting=false;
      }else if(mode==='gold_burst'){
        var burstStart=window.__PEACH_BURST_START__||0;
        var burstAge=(performance.now()-burstStart)/1000;
        if(burstStart&&burstAge>3.5){
          // Post-burst: gentle gold floaters — no more explosions
          this.x=Math.random()*W; this.y=Math.random()*H;
          this.wave=Math.random()*6.28; this.waveSp=0.008+Math.random()*0.015;
          this.driftSp=0.15+Math.random()*0.35; this.size=1+Math.random()*2;
          this.life=0.3+Math.random()*0.4; this.bursting=false;
        }else{
          var a=Math.random()*6.28,sp=CFG.speed*(1.5+Math.random()*3.5);
          this.vx=Math.cos(a)*sp; this.vy=Math.sin(a)*sp;
          this.x=W*0.5; this.y=H*0.5; this.life=1.0; this.size=2+Math.random()*4;
          this.bursting=true;
        }
      }else{
        this.x=Math.random()*W; this.y=Math.random()*H;
        this.wave=Math.random()*6.28; this.waveSp=0.01+Math.random()*0.02;
        this.driftSp=0.3+Math.random()*0.5; this.size=0.8+Math.random()*2.2;
        this.bursting=false;
      }
      this.phase=Math.random()*6.28;
    };
    this.update=function(){
      var trP=window.__PEACH_TR_PHASE__||0;
      var trPr=window.__PEACH_TR_PROGRESS__||0;
      // Phase 3: force non-bursting particles into gold_burst from center
      if(trP===3&&trPr>0.05&&!this.bursting&&Math.random()<0.12){
        var a=Math.random()*6.28,sp=CFG.speed*(2+Math.random()*4);
        this.vx=Math.cos(a)*sp;this.vy=Math.sin(a)*sp;
        this.x=W*0.5;this.y=H*0.45;this.life=1.0;this.size=2+Math.random()*5;
        this.bursting=true;
        return;
      }
      if(CFG.type==='petal'){
        this.y+=CFG.speed*this.fallSp; this.sway+=this.swaySp;
        this.x+=Math.sin(this.sway)*0.5;
        if(this.y>H+40){this.y=-20;this.x=Math.random()*W;this.sway=Math.random()*6.28;}
        if(this.x<-40)this.x=W+40;if(this.x>W+40)this.x=-40;
      }else if(CFG.type==='gold_burst'){
        if(this.bursting){
          this.vx*=0.97;this.vy*=0.97;this.x+=this.vx*CFG.speed;this.y+=this.vy*CFG.speed;
          this.life-=0.003;
          if(this.life<=0||this.x<-80||this.x>W+80||this.y<-80||this.y>H+80)this.reset('gold_burst');
        }else{
          // Post-burst gentle drift — gold floaters that never re-explode
          this.x+=CFG.speed*this.driftSp*0.4; this.wave+=this.waveSp;
          this.y+=Math.sin(this.wave)*0.25;
          this.life-=0.0008;
          if(this.life<=0||this.x>W+40){this.x=-20;this.y=Math.random()*H;this.life=0.3+Math.random()*0.4;}
          if(this.y<-40)this.y=H+40;if(this.y>H+40)this.y=-40;
        }
      }else{
        this.x+=CFG.speed*this.driftSp;this.wave+=this.waveSp;
        this.y+=Math.sin(this.wave)*0.3;
        if(this.x>W+40){this.x=-20;this.y=Math.random()*H;}
        if(this.y<-40)this.y=H+40;if(this.y>H+40)this.y=-40;
      }
      // Phase 1: contract toward center
      if(trP===1){
        var cx=W*0.5,cy=H*0.45;
        var force=0.02*(1+trPr*2);
        this.x+=(cx-this.x)*force;this.y+=(cy-this.y)*force;
      }
    };
    this.draw=function(t){
      var trP=window.__PEACH_TR_PHASE__||0;
      var tw=0.6+0.4*Math.sin(t*0.0004+this.phase);
      var alpha;
      if(CFG.type==='gold_burst'){
        alpha=this.bursting?Math.max(0,this.life)*tw*1.5:Math.max(0,this.life)*tw*0.7;
      }else{
        alpha=tw;
      }
      if(trP===2){alpha*=0.1;} // Critical: near total darkness
      else if(trP===1){alpha*=0.3+0.7*(1-(window.__PEACH_TR_PROGRESS__||0));} // Fade during constrict
      var sz=CFG.type==='gold_burst'?(this.bursting?this.size*this.life:this.size):this.size;
      var col=CFG.colors[Math.floor(Math.abs(Math.sin(this.phase*3.7))*CFG.colors.length)%CFG.colors.length];
      var m=col.match(/[\d.]+/g);
      if(m&&m.length>=4){
        ctx.fillStyle='rgba('+m[0]+','+m[1]+','+m[2]+','+Math.min(1,parseFloat(m[3])*alpha*1.6).toFixed(3)+')';
      }else{ctx.fillStyle=col;}
      ctx.beginPath();ctx.arc(this.x,this.y,Math.max(0.3,sz),0,6.28);ctx.fill();
    };
    this.reset(CFG.type);
  }
  function ensurePool(n){while(pool.length<n)pool.push(new P());while(pool.length>n)pool.pop();}
  ensurePool(CFG.count);
  var lastType=CFG.type,lastCount=CFG.count;
  function sync(){
    var g=window.__PEACH_PARTICLE_CONFIG__;if(!g)return;
    if(g.type&&g.type!==lastType){
      lastType=g.type;CFG.type=g.type;
      if(g.type==='gold_burst'){window.__PEACH_BURST_START__=performance.now();}
      for(var i=0;i<pool.length;i++)pool[i].reset(g.type);
    }
    if(g.count&&g.count!==lastCount){lastCount=g.count;CFG.count=g.count;ensurePool(g.count);}
    if(g.colors)CFG.colors=g.colors;
    if(g.speed!==undefined)CFG.speed=g.speed;
  }
  function A(t){
    sync();
    // ── 3-stage transition state machine ──
    var tr=window.__PEACH_TRANSITION__;
    var trPhase=0,trProgress=0;
    if(tr&&tr.state==='constrict'){
      var el=(t-tr.startTime)/1000;
      if(el<0.8){trPhase=1;trProgress=el/0.8;}
      else if(el<1.2){trPhase=2;}
      else if(el<2.5){trPhase=3;trProgress=(el-1.2)/1.3;}
      else{window.__PEACH_TRANSITION__=null;}
    }
    window.__PEACH_TR_PHASE__=trPhase;
    window.__PEACH_TR_PROGRESS__=trProgress;
    ctx.clearRect(0,0,W,H);
    for(var i=0;i<pool.length;i++){pool[i].update();pool[i].draw(t);}
    requestAnimationFrame(A);
  }
  requestAnimationFrame(A);
})();
"""

# ═══════════════════════════════════════════════════════════════════════════════
# CSS (raw string, injected via rx.html)
# ═══════════════════════════════════════════════════════════════════════════════

PEACH_CSS = """
/* Scene */
.peach-scene{position:absolute;inset:0;background:#020202;overflow:hidden;}
.peach-scene::before{content:'';position:absolute;inset:0;z-index:0;
  background-image:radial-gradient(circle,rgba(255,255,255,0.022)1px,transparent 1px);
  background-size:50px 50px;pointer-events:none;}

/* Radial Glow (z-10) */
.peach-glow{position:absolute;top:50%;left:50%;z-index:1;width:0;height:0;pointer-events:none;}
.peach-glow::before{content:'';position:absolute;width:700px;height:700px;border-radius:50%;
  transform:translate(-50%,-50%);transition:background 0.6s ease;}
.peach-glow.serene::before{background:radial-gradient(circle,rgba(180,190,210,0.06)0%,rgba(156,163,175,0.03)35%,transparent 70%);}
.peach-glow.enchanted::before{background:radial-gradient(circle,rgba(220,180,190,0.08)0%,rgba(200,160,170,0.04)35%,transparent 70%);}
.peach-glow.tense::before{background:radial-gradient(circle,rgba(80,60,30,0.03)0%,rgba(60,40,20,0.02)35%,transparent 70%);}
.peach-glow.released::before{background:radial-gradient(circle,rgba(240,220,140,0.1)0%,rgba(220,200,120,0.05)35%,transparent 70%);}
.peach-glow.tranquil::before{background:radial-gradient(circle,rgba(220,200,150,0.06)0%,rgba(200,180,130,0.03)35%,transparent 70%);}
.peach-glow.wistful::before{background:radial-gradient(circle,rgba(120,115,110,0.04)0%,rgba(100,95,90,0.02)35%,transparent 70%);}

/* Grade overlay (z-15) */
.peach-grade{position:fixed;inset:0;z-index:2;pointer-events:none;transition:background 0.6s ease;}
.peach-grade.serene{background:rgba(168,184,200,0.12);}
.peach-grade.enchanted{background:rgba(232,192,208,0.18);}
.peach-grade.tense{background:rgba(48,32,16,0.30);}
.peach-grade.released{background:rgba(240,232,192,0.12);}
.peach-grade.tranquil{background:rgba(232,216,176,0.10);}
.peach-grade.wistful{background:rgba(144,136,128,0.22);}

/* Vignette (z-16) */
.peach-vignette{position:fixed;inset:0;z-index:3;pointer-events:none;transition:background 0.6s ease;}
.peach-vignette.serene{background:radial-gradient(ellipse at center,transparent 40%,rgba(0,0,0,0.15)70%,rgba(0,0,0,0.35)100%);}
.peach-vignette.enchanted{background:radial-gradient(ellipse at center,transparent 45%,rgba(0,0,0,0.12)70%,rgba(0,0,0,0.28)100%);}
.peach-vignette.tense{background:radial-gradient(ellipse at 50% 45%,transparent 3%,rgba(0,0,0,0.25)8%,rgba(0,0,0,0.65)20%,rgba(0,0,0,0.92)50%);}
.peach-vignette.released{background:radial-gradient(ellipse at center,transparent 55%,rgba(0,0,0,0.08)75%,rgba(0,0,0,0.2)100%);}
.peach-vignette.tranquil{background:radial-gradient(ellipse at center,transparent 50%,rgba(0,0,0,0.1)72%,rgba(0,0,0,0.25)100%);}
.peach-vignette.wistful{background:radial-gradient(ellipse at center,transparent 30%,rgba(0,0,0,0.25)65%,rgba(0,0,0,0.55)100%);}

/* Light Point (z-6) — cave scene "山有小口，仿佛若有光" */
@keyframes point-breathe{0%,100%{transform:scale(1);opacity:0.5;}50%{transform:scale(1.4);opacity:0.9;}}
.peach-slit{position:fixed;top:45%;left:50%;z-index:6;width:40px;height:40px;margin-left:-20px;margin-top:-20px;
  border-radius:50%;pointer-events:none;opacity:0;transition:opacity 0.8s ease;
  background:radial-gradient(circle,rgba(255,250,240,0.7)0%,rgba(255,240,200,0.3)30%,rgba(240,210,160,0.08)60%,transparent 100%);
  box-shadow:0 0 30px rgba(255,245,230,0.4),0 0 80px rgba(240,220,180,0.15),0 0 150px rgba(220,200,150,0.06);}
.peach-slit.tense{opacity:1;animation:point-breathe 3s ease-in-out infinite;}

/* ── Transition: 时空隧道光点扩张 (~4s) ── */

/* z-6: 隧道壁 — 透明圆心 + 巨大黑色 box-shadow（圆内透光，圆外全黑） */
@keyframes tunnel-open{
  0%   {width:6vmin;height:6vmin;margin-left:-3vmin;margin-top:-3vmin;opacity:1;}
  30%  {width:20vmin;height:20vmin;margin-left:-10vmin;margin-top:-10vmin;opacity:1;}
  50%  {width:50vmin;height:50vmin;margin-left:-25vmin;margin-top:-25vmin;opacity:1;}
  55%  {width:60vmin;height:60vmin;margin-left:-30vmin;margin-top:-30vmin;opacity:1;}
  80%  {width:240vmin;height:240vmin;margin-left:-120vmin;margin-top:-120vmin;opacity:1;}
  100% {width:300vmin;height:300vmin;margin-left:-150vmin;margin-top:-150vmin;opacity:0;}
}
.peach-transition-overlay{position:fixed;top:45%;left:50%;z-index:6;pointer-events:none;
  border-radius:50%;background:transparent;
  box-shadow:0 0 0 150vmax rgba(0,0,0,0.95);
  opacity:0;}
.peach-transition-constrict .peach-transition-overlay{animation:tunnel-open 4s ease-in-out;}

/* 洞口边缘金色光晕环 */
.peach-transition-overlay::after{content:'';position:absolute;inset:-30px;border-radius:50%;
  box-shadow:inset 0 0 60px 20px rgba(255,220,140,0.5),inset 0 0 120px 40px rgba(255,200,100,0.2);
  opacity:0;pointer-events:none;}
.peach-transition-constrict .peach-transition-overlay::after{animation:tunnel-rim 4s ease-in-out;}
@keyframes tunnel-rim{
  0%   {opacity:0.2;}
  20%  {opacity:0.5;}
  40%  {opacity:0.9;}
  60%  {opacity:0.6;}
  100% {opacity:0;}
}

/* z-5: 隧道光源 — 纯白中心 + 同心光环（时光穿梭纵深感） */
.peach-transition-glow{position:fixed;inset:0;z-index:5;pointer-events:none;opacity:0;
  background:radial-gradient(circle at 50% 45%,rgba(255,255,255,1)0%,rgba(255,255,255,0.9)4%,rgba(255,252,248,0.5)12%,rgba(240,238,235,0.15)28%,transparent 45%);}
.peach-transition-constrict .peach-transition-glow{animation:tunnel-glow 4s ease-in-out;}
@keyframes tunnel-glow{
  0%   {opacity:0.95;transform:scale(0.3);}
  30%  {opacity:1;transform:scale(0.55);}
  55%  {opacity:1;transform:scale(1);}
  80%  {opacity:0.4;transform:scale(1.8);}
  100% {opacity:0;transform:scale(2.5);}
}

/* ::before 同心光环 — 扩散的速度环（非旋转，缩放产生纵深感） */
.peach-transition-glow::before{content:'';position:absolute;inset:-30%;
  background:repeating-radial-gradient(circle at 50% 45%,transparent 0%,transparent 5%,rgba(255,255,255,0.15)5.8%,transparent 6.5%,transparent 10%,rgba(255,255,255,0.08)10.8%,transparent 11.5%);opacity:0;}
.peach-transition-constrict .peach-transition-glow::before{animation:tunnel-rings 4s ease-in-out;}
@keyframes tunnel-rings{
  0%   {opacity:0;transform:scale(0.25);}
  30%  {opacity:0.5;transform:scale(0.55);}
  55%  {opacity:0.8;transform:scale(1.1);}
  80%  {opacity:0.25;transform:scale(2);}
  100% {opacity:0;transform:scale(3);}
}

/* Canvas layers */
#peach-particles{position:fixed;top:0;left:0;width:100%;height:100%;z-index:4;pointer-events:none;}

/* Background img (z-3, below particles z-4 so particles float above bg) */
@keyframes bg-fade-in{from{opacity:0;}to{opacity:1;}}
.peach-bg-img{position:absolute;inset:0;z-index:3;width:100%;height:100%;object-fit:cover;animation:bg-fade-in 0.8s ease-out both;}

/* Background video (z-3, same layer as bg-img) */
.peach-bg-video{position:absolute;inset:0;z-index:3;width:100%;height:100%;object-fit:cover;opacity:0;transition:opacity 0.8s ease;}

/* Overlay (z-40) */
.peach-overlay-area{position:absolute;inset:0;z-index:7;pointer-events:none;
  display:flex;align-items:center;justify-content:center;flex-wrap:wrap;gap:24px;padding:60px;}
@keyframes overlay-slide-in{from{transform:translateX(60px);opacity:0;}to{transform:translateX(0);opacity:1;}}
.peach-overlay-item{max-width:35%;max-height:50%;border-radius:8px;
  box-shadow:0 8px 40px rgba(0,0,0,0.5);animation:overlay-slide-in 0.5s ease-out both;}

/* Body text (z-45) */
.peach-body-area{position:absolute;bottom:18%;left:50%;transform:translateX(-50%);
  z-index:8;pointer-events:none;text-align:center;max-width:70%;transition:transform 0.4s,font-size 0.4s;}
.peach-body-area.compact{transform:translateX(-50%)translateY(40px);}
.peach-body-text{font-size:3rem;font-weight:700;color:#ffffff;letter-spacing:0.1em;line-height:1.6;
  text-shadow:0 0 40px rgba(255,245,220,0.5),0 0 100px rgba(255,220,160,0.25),0 0 200px rgba(200,160,100,0.1);white-space:pre-wrap;}
.peach-body-area.compact .peach-body-text{font-size:2rem;}

/* HUD (z-50) */
.peach-hud{position:absolute;top:0;left:0;right:0;z-index:10;
  display:flex;justify-content:space-between;align-items:flex-start;padding:28px 40px;pointer-events:none;}
.peach-chapter-title{font-size:1.3rem;color:rgba(240,232,200,0.7);letter-spacing:0.12em;font-weight:400;transition:opacity 0.8s ease;}
.peach-progress{display:flex;align-items:center;gap:8px;}
.peach-progress-dot{width:10px;height:10px;border-radius:50%;background:rgba(255,255,255,0.1);transition:all 0.5s ease;}
.peach-progress-dot.done{background:rgba(255,255,255,0.25);}
.peach-progress-dot.active{background:rgba(255,240,200,0.8);box-shadow:0 0 12px rgba(255,240,200,0.4);width:12px;height:12px;}
.peach-progress-line{width:28px;height:1.5px;background:rgba(255,255,255,0.08);}
"""
