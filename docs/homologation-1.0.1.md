# Rubedo 1.0.1 — final acceptance / Homologação final
**APPROVED BY MAINTAINER / APROVADA PELO IDEALIZADOR — 10/10 internal acceptance (7/10 logged/source evidence + 3/10 maintainer report).** Publication authorized; no store submission.
 
Runtime candidate: `166763ff57b920f18d947fe365311cb01f10d1f4`. Stage 06 [CI 46067486777](https://github.com/Kgasil/rubedo/actions/runs/46067486777) and [46067491501](https://github.com/Kgasil/rubedo/actions/runs/46067491501) both successful. Evidence tied to that runtime commit; this final documentation-only revision must pass its own CI. SHA-256 of reproducible and installed candidate ZIP: `a2fd6017a4f5a3813b924b0d249f91090f57857054ff565b80dc633d5eb95424`.
 
## Objective rubric / Matriz objetiva
Weights chosen for this acceptance review; not external certification. Binary points: pass receives weight, pending/fail receives zero. No rounding, no partial credit. All gates mandatory even if numerical minimum reached. No industrial validation or peer review claimed.
 
| Criterion | Weight | Evidence |
|---|---:|---|
| Scientific precision / Precisão científica | 2 | PASS — 257 independent oracle comparisons, 19 boundary groups, 84 existing rules and 5 reference cases pass |
| Reproducibility and Studio / Reprodutibilidade e Studio | 1 | PASS — 8 Studio checks, 8 transfers and 10 provenance/guard checks; snapshots and seeded cases |
| Automated usability and accessibility / Usabilidade e acessibilidade automatizadas | 1 | PASS — 97 browser checks, no page errors; selected contrast ≥4.5:1 text and ≥3:1 controls, keyboard, 320px and reduced motion |
| Privacy and security controls / Privacidade e controles | 1 | PASS — 12 boundary checks; local subresources, blocked fetch and text-only import; no declared extension permissions |
| Package integrity / Integridade | 1 | PASS — two reproducible builds, source parity, CRC, fixed historical hashes and same installed ZIP hash |
| Isolated Chromium install / Instalação Chromium | 0.5 | PASS — actual unpacked extension registered, four tools and JSON export |
| Identity and free distribution / Identidade e gratuidade | 0.5 | PASS — official symbol and icon assets and historical downloads unchanged in diff; dark wine UI, no payment/account requirement |
| Windows Chrome and Edge / Chrome e Edge no Windows | 1 | PASS (maintainer report) — Chrome/Edge on Windows reported passed for the 1.0.1 candidate; individual profile, clipboard/export, reload and uninstall observations not supplied |
| Updated malware scan / Antivírus atualizado | 1 | PASS (maintainer report) — updated Defender reported no detections for the candidate; raw logs, engine, definition version, timestamp and per-target results not supplied |
| Manual visual and accessibility review / Revisão visual e acessibilidade manual | 1 | PASS (maintainer report) — visual/keyboard/accessibility review reported passed; individual viewport and screen-reader records not supplied |
 
Total internal acceptance: 10.0/10; 7.0 points backed by CI/source review, 3.0 points by maintainer report. [Machine-readable matrix](homologation-1.0.1.json). Publication authorized. Any runtime modification invalidates affected evidence; rebuild, compare hash and repeat required tests. No unresolved critical/high regression permitted.
 
## Manual evidence checklist / Checklist manual
Use the exact tested candidate in a clean, authorized environment; never bypass Defender, SmartScreen, Safe Browsing or administrative policies. See [Windows validation instructions](windows-acceptance-1.0.1.md). Record evidence outside the public repository when it contains personal data; sanitize before sharing.
 
## Existing results
- 97 HTTP browser checks with no page errors, selected contrast ratios 16.62:1 text, 6.27:1 border and 11.7:1 primary.
- 257 independent Python/JS comparisons; 84 prior rules, 19 boundary groups, 8 Studio core, 8 model transfers + 10 provenance/guard checks, 12 security checks, five reference cases and 100 local links.
- Local asset and blocked-fetch checks on all three pages; imported markup rendered as text; unpacked bundled Chromium install and JSON export, same package hash.
- Runtime dependency review: no declared extension permissions or external runtime libraries; CI dependencies are not formally supply-chain attested.
- Logo assets and historical ZIPs unchanged; free experimental lab. No independent WCAG or antivirus certification.

## Maintainer approval / Aprovação do idealizador
Em 27/11/2026, o idealizador confirmou aprovação dos três grupos de testes manuais no candidato 1.0.1 (Chrome/Edge no Windows, Microsoft Defender atualizado sem detecções e revisão visual/teclado/acessibilidade) e autorizou a publicação. Resultados relatados, não reexecutados independentemente; logs do Defender, versões de navegador e capturas não fornecidos. / On 27 Nov 2026, the maintainer reported passing all three manual acceptance groups on candidate 1.0.1 and authorized publication. No independent rerun, raw Defender logs, browser versions or screenshots supplied.
