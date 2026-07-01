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
        "sigil_inner": "rgba(248,240,200,0.9)",
        "sigil_outer": "rgba(230,210,160,0.3)",
        "sigil_size": 1.0,
        "sigil_breath_s": 4.0,
        "sigil_trail": 15,
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
        "sigil_inner": "rgba(248,220,210,0.9)",
        "sigil_outer": "rgba(240,200,180,0.3)",
        "sigil_size": 1.05,
        "sigil_breath_s": 2.0,
        "sigil_trail": 12,
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
        "sigil_inner": "rgba(180,150,100,0.85)",
        "sigil_outer": "rgba(120,80,40,0.2)",
        "sigil_size": 0.7,
        "sigil_breath_s": 1.5,
        "sigil_trail": 5,
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
        "sigil_inner": "rgba(250,235,170,0.95)",
        "sigil_outer": "rgba(240,210,130,0.35)",
        "sigil_size": 1.3,
        "sigil_breath_s": 3.0,
        "sigil_trail": 20,
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
        "sigil_inner": "rgba(245,225,170,0.9)",
        "sigil_outer": "rgba(230,200,140,0.3)",
        "sigil_size": 1.1,
        "sigil_breath_s": 5.0,
        "sigil_trail": 18,
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
        "sigil_inner": "rgba(180,170,160,0.8)",
        "sigil_outer": "rgba(140,130,120,0.2)",
        "sigil_size": 0.8,
        "sigil_breath_s": 6.0,
        "sigil_trail": 8,
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
            f"sigilInner:'{cfg['sigil_inner']}'",
            f"sigilOuter:'{cfg['sigil_outer']}'",
            f"sigilSize:{cfg['sigil_size']}",
            f"sigilBreathS:{cfg['sigil_breath_s']}",
            f"sigilTrail:{cfg['sigil_trail']}",
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
  var POSITIONS={{center:{{x:0.50,y:0.45}},stream_left:{{x:0.28,y:0.55}},forest_edge:{{x:0.35,y:0.48}},cave_entrance:{{x:0.50,y:0.52}},village_center:{{x:0.50,y:0.40}}}};
  var lastMood='',lastPos='center',lastGesture='',lastTrans='',firstRun=true;
  function sync(){{
    var mood=store.getAttribute('data-atmosphere')||'';
    var pos=store.getAttribute('data-sigil-position')||'center';
    var gesture=store.getAttribute('data-sigil-gesture')||'';
    var trans=store.getAttribute('data-transition')||'';
    var dirty=false;

    if(mood&&(mood!==lastMood||firstRun)){{
      lastMood=mood;
      var cfg=MOODS[mood]||MOODS['serene'];
      window.__PEACH_PARTICLE_CONFIG__={{type:cfg.type,count:cfg.count,colors:cfg.colors,speed:cfg.speed}};
      var sigil=window.__PEACH_SIGIL_CONFIG__||{{}};
      sigil.mood=mood;sigil.innerColor=cfg.sigilInner;sigil.outerColor=cfg.sigilOuter;
      sigil.size=cfg.sigilSize;sigil.breathS=cfg.sigilBreathS;sigil.trailLen=cfg.sigilTrail;
      window.__PEACH_SIGIL_CONFIG__=sigil;
      dirty=true;
    }}

    if(pos&&(pos!==lastPos||firstRun)){{
      lastPos=pos;
      var pt=POSITIONS[pos]||POSITIONS['center'];
      var sigil=window.__PEACH_SIGIL_CONFIG__||{{}};
      sigil.targetX=pt.x;sigil.targetY=pt.y;
      window.__PEACH_SIGIL_CONFIG__=sigil;
    }}

    if(gesture!==lastGesture||firstRun){{
      lastGesture=gesture;
      window.__peachSetGesture&&window.__peachSetGesture(!!gesture);
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
  new MutationObserver(sync).observe(store,{{attributes:true,attributeFilter:['data-atmosphere','data-sigil-position','data-sigil-gesture','data-transition']}});
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
    this.reset=function(mode){
      if(mode==='petal'){
        this.x=Math.random()*W; this.y=-20-Math.random()*H*0.5;
        this.sway=Math.random()*6.28; this.swaySp=0.015+Math.random()*0.025;
        this.fallSp=0.5+Math.random()*0.6; this.size=1.5+Math.random()*2.5;
      }else if(mode==='gold_burst'){
        var a=Math.random()*6.28,sp=CFG.speed*(1.5+Math.random()*3.5);
        this.vx=Math.cos(a)*sp; this.vy=Math.sin(a)*sp;
        this.x=W*0.5; this.y=H*0.5; this.life=1.0; this.size=2+Math.random()*4;
      }else{
        this.x=Math.random()*W; this.y=Math.random()*H;
        this.wave=Math.random()*6.28; this.waveSp=0.01+Math.random()*0.02;
        this.driftSp=0.3+Math.random()*0.5; this.size=0.8+Math.random()*2.2;
      }
      this.phase=Math.random()*6.28;
    };
    this.update=function(){
      var trP=window.__PEACH_TR_PHASE__||0;
      var trPr=window.__PEACH_TR_PROGRESS__||0;
      // Phase 3: force-reset old particles to gold_burst from center
      if(trP===3&&trPr>0.05&&Math.random()<0.12){
        var a=Math.random()*6.28,sp=CFG.speed*(2+Math.random()*4);
        this.vx=Math.cos(a)*sp;this.vy=Math.sin(a)*sp;
        this.x=W*0.5;this.y=H*0.45;this.life=1.0;this.size=2+Math.random()*5;
        return;
      }
      if(CFG.type==='petal'){
        this.y+=CFG.speed*this.fallSp; this.sway+=this.swaySp;
        this.x+=Math.sin(this.sway)*0.5;
        if(this.y>H+40){this.y=-20;this.x=Math.random()*W;this.sway=Math.random()*6.28;}
        if(this.x<-40)this.x=W+40;if(this.x>W+40)this.x=-40;
      }else if(CFG.type==='gold_burst'){
        this.vx*=0.97;this.vy*=0.97;this.x+=this.vx*CFG.speed;this.y+=this.vy*CFG.speed;
        this.life-=0.003;
        if(this.life<=0||this.x<-80||this.x>W+80||this.y<-80||this.y>H+80)this.reset('gold_burst');
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
      var alpha=CFG.type==='gold_burst'?Math.max(0,this.life)*tw*1.5:tw;
      if(trP===2){alpha*=0.1;} // Critical: near total darkness
      else if(trP===1){alpha*=0.3+0.7*(1-(window.__PEACH_TR_PROGRESS__||0));} // Fade during constrict
      var sz=CFG.type==='gold_burst'?this.size*this.life:this.size;
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
    if(g.type&&g.type!==lastType){lastType=g.type;CFG.type=g.type;for(var i=0;i<pool.length;i++)pool[i].reset(g.type);}
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

SIGIL_SCRIPT = r"""
(function S(){
  var c=document.getElementById('peach-sigil');
  if(!c){setTimeout(S,80);return;}
  var ctx=c.getContext('2d'),W,H;
  function R(){W=c.width=window.innerWidth;H=c.height=window.innerHeight;}
  window.addEventListener('resize',R);R();
  var DEF=window.__PEACH_SIGIL_CONFIG__||{mood:'serene',innerColor:'rgba(248,240,200,0.9)',outerColor:'rgba(230,210,160,0.3)',size:1.0,breathS:4.0,trailLen:15};
  var cx=W*0.5,cy=H*0.45,targetX=0.5,targetY=0.45,trail=[],gesture=0,targetGesture=0;
  function lerp(a,b,t){return a+(b-a)*t;}
  function sync(){
    var g=window.__PEACH_SIGIL_CONFIG__;if(!g)return;
    if(g.innerColor)DEF.innerColor=g.innerColor;if(g.outerColor)DEF.outerColor=g.outerColor;
    if(g.size)DEF.size=g.size;if(g.breathS)DEF.breathS=g.breathS;if(g.trailLen)DEF.trailLen=g.trailLen;
    if(g.targetX!==undefined)targetX=g.targetX;if(g.targetY!==undefined)targetY=g.targetY;
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
    }
    // Transition multipliers
    var trSizeMul=1,trBreathMul=1,trAlphaMul=1;
    var trInner=DEF.innerColor,trOuter=DEF.outerColor;
    if(trPhase===1){
      trSizeMul=1-trProgress*0.6; // 1→0.4
      trBreathMul=1+trProgress*2; // breath accelerates
      trAlphaMul=1-trProgress*0.35;
      trInner='rgba(200,160,100,0.85)';trOuter='rgba(140,90,40,0.2)';
    }else if(trPhase===2){
      trSizeMul=0.18;trBreathMul=5;trAlphaMul=0.4;
      trInner='rgba(240,210,140,0.7)';trOuter='rgba(0,0,0,0)';
    }else if(trPhase===3){
      var ease=1-Math.pow(1-trProgress,3); // ease-out cubic
      trSizeMul=0.18+ease*1.32; // 0.18→1.5
      trBreathMul=5-ease*4; // fast→normal
      trAlphaMul=0.4+ease*0.8;
      trInner='rgba(250,235,170,'+(0.7+ease*0.25).toFixed(2)+')';
      trOuter='rgba(240,210,130,'+(0+ease*0.35).toFixed(2)+')';
    }
    // Position lerp
    var tx=W*targetX,ty=H*targetY;
    cx=lerp(cx,tx,0.04);cy=lerp(cy,ty,0.04);
    // Gesture lerp
    gesture=lerp(gesture,targetGesture,0.08);
    // Breath
    var breath=1+0.05*Math.sin(t*0.001*(4/(DEF.breathS*trBreathMul))*Math.PI*2);
    var sz=80*DEF.size*trSizeMul*breath;
    var alpha=(0.75+0.25*Math.sin(t*0.001*(4/DEF.breathS)*Math.PI*2))*trAlphaMul;
    ctx.clearRect(0,0,W,H);

    // Trail (suppressed during critical phase)
    if(trPhase!==2){
      trail.push({x:cx,y:cy});
    }
    while(trail.length>(trPhase===2?0:DEF.trailLen))trail.shift();
    for(var i=0;i<trail.length;i++){
      var tr=trail[i],frac=i/trail.length,trSz=sz*0.25*frac;
      ctx.beginPath();ctx.arc(tr.x,tr.y,Math.max(0.5,trSz),0,6.28);
      var tc=trPhase?trOuter:DEF.outerColor;
      var m=tc.match(/[\d.]+/g);
      ctx.fillStyle=m&&m.length>=4?'rgba('+m[0]+','+m[1]+','+m[2]+','+(parseFloat(m[3])*(0.4*frac)).toFixed(2)+')':tc;
      ctx.fill();
    }

    // Beam gesture
    if(gesture>0.01){
      var beamLen=140*gesture,dx=1;
      var grad=ctx.createLinearGradient(cx,cy,cx+dx*beamLen,cy);
      grad.addColorStop(0,'rgba(248,240,210,'+(0.35*gesture).toFixed(2)+')');
      grad.addColorStop(0.5,'rgba(248,240,210,'+(0.08*gesture).toFixed(2)+')');
      grad.addColorStop(1,'rgba(248,240,210,0)');
      ctx.beginPath();ctx.moveTo(cx,cy-sz*0.35);ctx.lineTo(cx+dx*beamLen,cy-sz*0.12);
      ctx.lineTo(cx+dx*beamLen,cy+sz*0.12);ctx.lineTo(cx,cy+sz*0.35);ctx.closePath();
      ctx.fillStyle=grad;ctx.fill();
    }

    // Orb body — 3-layer radial gradient
    var ic=trPhase?trInner:DEF.innerColor,oc=trPhase?trOuter:DEF.outerColor;
    var m2=ic.match(/[\d.]+/g);
    var innerA=m2&&m2.length>=4?Math.min(1,(parseFloat(m2[3])*alpha)).toFixed(2):'0.9';
    var g1=ctx.createRadialGradient(cx,cy,sz*0.02,cx,cy,sz*1.5);
    g1.addColorStop(0,'rgba('+m2[0]+','+m2[1]+','+m2[2]+','+innerA+')');
    g1.addColorStop(0.45,oc);g1.addColorStop(1,'rgba(0,0,0,0)');
    ctx.beginPath();ctx.arc(cx,cy,sz*1.5,0,6.28);ctx.fillStyle=g1;ctx.fill();
    var g2=ctx.createRadialGradient(cx,cy,0,cx,cy,sz*0.45);
    g2.addColorStop(0,ic);g2.addColorStop(1,'rgba(0,0,0,0)');
    ctx.beginPath();ctx.arc(cx,cy,sz*0.45,0,6.28);ctx.fillStyle=g2;ctx.fill();
    // Core (brighter during expand phase)
    var coreAlpha=trPhase===3?(0.9+trProgress*0.1)*alpha:0.9*alpha;
    ctx.beginPath();ctx.arc(cx,cy,sz*0.05,0,6.28);
    ctx.fillStyle='rgba(255,254,240,'+(Math.min(1,coreAlpha)).toFixed(2)+')';ctx.fill();

    requestAnimationFrame(A);
  }
  requestAnimationFrame(A);
  window.__peachSetGesture=function(v){targetGesture=v?1:0;};
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
#peach-sigil{position:fixed;top:0;left:0;width:100%;height:100%;z-index:5;pointer-events:none;}

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
.peach-body-text{font-size:2rem;font-weight:500;color:#f0e8d8;letter-spacing:0.08em;line-height:1.6;
  text-shadow:0 0 30px rgba(240,232,200,0.25),0 0 80px rgba(200,180,140,0.1);white-space:pre-wrap;}
.peach-body-area.compact .peach-body-text{font-size:1.4rem;}

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
