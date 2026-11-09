/* body.nav-up while the top nav is showing after scrolling down (i.e. while scrolling
   up), desktop only. Drives the pinned UP arrow (css: NAV + FOOTER, every page). Max 2026-11-08.
   Threshold (Max 11-08, per NN/g + NYC/PatternFly design systems): only on pages taller than
   4 screens, and only once scrolled 2 screens down. The footer's own arrow is unaffected. */
(function(){
  const nav=document.getElementById('nav');if(!nav)return;
  let t=false;
  function set(){t=false;document.body.classList.toggle('nav-up',innerWidth>860&&document.documentElement.scrollHeight>4*innerHeight&&scrollY>2*innerHeight&&!nav.classList.contains('nav-hidden'));}
  const req=()=>{if(!t){t=true;requestAnimationFrame(set);}};
  new MutationObserver(req).observe(nav,{attributes:true,attributeFilter:['class']});
  addEventListener('scroll',req,{passive:true});addEventListener('resize',req,{passive:true});set();
})();
