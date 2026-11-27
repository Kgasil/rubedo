"""Verify original Rubedo Mini packages, without executing their contents."""
from pathlib import Path
from hashlib import sha256
from zipfile import ZipFile
import json
import struct
import zlib

ROOT = Path(__file__).resolve().parents[1]
HASHES = {
    "1.0.0": "1799dc6ccadd786eb960f38c4f7d67cf241e9630942a9e69daebfe96fcfe6ab2",
    "0.3.0": "ee1bcf4a225783dd60a332ba1720d14127c2c9b88f213ee8e29f4872bd12f1c8",
}
ICONS = {str(n): f"icons/icon-{n}.png" for n in (16,32,48,128)}
EXPECTED = {"core.js","ui.js","manifest.json","popup.html","style.css",*ICONS.values()}
def require(ok, message):
    if not ok:
        raise SystemExit(message)
def png_check(data, n):
    require(data[:8] == b"\x89PNG\r\n\x1a\n", "Invalid PNG signature")
    p = 8
    first = True
    while p+12 <= len(data):
        length = struct.unpack_from(">I", data, p)[0]
        end = p+12+length
        require(end <= len(data), "PNG truncated")
        kind = data[p+4:p+8]
        payload = data[p+8:p+8+length]
        require(zlib.crc32(kind+payload) == struct.unpack_from(">I", data, end-4)[0], "PNG CRC mismatch")
        if first:
            require(kind == b"IHDR" and length == 13 and struct.unpack_from(">II",payload) == (n,n), "PNG dimensions invalid")
            first = False
        if kind == b"IEND":
            require(length == 0 and end == len(data), "Unexpected data after PNG")
            return
        p = end
    raise SystemExit("PNG missing IEND")
def main():
    for version, digest in HASHES.items():
        path = ROOT / "downloads" / f"Rubedo-Mini-v{version}-install.zip"
        require(sha256(path.read_bytes()).hexdigest() == digest, f"{version}: unexpected SHA-256")
        with ZipFile(path) as z:
            require(len(z.infolist()) == len(EXPECTED) and set(z.namelist()) == EXPECTED, "Unexpected ZIP entries")
            require(all(not i.is_dir() and not i.flag_bits & 1 for i in z.infolist()), "Unexpected encrypted entry or directory")
            require(z.testzip() is None, "ZIP CRC failed")
            m = json.loads(z.read("manifest.json"))
            require(m["manifest_version"] == 3 and m["version"] == version, "Manifest version mismatch")
            require(set(m) == {"manifest_version","name","version","description","action","icons"}, "Unexpected manifest capability")
            require(m["action"]["default_popup"] == "popup.html" and m["action"]["default_icon"] == ICONS and m["icons"] == ICONS, "Unexpected entry points")
            for n, name in ICONS.items():
                png_check(z.read(name), int(n))
            if version == json.loads((ROOT / "extension" / "manifest.json").read_text())["version"]:
                for name in EXPECTED:
                    require(z.read(name) == (ROOT / "extension" / name).read_bytes(), f"Source mismatch: {name}")
            print(f"{version}: SHA-256, 9 entries, CRC, manifest, PNG structure PASS" + (", source parity PASS" if version == json.loads((ROOT / "extension" / "manifest.json").read_text())["version"] else " (historical package; no comparison to current source)"))
    print("Integrity only; not an antivirus scan or installation approval.")
if __name__ == "__main__":
    main()
