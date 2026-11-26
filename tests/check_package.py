from pathlib import Path
from html.parser import HTMLParser
from urllib.parse import urlsplit, unquote
import json, zipfile, hashlib
ROOT=Path(__file__).resolve().parents[1]
class Links(HTMLParser):
    def __init__(self): super().__init__(); self.refs=[]; self.ids=set()
    def handle_starttag(self,tag,attrs):
        d=dict(attrs)
        if 'id' in d:
            assert d['id'] not in self.ids, ('duplicate ID',d['id'])
            self.ids.add(d['id'])
        for key in ('href','src'):
            if d.get(key): self.refs.append(d[key])
htmls={}
for p in ROOT.rglob('*.html'):
    h=Links();h.feed(p.read_text());htmls[p.resolve()]=h
count=0
for p,h in htmls.items():
    for link in h.refs:
        u=urlsplit(link)
        if u.scheme or u.netloc: continue
        target=(p.parent/unquote(u.path)).resolve() if u.path else p
        if target.is_dir(): target=target/'index.html'
        assert target.exists(),(p,link)
        if u.fragment and target in htmls: assert u.fragment in htmls[target].ids,(p,link)
        count+=1
manifest=json.loads((ROOT/'extension/manifest.json').read_text())
assert manifest['manifest_version']==3 and manifest['version']=='0.3.0'
assert not any(manifest.get(k) for k in ('permissions','host_permissions','content_scripts','background'))
expected={'manifest.json','popup.html','core.js','ui.js','style.css'} | set(manifest['icons'].values())
archive=ROOT/'downloads/Rubedo-Mini-v0.3.0-install.zip'
with zipfile.ZipFile(archive) as z:
    assert set(z.namelist())==expected and z.testzip() is None
    for name in expected: assert z.read(name)==(ROOT/'extension'/name).read_bytes()
assert (ROOT/'downloads/SHA256SUMS.txt').read_text().split()[0]==hashlib.sha256(archive.read_bytes()).hexdigest()
print(f'{len(htmls)} HTML pages; {count} local links; manifest and ZIP integrity OK')
