#!/usr/bin/env bash
# Ship gate for the hero video and the post-three.js layout (SPEC §8): panned-still placeholders
# must never ship, and models/draco must not be in the site.
# Usage: bash tools/check-video.sh [SITE_DIR]   (default: repo root; deploy.sh passes its worktree)
# The placeholder reference is read from the main checkout's assets-src/ (never committed); when it
# is gone there is nothing to compare, and the hero.json status check still applies.
set -euo pipefail
ROOT="$(cd "$(dirname "${BASH_SOURCE[0]}")/.." && pwd)"
SITE="${1:-$ROOT}"
PLACEHOLDER="$ROOT/assets-src/video/placeholder.mp4"
fail=0
bad() { echo "check-video: $*" >&2; fail=1; }

manifest="$SITE/public/video/hero.json"
if [[ -f "$manifest" ]] && grep -qE '"status"[[:space:]]*:[[:space:]]*"placeholder"' "$manifest"; then
  bad "public/video/hero.json has \"status\": \"placeholder\" (panned stills must never ship, SPEC §8.4)"
fi
shopt -s nullglob
if [[ -f "$PLACEHOLDER" ]]; then
  for f in "$SITE"/public/video/*.mp4; do
    cmp -s "$f" "$PLACEHOLDER" && bad "${f#"$SITE"/} is byte-identical to assets-src/video/placeholder.mp4"
  done
fi
for d in public/models public/draco; do
  [[ -d "$SITE/$d" ]] && [[ -n "$(find "$SITE/$d" -type f ! -name .DS_Store -print -quit)" ]] \
    && bad "$d/ must not be in the site (three.js removed; GLBs live in blender/export/)"
done

(( fail == 0 )) && echo "check-video: ok"
exit "$fail"
