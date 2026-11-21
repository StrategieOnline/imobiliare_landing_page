#!/usr/bin/env bash
# Pre-commit gate: run before every commit to main. Exits non-zero on any problem.
# 1. No reference-site names anywhere in the tree (terms live in tools/.blocklist, which is
#    gitignored on purpose: committing the names would itself leak them).
# 2. Nothing staged from reference/, assets-src/, dist/, node_modules/, public/models/,
#    public/draco/; no .mov / .blend1; .mp4 only under public/video/.
# 3. No staged file over 50 MB (GitHub warns at 50 MB, refuses at 100 MB).
# 4. tools/check-video.sh: no placeholder hero video, no models/draco in the site (SPEC §8).
set -euo pipefail
ROOT="$(cd "$(dirname "${BASH_SOURCE[0]}")/.." && pwd)"
cd "$ROOT"
BLOCKLIST="${BLOCKLIST:-tools/.blocklist}"
fail=0

[[ -s "$BLOCKLIST" ]] || { echo "precommit: $BLOCKLIST missing or empty (one term per line; ask the judge)" >&2; exit 1; }
if grep -rniIE -f "$BLOCKLIST" . \
     --exclude-dir=reference --exclude-dir=node_modules --exclude-dir=assets-src \
     --exclude-dir=dist --exclude-dir=.git --exclude="$(basename "$BLOCKLIST")"; then
  echo "precommit: reference-site names found above" >&2; fail=1
fi
# Binary files too (glb/blend metadata, image EXIF): list names only.
if grep -rliaE -f "$BLOCKLIST" public blender 2>/dev/null; then
  echo "precommit: reference-site names inside binary assets above" >&2; fail=1
fi

staged="$(git diff --cached --name-only --diff-filter=AM)"
if grep -E '^(reference|assets-src|dist|node_modules|public/models|public/draco)/|\.(mov|blend1)$' <<<"$staged" \
   || grep -E '\.mp4$' <<<"$staged" | grep -vE '^public/video/[^/]+\.mp4$'; then
  echo "precommit: forbidden paths staged above" >&2; fail=1
fi
while IFS= read -r f; do
  [[ -n "$f" && -f "$f" ]] || continue
  size=$(wc -c <"$f")
  (( size <= 50000000 )) || { echo "precommit: $f is $((size / 1000000)) MB (> 50 MB)" >&2; fail=1; }
done <<<"$staged"

bash "$ROOT/tools/check-video.sh" "$ROOT" || fail=1

(( fail == 0 )) && echo "precommit: ok"
exit "$fail"
