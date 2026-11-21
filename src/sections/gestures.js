import './css/gestures.css';
import { gsap, MQ, figure } from './util.js';

const CARDS = [
  { n: '01', title: 'PIATRA', img: 'tower-exterior', w: 1600, h: 2000, tone: 'dusk',
    alt: 'Turnul Orizont la apus: sticlă bronz și o dungă de travertin care leagă terasele',
    text: 'Travertinul urcă pe toată fațada și marchează, etaj cu etaj, fiecare terasă.' },
  { n: '02', title: 'TERASA', img: 'loggia', w: 2560, h: 1440, tone: 'dusk',
    alt: 'Terasă adâncă din travertin, cu ușile glisante deschise spre un living luminat cald',
    text: 'Adâncă de trei metri, ferită de vânt, deschisă spre parc și spre oraș.' },
  { n: '03', title: 'INTRAREA', img: 'threshold', w: 1600, h: 2000, tone: 'stone',
    alt: 'Ușă pivotantă din stejar deschisă spre un hol de piatră care duce spre living',
    text: 'O ușă pivotantă din stejar și un hol de piatră care se deschide spre lumină.' },
];

export function mountGestures(content) {
  const sec = document.createElement('section');
  sec.className = 'sec sec--paper gestures';
  sec.id = 'arhitectura';
  sec.setAttribute('aria-labelledby', 'arhitectura-h');
  sec.innerHTML = `
    <div class="gestures__track">
      <div class="gestures__intro">
        <p class="sec-label mono">02 / ARHITECTURA</p>
        <h2 class="display h-xl gestures__h" id="arhitectura-h">
          <span class="line"><span>TREI IDEI,</span></span>
          <span class="line"><span><em>un singur turn.</em></span></span>
        </h2>
        <p class="gestures__lede">Un turn se recunoaște de departe după câteva decizii clare. Acestea sunt ale noastre.</p>
        <p class="gestures__hint mono" aria-hidden="true">DERULEAZĂ <span>→</span></p>
      </div>
      ${CARDS.map((c) => `
        <article class="gcard gcard--${c.n}">
          <div class="gcard__media" data-cursor="view" data-cursor-label="${c.title}">
            ${figure({ name: c.img, alt: c.alt, w: c.w, h: c.h, tone: c.tone, cls: 'gcard__ph', imgCls: 'gcard__img' })}
          </div>
          <div class="gcard__body">
            <span class="gcard__num" aria-hidden="true">${c.n}</span>
            <h3 class="gcard__title"><span class="mono gcard__idx">${c.n} /</span> ${c.title}</h3>
            <p class="gcard__text">${c.text}</p>
          </div>
        </article>`).join('')}
    </div>`;
  content.append(sec);

  const track = sec.querySelector('.gestures__track');
  const cards = [...sec.querySelectorAll('.gcard')];
  const mm = gsap.matchMedia();

  mm.add(MQ.desktopMotion, () => {
    const distance = () => track.scrollWidth - document.documentElement.clientWidth;
    const scroll = gsap.to(track, {
      x: () => -distance(), ease: 'none',
      scrollTrigger: {
        trigger: sec, pin: true, scrub: 0.8, start: 'top top',
        end: () => `+=${distance()}`, invalidateOnRefresh: true, anticipatePin: 1,
      },
    });

    gsap.from(sec.querySelectorAll('.gestures__h .line > span'), {
      yPercent: 110, duration: .9, ease: 'power4.out', stagger: .08,
      scrollTrigger: { trigger: sec, start: 'top 70%' },
    });

    cards.forEach((card) => {
      const along = { containerAnimation: scroll, trigger: card, scrub: true };
      gsap.fromTo(card.querySelector('.gcard__ph'),
        { clipPath: 'inset(8% 0% 8% 100%)' },
        { clipPath: 'inset(0% 0% 0% 0%)', ease: 'power2.out', scrollTrigger: { ...along, start: 'left 100%', end: 'left 40%' } });
      gsap.fromTo(card.querySelector('.gcard__img'), { xPercent: -9 }, { xPercent: 9, ease: 'none', scrollTrigger: { ...along, start: 'left right', end: 'right left' } });
      // the outlined numeral travels faster than its card: reads as a nearer plane
      gsap.fromTo(card.querySelector('.gcard__num'), { x: '6vw' }, { x: '-4vw', ease: 'none', scrollTrigger: { ...along, start: 'left right', end: 'right left' } });
      gsap.from(card.querySelectorAll('.gcard__title, .gcard__text'), {
        y: 40, opacity: 0, ease: 'power2.out', stagger: .1,
        scrollTrigger: { ...along, start: 'left 75%', end: 'left 35%' },
      });
    });
  });

  mm.add('(max-width: 767px) and (prefers-reduced-motion: no-preference)', () => {
    cards.forEach((card) => {
      gsap.fromTo(card.querySelector('.gcard__ph'), { clipPath: 'inset(100% 0% 0% 0%)' }, {
        clipPath: 'inset(0% 0% 0% 0%)', duration: 1.1, ease: 'power4.out',
        scrollTrigger: { trigger: card, start: 'top 85%' },
      });
      gsap.fromTo(card.querySelector('.gcard__img'), { yPercent: -6 }, {
        yPercent: 6, ease: 'none', scrollTrigger: { trigger: card, start: 'top bottom', end: 'bottom top', scrub: true },
      });
    });
  });
}
