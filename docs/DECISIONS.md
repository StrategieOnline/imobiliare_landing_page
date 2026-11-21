# Decisions & requests (append-only)

- LEAD: Brand is ORIZONT (fictional), Romanian copy, Bucharest north. Reference site name/copy/imagery are not reused.
- LEAD: Repo must be public: the strategieonline org is on GitHub Free, where Pages needs a public repo.
- RELEASE: repo strategieonline/imobiliare_landing_page created public; Pages serves branch gh-pages (path /), published by tools/deploy.sh as a single orphan commit (force-push, no history). Teams never commit; RELEASE integrates with per-team commits. assets-src/ added to .gitignore.
