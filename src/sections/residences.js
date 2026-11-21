import './css/residences.css';
import { gsap, finePointer, reducedMotion, figure, imgSrc, clamp, lerp } from './util.js';

export const RESIDENCES = [
  { n: '01', name: 'APARTAMENT CU TERASĂ', option: 'Apartament cu terasă', key: 'terasa', img: 'res-loggia',
    specs: ['2–3 CAMERE', '112–160 m²', 'ETAJELE 4–18'], alt: 'Living al apartamentului cu terasă, deschis spre exterior' },
  { n: '02', name: 'APARTAMENT DE COLȚ', option: 'Apartament de colț', key: 'colt', img: 'res-corner',
    specs: ['3–4 CAMERE', '170–230 m²', 'ETAJELE 6–20'], alt: 'Apartament de colț, cu vitraj pe două laturi spre oraș' },
  { n: '03', name: 'PENTHOUSE', option: 'Penthouse', key: 'penthouse', img: 'res-penthouse',
    specs: ['5 CAMERE', '320–480 m²', 'ETAJELE 22–24'], alt: 'Penthouse cu living pe dublă înălțime și vedere peste oraș' },
];

export function mountResidences(content) {
  const sec = document.createElement('section');
  sec.className = 'sec residences';
  sec.id = 'rezidente';
  sec.setAttribute('aria-labelledby', 'rezidente-h');
  sec.innerHTML = `
    <div class="residences__head">
      <div>
        <p class="sec-label mono">03 / APARTAMENTE</p>
        <h2 class="display h-lg" id="rezidente-h">
          <span class="line"><span>ALEGE-ȚI</span></span>
          <span class="line"><span><em>înălțimea.</em></span></span>
        </h2>
      </div>
      <p class="residences__note mono">46 de locuințe, între 112 și 480 m²<br><span>Plan deschis, lumină pe două laturi, materiale calde.</span></p>
    </div>
    <ul class="rlist" role="list">
      ${RESIDENCES.map((r, i) => `
        <li class="rrow" data-i="${i}">
          <a class="rrow__link" href="#vizionare" data-residence="${r.key}" data-cursor="view">
            <span class="rrow__n mono">${r.n}</span>
            <span class="rrow__name">${r.name}</span>
            <span class="rrow__specs mono">${r.specs.join('<i>·</i>')}</span>
            <span class="rrow__arrow" aria-hidden="true">↗</span>
          </a>
          ${figure({ name: r.img, alt: r.alt, w: 1200, h: 1500, cls: 'rrow__inline' })}
        </li>`).join('')}
    </ul>`;
  content.append(sec);

  const list = sec.querySelector('.rlist');
  const rows = [...sec.querySelectorAll('.rrow')];

  // Dim the others on hover/focus (works for keyboard too)
  const setActive = (i) => {
    list.classList.toggle('has-active', i >= 0);
    rows.forEach((r, k) => r.classList.toggle('is-active', k === i));
  };
  rows.forEach((row, i) => {
    const a = row.querySelector('a');
    a.addEventListener('pointerenter', () => setActive(i));
    a.addEventListener('focus', () => setActive(i));
    a.addEventListener('blur', () => setActive(-1));
  });
  list.addEventListener('pointerleave', () => setActive(-1));

  if (!reducedMotion) {
    gsap.from(sec.querySelectorAll('.residences__head .line > span'), {
      yPercent: 110, duration: .9, ease: 'power4.out', stagger: .08,
      scrollTrigger: { trigger: sec, start: 'top 72%' },
    });
    gsap.from(rows, {
      y: 60, opacity: 0, duration: 1, ease: 'power3.out', stagger: .1,
      scrollTrigger: { trigger: list, start: 'top 85%' },
    });
  }
  if (finePointer.matches) mountPreview(list, rows);
}

/** Floating 4:5 preview that trails the cursor with lerp, tilts with horizontal velocity, and wipes between rows. */
function mountPreview(list, rows) {
  const box = document.createElement('div');
  box.className = 'rpreview';
  box.setAttribute('aria-hidden', 'true');
  box.innerHTML = RESIDENCES.map((r) => `<div class="rpreview__layer ph"><img class="ph__img" data-src="${imgSrc(r.img)}" alt="" width="1200" height="1500" decoding="async"></div>`).join('');
  document.body.append(box);
  const layers = [...box.children];
  layers.forEach((l) => {
    const img = l.querySelector('img');
    img.addEventListener('load', () => img.classList.add('is-loaded'), { once: true });
    img.addEventListener('error', () => img.remove(), { once: true });
  });

  // lazy loading does not apply inside a fixed box, so fetch on approach or first interaction
  let fetched = false;
  const fetchImages = () => {
    if (fetched) return;
    fetched = true;
    io.disconnect();
    box.querySelectorAll('img[data-src]').forEach((img) => { img.src = img.dataset.src; });
  };
  const io = new IntersectionObserver((es) => { if (es.some((e) => e.isIntersecting)) fetchImages(); }, { rootMargin: '100% 0px' });
  io.observe(list.closest('section'));
  list.addEventListener('pointerenter', fetchImages, { once: true });
  list.addEventListener('focusin', fetchImages, { once: true });

  const target = { x: 0, y: 0 };
  const pos = { x: 0, y: 0, rot: 0, prevX: 0 };
  let shown = false;
  let current = -1;
  let z = 1;

  const show = (on) => {
    shown = on;
    gsap.to(box, { autoAlpha: on ? 1 : 0, scale: on ? 1 : 0.86, duration: on ? .5 : .35, ease: 'power3.out', overwrite: 'auto' });
  };
  const swap = (i) => {
    if (i === current) return;
    const prev = current;
    current = i;
    const layer = layers[i];
    gsap.set(layer, { zIndex: ++z });
    gsap.fromTo(layer, { clipPath: prev < 0 ? 'inset(0% 0% 0% 0%)' : (i > prev ? 'inset(100% 0% 0% 0%)' : 'inset(0% 0% 100% 0%)') },
      { clipPath: 'inset(0% 0% 0% 0%)', duration: .7, ease: 'power4.out' });
    gsap.fromTo(layer.querySelector('img') || layer, { scale: 1.25 }, { scale: 1, duration: 1, ease: 'power3.out' });
  };

  list.addEventListener('pointermove', (e) => {
    target.x = e.clientX;
    target.y = e.clientY;
  });
  rows.forEach((row, i) => row.querySelector('a').addEventListener('pointerenter', (e) => {
    target.x = e.clientX;
    target.y = e.clientY;
    if (!shown) { pos.x = pos.prevX = target.x; pos.y = target.y; show(true); }
    swap(i);
  }));
  list.addEventListener('pointerleave', () => show(false));
  addEventListener('scroll', () => { if (shown && !list.matches(':hover')) show(false); }, { passive: true });

  gsap.ticker.add((_, dt) => {
    if (!shown && gsap.getProperty(box, 'opacity') === 0) return;
    const k = 1 - Math.pow(1 - 0.14, dt / 16.67);
    pos.x = lerp(pos.x, target.x, k);
    pos.y = lerp(pos.y, target.y, k);
    const vx = pos.x - pos.prevX;
    pos.prevX = pos.x;
    pos.rot = lerp(pos.rot, clamp(vx * 0.5, -9, 9), 0.12);
    box.style.translate = `${pos.x}px ${pos.y}px`;
    box.style.rotate = `${pos.rot}deg`;
  });
}
