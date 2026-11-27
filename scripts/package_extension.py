"""Reproducible ZIP: exact files, stable order, fixed timestamps, SHA256."""
from pathlib import Path
from zipfile import ZipFile, ZipInfo, ZIP_STORED
import argparse, hashlib, json
ROOT=Path(__file__).resolve().parents[1]
version=json.loads((ROOT/'extension/manifest.json').read_text())['version']
parser=argparse.ArgumentParser()
parser.add_argument('--output-dir', type=Path, required=True, help='Staging directory outside the public downloads folder')
args=parser.parse_args()
output=args.output_dir.resolve()
if output == (ROOT/'downloads').resolve() or (ROOT/'downloads').resolve() in output.parents:
    parser.error('Public downloads are immutable; stage the candidate elsewhere.')
archive=output/f'Rubedo-Mini-v{version}-install.zip'
archive.parent.mkdir(exist_ok=True)
files=sorted(['core.js','manifest.json','popup.html','style.css','ui.js']+list(json.loads((ROOT/'extension/manifest.json').read_text())['icons'].values()))
with ZipFile(archive,'w',compression=ZIP_STORED) as z:
    for name in files:
        info=ZipInfo(name,date_time=(2026,1,1,0,0,0));info.compress_type=ZIP_STORED;info.external_attr=0o100644<<16
        z.writestr(info,(ROOT/'extension'/name).read_bytes(),compress_type=ZIP_STORED)
(output/'SHA256SUMS.txt').write_text(f'{hashlib.sha256(archive.read_bytes()).hexdigest()}  {archive.name}\n')
print(archive.name)
