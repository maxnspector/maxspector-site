/* Scroll-in for hand-built pages (homepage, About), Max 2026-11-01.
   Mirrors the case-study row scroll-in: below the screen = waiting; entering =
   rise + fade in; dropping back below = reset; already on screen at load or
   jumped past = shown at once. Needs `rows-anim` on <html> (set in the head
   unless reduced motion is on). */
(function(){
  if(!document.documentElement.classList.contains('rows-anim'))return;
  const els=[...document.querySelectorAll('.row-in')];
  const show=(el,instant)=>{if(instant){el.classList.add('row-instant','in');requestAnimationFrame(()=>requestAnimationFrame(()=>el.classList.remove('row-instant')));}else el.classList.add('in');};
  els.forEach(el=>{if(el.getBoundingClientRect().top<innerHeight)show(el,true);});
  const io=new IntersectionObserver(es=>es.forEach(e=>{
    if(e.isIntersecting)show(e.target,false);
    else if(e.boundingClientRect.top>=(e.rootBounds?e.rootBounds.bottom:innerHeight))e.target.classList.remove('in');
    else if(!e.target.classList.contains('in'))show(e.target,true);
  }),{threshold:0});
  els.forEach(el=>io.observe(el));
})();
