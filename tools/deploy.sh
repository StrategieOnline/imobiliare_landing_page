#!/usr/bin/env bash
# Build the site and publish dist/ to the gh-pages branch of origin.
# Idempotent: every run force-pushes one fresh orphan commit (gh-pages keeps no history).
# Usage: bash tools/deploy.sh   (or: npm run deploy)
set -euo pipefail

ROOT="$(cd "$(dirname "${BASH_SOURCE[0]}")/.." && pwd)"
cd "$ROOT"

PAGES_URL="https://strategieonline.github.io/imobiliare_landing_page/"
REMOTE="${DEPLOY_REMOTE:-origin}"

git remote get-url "$REMOTE" >/dev/null 2>&1 || { echo "deploy: no git remote '$REMOTE'" >&2; exit 1; }

echo "==> install"
if [[ -f package-lock.json ]]; then npm ci --no-audit --no-fund; else npm i --no-audit --no-fund; fi

echo "==> build"
rm -rf dist
npx vite build

echo "==> verify dist"
[[ -f dist/index.html ]] || { echo "deploy: dist/index.html missing" >&2; exit 1; }
# Sub-path safety: the site lives under /imobiliare_landing_page/, so root-absolute
# asset URLs (src="/x", href="/x") would 404. Protocol-relative "//" URLs are allowed.
if grep -nE '(src|href)="/[^/]' dist/index.html; then
  echo "deploy: absolute asset URLs in dist/index.html (must be relative, base './')" >&2
  exit 1
fi
if grep -rnE --include='*.css' 'url\(["'"'"']?/[^/]' dist; then
  echo "deploy: absolute url(/...) in built CSS" >&2
  exit 1
fi
if [[ -d reference ]] && [[ -n "$(find dist -path '*reference*' -print -quit)" ]]; then
  echo "deploy: reference material leaked into dist/" >&2
  exit 1
fi
touch dist/.nojekyll

echo "==> publish to gh-pages"
SRC_SHA="$(git rev-parse --short HEAD 2>/dev/null || echo uncommitted)"
TMP="$(mktemp -d)"
trap 'rm -rf "$TMP"' EXIT
cp -R dist/. "$TMP/"
(
  cd "$TMP"
  git init -q
  git checkout -q --orphan gh-pages
  git add -A
  # Reuse the repo's configured identity; never change git config.
  git -c user.name="$(git -C "$ROOT" config user.name)" \
      -c user.email="$(git -C "$ROOT" config user.email)" \
      commit -q -m "deploy: build of main@${SRC_SHA}"
  git push -q -f "$(git -C "$ROOT" remote get-url "$REMOTE")" HEAD:gh-pages
)

echo "==> published main@${SRC_SHA} to gh-pages"
echo "Pages URL: $PAGES_URL"
