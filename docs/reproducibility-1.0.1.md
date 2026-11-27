# Stage 03 — Reproducibility / Reprodutibilidade
Candidate branch only. Stage 02 CI passed at b9a34d9180fb6cad21e3e144a093bd7a9892482d; no release or merge.

## Independent validation
Run `python3 tests/independent_oracles.py` with Python 3.10+ and Node. Python standard library Fraction and statistics use independent arithmetic; LP projects onto x and compares endpoints and the upper-envelope crossing instead of enumerating all constraint pairs. Seeded Python random.Random uses Mersenne Twister and Lindley's recurrence for M/M/1, compared with JS simulation and stationary theory. Triangular samples and analytical survival are separately compared. Deterministic oracle seed 713; stochastic tests have predetermined tolerances, not equality expectations or formal confidence intervals. R05 checks metadata semantics only.
The oracle invokes the JS bridge with JSON input, checks all 13 model/protocol identifiers, and fails on mismatches. No runtime Python dependency and no external data. CI status for the new commit is required before acceptance.

## Studio v2
Manual records include declared model version, parameters/seed, source, limitations, numeric value, metric, unit and UTC entry timestamp. JSON export/restoration is explicit and local. v1 data migrate as legacy-manual, unknown model version and null time; unknown versions are not compared. Imports validate size (2 MiB), schema, count (100), field lengths and numeric bounds; invalid import preserves records. Users must confirm replacement. Data and provenance are user claims, not verified signatures; do not enter confidential data. No persistence, telemetry or accounts.
 
## Limits
Synthetic examples only, no industrial calibration, no claims of certified research. Browser, actual extension install, visual review and global 9/10 approval remain gates. Public ZIPs unchanged. No changes to logos, themes or free distribution.
