import './hero.css';
import gsap from 'gsap';
import { ScrollTrigger } from 'gsap/ScrollTrigger';
import { MOBILE_MQ, PIN_VH, videoUrl } from './config.js';
import { Overlay } from './overlay.js';
import { mountStatic } from './static.js';
import { buildTimeline, loadTimeline } from './timeline.js';
import { VideoScrub } from './video.js';

gsap.registerPlugin(ScrollTrigger);

const cursor = (state) => window.__cursor?.setState(state);

/**
 * Pinned hero: one merged video scrubbed by scroll, with the DOM overlay on top. Scroll progress
 * sets a target time; the video eases toward it; the overlay follows the time on screen, so copy
 * and footage stay locked together in both directions.
 */
export function mountHero(el) {
  if (matchMedia('(prefers-reduced-motion: reduce)').matches) return mountStatic(el);

  el.classList.add('hx');
  el.innerHTML = '<div class="hx-stage"><div class="hx-frame"></div></div>';
  const stage = el.firstElementChild;
  const frame = stage.firstElementChild;
  const mobile = matchMedia(MOBILE_MQ);

  let tl = buildTimeline(null);
  const overlay = new Overlay(frame, tl);
  const scrub = new VideoScrub(frame, { onBuffered: (f) => overlay.loading(f) });
  overlay.loading(0);

  let progress = 0;
  let active = true;
  const pin = ScrollTrigger.create({
    trigger: el,
    start: 'top top',
    end: () => `+=${innerHeight * ((mobile.matches ? PIN_VH.mobile : PIN_VH.desktop) - 1)}`,
    pin: stage,
    scrub: true,
    refreshPriority: 1,
    invalidateOnRefresh: true,
    onUpdate: (self) => { progress = self.progress; },
  });
  const visibility = ScrollTrigger.create({
    trigger: el,
    start: 'top bottom',
    end: 'bottom top',
    onToggle: (self) => {
      active = self.isActive;
      if (!active) cursor('default');
    },
  });

  function tick(_, dt) {
    if (!active) return;
    const t = scrub.tick(progress * tl.duration, dt);
    overlay.update(Math.min(t / tl.duration, 1));
  }

  const onResize = () => overlay.fit();
  const onEnter = () => cursor('scroll');
  const onLeave = () => cursor('default');
  addEventListener('resize', onResize);
  stage.addEventListener('pointerenter', onEnter);
  stage.addEventListener('pointerleave', onLeave);
  gsap.ticker.add(tick);

  // hero.json and the poster load right away; the video request waits until the poster has
  // decoded and painted, so it never competes with first paint.
  const timeline = loadTimeline().then((loaded) => {
    tl = loaded;
    scrub.fps = tl.fps;
    overlay.setTimeline(tl);
  });
  Promise.all([timeline, scrub.showPoster(videoUrl(tl.sources.poster))])
    .then(() => scrub.stream(VideoScrub.pick(tl.sources)));

  document.fonts.ready.then(() => { overlay.fit(); overlay.intro(); });

  return {
    destroy() {
      gsap.ticker.remove(tick);
      pin.kill(true);
      visibility.kill();
      removeEventListener('resize', onResize);
      scrub.dispose();
      el.innerHTML = '';
      el.classList.remove('hx');
    },
  };
}
