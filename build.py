#!/usr/bin/env python3
"""Build the static website and discover its pages for sitemap.xml."""

from pathlib import Path
import shutil
import xml.etree.ElementTree as ET

ROOT = Path(__file__).resolve().parent
OUT = ROOT / "dist"
DOMAIN = "https://glancevnc.com"
SITEMAP_NS = "http://www.sitemaps.org/schemas/sitemap/0.9"


def copy_public(source, destination):
    """Copy public files, omitting hidden files such as .DS_Store."""
    if source.name.startswith("."):
        return
    if source.is_dir():
        destination.mkdir(parents=True, exist_ok=True)
        for child in sorted(source.iterdir()):
            copy_public(child, destination / child.name)
    else:
        destination.parent.mkdir(parents=True, exist_ok=True)
        shutil.copy2(source, destination)


def build():
    # dist is generated output. Cleaning it removes pages/assets deleted in source.
    if OUT.exists():
        shutil.rmtree(OUT)
    OUT.mkdir()

    for page in sorted(ROOT.glob("*.html")):
        copy_public(page, OUT / page.name)
    for name in ("styles.css", "llms.txt", "assets", "guides"):
        copy_public(ROOT / name, OUT / name)

    pages = sorted(OUT.rglob("*.html"))
    ET.register_namespace("", SITEMAP_NS)
    urlset = ET.Element(f"{{{SITEMAP_NS}}}urlset")
    for page in pages:
        relative = page.relative_to(OUT).as_posix()
        route = relative[:-len("index.html")] if page.name == "index.html" else relative
        entry = ET.SubElement(urlset, f"{{{SITEMAP_NS}}}url")
        ET.SubElement(entry, f"{{{SITEMAP_NS}}}loc").text = f"{DOMAIN}/{route}"
    ET.indent(urlset, space="  ")
    sitemap = ET.tostring(urlset, encoding="utf-8", xml_declaration=True)
    (OUT / "sitemap.xml").write_bytes(sitemap + b"\n")
    (OUT / "robots.txt").write_text(
        f"User-agent: *\nAllow: /\n\nSitemap: {DOMAIN}/sitemap.xml\n"
    )
    print(f"Built {len(pages)} pages, assets, sitemap.xml and robots.txt in {OUT}")


if __name__ == "__main__":
    build()
