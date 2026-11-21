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

// Team mounts. Each team adds exactly one import + mount line in its block.
// --- HERO ---
// --- SECTIONS ---

window.addEventListener('load', () => ScrollTrigger.refresh());
