"""Generate the LLM reference from the HTML shipped by this build."""
from html.parser import HTMLParser
import re

class Reference(HTMLParser):
    def __init__(self, source):
        super().__init__(convert_charrefs=True)
        self.in_main = False
        self.skip = 0
        self.parts = []
        self.description = ""
        self.store_links = set()
        self.title = ""
        self.in_title = False
        self.feed(source)
    def handle_starttag(self, tag, attrs):
        attrs = dict(attrs)
        if tag == "a" and attrs.get("href", "").startswith("https://apps.apple.com/"):
            self.store_links.add(attrs["href"])
        if tag == "meta" and attrs.get("name") == "description":
            self.description = attrs.get("content", "")
        if tag == "title": self.in_title = True
        if tag == "main": self.in_main = True
        if self.in_main and tag in ("nav", "script", "style", "figure", "aside"):
            self.skip += 1
        if tag in ("p", "li", "h1", "h2", "h3", "tr", "summary"):
            self.parts.append("\n")
    def handle_endtag(self, tag):
        if self.in_main and tag in ("nav", "script", "style", "figure", "aside"):
            self.skip = max(0, self.skip - 1)
        if tag == "title": self.in_title = False
        if tag == "main": self.in_main = False
        if tag in ("p", "li", "h1", "h2", "h3", "tr", "summary"):
            self.parts.append("\n")
    def handle_data(self, data):
        if self.in_title: self.title += data
        if self.in_main and not self.skip: self.parts.append(data + " ")
    @property
    def text(self):
        return "\n\n".join(re.sub(r"\s+", " ", line).strip() for line in "".join(self.parts).splitlines() if line.strip())

def write_llms(out, domain, routes, name):
    pages = {}
    for route in routes:
        path = out / route.lstrip("/")
        if route.endswith("/"): path /= "index.html"
        pages[route] = Reference(path.read_text())
    lines = ["# " + name, "", "> " + pages["/"].description, "",
             "Generated from the published page content and route table on every build. "
             "Follow the linked pages for complete instructions and their content dates. "
             "The App Store, when linked, is authoritative for release availability and regional pricing.", "",
             "## Official pages", ""]
    for route, page in pages.items():
        lines.append(f"- [{page.title}]({domain}{route}): {page.description}")
    for link in sorted(pages["/"].store_links):
        lines.append(f"- [Official App Store listing]({link})")
    lines += ["", f"- [Sitemap]({domain}/sitemap.xml)", "",
              "## Product facts from the homepage", "", pages["/"].text]
    for route in ("/faq/", "/support/", "/support.html", "/privacy/", "/privacy.html"):
        if route in pages:
            lines += ["", "## " + pages[route].title, "", pages[route].text]
    (out / "llms.txt").write_text("\n".join(lines) + "\n")
