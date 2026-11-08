/* body.nav-up while the top nav is showing after scrolling down (i.e. while scrolling
   up), desktop only. Drives the pinned UP arrow (css: NAV + FOOTER, every page). Max 2026-11-08. */
(function(){
  const nav=document.getElementById('nav');if(!nav)return;
  let t=false;
  function set(){t=false;document.body.classList.toggle('nav-up',innerWidth>860&&scrollY>140&&!nav.classList.contains('nav-hidden'));}
  const req=()=>{if(!t){t=true;requestAnimationFrame(set);}};
  new MutationObserver(req).observe(nav,{attributes:true,attributeFilter:['class']});
  addEventListener('scroll',req,{passive:true});addEventListener('resize',req,{passive:true});set();
})();
