#!/usr/bin/env python3
"""Validate generated routes, resources, anchors and sitemap without a server."""

from html.parser import HTMLParser
from urllib.parse import unquote, urlsplit
import xml.etree.ElementTree as ET

from build import DOMAIN, OUT, PAGES, SITEMAP_NS


class Page(HTMLParser):
    def __init__(self, path):
        super().__init__()
        self.path = path
        self.ids = set()
        self.references = []
        self.headings = 0
        self.feed(path.read_text())

    def handle_starttag(self, tag, attrs):
        attrs = dict(attrs)
        if "id" in attrs:
            self.ids.add(attrs["id"])
        if tag == "h1":
            self.headings += 1
        if tag == "img":
            assert "alt" in attrs, f"Missing image alt: {self.path}"
        for field in ("href", "src"):
            value = attrs.get(field, "")
            parsed = urlsplit(value)
            if value and not parsed.scheme and not parsed.netloc:
                self.references.append(parsed)


def check():
    pages = {path: Page(path) for path in OUT.rglob("*.html")}
    expected = {OUT / route.lstrip("/") / "index.html" if route.endswith("/")
                else OUT / route.lstrip("/") for route in PAGES}
    assert set(pages) == expected, "Generated pages differ from the route table; run build.py"
    for path, page in pages.items():
        assert page.headings == 1, f"Expected one H1: {path}"
        for link in page.references:
            if not link.path:
                target = path
            elif link.path.startswith("/"):
                target = OUT / unquote(link.path).lstrip("/")
            else:
                target = path.parent / unquote(link.path)
            target = target.resolve()
            assert target.is_relative_to(OUT), f"Resource outside site: {link.geturl()}"
            if target.is_dir():
                target /= "index.html"
            assert target.is_file(), f"Missing resource in {path}: {link.geturl()}"
            if link.fragment:
                assert target in pages and unquote(link.fragment) in pages[target].ids, (
                    f"Missing anchor in {path}: {link.geturl()}"
                )
        print("PASS", path.relative_to(OUT))
    sitemap = ET.parse(OUT / "sitemap.xml")
    urls = [node.text for node in sitemap.findall(f"{{{SITEMAP_NS}}}url/{{{SITEMAP_NS}}}loc")]
    assert len(urls) == len(PAGES) and set(urls) == {DOMAIN + route for route in PAGES}
    assert f"Sitemap: {DOMAIN}/sitemap.xml" in (OUT / "robots.txt").read_text()
    print("All generated pages, resources, anchors, image alt, headings and sitemap checks pass.")


if __name__ == "__main__":
    check()
