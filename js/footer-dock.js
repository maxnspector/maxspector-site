/* FOOTER DOCK (Max 2026-10-25)
   At the bottom of a page the nav's logo and + travel down and land in the footer,
   and the + turns into the back-to-top arrow. Scroll back up and they fly home to the
   top. The footer's own logo and arrow only show once the travelling ones land, so
   there is only ever one logo on screen.
   Footer slots: [data-dock="logo"] and [data-dock="btn"]. */
(() => {
  const nav = document.getElementById('nav');
  if (!nav) return;
  const logo = nav.querySelector('.nav-inner > a, .nav-inner > .nav-logo');
  const btn = document.getElementById('menuBtn');
  const lslot = document.querySelector('[data-dock="logo"]');
  const bslot = document.querySelector('[data-dock="btn"]');
  if (!logo || !lslot) return;
  const pairs = [[logo, lslot]];
  if (btn && bslot) pairs.push([btn, bslot]);
  const reduce = matchMedia('(prefers-reduced-motion:reduce)').matches;
  const DUR = reduce ? 0 : 720;
  const ease = t => 1 - Math.pow(1 - t, 3);            // ease-out: fast start, soft landing
  const root = document.documentElement, body = document.body;
  root.classList.add('dock-ready');                      // footer copies wait for the landing

  if (btn) {                                             // arrow that the + fades into
    const a = document.createElementNS('http://www.w3.org/2000/svg', 'svg');
    a.setAttribute('viewBox', '0 0 16 18'); a.setAttribute('class', 'dock-arrow');
    a.setAttribute('aria-hidden', 'true');
    a.innerHTML = '<path d="M8 17V2M1.5 8.5L8 2l6.5 6.5" fill="none" stroke="currentColor" stroke-width="2"/>';
    btn.appendChild(a);
  }

  let state = 'top', busy = false;
  const mid = r => [r.left + r.width / 2, r.top + r.height / 2];
  // Where an element sits with no transform applied (its home in the nav).
  const home = el => { const t = el.style.transform; el.style.transform = 'none'; const m = mid(el.getBoundingClientRect()); el.style.transform = t; return m; };

  function fly(toDock) {
    busy = true;
    const starts = pairs.map(([el, slot]) => toDock ? mid(el.getBoundingClientRect()) : mid(slot.getBoundingClientRect()));
    body.classList.remove('is-docked');
    body.classList.add('dock-flying');                   // nav pinned in view, footer copies hidden
    if (btn) btn.classList.toggle('as-arrow', toDock);
    const homes = pairs.map(([el]) => home(el));
    const t0 = performance.now();
    function frame(now) {
      const p = DUR ? Math.min(1, (now - t0) / DUR) : 1, e = ease(p);
      pairs.forEach(([el, slot], i) => {
        const to = toDock ? mid(slot.getBoundingClientRect()) : homes[i];   // re-aim every frame
        const x = starts[i][0] + (to[0] - starts[i][0]) * e - homes[i][0];
        const y = starts[i][1] + (to[1] - starts[i][1]) * e - homes[i][1];
        el.style.transform = `translate(${x.toFixed(1)}px,${y.toFixed(1)}px)`;
      });
      if (p < 1) return requestAnimationFrame(frame);
      pairs.forEach(([el]) => { el.style.transform = ''; });
      body.classList.remove('dock-flying');
      if (toDock) body.classList.add('is-docked');
      else nav.classList.remove('nav-hidden');
      state = toDock ? 'dock' : 'top';
      busy = false;
      check();
    }
    requestAnimationFrame(frame);
  }

  function check() {
    if (busy || body.classList.contains('menu-open')) return;
    const r = lslot.getBoundingClientRect(), vh = innerHeight;
    const scrollable = root.scrollHeight - vh > 200;
    if (state === 'top' && scrollable && scrollY > 0 && r.bottom <= vh) fly(true);
    else if (state === 'dock' && r.top > vh - 20) fly(false);
  }
  let ticking = false;
  addEventListener('scroll', () => { if (!ticking) { ticking = true; requestAnimationFrame(() => { ticking = false; check(); }); } }, { passive: true });
  addEventListener('resize', check, { passive: true });

  // Reloaded at the bottom of the page: land without the flight.
  const r0 = lslot.getBoundingClientRect();
  if (scrollY > 0 && root.scrollHeight - innerHeight > 200 && r0.bottom <= innerHeight) { body.classList.add('is-docked'); state = 'dock'; }

  // Back to top: smooth scroll; the logo and + fly home on the way up.
  if (bslot) bslot.addEventListener('click', e => { e.preventDefault(); scrollTo({ top: 0, behavior: reduce ? 'auto' : 'smooth' }); });
})();
