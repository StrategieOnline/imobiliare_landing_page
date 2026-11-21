import './css/manifesto.css';
import { gsap, ScrollTrigger, reducedMotion, splitWords } from './util.js';

const STATS = [
  { label: 'APARTAMENTE', value: '46' },
  { label: 'NIVELURI', value: '24' },
  { label: 'LIVRARE', value: '2028' },
  { label: 'ÎNĂLȚIME', value: '96', unit: 'm' },
];

const GLYPHS = '0123456789#%&/+<>=$§';

export function mountManifesto(content) {
  const sec = document.createElement('section');
  sec.className = 'sec manifesto';
  sec.id = 'proiectul';
  sec.setAttribute('aria-labelledby', 'proiectul-h');
  sec.innerHTML = `
    <p class="sec-label mono">01 / PROIECTUL</p>
    <h2 class="sr-only" id="proiectul-h">Proiectul</h2>
    <p class="manifesto__text">Orizont adună 46 de apartamente pe 24 de niveluri, la marginea parcului Herăstrău.
      <span class="manifesto__soft">Am desenat turnul pornind de la terasă: o încăpere fără pereți, cu lumină pe trei laturi, pe care o are fiecare locuință.</span>
      <em>Restul — piatra, lemnul, liniștea — vine de la sine.</em></p>
    <dl class="stats">
      ${STATS.map((s) => `
        <div class="stat">
          <dt class="mono">${s.label}</dt>
          <dd class="stat__num" aria-label="${s.value}${s.unit ? ' ' + s.unit : ''}">
            <span class="stat__val" data-value="${s.value}" aria-hidden="true">${s.value}</span>${s.unit ? `<span class="stat__unit" aria-hidden="true">${s.unit}</span>` : ''}
          </dd>
        </div>`).join('')}
    </dl>`;
  content.append(sec);

  const text = sec.querySelector('.manifesto__text');
  const words = splitWords(text);
  if (reducedMotion) return;

  gsap.fromTo(words, { opacity: 0.15 }, {
    opacity: 1, ease: 'none', stagger: 0.05,
    scrollTrigger: { trigger: text, start: 'top 82%', end: 'bottom 42%', scrub: 0.6 },
  });

  const vals = [...sec.querySelectorAll('.stat__val')];
  vals.forEach((v) => { v.textContent = v.dataset.value.replace(/./g, '0'); });
  ScrollTrigger.create({
    trigger: sec.querySelector('.stats'),
    start: 'top 88%',
    once: true,
    onEnter: () => vals.forEach((v, i) => scramble(v, i * 0.12)),
  });
}

/**
 * Glitch reveal: every slot cycles random glyphs for ~0.8s while the number counts up,
 * then slots lock left→right to the final digits. Jitter + RGB-split shadow fade out at the end.
 */
function scramble(el, delay) {
  const final = el.dataset.value;
  const n = final.length;
  const target = parseInt(final, 10);
  const state = { t: 0 };
  el.classList.add('is-glitching');
  gsap.to(state, {
    t: 1, duration: 1.35, delay, ease: 'none',
    onUpdate: () => {
      const t = state.t;
      const counted = String(Math.round(target * gsap.parseEase('power2.out')(Math.min(t / 0.6, 1)))).padStart(n, '0');
      const locked = Math.floor(n * gsap.utils.clamp(0, 1, (t - 0.6) / 0.4));
      let out = '';
      for (let i = 0; i < n; i++) {
        if (i < locked) out += final[i];
        else out += Math.random() < 0.45 ? GLYPHS[(Math.random() * GLYPHS.length) | 0] : counted[i];
      }
      el.textContent = out;
      const amp = (1 - t) * 6;
      el.style.setProperty('--jx', `${(Math.random() - 0.5) * amp}px`);
      el.style.setProperty('--split', `${amp * 0.6 + 0.5}px`);
    },
    onComplete: () => {
      el.textContent = final;
      el.classList.remove('is-glitching');
      el.style.removeProperty('--jx');
    },
  });
}
