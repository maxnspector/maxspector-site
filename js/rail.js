/* Rail layout section labels (Max 2026-11-07, fandom-rail test).
   1. Fade: once a section's end is 400px from the point where its stuck label
      starts moving off, the label fades, reaching 0 (invisible) just as it
      leaves the top of the window. Position-based, so it reverses on scroll-up.
   2. Page name: while the nav is showing (i.e. while scrolling up) the body gets
      .rail-nav-up, which hides each head's page name (Max 11-08; replaces the
      108px shift); it comes back on scroll-down. */
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
    document.body.classList.toggle('rail-nav-up',desk&&navUp);
    heads.forEach(h=>{
      if(!desk){h.style.opacity='';return;}
      const r=h.getBoundingClientRect(), w=h.parentElement.getBoundingClientRect();
      const left=Math.max(w.bottom-r.bottom,0);           // px until the label starts moving off
      const off=left+Math.max(r.bottom,0);                // px until it is fully off the top
      const span=FADE+top+r.height;
      const t=Math.min(Math.max(off/span,0),1);
      h.style.opacity=(MIN+(1-MIN)*t).toFixed(3);
    });
  }
  function req(){if(!ticking){ticking=true;requestAnimationFrame(update);}}
  addEventListener('scroll',req,{passive:true});
  addEventListener('resize',req,{passive:true});
  if(nav)new MutationObserver(req).observe(nav,{attributes:true,attributeFilter:['class']});
  update();
})();

/* Persistent page name (Max 2026-11-08). The first section's page name scrolls
   up with it; once it reaches the sticky stop, a fixed copy takes over and stays
   put while later section labels swap underneath it. It is pushed off the top by
   the end of the last section, and hides with the rest while the nav shows. */
(function(){
  if(!document.body.classList.contains('cs-rail'))return;
  const src=document.querySelector('.cs-media .rail-head .rail-page');
  const walls=[...document.querySelectorAll('.cs-media .wrap.rail')];
  if(!src||!walls.length)return;
  const fx=src.cloneNode(true);fx.classList.add('rail-page-fixed');fx.setAttribute('aria-hidden','true');
  document.body.appendChild(fx);
  const last=walls[walls.length-1];
  let t=false;
  function update(){t=false;
    if(innerWidth<=860){fx.classList.remove('on');src.classList.remove('handed');return;}
    const top=parseFloat(getComputedStyle(document.body).getPropertyValue('--rail-top'))||28;
    const stuck=src.getBoundingClientRect().top<=top+0.5;
    const h=fx.offsetHeight, end=last.getBoundingClientRect().bottom;
    const on=stuck&&end>0;
    fx.classList.toggle('on',on);src.classList.toggle('handed',on);
    fx.style.transform=on?`translateY(${Math.min(0,end-top-h).toFixed(1)}px)`:'';
  }
  const req=()=>{if(!t){t=true;requestAnimationFrame(update);}};
  addEventListener('scroll',req,{passive:true});addEventListener('resize',req,{passive:true});update();
})();
