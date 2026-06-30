"""Countdown Timer — reusable JS-driven timer for Reflex layouts.

Provides the IIFE script that drives a DOM countdown display
and helper to build the required DOM elements.
"""

import reflex as rx

TIMER_SCRIPT = """
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


def timer_elements(timer_state_var) -> list[rx.Component]:
    """Build timer display + hidden store DOM elements.

    Args:
        timer_state_var: Reflex state Var[str], format "running:60" / "stopped:0"
    """
    return [
        rx.text(
            "00:00",
            id="courtroom-timer-display",
            class_name="courtroom-timer timer-safe",
        ),
        rx.box(
            rx.el.div(data_timer_state=timer_state_var),
            id="courtroom-timer-store",
            display="none",
        ),
    ]
