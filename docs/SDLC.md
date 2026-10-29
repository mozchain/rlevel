# Rlevel Carpentry Solutions — Software Development Lifecycle (SDLC)

*Owner: Mark Mosbauer (Product Owner)*  
*Target Domain: `rlevelcarpentrysolutions.com.au`*  
*Deployment Target: Cloudflare Pages*

---

## 1. Purpose & Philosophy

This document defines the structured development lifecycle for **Rlevel Carpentry Solutions**.
It transitions development away from unstructured "vibe coding" (direct edits to `main`, unverified asset paths, missing alt tags, SEO drift) into a governed, repeatable 3-Gate process where quality and brand integrity are continuously verified.

The core principle adapted from institutional projects is:
> **The Human Owns the Gates; Agents Do the Work Between Them.**
> Code is never deployed to production without an approved specification, automated validation, and human visual sign-off.

---

## 2. The 3-Gate Pipeline

| Stage / Gate | Type | Name | Actor | Description & Deliverables |
|---|---|---|---|---|
| **Stage 1** | Agent Stage | **Specification & Proposal** | Dev / Agent | Drafts concise feature spec using `docs/specs/TEMPLATE.md`. Outlines copy, visual assets, SEO meta, and acceptance criteria. |
| **◆ GATE 1** | **HUMAN GATE** | **Spec Approval** | **Product Owner** | Mark approves the proposal in chat. Implementation is locked until approved. |
| **Stage 2** | Agent Stage | **Implementation** | Dev / Agent | Implements HTML and CSS on a task branch (`feat/*`, `fix/*`). Zero direct commits to `main`. |
| **Stage 3** | Automated Stage | **Automated Quality Check** | System (`npm run check`) | Runs `scripts/check-site.py` validating 100% link resolution, image alt tags, sitemap alignment, and asset size hygiene. Must pass with 0 errors. |
| **Stage 4** | Automated Stage | **Preview Deployment** | System (`npm run deploy:preview`) | Deploys to Cloudflare Pages preview alias (`https://preview.rlevel.pages.dev`). |
| **◆ GATE 2** | **HUMAN GATE** | **Visual Sign-Off** | **Product Owner** | Mark tests preview URL on mobile and desktop viewports, confirming layout, typography, and UX. |
| **◆ GATE 3** | **HUMAN GATE** | **Production Release** | **Product Owner** | Branch is merged to `main`. Cloudflare Pages deploys to `rlevelcarpentrysolutions.com.au`. |

---

## 3. Invariants & Quality Standards

### 3.1 Link and Asset Integrity
- No relative link or resource (`href`, `src`) may be committed if it points to a non-existent file on disk.
- Clean URLs (`/about`, `/projects`) are used in navigation and sitemaps, which Cloudflare Pages maps automatically to `.html` files.

### 3.2 Media & Performance Standards
- Images must be processed before addition:
  - Formats: WebP or high-quality JPEG.
  - Sizing: Hero images < 300 KB; gallery photos < 200 KB; icons/logos in SVG.
  - Placement: Strictly in `assets/`.
  - Naming: Lowercase kebab-case (e.g., `commercial-fitout-melbourne.jpg`).

### 3.3 SEO & Discoverability
- Every public page must be registered in `sitemap.xml`.
- Page title format: `<Page Topic> | Rlevel Carpentry Solutions | Melbourne`
- Meta description: 140–160 characters describing the service and offering a call to action.

### 3.4 Brand Consistency
- Contact telephone, email, and operating areas must be uniform across the header, footer, and contact page.

---

## 4. Change History & Audit Trail
All feature specifications and architectural decisions are archived under `docs/specs/` and `docs/adr/` to maintain project memory across developer and agent sessions.
