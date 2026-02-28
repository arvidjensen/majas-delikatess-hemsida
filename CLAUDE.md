# CLAUDE.md

This file provides guidance to Claude Code (claude.ai/code) when working with code in this repository.

## Workflow Rules

**Always** use the `frontend-design` skill (`SKILL.md`) when doing any frontend work — adding components, pages, sections, styling, layout changes, or any other visual/UI modifications. Read and follow the guidelines in `SKILL.md` before writing frontend code.

## Project Overview

Single-page website for **Maja's Delikatess**, a retro-inspired delicatessen shop in Fritsla, Sweden. The site is entirely in Swedish.

## Commands

- `npm run dev` — Start dev server (Astro)
- `npm run build` — Production build (outputs to `dist/`)
- `npm run preview` — Preview production build locally

No test runner or linter is configured.

## Tech Stack

- **Astro 5** with React integration (`@astrojs/react`)
- **Tailwind CSS v4** via Vite plugin (`@tailwindcss/vite`), imported in `src/styles/global.css`
- **TypeScript** with strict config extending `astro/tsconfigs/strict`
- JSX configured for React (`jsxImportSource: "react"`)

## Architecture

This is a single-page site with one Astro page and one React island:

- `src/pages/index.astro` — The entire site: nav, hero, sortiment, om oss, gallery, contact, footer. Contains all CSS custom properties, animations, and the "apothecary" design system inline in a `<style>` block.
- `src/components/FacebookFeed.tsx` — React component hydrated with `client:load`. Displays Facebook posts with two modes: static posts (passed as props) or dynamic fetch via Facebook Graph API. Falls back to static posts on API failure.
- `src/styles/global.css` — Minimal; just imports Tailwind (`@import "tailwindcss"`).

## Design System

The site uses an "apothecary/vintage" aesthetic defined via CSS custom properties in `index.astro`:

- **Colors**: `--walnut`, `--cream`, `--brass`, `--sage`, `--burgundy`, `--orange` families
- **Fonts**: `--font-display` (Playfair Display SC), `--font-body` (EB Garamond), `--font-script` (Pinyon Script), `--font-logo` (Coustard) — loaded from Google Fonts
- **Reusable CSS classes**: `.paper-texture`, `.paper-dark`, `.damask-overlay`, `.ornate-frame`, `.label-frame`, `.display-case`, `.gallery-apothecary`, `.wax-seal`, `.brass-line`, `.ornamental-divider`
- **Animation classes**: `.anim-fade-up`, `.anim-slide-right`, `.anim-scale-in`, `.anim-drawer`, `.anim-seal` with `.delay-1` through `.delay-6`
- **Button variants**: `.btn-primary` (orange), `.btn-brass` (outlined), `.btn-walnut` (dark filled)

Tailwind utility classes are used alongside these custom classes throughout the markup.

## Environment Variables

- `PUBLIC_FB_ACCESS_TOKEN` — Facebook Graph API token for the FacebookFeed component. When absent, the component uses static posts passed as props.

## Static Assets

Images are in `public/images/` and referenced with absolute paths (e.g., `/images/logga.jpg`).
