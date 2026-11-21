import './css/nav.css';
import { gsap, ScrollTrigger, reducedMotion, scrollToTarget, lenis } from './util.js';

export const NAV_LINKS = [
  { n: '01', label: 'PROIECTUL', href: '#proiectul' },
  { n: '02', label: 'ARHITECTURA', href: '#arhitectura' },
  { n: '03', label: 'APARTAMENTE', href: '#rezidente' },
  { n: '04', label: 'LOCAȚIE', href: '#locatie' },
];

const roll = (text) => `<span class="roll" data-text="${text}"><span>${text}</span></span>`;

export function mountNav(root) {
  root.classList.add('nav');
  root.innerHTML = `
    <div class="nav__bar">
      <a class="nav__brand" href="#top" aria-label="ORIZONT, înapoi sus">
        <span class="nav__word">ORIZONT</span>
        <span class="nav__city mono">BUCUREȘTI / NORD</span>
      </a>
      <nav class="nav__links" aria-label="Secțiuni">
        ${NAV_LINKS.map((l) => `<a class="nav__link mono" href="${l.href}"><span class="nav__n">${l.n}</span>${roll(l.label)}</a>`).join('')}
      </nav>
      <a class="pill nav__cta" href="#vizionare">${roll('PROGRAMEAZĂ O VIZITĂ')}</a>
      <button class="nav__toggle mono" type="button" aria-expanded="false" aria-controls="nav-menu">
        <span class="nav__toggle-txt">MENIU</span><span class="nav__burger" aria-hidden="true"><i></i><i></i></span>
      </button>
    </div>
    <div class="nav__menu" id="nav-menu" hidden>
      <nav class="nav__menu-links" aria-label="Meniu">
        ${NAV_LINKS.map((l) => `<a class="nav__menu-link" href="${l.href}"><span class="mono">${l.n}</span><span class="nav__menu-label">${l.label}</span></a>`).join('')}
      </nav>
      <div class="nav__menu-foot">
        <a class="pill" href="#vizionare">PROGRAMEAZĂ O VIZITĂ</a>
        <p class="mono">Șoseaua Nordului 12, București</p>
      </div>
    </div>`;

  wireAnchors();
  wireMenu(root);

  // Solid ink bar once the content starts (past the hero, whatever its pinned height),
  // hide on scroll down / reveal on scroll up like the reference.
  ScrollTrigger.create({
    trigger: '#content',
    start: 'top 72px',
    onToggle: (self) => root.classList.toggle('is-solid', self.isActive || self.progress > 0),
    onUpdate: (self) => {
      if (root.classList.contains('is-open')) return;
      root.classList.toggle('is-tucked', self.direction === 1 && self.scroll() - self.start > 160);
    },
    end: 'max',
  });

  // Active chapter highlight
  NAV_LINKS.forEach((l, i) => {
    ScrollTrigger.create({
      trigger: l.href,
      start: 'top 50%',
      end: 'bottom 50%',
      onToggle: (self) => root.querySelectorAll('.nav__link')[i].classList.toggle('is-active', self.isActive),
    });
  });
}

/** Every in-page anchor (ours and the hero's CTAs) scrolls through Lenis. */
function wireAnchors() {
  document.addEventListener('click', (e) => {
    const a = e.target instanceof Element && e.target.closest('a[href^="#"]');
    if (!a) return;
    const id = a.getAttribute('href');
    e.preventDefault();
    if (id === '#top' || id === '#') scrollToTarget(0);
    else if (document.querySelector(id)) scrollToTarget(id);
    if (a.dataset.residence) {
      document.dispatchEvent(new CustomEvent('orizont:residence', { detail: a.dataset.residence }));
    }
  });
}

function wireMenu(root) {
  const btn = root.querySelector('.nav__toggle');
  const txt = root.querySelector('.nav__toggle-txt');
  const menu = root.querySelector('.nav__menu');
  const items = menu.querySelectorAll('.nav__menu-link, .nav__menu-foot > *');

  const set = (open) => {
    root.classList.toggle('is-open', open);
    btn.setAttribute('aria-expanded', String(open));
    txt.textContent = open ? 'ÎNCHIDE' : 'MENIU';
    if (open) {
      menu.hidden = false;
      lenis()?.stop();
      root.classList.remove('is-tucked');
      if (!reducedMotion) {
        gsap.fromTo(menu, { clipPath: 'inset(0 0 100% 0)' }, { clipPath: 'inset(0 0 0% 0)', duration: .7, ease: 'power4.inOut' });
        gsap.fromTo(items, { yPercent: 60, opacity: 0 }, { yPercent: 0, opacity: 1, duration: .8, ease: 'power4.out', stagger: .06, delay: .25 });
      }
      menu.querySelector('a').focus({ preventScroll: true });
    } else {
      lenis()?.start();
      const hide = () => { menu.hidden = true; };
      if (reducedMotion) hide();
      else gsap.to(menu, { clipPath: 'inset(0 0 100% 0)', duration: .5, ease: 'power3.inOut', onComplete: hide });
    }
  };

  btn.addEventListener('click', () => set(!root.classList.contains('is-open')));
  menu.addEventListener('click', (e) => { if (e.target.closest('a')) set(false); });
  addEventListener('keydown', (e) => {
    if (e.key === 'Escape' && root.classList.contains('is-open')) { set(false); btn.focus(); }
  });
  matchMedia('(min-width: 961px)').addEventListener('change', (e) => { if (e.matches) set(false); });
}
