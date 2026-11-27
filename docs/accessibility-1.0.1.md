# Stage 04 — experience and accessibility / Experiência e acessibilidade
Candidate only; no merge, release or distribution changes. Baseline 80728b1f3a891af013d2ece0412c059523f6f32c.
 
## Design
Dark wine palette scoped to Research Workspace and shared Mini/popup; official logo assets and GRAAL navigation untouched. Grouped model links, interpretation guides, accessible skip links and visible focus, stronger field boundary contrast, readable scientific outputs and textual chart equivalents. All four Mini tools and all Research models remain. No external font, package or network permission added.
 
## Verification
Browser smoke checks include actual computed foreground/background contrast (selected text/control pairs, thresholds 4.5:1 and 3:1), 320 CSS px reflow, keyboard activation, focus, reduced motion and bilingual output. Existing regressions and Python oracles remain mandatory. These are targeted checks, not a WCAG certification or exhaustive screen-reader evaluation. Real extension installation and manual assistive-technology/visual assessment remain pending. New candidate hash must be obtained from CI; historical ZIPs remain intact.
