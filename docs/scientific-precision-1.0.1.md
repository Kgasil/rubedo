# Rubedo — Scientific precision candidate 1.0.1 / Candidato científico
Baseline: eaa1dd57700bb2acb1ae49864bacf7701af3f071. No release, merge or public ZIP replacement.

## R04
The old absolute tolerance merged distinct vertices near zero and could admit infeasible points. Exact integer determinants and cross-products now compare normalized decimal coefficients, constraints, coordinates and objective values. Only output converts to binary64. Input Number normalization, representability and two-variable continuous model limitations remain. Display uses scientific notation for tiny nonzero values; axes scale independently.

Independent analytical oracles: rectangular feasible sets x=B/a, y=D/b for positive objective coefficients; objective c*x+d*y. For the regression case x≤0.001/1e6, y≤1, maximize 1e6*x, the true objective is 0.001. Additional formulas use Little's law, triangular mean/CDF, exponential reliability, sample variance and known affine data. These are model-level synthetic checks, not industrial validation.

## Packaging
Source candidate 1.0.1; historical ZIPs and SHA256SUMS remain immutable. Package test builds twice in separate temporary directories and checks byte parity, CRC, manifest and source parity. Historical packages independently checked against fixed hashes. Never install or publish a candidate solely on CI results.

## Evidence and gates
Baseline CI: https://github.com/Kgasil/rubedo/actions/runs/46007461543
Run node tests/scientific-boundaries.test.js and existing validation workflow. Candidate test results must be recorded from its own commit; this document does not claim they have passed. Manual Chrome/Edge installation, expanded browser coverage, industrial validation and approval remain pending. No design/logo changes or paid services.
