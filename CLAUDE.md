# CLAUDE.md

This file provides guidance to Claude Code (claude.ai/code) when working with code in this repository.

## What This Is

A personal academic website for Ramchandran Muthukumar (PhD student at Johns Hopkins) built with **Hugo** and the **Wowchemy Academic theme**, deployed to GitHub Pages.

## Local GUI Editor

The easiest way to edit the site content is via the local GUI:

```bash
./start_gui.sh   # then open http://localhost:5001
```

This provides forms for editing the profile, publications, news, and CV, plus preview and one-click publish. No code editing needed.

The GUI lives in `gui/` (Flask + vanilla JS). Requires Python 3 with `flask` and `python-frontmatter`.

## Build Commands

```bash
# Local development server
hugo server

# Production build (matches GitHub Actions)
hugo --gc --minify --baseURL "https://ramcha24.github.io/"
```

Hugo version in use: **0.115.4** (GitHub Actions). No Makefile or npm scripts.

## Architecture

### Configuration
All site config lives in `config/_default/`:
- `config.yaml` — Hugo core settings, base URL, module imports
- `params.yaml` — Theme, font, features (math, syntax highlighting), SEO
- `menus.yaml` — Navigation bar items

The site uses **Hugo modules** (not git submodules) for the Wowchemy theme — dependencies are in `go.mod`.

### Content Model

**Homepage widgets** (`content/home/`): Each `.md` file is a widget with `widget:` frontmatter. Toggle with `active: true/false`. Order controlled by `weight:`.

**Author profile** (`content/authors/admin/_index.md`): The main "about" section — name, bio, education, social links, interests. This is what drives the homepage `about` widget.

**Publications** (`content/publication/<folder>/index.md`): Each publication is its own directory. Include:
- `index.md` with frontmatter (title, date, authors, abstract, publication type, tags, URLs)
- `cite.bib` for BibTeX citation
- `featured.png` if it should appear in the featured publications widget

**News** (`content/post/` or widget `content/home/recent_news.md`): Short news items shown on homepage.

### Deployment

GitHub Actions (`.github/workflows/hugo.yaml`) builds and deploys to GitHub Pages on every push to `master`. No manual deploy step needed.

## Common Update Tasks

**Add a publication:** Create `content/publication/<name>/` with `index.md` and `cite.bib`. Set `featured: true` to show in the featured widget.

**Update profile:** Edit `content/authors/admin/_index.md`.

**Update CV:** Replace `static/uploads/resume.pdf`.

**Add/reorder nav items:** Edit `config/_default/menus.yaml`.

**Change homepage sections:** Edit widget files in `content/home/` — toggle `active` or adjust `weight` for ordering.
