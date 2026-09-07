# Shared corpus, 2026-09-06

Raw evidence collected by the phase-1 research agents. No report lives here;
the reports are in the sibling folders. This folder holds data two or more
agents shared or left behind.

Contents under `raw/`:

- `pronom-catia-signatures.json`, `pronom-catia-records.txt`: the CATIA-relevant
  PRONOM signature records (x-fmt/439, x-fmt/440, fmt/1615) extracted for
  safe file-type identification.
- `pronom-main/`: full PRONOM signature corpus dump (65 MB, thousands of
  unrelated file-type JSONs). Kept so cited entries stay offline-verifiable.
  It is re-downloadable; delete if the repo needs to stay small.
- `cl_*.json`: reverse-engineering case-law captures (sega, connectix, bowers,
  bleem, lotus, lexmark, apple/franklin, apple/formula, davidson, juniper,
  corley, network-auto, edsi, cdmaps, bnetd, atari/fed). Source for
  `2026-09-06-legal-routes/`.
- `q01-q03.html`, `b01-b03.html`: raw search/browse captures.
- `so/`: Stack Exchange search dumps.
- `searches/`: per-query search-result captures.
- `file-magdir-cad.txt`: libmagic Magdir CAD entries.
- `me/`: agent working material (includes the pronom-main clone above).
