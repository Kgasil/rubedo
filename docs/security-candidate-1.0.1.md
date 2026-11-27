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

## Stage 06 evidence
Commit 166763ff57b920f18d947fe365311cb01f10d1f4: both workflows [46067486777](https://github.com/Kgasil/rubedo/actions/runs/46067486777) and [46067491501](https://github.com/Kgasil/rubedo/actions/runs/46067491501) passed. Logs confirm 97 interface checks, 12 security boundary checks, blocked fetch on three web pages, text-only imported markup, unpacked Chromium extension registration and four tools/JSON export. Reproducible ZIP and installed ZIP SHA-256: a2fd6017a4f5a3813b924b0d249f91090f57857054ff565b80dc633d5eb95424. Branded Windows browser tests and antivirus not executed. [Final acceptance](homologation-1.0.1.md).

## Approval update — 2026-11-27
Em 27/11/2026, o idealizador confirmou aprovação dos três grupos de testes manuais no candidato 1.0.1 (Chrome/Edge no Windows, Microsoft Defender atualizado sem detecções e revisão visual/teclado/acessibilidade) e autorizou a publicação. Resultados relatados, não reexecutados independentemente; logs do Defender, versões de navegador e capturas não fornecidos. / On 27 Nov 2026, the maintainer reported passing all three manual acceptance groups on candidate 1.0.1 and authorized publication. No independent rerun, raw Defender logs, browser versions or screenshots supplied.
