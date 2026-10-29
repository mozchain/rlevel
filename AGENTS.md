# Rlevel Project Constitution & SDLC Guidelines

Welcome to **Rlevel Carpentry Solutions** (`rlevelcarpentrysolutions.com.au`).
All AI agents and developers contributing to this codebase MUST strictly adhere to this SDLC framework. **No vibe coding or direct unverified edits permitted.**

---

## 1. Core Principles

1. **The Human Owns the Gates; Agents Do the Work Between Them:**
   Agents propose specifications, write code, run checks, and trigger preview deployments. **Agents never self-approve gates or merge directly to `main` without human confirmation.**
2. **Spec Before Code:**
   No non-trivial page, section, or styling overhaul is written without a concise specification approved in chat (adhering to `docs/specs/TEMPLATE.md`).
3. **Continuous Green Invariant:**
   `npm run check` MUST pass with zero errors before any preview deployment or review request.
4. **Environment & Branch Isolation:**
   Work happens on feature/task branches (`feat/*`, `fix/*`). Preview builds are deployed via Cloudflare Pages preview aliases (`preview.rlevel.pages.dev`). Production (`main`) is only updated upon explicit approval.

---

## 2. The 3-Gate SDLC Pipeline

```
  [Stage 1: Proposal / Spec] ──── docs/specs/<feature>.md (copy, assets, SEO, layout)
       │
  ◆ GATE 1: SPEC SIGN-OFF ────── Product Owner approves specification in chat
       │
  [Stage 2: Implementation] ───── HTML/CSS edits on branch `feat/*`
       │
  [Stage 3: Automated Quality] ── Run `npm run check` (0 errors required)
       │
  [Stage 4: Preview Deploy] ───── Run `npm run deploy:preview`
       │
  ◆ GATE 2: VISUAL SIGN-OFF ──── Product Owner inspects `https://preview.rlevel.pages.dev`
       │
  ◆ GATE 3: PROD RELEASE ─────── Merge PR to `main` -> live on rlevelcarpentrysolutions.com.au
```

---

## 3. Mandatory Invariants

### Invariant 1: Asset Hygiene & Media Management
- All images, icons, and illustrations MUST reside in the [`assets/`](file:///home/mark/antigravity/Rlevel/assets) folder.
- **Zero loose media files in root.**
- File naming must be strict lowercase kebab-case (e.g., `commercial-door-install.jpg`, NOT `Rob Photo.jpeg` or `IMG_1234.PNG`).
- All `<img>` tags MUST have a descriptive, non-empty `alt` attribute.
- Image sizes should be compressed (< 500 KB) to protect Google PageSpeed and Core Web Vitals (LCP).

### Invariant 2: SEO & Sitemap Synchronization
Whenever a page is added, renamed, or modified:
1. Ensure `<title>` and `<meta name="description">` are populated with targeted, localized keywords.
2. Ensure `<meta name="viewport" content="width=device-width, initial-scale=1.0">` is present.
3. Add or update the canonical `<url>` entry in [`sitemap.xml`](file:///home/mark/antigravity/Rlevel/sitemap.xml) with the matching clean URL.
4. Verify [`robots.txt`](file:///home/mark/antigravity/Rlevel/robots.txt) allows crawling and references the sitemap.

### Invariant 3: Site-Wide Component Consistency
Because this is a static multi-page site without templating:
- Global Navigation Header, Mobile Menu, Call-to-Action (CTA) sections, and Footer MUST remain synchronized across all HTML pages.
- Business contact details (phone number, email address, service areas) must be identical across all pages.

---

## 4. Developer & Agent Commands

| Command | Action |
|---|---|
| `npm run dev` | Starts local development server on `http://localhost:3000` |
| `npm run check` | Executes `scripts/check-site.py` (link validation, SEO, sitemap sync, image audit) |
| `npm run deploy:preview` | Deploys current state to Cloudflare Pages `preview` branch (`https://preview.rlevel.pages.dev`) |
| `npm run deploy:prod` | Deploys to Cloudflare Pages `main` branch |
