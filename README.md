# GlanceVNC website

A static website generated from shared templates with a dependency-free Python
build, following the same pattern as GlanceSSH:

```sh
python3 build.py
```

The deployable website is written to `dist/`. The build renders all pages from
the `PAGES` route table in `build.py`, copies public assets, and generates
`sitemap.xml` and `robots.txt` from those same routes. Existing `.html` and
trailing-slash URLs are preserved. No Python packages or Node installation are
required. The output directory is cleaned so removed routes do not linger.

Edit the site in these locations:

- `templates/base.html`: shared document head, analytics, scripts and page layout.
- `templates/header.html` and `templates/footer.html`: shared site navigation.
- `templates/pages/`: page-specific main content.
- `build.py`: routes, page titles, descriptions, active navigation and structured data.
- `styles.css`, `guides/guides.css`, and `assets/`: styling and public assets.

Add a page body under `templates/pages/` and register its route in `PAGES` to
generate the page and include it in the sitemap. Remove the route to remove it
from the output and sitemap. Templates and project files are not deployed.
Generated files are not committed; do not edit `dist/` directly.

Validate the built site without a preview server:

```sh
python3 check.py
```

This checks generated routes, local resources, anchors, image alt attributes,
headings, sitemap URLs and the robots sitemap declaration.

Preview the built website:

```sh
python3 -m http.server 4173 --directory dist
```

Deploy the built output to the existing GlanceVNC host:

```sh
rsync -az --delete dist/ root@209.97.177.186:/var/www/glancevnc.com/
```

The shared deployment documentation and live content verifier are in
`../glance-websites/`. Run `python3 verify.py` there after deploying; it compares
the deployed files against `dist/` and checks HTTPS and redirects for both sites.


## Search and AI discovery — 9 November 2026

The build registers every public route in `sitemap.xml`, gives pages canonical and social URLs, and generates `dist/llms.txt` from the rendered homepage, support/FAQ/privacy content and complete page descriptions. Edit the page copy and route definitions, then rebuild; never hand-edit the generated LLM reference. Content dates identify actual editorial revisions, not build times.

Guide content lives in `guide_content.py`; the guide index links to every article. Guides use genuine app screenshots with descriptive alt text, clear example captions, contents links and related reading. External setup references are linked inside the articles. These instructions were checked against product source and official documentation; they are not a claim that every remote operating-system/server combination was tested end to end.

Run `python3 build.py`, the existing `python3 check.py`, and `python3 check_discovery.py`. The latter checks canonical URLs, unique descriptions, social metadata, JSON-LD, visible article dates, sitemap coverage and exact regeneration of `llms.txt`. GlanceSSH's existing route checker needs the preview server running on port 4173.

GlanceSSH's App Store URL and monitored support contact remain pending; do not invent them or add unverified prices/reviews to structured data. Host-level redirects live in the shared `glance-websites/nginx/https/` configuration.
