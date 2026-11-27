# Candidate 1.0.1 — security and release gates / Segurança e distribuição
Stage 05 baseline 65dcd784fa5ab5191e2a472d369d45e66c113ce0; public main f2193e4bed955bd1290f822c5538435c0b59cdb2 integrated in candidate only. No public release, merge or store submission.

## Review scope and measures
- Manifest V3: no permissions, host permissions, background or content scripts; explicit restrictive extension CSP. All runtime dependencies are repository-owned JS/CSS; Python, Node, Playwright and Chromium are build/test tools, not runtime packages. No package-manager manifest for runtime. No external scripts/fonts. The web portal/Research/Mini use local institutional assets, CSP connect-src none, no-referrer; outbound user-clicked ecosystem links still navigate externally. Hosting/browser/network services may collect their own metadata. No claim of anonymous browsing.
- JSON import: byte caps, normalized fields, bounded recursive snapshot tree, rejected prototype keys, invalid numeric values and nonfinite deltas. Protocol import guards against edits during asynchronous read. Imported content is displayed as text; provenance is unverified. No persistent research storage; export can contain sensitive input.
- Staging: empty output directory, deterministic ZIP, no overwrite, fixed historical hashes, source parity, CRC and PNG structure. SHA-256 is integrity evidence, not a signature or malware certification.
- CI checks real unpacked installation in a fresh persistent bundled Chromium profile, plus local HTTP privacy tests. Chromium is not branded Chrome/Edge on Windows. Test-only dependency Playwright is version-pinned; CI action tags and transitive dependencies still require review before a formal supply-chain attestation.

## Release gates — all mandatory
1. Exact candidate commit CI complete, no regressions; record candidate ZIP SHA-256 and build environment.
2. Windows clean Chrome and Edge profiles: verify installed extension/version, all four tools, language, clipboard/export, reload and removal. Capture evidence; no bypass of policies.
3. Scan exact ZIP and extracted files with updated Defender, log engine and signature version/date/hash/result; optional additional ClamAV scan if available. Stop on detections. No certification claimed.
4. Manual visual/accessibility review; document limitations and scientific scope. Global 9/10 requires documented rubric and approval, not mere CI pass.
5. Maintainer explicit approval; only then update public distribution/catalog and release notes with exact hash. Historical ZIPs preserved; free access.
