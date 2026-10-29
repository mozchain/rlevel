# Feature Specification: Asset Localization & Component Synchronization

- **Author:** Antigravity / Mark Mosbauer
- **Date:** 2026-10-29
- **Gate 1 Status:** Approved
- **Branch:** `feat/asset-localization`

---

## 1. Overview & Purpose
Eliminate reliance on third-party Google Stitch/AIDA CDN URLs for primary brand assets, clean up obsolete placeholder CSS, and enforce automated cross-page consistency for global header and footer components.

---

## 2. Changes Summary
1. **Localize Logos:**
   - Download header and footer brand marks to `assets/logo.png` and `assets/logo-footer.png`.
   - Update `<img>` tags across all 6 HTML pages to point to local assets.
2. **Component Synchronization Invariant:**
   - Extend `scripts/check-site.py` to extract `<header>` and `<footer>` components across all HTML files and assert structure and contact consistency.
3. **Dead Code Cleanup:**
   - Replace obsolete placeholder rules in `css/style.css` with clean base styling or keep as minimal global overrides.

---

## 3. Assets & Media
- `assets/logo.png` (512x128 PNG, ~34 KB, Header brand mark)
- `assets/logo-footer.png` (512x128 PNG, ~34 KB, Footer brand mark)

---

## 4. Acceptance Criteria (AC)
- [x] **AC-01:** Zero references to `lh3.googleusercontent.com` across all HTML pages.
- [x] **AC-02:** All 6 HTML pages reference `assets/logo.png` in the header and `assets/logo-footer.png` in the footer.
- [x] **AC-03:** `scripts/check-site.py` verifies component integrity and passes with 0 errors.
- [x] **AC-04:** Preview deployment verified on `preview.rlevel.pages.dev`.
