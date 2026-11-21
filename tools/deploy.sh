#!/usr/bin/env bash
# Build the committed HEAD, publish it to the gh-pages branch of origin, then verify it live.
#
# The build runs in a throwaway `git worktree` of HEAD, so it ships exactly what is committed
# (the SHA in the gh-pages commit message is the truth) and `npm ci` never touches the shared
# node_modules/ other people are working with. Uncommitted or untracked site files would be
# silently left out, so the script refuses to run while there are any (DEPLOY_ALLOW_DIRTY=1
# overrides). Idempotent: every run force-pushes one fresh orphan commit (no gh-pages history).
#
# Usage: bash tools/deploy.sh   (or: npm run deploy)
# Env:   DEPLOY_ALLOW_DIRTY=1       deploy HEAD even with uncommitted/untracked site files
#        DEPLOY_REMOTE=origin       remote to push to
#        DEPLOY_VERIFY_TIMEOUT=600  seconds to wait for the Pages build
set -euo pipefail

ROOT="$(cd "$(dirname "${BASH_SOURCE[0]}")/.." && pwd)"
cd "$ROOT"

REPO="strategieonline/imobiliare_landing_page"
PAGES_URL="https://strategieonline.github.io/imobiliare_landing_page/"
REMOTE="${DEPLOY_REMOTE:-origin}"
TIMEOUT="${DEPLOY_VERIFY_TIMEOUT:-600}"
# Everything that ends up in the build.
SITE_PATHS=(src public index.html blender vite.config.js package.json package-lock.json)

die() { echo "deploy: $*" >&2; exit 1; }

REMOTE_URL="$(git remote get-url "$REMOTE" 2>/dev/null)" || die "no git remote '$REMOTE'"
command -v gh >/dev/null || die "gh CLI is needed to watch the Pages build"
SHA="$(git rev-parse HEAD)"
SHORT="$(git rev-parse --short HEAD)"

echo "==> preflight ($SHORT)"
DIRTY="$(git status --porcelain --untracked-files=all -- "${SITE_PATHS[@]}")"
if [[ -n "$DIRTY" ]]; then
  echo "deploy: these site files are uncommitted or untracked, so they would NOT be deployed:" >&2
  echo "$DIRTY" | sed 's/^/  /' >&2
  [[ "${DEPLOY_ALLOW_DIRTY:-0}" == 1 ]] || die "commit them first, or set DEPLOY_ALLOW_DIRTY=1 to deploy HEAD anyway"
  echo "deploy: DEPLOY_ALLOW_DIRTY=1, deploying HEAD without them" >&2
fi
git fetch -q "$REMOTE" main 2>/dev/null || true
if ! git merge-base --is-ancestor HEAD "$REMOTE/main" 2>/dev/null; then
  echo "deploy: WARNING: HEAD $SHORT is not on $REMOTE/main; push main so the deployed SHA can be found" >&2
fi

TMP="$(mktemp -d)"
WT="$TMP/src"
cleanup() { git -C "$ROOT" worktree remove --force "$WT" >/dev/null 2>&1 || true; rm -rf "$TMP"; }
trap cleanup EXIT
git worktree add -q --detach "$WT" "$SHA"
cd "$WT"

echo "==> ship gate (committed content)"
bash "$ROOT/tools/check-video.sh" "$WT" || die "ship gate failed (tools/check-video.sh)"

echo "==> install"
if [[ -f package-lock.json ]]; then npm ci --no-audit --no-fund; else npm i --no-audit --no-fund; fi

echo "==> build"
npx vite build

echo "==> verify dist"
[[ -f dist/index.html ]] || die "dist/index.html missing"
# Sub-path safety: the site lives under /imobiliare_landing_page/, so root-absolute URLs
# (src="/x", href="/x", url(/x), '/img/x' in JS) 404 on Pages. Protocol-relative "//" is fine.
if grep -nE '(src|href|content)="/([^/]|$)' dist/index.html; then
  die "root-absolute URLs in dist/index.html (must be relative, base './')"
fi
if grep -rnoE --include='*.css' 'url\(["'"'"']?/[^/][^)]{0,80}' dist; then
  die "root-absolute url(/...) in built CSS"
fi
if grep -rnoE --include='*.js' '["'"'"'`]/(img|models|fonts|draco|basis|assets)/[^"'"'"'`]{0,80}' dist; then
  die "root-absolute asset paths in built JS (use relative paths or import.meta.env.BASE_URL)"
fi
if [[ -n "$(find dist \( -path '*reference*' -o -name '*.blend' -o -name '*.blend1' -o -name '*.glb' -o -path 'dist/models*' -o -path 'dist/draco*' \) -print -quit)" ]]; then
  die "reference material, Blender sources, models/ or draco/ leaked into dist/"
fi
if [[ -n "$(find dist -name '*.mp4' ! -path 'dist/video/*' -print -quit)" ]]; then
  die ".mp4 outside dist/video/ (reference material?)"
fi
touch dist/.nojekyll
FILES="$(cd dist && find . -type f ! -name '.DS_Store' | sed 's|^\./||' | sort)"
echo "$(echo "$FILES" | wc -l | tr -d ' ') files, $(du -sh dist | cut -f1)"

echo "==> publish to gh-pages"
(
  cd dist
  git init -q
  git checkout -q --orphan gh-pages
  git add -A
  # Reuse the repo's configured identity; never change git config.
  git -c user.name="$(git -C "$ROOT" config user.name)" \
      -c user.email="$(git -C "$ROOT" config user.email)" \
      commit -q -m "deploy: build of main@${SHORT}" -m "Source: ${SHA}"
  git push -q -f "$REMOTE_URL" HEAD:gh-pages
)
PAGES_SHA="$(git -C dist rev-parse HEAD)"
git -C "$ROOT" fetch -q "$REMOTE" gh-pages 2>/dev/null || true
echo "gh-pages -> ${PAGES_SHA:0:7}"

echo "==> wait for the Pages build of ${PAGES_SHA:0:7} (max ${TIMEOUT}s)"
deadline=$((SECONDS + TIMEOUT))
while :; do
  build="$(gh api "repos/$REPO/pages/builds/latest" --jq '[.commit, .status, (.error.message // "")] | @tsv' 2>/dev/null || true)"
  IFS=$'\t' read -r b_commit b_status b_error <<<"$build" || true
  if [[ "${b_commit:-}" == "$PAGES_SHA" ]]; then
    [[ "$b_status" == built ]] && break
    [[ "$b_status" == errored ]] && die "Pages build errored: ${b_error:-no message}; see: gh run list -R $REPO --workflow pages-build-deployment"
  fi
  (( SECONDS < deadline )) || die "Pages build of ${PAGES_SHA:0:7} not built after ${TIMEOUT}s (latest: ${build:-none})"
  sleep 10
done
echo "Pages build: built"

echo "==> verify live (every file in dist/)"
# The query string busts the Pages CDN cache (max-age=600) so we see this deploy, not the last one.
fail=0
check() {
  local path="$1" code
  code="$(curl -s -o /dev/null -w '%{http_code}' --retry 2 "${PAGES_URL}${path}?v=${PAGES_SHA:0:7}")"
  if [[ "$code" == 200 ]]; then echo "  200 /${path}"; else echo "  $code /${path}" >&2; fail=1; fi
}
check ""
while IFS= read -r f; do check "$f"; done <<<"$FILES"
# The live index must be this deploy's index.
curl -s "${PAGES_URL}?v=${PAGES_SHA:0:7}" | cmp -s - dist/index.html \
  || { echo "  live index.html differs from this build (CDN lag?)" >&2; fail=1; }
(( fail == 0 )) || die "live verification failed"

echo "==> deployed main@${SHORT} (gh-pages ${PAGES_SHA:0:7})"
echo "Pages URL: $PAGES_URL"
