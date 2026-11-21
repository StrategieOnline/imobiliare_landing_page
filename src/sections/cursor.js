import { gsap, finePointer, lerp } from './util.js';

const LINKS = 'a, button, select, label';
const TEXT = 'input, textarea';
const LABELS = { view: 'VEZI', scroll: 'DERULEAZĂ' };
const STATES = ['default', 'link', 'scroll', 'view'];

/**
 * Hairline ⊙ ring that trails the pointer.
 * States: default | link (grows) | view (filled disc + label) | scroll (wide ring + label).
 * Hover picks link/view from the DOM ([data-cursor="view|scroll"], optional [data-cursor-label]);
 * other teams can force a state with window.__cursor.setState(name) (the hero uses 'scroll').
 */
export function mountCursor() {
  const api = { setState: () => {} };
  window.__cursor = api;
  if (!finePointer.matches) return;

  const el = document.createElement('div');
  el.className = 'cursor';
  el.setAttribute('aria-hidden', 'true');
  el.innerHTML = '<span class="cursor__ring"></span><span class="cursor__dot"></span><span class="cursor__label"></span>';
  document.body.append(el);
  const label = el.querySelector('.cursor__label');

  let hover = { state: 'default', text: '' };
  let forced = 'default';
  const render = () => {
    const state = hover.state !== 'default' ? hover.state : forced;
    STATES.forEach((s) => el.classList.toggle(`is-${s}`, s === state));
    label.textContent = hover.state !== 'default' ? hover.text : LABELS[forced] || '';
  };
  api.setState = (name) => {
    forced = STATES.includes(name) ? name : 'default';
    render();
  };

  // Resting position before the first move: right-middle of the viewport, as in the reference.
  const target = { x: innerWidth * 0.76, y: innerHeight * 0.56 };
  const pos = { ...target };

  addEventListener('pointermove', (e) => {
    if (e.pointerType !== 'mouse') return;
    target.x = e.clientX;
    target.y = e.clientY;
    el.classList.remove('is-hidden');
  }, { passive: true });
  document.documentElement.addEventListener('pointerleave', () => el.classList.add('is-hidden'));

  addEventListener('pointerover', (e) => {
    const t = e.target instanceof Element ? e.target : null;
    if (!t) return;
    const tagged = t.closest('[data-cursor]');
    if (tagged) {
      const state = tagged.dataset.cursor;
      hover = { state, text: tagged.dataset.cursorLabel || LABELS[state] || '' };
    } else {
      hover = { state: t.closest(LINKS) ? 'link' : 'default', text: '' };
    }
    // a forced state belongs to the region that set it (the hero); drop it once we leave
    if (forced !== 'default' && !t.closest('#hero')) forced = 'default';
    el.classList.toggle('is-text', !!t.closest(TEXT));
    render();
  }, { passive: true });

  gsap.ticker.add((_, dt) => {
    const k = 1 - Math.pow(1 - 0.2, dt / 16.67);   // frame-rate independent lerp
    pos.x = lerp(pos.x, target.x, k);
    pos.y = lerp(pos.y, target.y, k);
    el.style.transform = `translate3d(${pos.x}px, ${pos.y}px, 0)`;
  });
}
