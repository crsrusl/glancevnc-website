# GlanceVNC website

A static website with a dependency-free Python build. Edit the root HTML pages,
`styles.css`, `assets/`, and `guides/`, then build:

```sh
python3 build.py
```

The deployable website is written to `dist/`. Each build starts with a clean
output directory, copies the public pages and assets, and generates `sitemap.xml`
from the resulting HTML pages. Root pages keep their `.html` URLs; directory
`index.html` pages use trailing-slash URLs. `robots.txt` is generated with the
canonical HTTPS sitemap location. No Python packages or Node installation are
required.

Add a root HTML page or a page under `guides/` and rebuild to include it in the
sitemap. Deleted source pages disappear from both the output and sitemap on the
next build. Generated files are not committed; do not edit `dist/` directly.

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
