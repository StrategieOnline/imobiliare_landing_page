#!/usr/bin/env bash
# Build the committed HEAD and publish it to the gh-pages branch of origin.
#
# The build runs in a throwaway `git worktree` of HEAD, so it ships exactly what is committed
# (the SHA in the gh-pages commit message is the truth) and `npm ci` never touches the shared
# node_modules/ other people are working with. Uncommitted changes are NOT deployed.
# Idempotent: every run force-pushes one fresh orphan commit (gh-pages keeps no history).
# Usage: bash tools/deploy.sh   (or: npm run deploy)
set -euo pipefail

ROOT="$(cd "$(dirname "${BASH_SOURCE[0]}")/.." && pwd)"
cd "$ROOT"

PAGES_URL="https://strategieonline.github.io/imobiliare_landing_page/"
REMOTE="${DEPLOY_REMOTE:-origin}"

REMOTE_URL="$(git remote get-url "$REMOTE" 2>/dev/null)" || { echo "deploy: no git remote '$REMOTE'" >&2; exit 1; }
SHA="$(git rev-parse HEAD)"
SHORT="$(git rev-parse --short HEAD)"
if [[ -n "$(git status --porcelain --untracked-files=no)" ]]; then
  echo "deploy: note: uncommitted changes are not deployed; building HEAD ($SHORT)" >&2
fi

TMP="$(mktemp -d)"
WT="$TMP/src"
cleanup() { git -C "$ROOT" worktree remove --force "$WT" >/dev/null 2>&1 || true; rm -rf "$TMP"; }
trap cleanup EXIT
git worktree add -q --detach "$WT" "$SHA"
cd "$WT"

echo "==> install ($SHORT)"
if [[ -f package-lock.json ]]; then npm ci --no-audit --no-fund; else npm i --no-audit --no-fund; fi

echo "==> build"
npx vite build

echo "==> verify dist"
[[ -f dist/index.html ]] || { echo "deploy: dist/index.html missing" >&2; exit 1; }
# Sub-path safety: the site lives under /imobiliare_landing_page/, so root-absolute
# asset URLs (src="/x", href="/x", url(/x)) would 404. Protocol-relative "//" is fine.
if grep -nE '(src|href)="/([^/]|$)' dist/index.html; then
  echo "deploy: absolute asset URLs in dist/index.html (must be relative, base './')" >&2
  exit 1
fi
if grep -rnE --include='*.css' 'url\(["'"'"']?/[^/]' dist; then
  echo "deploy: absolute url(/...) in built CSS" >&2
  exit 1
fi
if [[ -n "$(find dist -path '*reference*' -print -quit)" ]]; then
  echo "deploy: reference material leaked into dist/" >&2
  exit 1
fi
touch dist/.nojekyll

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
git -C "$ROOT" fetch -q "$REMOTE" gh-pages 2>/dev/null || true

echo "==> published main@${SHORT} to gh-pages"
echo "Pages URL: $PAGES_URL"
