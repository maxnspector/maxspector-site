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

/* UP button light/dark (Max 2026-11-08). Looks at what sits behind the pinned UP
   button (an image or video's pixels, or a panel's background color) and sets
   .on-dark when it's dark, which turns UP and its arrow white. */
(function(){
  if(!document.body.classList.contains('cs-rail'))return;
  const btn=document.querySelector('.dock-top');
  if(!btn)return;
  const cv=document.createElement('canvas');cv.width=cv.height=6;
  const cx=cv.getContext('2d',{willReadFrequently:true});
  const lum=(r,g,b)=>(0.2126*r+0.7152*g+0.0722*b)/255;
  function media(el,x,y){                      // pixel luminance of an img/video under (x,y)
    const nw=el.naturalWidth||el.videoWidth, nh=el.naturalHeight||el.videoHeight;
    if(!nw||!nh)return null;
    const b=el.getBoundingClientRect(), fit=getComputedStyle(el).objectFit;
    const s=fit==='contain'?Math.min(b.width/nw,b.height/nh):fit==='fill'?null:Math.max(b.width/nw,b.height/nh);
    const sx=s?(x-b.left-(b.width-nw*s)/2)/s:(x-b.left)*nw/b.width;
    const sy=s?(y-b.top-(b.height-nh*s)/2)/s:(y-b.top)*nh/b.height;
    const r=6/(s||b.width/nw);
    if(sx<0||sy<0||sx>nw||sy>nh)return null;
    try{cx.clearRect(0,0,6,6);cx.drawImage(el,sx-r/2,sy-r/2,r,r,0,0,6,6);
      const d=cx.getImageData(0,0,6,6).data;let t=0;for(let i=0;i<d.length;i+=4)t+=lum(d[i],d[i+1],d[i+2]);return t/36;}
    catch(e){return null;}
  }
  function at(x,y){
    for(const el of document.elementsFromPoint(x,y)){
      if(btn.contains(el))continue;
      if(el.tagName==='IMG'&&el.complete||el.tagName==='VIDEO'&&el.readyState>=2){const v=media(el,x,y);if(v!==null)return v;}
      if(el.tagName==='IFRAME')return null;
      const m=getComputedStyle(el).backgroundColor.match(/rgba?\(([\d.]+),\s*([\d.]+),\s*([\d.]+)(?:,\s*([\d.]+))?/);
      if(m&&(m[4]===undefined||+m[4]>0.5))return lum(+m[1],+m[2],+m[3]);
    }
    return 1;                                   // page itself is white
  }
  let t=false;
  function check(){t=false;
    const b=btn.getBoundingClientRect(); if(b.top>innerHeight)return;
    const y=b.top+b.height/2, vals=[b.left+4,b.left+b.width/2,b.right-4].map(x=>at(x,y)).filter(v=>v!==null);
    if(!vals.length)return;
    btn.classList.toggle('on-dark',vals.reduce((a,c)=>a+c,0)/vals.length<0.5);
  }
  const req=()=>{if(!t){t=true;requestAnimationFrame(check);}};
  addEventListener('scroll',req,{passive:true});addEventListener('resize',req,{passive:true});
  addEventListener('load',req);setInterval(req,700);   // videos change frame by frame
})();
