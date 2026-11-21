import './css/materials.css';
import { gsap, MQ, figure } from './util.js';

export function mountMaterials(content) {
  const sec = document.createElement('section');
  sec.className = 'materials';
  sec.id = 'materiale';
  sec.setAttribute('aria-labelledby', 'materiale-h');
  sec.innerHTML = `
    <div class="materials__frame">
      ${figure({ name: 'materials', alt: 'Interior cu stejar afumat, travertin neșlefuit și lumină caldă ascunsă în tavan', w: 2560, h: 1440, cls: 'materials__ph', imgCls: 'materials__img' })}
      <div class="materials__shade" aria-hidden="true"></div>
      <p class="materials__tag mono" aria-hidden="true"><span>INTERIOR</span><span>APARTAMENT DE COLȚ · ETAJUL 14</span></p>
      <div class="materials__copy">
        <h2 class="display h-lg" id="materiale-h">
          <span class="line"><span>STEJAR,</span></span>
          <span class="line"><span>TRAVERTIN,</span></span>
          <span class="line"><span><em>umbră caldă.</em></span></span>
        </h2>
        <p class="materials__body">Am ales puține materiale și le-am lăsat să îmbătrânească frumos: stejar afumat, travertin neșlefuit, bronz patinat.</p>
      </div>
      <ul class="materials__list mono" aria-label="Materiale">
        <li>Stejar afumat</li><li>Travertin neșlefuit</li><li>Bronz patinat</li>
      </ul>
    </div>`;
  content.append(sec);

  gsap.matchMedia().add(MQ.motion, () => {
    gsap.fromTo(sec.querySelector('.materials__img'), { scale: 1.15 }, {
      scale: 1, ease: 'none',
      scrollTrigger: { trigger: sec, start: 'top bottom', end: 'bottom bottom', scrub: true },
    });
    gsap.from(sec.querySelectorAll('.materials__copy .line > span'), {
      yPercent: 110, duration: 1, ease: 'power4.out', stagger: .09,
      scrollTrigger: { trigger: sec.querySelector('.materials__copy'), start: 'top 88%' },
    });
    gsap.from(sec.querySelectorAll('.materials__body, .materials__list li'), {
      opacity: 0, y: 16, duration: .9, ease: 'power3.out', stagger: .06, delay: .3,
      scrollTrigger: { trigger: sec.querySelector('.materials__copy'), start: 'top 88%' },
    });
  });
}
