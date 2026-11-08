/* Cover down arrow picks light or dark (Max 2026-11-08). Reads the cover image
   pixels right behind the arrow (for whichever cover is showing: desktop or
   phone art, at the current crop) and adds .on-light when they're light, which
   turns the arrow dark. Rechecks on resize and while the cover scrolls. */
(function(){
  const media=document.querySelector('.cs-cover-media.has-img');
  const arrow=document.querySelector('.cs-scroll');
  if(!media||!arrow)return;
  const MAX=600, PAD=16, LIGHT=0.55;
  let data=null, iw=0, ih=0, url='';
  function load(){
    const m=getComputedStyle(media).backgroundImage.match(/url\(["']?(.*?)["']?\)/);
    if(!m||m[1]===url)return;
    url=m[1];const img=new Image();
    img.onload=()=>{const k=Math.min(1,MAX/Math.max(img.naturalWidth,img.naturalHeight));
      iw=Math.round(img.naturalWidth*k);ih=Math.round(img.naturalHeight*k);
      const c=document.createElement('canvas');c.width=iw;c.height=ih;
      const x=c.getContext('2d',{willReadFrequently:true});x.drawImage(img,0,0,iw,ih);
      try{data=x.getImageData(0,0,iw,ih).data;}catch(e){data=null;}
      check();};
    img.src=url;
  }
  function check(){
    if(!data)return;
    const b=media.getBoundingClientRect(), a=arrow.getBoundingClientRect();
    if(a.bottom<0)return;
    const size=getComputedStyle(media).backgroundSize;
    const s=size==='contain'?Math.min(b.width/iw,b.height/ih):Math.max(b.width/iw,b.height/ih);
    const ox=b.left+(b.width-iw*s)/2, oy=b.top+(b.height-ih*s)/2;   // background-position: center
    const x0=Math.max(0,Math.floor((a.left-PAD-ox)/s)), x1=Math.min(iw-1,Math.ceil((a.right+PAD-ox)/s));
    const y0=Math.max(0,Math.floor((a.top-PAD-oy)/s)), y1=Math.min(ih-1,Math.ceil((a.bottom+PAD-oy)/s));
    if(x1<x0||y1<y0)return;
    let sum=0,n=0;
    for(let y=y0;y<=y1;y++)for(let x=x0;x<=x1;x++){const i=(y*iw+x)*4;
      sum+=(0.2126*data[i]+0.7152*data[i+1]+0.0722*data[i+2])/255;n++;}
    arrow.classList.toggle('on-light',sum/n>LIGHT);
  }
  let t=false;const req=()=>{if(!t){t=true;requestAnimationFrame(()=>{t=false;load();check();});}};
  addEventListener('resize',req,{passive:true});
  addEventListener('scroll',req,{passive:true});
  load();
})();
