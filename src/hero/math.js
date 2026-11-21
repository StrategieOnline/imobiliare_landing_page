export const clamp = (v, a = 0, b = 1) => (v < a ? a : v > b ? b : v);
export const lerp = (a, b, t) => a + (b - a) * t;
export const range = (p, a, b) => clamp((p - a) / (b - a));
export const smooth = (t) => t * t * (3 - 2 * t);
export const easeIn = (t) => t * t * t;
export const easeOut = (t) => 1 - (1 - t) ** 3;
export const easeInOut = (t) => (t < 0.5 ? 4 * t * t * t : 1 - (-2 * t + 2) ** 3 / 2);
/** 0 → 1 → 0 across [a, b]. */
export const bell = (p, a, b) => {
  const t = range(p, a, b);
  return t > 0 && t < 1 ? Math.sin(t * Math.PI) : 0;
};

/**
 * Samples keyframes `[[p, v0, v1, ...], ...]` at progress p with smoothstep easing
 * between keys, writing values into `out` (no allocation).
 */
export function sampleKeys(keys, p, out) {
  const n = keys[0].length - 1;
  let a = keys[0];
  let b = a;
  if (p >= keys[keys.length - 1][0]) a = b = keys[keys.length - 1];
  else {
    for (let i = 1; i < keys.length; i++) {
      if (p < keys[i][0]) { a = keys[i - 1]; b = keys[i]; break; }
    }
  }
  const t = a === b ? 0 : smooth(range(p, a[0], b[0]));
  for (let j = 0; j < n; j++) out[j] = lerp(a[j + 1], b[j + 1], t);
  return out;
}
