# HANDOFF: Team SECTIONS

## What was built
`src/sections/**`, mounted by one line in the `// --- SECTIONS ---` block of `src/main.js`:
`mountSections({ nav, content, footer })` from `src/sections/index.js`. One module per section, with per-section CSS in `src/sections/css/` and shared primitives in `sections.css` and `util.js`. All copy follows SPEC §7.2 (Amendment 1).

| module | anchor | what it does |
|---|---|---|
| `nav.js` | — | Fixed nav: wordmark + `BUCUREȘTI / NORD`, mono links `01 PROIECTUL · 02 ARHITECTURA · 03 APARTAMENTE · 04 LOCAȚIE` with roll-on-hover, active chapter highlight, `PROGRAMEAZĂ O VIZITĂ` pill. Transparent over the hero, ink bar + blur once `#content` reaches it. Hides on scroll down, returns on scroll up. ≤960px: `MENIU` toggle + full-screen overlay (clip reveal, Esc closes, Lenis stopped while open). A delegated listener sends every `a[href^="#"]` (the hero CTAs too) through `__lenis.scrollTo`. |
| `cursor.js` | — | ⊙ ring, lerped. `window.__cursor.setState('default'\|'link'\|'scroll'\|'view')`. Hover sets link (a/button) and view (`[data-cursor="view"]`, a filled disc with a label). A forced state is dropped when the pointer leaves `#hero`. Hidden on touch. |
| `manifesto.js` | `#proiectul` | Word spans, opacity .15→1 scrubbed. Stats row (`APARTAMENTE 46 · NIVELURI 24 · LIVRARE 2028 · ÎNĂLȚIME 96 m`) with a scramble: random glyphs plus a count-up for ~0.8s, then digits lock left→right, with jitter and an RGB-split shadow. |
| `marquee.js` | — | Two rows in opposite directions, filled/outlined words + gold ✦. Base 60px/s plus Lenis velocity boost; direction follows scroll direction (smoothed); slight velocity skew. Runs only while visible. |
| `gestures.js` | `#arhitectura` | Paper bg. ≥768px: pinned horizontal track (intro + 3 cards); clip-path reveal and inner parallax per image via `containerAnimation`; outlined numerals on a faster plane. <768px or reduced motion: vertical stack, no pin. |
| `residences.js` | `#rezidente` | `ALEGE-ȚI înălțimea.` + an index list of 3 rows. Fine pointer: outlined→filled, others dim to .35, a floating 4:5 preview that follows with lerp, tilts with velocity, and clip-wipes between rows (direction-aware). Touch: inline image under each row. A row click scrolls to the form and preselects that type. |
| `materials.js` | `#materiale` | Inset frame (gutters, 10px radius), 100vh, image scale 1.15→1 scrubbed, line-mask headline. |
| `location.js` | `#locatie` | Slate. Headline, coordinates, address, body; distance table rows stagger in while their hairlines draw left→right (`--line` scaleX). Image parallax. |
| `viewing.js` | `#vizionare` | Smeared headline: each letter goes from scaleY 2.2, blur 14px and an offset to rest, scrubbed with a stagger. Underline form with mono labels and gold focus underline. Validation: name, valid email, phone (≥9 digits), with inline Romanian messages, `aria-invalid` and focus on the first error. Inline success state, no network. |
| `footer.js` | — | Mono nav + `ÎNAPOI SUS ↑` (Lenis), legal line, `© 2026`. A giant `ORIZONT`, JS-fitted to full width, rises (yPercent 70→0 scrubbed) and is clipped by the bottom edge. |

Images: `./img/<name>.webp` via `import.meta.env.BASE_URL`, `loading="lazy"`, `decoding="async"`, width/height plus an aspect-ratio wrapper. Each one sits on a gradient placeholder (dusk/slate/stone + grain) and fades in once decoded; on a 404 the img is removed so the placeholder stays.

## How to verify
- `npx vite build`, then load the page. Scroll the whole page, hover the apartment rows, submit the form empty, then valid.
- 375px: no horizontal overflow (`documentElement.scrollWidth === 375` checked), gestures stacked, inline apartment images, overlay menu.
- `prefers-reduced-motion`: no pins, all words and stats visible immediately, smear and marquee static.

Checked with headless Chrome over CDP (the claude-in-chrome extension was not connected): desktop 1440×900, mobile 375×812 with touch emulation, and reduced motion. With the real hero mounted there were no console errors from SECTIONS, and the gestures pin lands at top 0 after the hero's pin.

## Known gaps / notes for other teams
- ScrollTriggers use the default `refreshPriority`, and the hero pin uses 1 (§7.3). If the hero creates its pin asynchronously, it should call `ScrollTrigger.refresh()` afterwards.
- LEAD: `/favicon.ico` 404s in dev (index.html has no icon link), which is the only console error.
- The contact phone and email in the viewing section are placeholders shown as plain text.
- Unbounded's E/B at weight 800 have ink-trap notches. That is the typeface design, not a bug.

## Round 2 (judge: PASS, 8.5/10)
1. `DERULEAZĂ →` hint hidden in the vertical-stack layouts (<768px and reduced motion).
2. Contact details are clearly fictional: `+40 21 000 0000`, `vizionari@orizont.example`.
3. Gesture numerals: parallax reduced from 22vw→−14vw to 6vw→−4vw, so they stay with their card.
4. Apartment preview images get no `src` until `#rezidente` is within one viewport (IntersectionObserver, `rootMargin: 100%`), or until the list gets its first hover or focus, whichever comes first. Verified: 0 `res-*` requests at page load, all 3 after approaching the list.
Triggers still rely on ScrollTrigger refresh, so the hero's new ~650vh pin needs no change here.
