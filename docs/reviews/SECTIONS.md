# SECTIONS review

## Round 1 (2026-11-21)

**Verdict: PASS** · **Craft 8.5/10**

**Craft justification:** this is the closest component-for-component match to the reference so far.
- **Residences hover** (outlined rows, the active row filled and nudged right, others dimmed to .35, a cursor-following 4:5 preview with a "VEZI" disc) is nearly frame-identical to ref t_13.8.
- **Marquee** (filled/outlined + gold ✦), **inset materials**, **slate location with hairline table**, and the **giant clipped footer wordmark** all hit their keyframes (t_9.0, t_14.6, t_16.2, t_18.0).
- **Type system** holds everywhere: CAPS Unbounded + gold italic serif tail, mono labels, generous rhythm. The manifesto puts the serif phrase *inside* the paragraph, as the reference does.
- **What keeps it from a 9:** the gestures numerals sit a little loose against their titles mid-scroll, plus two small content nits (fixes below).

Method: the Chrome extension isn't connected, so I used headless Chrome over raw CDP (my own script, Node's built-in WebSocket) against `npx vite --port 5104`:
- Viewports: 1440×900 (motion), 375×812 (touch emulation) and 1440×900 with `prefers-reduced-motion: reduce`.
- Screenshots of each section (5 positions across the gestures pin), hover passes over all 3 apartment rows, an empty submit, a bad-email submit and a valid submit with network capture, plus copy dumps.
- `npx vite build` to a scratch outDir: passes (47 modules; the 792 kB main chunk is mostly three.js, from HERO).
- The dev server was killed afterwards.

### Checklist

| ID | | evidence |
|---|---|---|
| G1 | ✅ | build passes |
| G2 | ✅ | `src/sections/**` + one mount line (the lead's `safeMount` wrapper is fine) |
| G3 | ✅ | images go through `import.meta.env.BASE_URL`; no absolute `/img` |
| G4 | ✅ | no reference names |
| G5 | ✅ | **0 console errors, 0 exceptions, 0 failed requests** in all three runs |
| G6 | ✅ | all §7.2 copy verbatim (rendered `innerText` diffed against §7.2); comma-below Ș/Ț everywhere; grep finds **no §3 leftovers** (`TREI GESTURI`, `REZIDENȚA LOGIA`, `PROGRAMEAZĂ O VIZIONARE`, `Te întâmpinăm`, … all absent) |
| S0 | ✅ | `#proiectul #arhitectura #rezidente #materiale #locatie #vizionare` exist. A delegated listener routes every `#` link (hero CTAs included) through Lenis |
| S1 | ✅ | nav exact (`03 APARTAMENTE`, pill `PROGRAMEAZĂ O VIZITĂ`); ink bar with blur after the hero; active-chapter highlight works (screenshot: `03 APARTAMENTE` gold while in #rezidente) |
| S2 | ✅ | 375px: `MENIU` toggle with a full-screen clip-reveal overlay, Esc closes it, Lenis stops while it's open |
| S3 | ✅ | `window.__cursor.setState` with `default/link/scroll/view`; view = filled disc + label (seen over images); hidden on coarse pointers; transform-only; a forced state is released outside `#hero` |
| S4 | ✅ | manifesto verbatim. Word scrub .15→1; after scrolling past, 0/45 words are below full opacity |
| S5 | ✅ | stats end at exactly `46 / 24 / 2028 / 96 m`. Glyph scramble + count-up with a left→right lock, time-based, so it settles even on a fast scroll-past |
| S6–S7 | ✅ | words exact, filled/outlined alternate, seamless wrap (group-width wrap); velocity boost + direction flip + skew; ticks only while visible; static under reduced motion |
| S8–S9 | ✅ | paper bg, pinned at top 0 after the hero pin; `TREI IDEI, un singur turn.`; 3 cards (PIATRA / TERASA / INTRAREA, §7.2 texts); clip-path reveal + inner parallax through `containerAnimation`; outlined numerals on a faster plane |
| S10 | ✅ | <768px and reduced motion: vertical stack, no pin, no overflow |
| S11–S12 | ✅ | §7.2 rows and specs exact. Hover matches ref t_13.8; previews swap with a direction-aware clip wipe; clicking a row scrolls to the form and preselects the type (a nice touch) |
| S13 | ✅ | keyboard focus gives the same active/dim state; touch shows inline images under each row |
| S14 | ✅ | inset frame (gutters, radius), 100vh, scale 1.15→1 scrubbed, §7.2 headline + body |
| S15–S16 | ✅ | slate, §7.2 headline, coordinates (44.4791 N / 26.0853 E, the Herăstrău north shore, plausible), the address, 4 rows exact, hairlines drawing left→right with a stagger |
| S17 | ✅ | `HAI SĂ NE vedem acolo.`: per-letter scaleY 2.2 + blur 14 px + offset settling, scrubbed; static under reduced motion. Body verbatim |
| S18 | ✅ | 2-column underline form with mono labels; select is exactly `Apartament cu terasă / Apartament de colț / Penthouse / Încă nu știu`; 1 column at 375px |
| S19 | ✅ | empty submit → 3 Romanian errors, `aria-invalid` on name/email/phone, focus on `#f-name`; a bad email → "Adresa de email nu pare validă."; a valid submit → inline success "MULȚUMIM, Ana." with **zero network requests** and no navigation |
| S20 | ✅ | mono nav + `ÎNAPOI SUS ↑` (Lenis), legal line verbatim; the wordmark is JS-fitted to 98.5% width, rises yPercent 70→0 and is clipped by the bottom edge |
| S21 | ✅ | `loading="lazy"`, decode-then-fade over gradient placeholders; on a 404 the img is removed so the placeholder shows (code path checked) |
| S22 | ✅ | reduced motion: no pins, every word and stat visible immediately, smear and marquee static, form works (run 3: 0 dim words, stats final, the same form results) |
| S23 | ✅ | 375px: `scrollWidth − innerWidth = 0` at all 8 positions; body ≥15 px |
| S24 | ✅ | refresh on `document.fonts.ready`, after a submit and on reset |
| S25 | ✅ | editorial, not templated |

(A duplicated strip in one viewing-section screenshot was a headless raster artefact. Re-shot twice at the same position, the DOM has 4 contact rows and 4 options and renders clean.)

### Fixes (minor, nice-to-have)

1. **minor · `src/sections/gestures.js:30` · Wrong hint on mobile.** The `DERULEAZĂ →` hint also shows in the <768px / reduced-motion vertical stack, where it points the wrong way. **Fixed:** hide it outside `MQ.desktopMotion`, or switch the arrow to `↓` there.
2. **minor · `src/sections/viewing.js:37-38` · Contact details point at a real domain.** `vizionari@orizont.ro` belongs to a real, registrable domain the project doesn't own, and readers may copy it and email a stranger. **Fixed:** a non-routable address (`vizionari@orizont.example`), or drop the email row and keep the phone as an obvious placeholder. Mention it in DECISIONS.
3. **nice-to-have · `src/sections/gestures.js:72` · Numerals drift away mid-scroll.** The numeral's `x: 22vw → -14vw` travel sometimes leaves it floating away from its title and closer to the next card's text. Narrow it (e.g. `10vw → -6vw`) so the numeral always reads as belonging to its own card, as in ref t_10.6–12.2.

4. **minor · `src/sections/residences.js:77` · Previews load before first paint.** Found while measuring the production build (served from `/imobiliare_landing_page/`): the three hover-preview images (`res-loggia`, `res-penthouse`, `res-corner`, **473 KB**) download **at page load**, at t≈405 ms, before first paint. The reason: `loading="lazy"` has no effect inside the fixed-position `.rpreview` box, which is always "in the viewport". The first view is still well under the §7.3 3 MB budget (≈0.6 MB gz JS+CSS + 350 KB rooftop + these), so this isn't a blocker. **Fixed:** create the preview `<img>`s (or set their `src`) on the first `pointerenter` of the list, or when `#rezidente` comes within ~1 viewport (IntersectionObserver), not at mount.

No blockers or majors. Ready for integration.
