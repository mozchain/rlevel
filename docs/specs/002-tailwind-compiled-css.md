# Feature Specification: Compiled Static Tailwind CSS

- **Author:** Antigravity / Mark Mosbauer
- **Date:** 2026-10-29
- **Gate 1 Status:** Approved
- **Branch:** `feat/tailwind-compiled-css`

---

## 1. Overview & Purpose
Replace the development-only Tailwind Play CDN (`https://cdn.tailwindcss.com`) and duplicated 160-line inline JavaScript configuration blocks across all 6 HTML pages with a compiled, minified static stylesheet (`css/style.css`).

This eliminates client-side CSS compilation, prevents Cumulative Layout Shift (CLS) / Flash of Unstyled Content (FOUC), and optimizes Core Web Vitals and PageSpeed for mobile visitors.

---

## 2. Technical Design & Architecture
1. **Shared Configuration:**
   Create [`tailwind.config.js`](file:///home/mark/antigravity/Rlevel/tailwind.config.js) in the project root containing all custom color tokens, font families, typography presets, spacing units, and radius definitions exported from Google Stitch.
2. **Input CSS:**
   Create [`css/input.css`](file:///home/mark/antigravity/Rlevel/css/input.css) with `@tailwind base; @tailwind components; @tailwind utilities;` and global scroll/reset rules.
3. **Compilation Pipeline:**
   Use Tailwind CLI to scan all `*.html` files and compile to [`css/style.css`](file:///home/mark/antigravity/Rlevel/css/style.css).
4. **HTML Simplification:**
   In all 6 HTML files:
   - Remove `<script src="https://cdn.tailwindcss.com"></script>`
   - Remove `<script id="tailwind-config">...</script>`
   - Link compiled static CSS: `<link rel="stylesheet" href="css/style.css">`
5. **Tooling & Checks:**
   - Add `"build:css"` command in `package.json`.
   - Update `npm run check` in `scripts/check-site.py` to ensure zero references to `cdn.tailwindcss.com` remain and `css/style.css` is verified.

---

## 3. Acceptance Criteria (AC)
- [ ] **AC-01:** `tailwind.config.js` and `css/input.css` created with 100% parity of existing tokens.
- [ ] **AC-02:** `npm run build:css` compiles a minified `css/style.css`.
- [ ] **AC-03:** All 6 HTML pages reference `css/style.css` and have zero references to `cdn.tailwindcss.com`.
- [ ] **AC-04:** `npm run check` passes with 0 errors and 0 warnings.
- [ ] **AC-05:** Visual layout and responsive styling on `preview.rlevel.pages.dev` matches original design 1:1.
