# Documentation Structure Guide

This page describes how to organize files under `docs/` and how to add/restructure pages.

## Principles

- Design `nav` based on the participant reading flow
- Avoid changing URLs; if necessary, provide redirects
- Use `mkdocs-static-i18n` suffix files (`.ja.md` / `.en.md`)
- Put unpublished drafts under `drafts/` (not under `docs/`)

## Adding a new page

1. Create `docs/<path>.ja.md` and `docs/<path>.en.md`
2. Add `<path>.md` (without suffix) to `nav:` in `mkdocs.yaml`
3. Run `mkdocs build` and fix warnings/links
