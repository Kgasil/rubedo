"""Reproducible ZIP: exact files, stable order, fixed timestamps, SHA256."""
from pathlib import Path
from zipfile import ZipFile, ZipInfo, ZIP_DEFLATED
import hashlib, json
ROOT=Path(__file__).resolve().parents[1]
version=json.loads((ROOT/'extension/manifest.json').read_text())['version']
archive=ROOT/'downloads'/f'Rubedo-Mini-v{version}-install.zip'
archive.parent.mkdir(exist_ok=True)
files=sorted(['core.js','manifest.json','popup.html','style.css','ui.js']+list(json.loads((ROOT/'extension/manifest.json').read_text())['icons'].values()))
with ZipFile(archive,'w',compression=ZIP_DEFLATED,compresslevel=9) as z:
    for name in files:
        info=ZipInfo(name,date_time=(2026,1,1,0,0,0));info.compress_type=ZIP_DEFLATED;info.external_attr=0o100644<<16
        z.writestr(info,(ROOT/'extension'/name).read_bytes(),compress_type=ZIP_DEFLATED,compresslevel=9)
(ROOT/'downloads/SHA256SUMS.txt').write_text(f'{hashlib.sha256(archive.read_bytes()).hexdigest()}  {archive.name}\n')
print(archive.name)
