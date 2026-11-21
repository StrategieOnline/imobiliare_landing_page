import './css/footer.css';
import { gsap, MQ, scrollToTarget } from './util.js';
import { NAV_LINKS } from './nav.js';

export function mountFooter(root) {
  root.classList.add('foot');
  root.innerHTML = `
    <div class="foot__top">
      <nav class="foot__nav mono" aria-label="Subsol">
        ${[...NAV_LINKS, { label: 'VIZITĂ', href: '#vizionare' }].map((l) => `<a href="${l.href}">${l.label}</a>`).join('')}
      </nav>
      <button class="foot__up mono" type="button">ÎNAPOI SUS <span aria-hidden="true">↑</span></button>
    </div>
    <div class="foot__meta">
      <p class="foot__legal">Vizualizările sunt generate digital și au rol de prezentare; nu constituie ofertă contractuală.</p>
      <p class="foot__copy mono">© 2026 ORIZONT · BUCUREȘTI / NORD</p>
    </div>
    <div class="foot__mark" aria-hidden="true"><span class="foot__word">ORIZONT</span></div>`;

  root.querySelector('.foot__up').addEventListener('click', () => scrollToTarget(0, { duration: 2.2 }));

  // Fit the wordmark to the full width (Unbounded is wide, so a fixed vw would overflow).
  const word = root.querySelector('.foot__word');
  const fit = () => {
    word.style.fontSize = '100px';
    const w = word.getBoundingClientRect().width;
    word.style.fontSize = `${(100 * root.clientWidth * 0.985) / w}px`;
  };
  fit();
  addEventListener('resize', fit);
  document.fonts?.ready.then(fit);

  gsap.matchMedia().add(MQ.motion, () => {
    gsap.fromTo(word, { yPercent: 70 }, {
      yPercent: 0, ease: 'none',
      scrollTrigger: { trigger: root, start: 'top bottom', end: 'bottom bottom', scrub: true },
    });
  });
}
