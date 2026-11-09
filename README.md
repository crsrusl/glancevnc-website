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
