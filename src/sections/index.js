import './sections.css';
import { ScrollTrigger, wireImages } from './util.js';
import { mountNav } from './nav.js';
import { mountCursor } from './cursor.js';
import { mountManifesto } from './manifesto.js';
import { mountMarquee } from './marquee.js';
import { mountGestures } from './gestures.js';
import { mountResidences } from './residences.js';
import { mountMaterials } from './materials.js';
import { mountLocation } from './location.js';
import { mountViewing } from './viewing.js';
import { mountFooter } from './footer.js';

/**
 * Team SECTIONS entry: nav, cursor, content sections 1–8 and the footer.
 * Runs after the hero has mounted so our ScrollTriggers (including the pinned
 * gestures strip) are created after, and refreshed after, the hero's pin.
 */
export function mountSections({ nav, content, footer }) {
  mountManifesto(content);
  mountMarquee(content);
  mountGestures(content);
  mountResidences(content);
  mountMaterials(content);
  mountLocation(content);
  mountViewing(content);
  mountFooter(footer);
  mountNav(nav);
  mountCursor();
  wireImages(document);

  // Webfont metrics change paragraph heights and the footer wordmark size.
  document.fonts?.ready.then(() => ScrollTrigger.refresh());
}
