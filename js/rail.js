/* Rail layout section labels (Max 2026-11-07, fandom-rail test).
   1. Fade: once a section's end is 400px from the point where its stuck label
      starts moving off, the label fades, reaching 0 (invisible) just as it
      leaves the top of the window. Position-based, so it reverses on scroll-up.
   2. Shift: while the nav is showing (i.e. while scrolling up), every section
      label sits 108px right so it clears the logo; it returns on scroll-down. */
(function(){
  if(!document.body.classList.contains('cs-rail'))return;
  const FADE=400, MIN=0;
  const nav=document.getElementById('nav');
  const heads=[...document.querySelectorAll('.cs-media .wrap.rail > .rail-head')];
  if(!heads.length)return;
  const railTop=()=>parseFloat(getComputedStyle(document.body).getPropertyValue('--rail-top'))||28;
  let ticking=false;
  function update(){
    ticking=false;
    const desk=innerWidth>860;
    const navUp=nav&&!nav.classList.contains('nav-hidden')&&scrollY>140;
    const top=railTop();
    heads.forEach(h=>{
      if(!desk){h.style.opacity='';h.classList.remove('shift');return;}
      const r=h.getBoundingClientRect(), w=h.parentElement.getBoundingClientRect();
      const left=Math.max(w.bottom-r.bottom,0);           // px until the label starts moving off
      const off=left+Math.max(r.bottom,0);                // px until it is fully off the top
      const span=FADE+top+r.height;
      const t=Math.min(Math.max(off/span,0),1);
      h.style.opacity=(MIN+(1-MIN)*t).toFixed(3);
      h.classList.toggle('shift',navUp);
    });
  }
  function req(){if(!ticking){ticking=true;requestAnimationFrame(update);}}
  addEventListener('scroll',req,{passive:true});
  addEventListener('resize',req,{passive:true});
  if(nav)new MutationObserver(req).observe(nav,{attributes:true,attributeFilter:['class']});
  update();
})();
