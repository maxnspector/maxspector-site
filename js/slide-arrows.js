/* Homepage slide arrows pick light or dark (Max 2026-11-09). Reads the active
   slide's pixels right behind each arrow (image, or a video's poster, at its
   object-fit: cover crop) and adds .on-light when they're light, turning that
   arrow dark. Rechecks when the slide changes and on resize. */
(function(){
  const slides=[...document.querySelectorAll('#slides .slide')];
  const arrows=[...document.querySelectorAll('.home .slider-arrow')];
  if(!slides.length||!arrows.length)return;
  const MAX=600,PAD=12,LIGHT=0.55,cache=new Map();
  function srcOf(s){const im=s.querySelector('img');if(im)return im.currentSrc||im.src;const v=s.querySelector('video');return v?v.poster:'';}
  function pixels(url){
    if(cache.has(url))return cache.get(url);
    const p=new Promise(res=>{const img=new Image();img.onload=()=>{
      const k=Math.min(1,MAX/Math.max(img.naturalWidth,img.naturalHeight));
      const w=Math.round(img.naturalWidth*k),h=Math.round(img.naturalHeight*k);
      const c=document.createElement('canvas');c.width=w;c.height=h;const x=c.getContext('2d',{willReadFrequently:true});x.drawImage(img,0,0,w,h);
      try{res({w,h,d:x.getImageData(0,0,w,h).data});}catch(e){res(null);}};img.onerror=()=>res(null);img.src=url;});
    cache.set(url,p);return p;
  }
  async function check(){
    const s=slides.find(x=>x.classList.contains('active'));if(!s)return;
    const url=srcOf(s);if(!url)return;const px=await pixels(url);if(!px)return;
    if(!s.classList.contains('active'))return;
    const b=s.getBoundingClientRect(),sc=Math.max(b.width/px.w,b.height/px.h);
    const ox=b.left+(b.width-px.w*sc)/2,oy=b.top+(b.height-px.h*sc)/2;
    arrows.forEach(a=>{const g=(a.querySelector('svg')||a).getBoundingClientRect();
      const x0=Math.max(0,Math.floor((g.left-PAD-ox)/sc)),x1=Math.min(px.w-1,Math.ceil((g.right+PAD-ox)/sc));
      const y0=Math.max(0,Math.floor((g.top-PAD-oy)/sc)),y1=Math.min(px.h-1,Math.ceil((g.bottom+PAD-oy)/sc));
      if(x1<x0||y1<y0)return;let sum=0,n=0;
      for(let y=y0;y<=y1;y++)for(let x=x0;x<=x1;x++){const i=(y*px.w+x)*4;sum+=(0.2126*px.d[i]+0.7152*px.d[i+1]+0.0722*px.d[i+2])/255;n++;}
      a.classList.toggle('on-light',sum/n>LIGHT);});
  }
  slides.forEach(s=>new MutationObserver(check).observe(s,{attributes:true,attributeFilter:['class']}));
  addEventListener('resize',check,{passive:true});
  check();
})();
