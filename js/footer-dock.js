/* FOOTER DOCK (Max 2026-10-25, revised same day)
   When you reach the bottom of the page, the footer's logo and back-to-top arrow rise
   up from below the window into place — the opposite of the nav sliding down from the
   top when you scroll up. Scroll back up from the bottom and they drop away again.
   The motion itself is a CSS transition on .is-docked (css/styles.css, FOOTER DOCK).
   Footer slots: [data-dock="logo"] and [data-dock="btn"]. */
(() => {
  const lslot = document.querySelector('[data-dock="logo"]');
  if (!lslot) return;
  const bslot = document.querySelector('[data-dock="btn"]');
  const root = document.documentElement, body = document.body;
  const reduce = matchMedia('(prefers-reduced-motion:reduce)').matches;
  const NEAR = 4;    // px from the very bottom that counts as "hit the bottom"
  const LEAVE = 40;  // scroll up this far from the bottom and they drop away
  let shown = false;
  function check() {
    const left = root.scrollHeight - innerHeight - scrollY;   // px still to scroll
    const short = root.scrollHeight - innerHeight < 200;       // page barely scrolls: always show
    if (!shown && (short || left <= NEAR)) { shown = true; body.classList.add('is-docked'); }
    else if (shown && !short && left > LEAVE) { shown = false; body.classList.remove('is-docked'); }
  }
  // Already at the bottom on load (reload, short page): show without the rise.
  check();
  if (shown) {
    [lslot, bslot].forEach(el => { if (el) el.style.transition = 'none'; });
    requestAnimationFrame(() => requestAnimationFrame(() => [lslot, bslot].forEach(el => { if (el) el.style.transition = ''; })));
  }
  root.classList.add('dock-ready');
  let ticking = false;
  addEventListener('scroll', () => { if (!ticking) { ticking = true; requestAnimationFrame(() => { ticking = false; check(); }); } }, { passive: true });
  addEventListener('resize', check, { passive: true });
  if (bslot) bslot.addEventListener('click', e => { e.preventDefault(); scrollTo({ top: 0, behavior: reduce ? 'auto' : 'smooth' }); });
})();
