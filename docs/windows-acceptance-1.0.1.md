# Windows acceptance — candidate 1.0.1 / Aceitação Windows
**Pending.** This is a procedure, not an executed test or malware approval.
 
## 1. Rebuild privately from exact source
Prerequisites: Git, Python 3, clean authorized Windows test environment; do not change protection settings. In PowerShell:
 
```powershell
git clone https://github.com/Kgasil/rubedo.git rubedo-acceptance
Set-Location rubedo-acceptance
git checkout --detach 166763ff57b920f18d947fe365311cb01f10d1f4
$stage = Join-Path $env:TEMP ("rubedo-candidate-" + [guid]::NewGuid())
python scripts/package_extension.py --output-dir $stage
$zip = Join-Path $stage "Rubedo-Mini-v1.0.1-install.zip"
$expected = "a2fd6017a4f5a3813b924b0d249f91090f57857054ff565b80dc633d5eb95424"
$actual = (Get-FileHash -Algorithm SHA256 -LiteralPath $zip).Hash.ToLowerInvariant()
if ($actual -ne $expected) { throw "Unexpected ZIP hash; STOP" }
$actual
```
 
Stop if any command fails. Do not download the public 1.0.0 ZIP as a substitute.
 
## 2. Microsoft Defender
In an authorized Windows environment with Defender active, update security intelligence through Windows Security. Record the current engine and security-intelligence versions, date, and SHA-256. Scan the ZIP via Windows Security custom scan or Explorer's Defender scan. Only after a clean result, extract into an isolated folder and scan all extracted files. Record scan scope and result; investigate every detection; do not restore quarantined files or disable protections. If another antivirus controls the machine, record that limitation; Defender gate remains pending until a valid Defender test. Optional updated ClamAV scan is supplementary, not a replacement.
 
## 3. Chrome and Edge
After clean scans, create a separate fresh profile in each branded browser (Windows). Open chrome://extensions/ or edge://extensions/. If organizational policy permits developer mode, choose Load unpacked and select the extracted directory containing manifest.json. Verify name, version 1.0.1, no requested host permissions, all four tools, PT/EN, clipboard and JSON export; reload, retest, remove. Record browser and Windows versions, screenshots and outcomes. Stop on security warnings.
 
## 4. Manual visual/accessibility review
Review Research, Mini and installed popup at desktop and narrow widths; keyboard-only focus order, accessible names, screen-reader output (e.g. Narrator or NVDA), legibility, charts and scientific text. Log defects and severity. Do not claim WCAG conformance based on this limited review.
 
## 5. Evidence template (fill after actual execution)
- Runtime commit / ZIP SHA-256:
- Windows build / Chrome / Edge versions:
- Defender engine / definitions version / update date:
- Scan time, exact paths, results (ZIP and extracted):
- Chrome checks and results:
- Edge checks and results:
- Visual, keyboard, screen-reader checks and results:
- Remaining defects / reviewer / date:
 
No public release or maintainer approval implied by filling this template.
