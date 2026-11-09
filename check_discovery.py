"""Check discovery metadata and regenerate the expected LLM reference in isolation."""
from html.parser import HTMLParser
from pathlib import Path
from urllib.parse import urlsplit
import json
import shutil
import tempfile
import xml.etree.ElementTree as ET
from discovery import write_llms

class Metadata(HTMLParser):
    def __init__(self, text):
        super().__init__()
        self.canonicals=[]; self.meta={}; self.schemas=[]; self.in_schema=False
        self.schema_text=[]; self.images=[]; self.h1=0
        self.feed(text)
    def handle_starttag(self,tag,attrs):
        a=dict(attrs)
        if tag=='h1': self.h1+=1
        if tag=='meta': self.meta[a.get('name',a.get('property',''))]=a.get('content','')
        if tag=='link' and a.get('rel')=='canonical': self.canonicals.append(a['href'])
        if tag=='script' and a.get('type')=='application/ld+json': self.in_schema=True;self.schema_text=[]
        if tag=='img': self.images.append(a)
    def handle_data(self,data):
        if self.in_schema:self.schema_text.append(data)
    def handle_endtag(self,tag):
        if tag=='script' and self.in_schema:
            value=json.loads(''.join(self.schema_text))
            self.schemas.extend(value if isinstance(value,list) else [value]);self.in_schema=False

def check(root,domain,name):
    out=Path(root)/'dist'
    ns={'s':'http://www.sitemaps.org/schemas/sitemap/0.9'}
    urls=[x.text for x in ET.parse(out/'sitemap.xml').findall('s:url/s:loc',ns)]
    assert len(urls)==len(set(urls)), 'Duplicate sitemap URLs'
    descriptions=[]; routes=[]; paths=[]
    for url in urls:
        assert url.startswith(domain+'/'), ('Noncanonical sitemap URL',url)
        route=url[len(domain):];routes.append(route)
        path=out/route.lstrip('/')
        if route.endswith('/'): path/='index.html'
        paths.append(path)
        text=path.read_text();meta=Metadata(text)
        assert meta.canonicals==[url], ('Canonical mismatch',url)
        assert meta.meta.get('og:url')==url, ('Social URL mismatch',url)
        assert meta.meta.get('og:image','').startswith(domain+'/'), ('Missing social image',url)
        assert meta.meta.get('description'), ('Missing description',url)
        assert meta.h1==1, ('H1 count',url)
        assert 'noindex' not in meta.meta.get('robots',''), ('Unexpected noindex',url)
        descriptions.append(meta.meta['description'])
        assert meta.schemas, ('Missing structured data',url)
        for schema in meta.schemas:
            assert schema.get('@context')=='https://schema.org', ('Schema context',url)
            if schema.get('@type')=='TechArticle':
                assert 'datetime="'+schema['dateModified']+'"' in text, ('Visible/schema date mismatch',url)
        assert all('alt' in image for image in meta.images), ('Missing alt',url)
    assert set(out.rglob('*.html'))==set(paths), 'Stale HTML outside the sitemap'
    assert len(descriptions)==len(set(descriptions)), 'Repeated meta descriptions'
    with tempfile.TemporaryDirectory() as temp:
        mirror=Path(temp)
        for path in paths:
            target=mirror/path.relative_to(out);target.parent.mkdir(parents=True,exist_ok=True);shutil.copyfile(path,target)
        write_llms(mirror,domain,routes,name)
        assert (mirror/'llms.txt').read_bytes()==(out/'llms.txt').read_bytes(), 'llms.txt is stale; rebuild'
    llms=(out/'llms.txt').read_text()
    assert all(url in llms for url in urls), 'Missing llms page references'
    assert f'Sitemap: {domain}/sitemap.xml' in (out/'robots.txt').read_text()
    print(f'PASS {name}: {len(urls)} canonical pages, unique descriptions, social metadata, structured data, article dates and generated llms.txt')

if __name__=='__main__':
    root=Path(__file__).resolve().parent
    name='GlanceVNC' if 'GlanceVNC' in str(root) else 'GlanceSSH'
    check(root, 'https://glancevnc.com' if name=='GlanceVNC' else 'https://glancessh.com', name)
