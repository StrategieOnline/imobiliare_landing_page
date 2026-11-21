import './css/location.css';
import { gsap, MQ, figure } from './util.js';

const DISTANCES = [
  ['Parcul Herăstrău', '3 min pe jos'],
  ['Piața Charles de Gaulle', '6 min'],
  ['Aeroportul Otopeni', '18 min'],
  ['Centrul Vechi', '15 min'],
];

export function mountLocation(content) {
  const sec = document.createElement('section');
  sec.className = 'sec sec--slate location';
  sec.id = 'locatie';
  sec.setAttribute('aria-labelledby', 'locatie-h');
  sec.innerHTML = `
    <div class="location__grid">
      <div class="location__copy">
        <p class="sec-label mono">04 / LOCAȚIE</p>
        <h2 class="display h-lg" id="locatie-h">
          <span class="line"><span>LÂNGĂ PARC,</span></span>
          <span class="line"><span><em>aproape de tot.</em></span></span>
        </h2>
        <p class="location__coords mono">44.4791° N <i>/</i> 26.0853° E</p>
        <p class="location__addr mono">Șoseaua Nordului 12, București</p>
        <p class="location__body">La marginea parcului Herăstrău, între vile interbelice și străzi cu tei. Orașul e la câteva minute, zgomotul lui rămâne jos.</p>
        <table class="dist mono">
          <caption class="sr-only">Distanțe de la Orizont</caption>
          <tbody>
            ${DISTANCES.map(([place, time]) => `<tr class="dist__row"><th scope="row">${place}</th><td>${time}</td></tr>`).join('')}
          </tbody>
        </table>
      </div>
      <div class="location__media">
        ${figure({ name: 'location', alt: 'Turnul Orizont între clădirile orașului la ora albastră, lângă lacul Herăstrău', w: 1600, h: 2000, tone: 'slate', cls: 'location__ph', imgCls: 'location__img' })}
        <p class="location__cap mono" aria-hidden="true"><span>HERĂSTRĂU, ORA ALBASTRĂ</span><span>N ↑</span></p>
      </div>
    </div>`;
  content.append(sec);

  gsap.matchMedia().add(MQ.motion, () => {
    gsap.from(sec.querySelectorAll('.location__copy .line > span'), {
      yPercent: 110, duration: .9, ease: 'power4.out', stagger: .08,
      scrollTrigger: { trigger: sec, start: 'top 70%' },
    });
    gsap.fromTo(sec.querySelector('.location__img'), { yPercent: -7 }, {
      yPercent: 7, ease: 'none',
      scrollTrigger: { trigger: sec.querySelector('.location__media'), start: 'top bottom', end: 'bottom top', scrub: true },
    });
    const rows = sec.querySelectorAll('.dist__row');
    const tl = gsap.timeline({ scrollTrigger: { trigger: sec.querySelector('.dist'), start: 'top 85%' } });
    tl.from(rows, { '--line': 0, duration: 1.1, ease: 'power3.inOut', stagger: .12 }, 0)
      .from(sec.querySelectorAll('.dist__row th, .dist__row td'), { y: 14, opacity: 0, duration: .7, ease: 'power3.out', stagger: .06 }, .15);
  });
}
