(function(){
  const reduce=matchMedia('(prefers-reduced-motion: reduce)').matches;
  const $=(s,c=document)=>c.querySelector(s), $$=(s,c=document)=>[...c.querySelectorAll(s)];
  const clamp=(v,a,b)=>Math.min(b,Math.max(a,v));

  let lenis=null;
  if(!reduce && window.Lenis){ lenis=new Lenis({lerp:.09,smoothWheel:true}); }

  /* reveal */
  if(reduce||!('IntersectionObserver' in window)){ $$('.rv').forEach(e=>e.classList.add('in')); }
  else{
    const io=new IntersectionObserver(es=>es.forEach(e=>{if(e.isIntersecting){e.target.classList.add('in');io.unobserve(e.target);}}),{rootMargin:'0px 0px -6% 0px'});
    $$('.rv').forEach(e=>io.observe(e));
  }

  /* texto principal: palavra por palavra */
  const lead=$('.lead');
  if(lead){ lead.innerHTML=lead.textContent.trim().split(/\s+/).map(w=>`<span class="w">${w}</span>`).join(' '); }
  const words=lead?$$('.w',lead):[];

  /* vídeos: tocam só quando aparecem, som opcional */
  const vids=$$('video[data-auto]');
  if('IntersectionObserver' in window){
    const vo=new IntersectionObserver(es=>es.forEach(e=>{const v=e.target; if(e.isIntersecting){v.play().catch(()=>{});} else v.pause();}),{threshold:.25});
    vids.forEach(v=>vo.observe(v));
  }
  $$('.snd').forEach(b=>b.addEventListener('click',()=>{
    const v=b.parentElement.querySelector('video'); if(!v) return;
    const on=v.muted; vids.forEach(x=>{x.muted=true;}); $$('.snd').forEach(x=>x.textContent='♪');
    v.muted=!on; b.textContent=on?'■':'♪'; if(on) v.play().catch(()=>{});
  }));

  /* carrosséis: passam sozinhos para o lado enquanto estão na tela; clique avança */
  $$('.carr').forEach(c=>{
    const strip=$('.strip',c), n=+c.dataset.n, box=c.closest('.screen')||c;
    const dots=$$('.dots i',box), cnt=$('.cnt',box); let i=0, vis=false;
    const go=k=>{ i=(k+n)%n; strip.style.transform=`translate3d(${-i*100}%,0,0)`; dots.forEach((d,j)=>d.classList.toggle('on',j===i)); if(cnt) cnt.textContent=`${String(i+1).padStart(2,'0')} / ${String(n).padStart(2,'0')}`; };
    go(0); c.style.cursor='pointer'; c.addEventListener('click',()=>go(i+1));
    if('IntersectionObserver' in window) new IntersectionObserver(es=>{vis=es[0].isIntersecting;},{threshold:.4}).observe(c);
    setInterval(()=>{ if(vis && !document.hidden) go(i+1); },2800);
  });

  const hero=$('.c-hero'), frame=hero&&$('.frame',hero);
  const pars=$$('.par'), tracks=$$('.track'), phones=$$('[data-drift]'), bar=$('.progress');

  function frameTick(){
    const vh=innerHeight, y=scrollY;
    if(bar){ const h=document.documentElement.scrollHeight-vh; bar.style.transform=`scaleX(${h>0?y/h:0})`; }
    if(frame && !reduce){
      const r=hero.getBoundingClientRect();
      const p=clamp(1-(r.top+r.height*0.35)/vh,0,1);
      const mob=innerWidth<860;
      frame.style.setProperty('--w',`${(mob?86:68)+p*(100-(mob?86:68))}%`);
      frame.style.setProperty('--hr',`${14*(1-p)}px`);
    }
    if(!reduce) pars.forEach(el=>{
      const r=el.parentElement.getBoundingClientRect();
      if(r.bottom<0||r.top>vh) return;
      const p=(r.top+r.height/2-vh/2)/(vh+r.height);
      el.style.transform=`translate3d(0,${p*-60}px,0)`;
    });
    tracks.forEach(t=>{
      const row=$('.row',t), r=t.getBoundingClientRect();
      const dist=row.scrollWidth-innerWidth;
      const p=clamp(-r.top/(r.height-vh),0,1);
      row.style.transform=`translate3d(${-dist*p}px,0,0)`;
      const b=$('.bar i',t); if(b) b.style.transform=`scaleX(${p})`;
    });
    if(!reduce && innerWidth>860) phones.forEach(ph=>{
      const r=ph.getBoundingClientRect(); if(r.bottom<0||r.top>vh) return;
      const p=(r.top+r.height/2-vh/2)/vh;
      ph.style.transform=`translate3d(0,${p*parseFloat(ph.dataset.drift)}px,0)`;
    });
    if(words.length){
      const r=lead.getBoundingClientRect();
      const p=clamp((vh*0.85-r.top)/(r.height+vh*0.35),0,1);
      const n=Math.round(p*words.length);
      words.forEach((w,i)=>w.classList.toggle('on',i<n));
    }
  }
  /* altura de cada faixa horizontal = largura que ela precisa percorrer */
  function sizeTracks(){
    tracks.forEach(t=>{ const row=$('.row',t); const dist=Math.max(0,row.scrollWidth-innerWidth); t.style.setProperty('--len',`${innerHeight+dist}px`); });
  }
  addEventListener('resize',()=>{sizeTracks();frameTick();});
  addEventListener('load',()=>{sizeTracks();frameTick();});
  sizeTracks();
  function raf(t){ if(lenis) lenis.raf(t); frameTick(); requestAnimationFrame(raf); }
  requestAnimationFrame(raf);
})();
