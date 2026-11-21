import './styles/tokens.css';
import gsap from 'gsap';
import { ScrollTrigger } from 'gsap/ScrollTrigger';
import Lenis from 'lenis';

gsap.registerPlugin(ScrollTrigger);

export const reducedMotion = window.matchMedia('(prefers-reduced-motion: reduce)').matches;

export const lenis = new Lenis({ lerp: 0.09, smoothWheel: !reducedMotion });
lenis.on('scroll', ScrollTrigger.update);
gsap.ticker.add((t) => lenis.raf(t * 1000));
gsap.ticker.lagSmoothing(0);
window.__lenis = lenis;

// A failing team module must not blank the rest of the page.
function safeMount(name, fn) {
  try { fn(); } catch (err) { console.error(`[${name}] mount failed`, err); }
}

// Team mounts. Each team adds exactly one import + mount line in its block.
// --- HERO ---
import { mountHero } from './hero/index.js'; safeMount('hero', () => mountHero(document.getElementById('hero')));
// --- SECTIONS ---
import { mountSections } from './sections/index.js'; safeMount('sections', () => mountSections({ nav: document.getElementById('nav'), content: document.getElementById('content'), footer: document.getElementById('footer') }));

// Pins change the document height; keep Lenis' scroll limit in sync so early scrollTo() calls aren't clamped to 0.
ScrollTrigger.addEventListener('refresh', () => lenis.resize());
ScrollTrigger.refresh();
window.addEventListener('load', () => ScrollTrigger.refresh());
