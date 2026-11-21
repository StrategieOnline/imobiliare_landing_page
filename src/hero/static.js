import './hero.css';
import { CHAPTERS, INTRO, imgUrl, videoUrl } from './config.js';
import { fitWordmark, hudHTML, wordmarkHTML } from './overlay.js';

const img = (name, alt, eager = false) =>
  `<img src="${imgUrl(name)}" alt="${alt}" ${eager ? 'fetchpriority="high"' : 'loading="lazy"'} decoding="async" onerror="this.remove()" />`;

/**
 * prefers-reduced-motion: no pin, no scrub. The video poster (rooftop plate if it is missing) +
 * wordmark as a static hero, then chapters 1–4 as stacked blocks (plate image + headline + body) and the ch5 invitation.
 */
export function mountStatic(el) {
  el.classList.add('hx', 'hx--static');
  const blocks = CHAPTERS.slice(1, 5).map((ch) => `
    <article class="hx-block">
      <figure class="hx-block__img">${img(ch.plate, '')}</figure>
      <div class="hx-block__text">
        <p class="hx-ch__label mono"><span class="hx-rule"></span>${ch.label}</p>
        <h2 class="display">${ch.title.join(' ')}</h2>
        <p class="hx-ch__body">${ch.body}</p>
      </div>
    </article>`).join('');
  const cta = CHAPTERS[5];
  el.innerHTML = `
    <div class="hx-frame hx-frame--static">
      <figure class="hx-static__plate"><img src="${videoUrl('hero-poster.webp')}" alt="Terasă pe acoperiș la apus, deasupra parcului Herăstrău" fetchpriority="high" decoding="async" onerror="this.onerror=null;this.src='${imgUrl('hero-rooftop')}'" /></figure>
      ${wordmarkHTML()}
      <div class="hx-intro">
        <p class="hx-sub">${INTRO.sub}</p>
        <p class="hx-lead">${INTRO.body}</p>
      </div>
      ${hudHTML()}
    </div>
    <div class="hx-blocks">${blocks}
      <article class="hx-block hx-block--cta">
        <h2 class="display">${cta.title.join(' ')}</h2>
        <div class="hx-ch__cta">${cta.cta.map((b) => `<a class="${b.cls}" href="${b.href}">${b.text}</a>`).join('')}</div>
      </article>
    </div>`;
  const frame = el.querySelector('.hx-frame');
  frame.querySelector('.hx-list li').classList.add('is-active');
  const fit = () => fitWordmark(frame);
  document.fonts.ready.then(fit);
  addEventListener('resize', fit);
  return {
    destroy() {
      removeEventListener('resize', fit);
      el.innerHTML = '';
      el.classList.remove('hx', 'hx--static');
    },
  };
}
