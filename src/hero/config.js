// Hero configuration: copy, media URLs and the fallback video timeline. Overlay timing comes from
// ./video/hero.json at runtime (see timeline.js), so a new cut of the video only needs a new JSON.

export const BASE = import.meta.env.BASE_URL;
export const imgUrl = (name) => `${BASE}img/${name}.webp`;
export const videoUrl = (name) => `${BASE}video/${name}`;

export const PIN_VH = { desktop: 6.5, mobile: 4 };   // hero height in viewport heights (§8: ~650vh / ≤ 400vh)
export const MOBILE_MQ = '(max-width: 767px)';

// Copy: SPEC §7.1 (Amendment 1).
export const INTRO = {
  label: '01 — ÎNCEPUT',
  sub: 'Rezidențe private în <em>București</em>',
  body: 'Patruzeci și șase de case suspendate deasupra parcului Herăstrău.',
  cue: 'DERULEAZĂ PENTRU A INTRA',
};

export const LIST = ['ÎNCEPUT', 'ETAJE', 'PIATRĂ', 'TERASĂ', 'ACASĂ'];

export const CHAPTERS = [
  { list: 0, label: INTRO.label },
  {
    list: 1, label: '02 — ETAJE', plate: 'skyline-dusk',
    title: ['ETAJ CU ETAJ,', '<em>un reper.</em>'],
    body: 'Douăzeci și patru de niveluri de sticlă bronz, ridicate între tei și bulevarde.',
  },
  {
    list: 2, label: '03 — PIATRĂ', plate: 'tower-exterior',
    title: ['TRAVERTIN', '<em>pe verticală.</em>'],
    body: 'O dungă de piatră caldă leagă terasele, de la sol până la coroană.',
  },
  {
    list: 3, label: '04 — TERASĂ', plate: 'loggia',
    title: ['TERASA,', '<em>a cincea cameră.</em>'],
    body: 'Fiecare apartament își prelungește livingul afară, la adăpost de vânt, cu priveliștea întreagă.',
  },
  {
    list: 4, label: '05 — ACASĂ', plate: 'interior-living',
    title: ['ACASĂ,', '<em>deasupra zgomotului.</em>'],
    body: 'Stejar afumat, piatră mată și lumină ascunsă în tavan. Bulevardul rămâne jos.',
  },
  {
    list: 4, label: '',
    title: ['INTRĂ', '<em>și simte spațiul.</em>'],
    cta: [
      { text: 'PROGRAMEAZĂ O VIZITĂ', href: '#vizionare', cls: 'pill' },
      { text: 'VEZI APARTAMENTELE', href: '#rezidente', cls: 'pill pill--ghost' },
    ],
  },
];

// Used when hero.json is missing or malformed: the §8.2 shot list with the agreed cut points.
const cuts = [0, 5.25, 12.25, 19.25, 24.25, 29.25, 34];
export const FALLBACK_TIMELINE = {
  duration: 34,
  fps: 24,
  shots: cuts.slice(0, 6).map((start, i) => ({ id: `S${i + 1}`, start, end: cuts[i + 1] })),
  chapters: [{ index: 0, start: 0, end: 3 }, { index: 1, start: 3, end: 12.25 }]
    .concat(cuts.slice(2, 6).map((start, i) => ({ index: i + 2, start, end: cuts[i + 3] }))),
};

export const TIMECODE_FPS = 25;   // the HUD timecode counts in 25 fps-style frames, like the reference
