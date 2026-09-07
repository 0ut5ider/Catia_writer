# Shared corpus, 2026-09-06

Raw evidence shared by two or more research agents. **No report lives here.**
Reports are in the sibling folders:

- Phase 1: `../2026-09-06-format-internals/` and the other unprefixed
  `2026-09-06-*` folders.
- Phase 2, Datakit route: `../2026-09-06-dk-*/`.
- Phase 3, seven-agent second opinion: `../2026-09-06-p3-*/`. These reports were
  originally dumped flat in this folder and moved out on 2026-09-07, so their
  internal links now point back here.
- Verification pass: `../2026-09-07-upstream-verification/` and
  `../2026-09-07-container-invariant-sweep/`.

Total size 64 MB, of which 35 MB is `raw/me/`.

## `raw/cadmpeg/` (2.0 MB)

Local mirror of `github.com/cadmpeg/cadmpeg` `docs/`. This is the single most
valuable thing in the repository: `catia.md` is a 265 KB byte-level CATIA V5
format spec under CC-BY-4.0, `catia.toml` is the machine-checked layout table it is
generated from, and `catia-open-items.md` is a coverage ledger that states plainly
what is not known yet. `catia-coverage.md` and `format-support.md` give the L1 to
L9 ladder per format, including the write column that proves CATIA is decode-only
while STEP and IGES have semantic writers. `LEGAL.md` documents their clean-room
posture, which is the posture this project should copy.

## `raw/samples/` (native files)

Three native V5 files plus the dumps made from them. Used by
`../../2026-09-07-container-invariant-sweep/container_sweep.py`, which sweeps every
native file in the repository, not only these.

- `Print.CATProduct` (14,975 B): the best template-patch candidate we have. Small,
  version-silent, no inner container. `*.matrix-version.txt` and `*.streams.txt`
  already give the byte offsets of the part-name string and the placement terms.
- `Part1.CATPart` (112,111 B): V5R14 era. The only sample where the `0x10..0x17`
  fill is not `ff * 8`, and where the release reads `CATIAV5R14` instead of
  `V5RxxSPxxHFxx`. Useful as the old-band counterexample.
- `MM_Oil_Dipstick.CATPart` (227,597 B): V5R30SP6HF0, newest sample, from
  `Momento2025/CATPART`.

## `raw/pronom-catia-signatures.json`, `raw/pronom-catia-records.txt`

The 7 CATIA-relevant PRONOM signature records: `fmt/1615` (CATIA Drawing),
`fmt/1714` (V3 model), `x-fmt/436` to `x-fmt/440`. Read
`../../2026-09-07-container-invariant-sweep/container-invariant-sweep.md` before
using them in detection code. Their internal signatures match 2 of 10 real files in
this repository.

## `raw/me/pronom-main/` (13 MB, 2,853 files, committed)

Full PRONOM signature corpus from `github.com/nationalarchives/pronom`. Kept so
cited entries stay offline-verifiable. It is 82% of the tracked files in this
repository and re-downloadable, so it is the first thing to untrack if the repo
needs to shrink. `.gitignore` also blocks a second copy at
`raw/pronom-main/`.

## `raw/cl_*.json` (reverse-engineering case law)

Per-case captures: `sega`, `connectix`, `bowers`, `bleem`, `lotus`, `lexmark`,
`apple/franklin`, `apple/formula`, `davidson`, `juniper`, `corley`,
`network-auto`, `edsi`, `cdmaps`, `bnetd`, `atari/fed`, `chamberlain`, `oracle`,
`vault`, `brightstar`, `atari/ndcal`. Plus `cl_ds_cases.json` and `cl_ds_re.json`,
the Dassault licence terms and their anti-RE clauses. Source for
`../2026-09-06-legal-routes/` and `../2026-09-06-p3-legal-re-constraints/`.
Stripped text is in `../txt/`.

Four captures are 97-byte stubs and one is 52 bytes, where the source refused the
fetch (`cl_sega.json`, `cl_vault.json`, `cl_brightstar.json`, `cl_atari_ndcal.json`,
`cl_cdmaps.json`). Do not cite those as evidence of anything; the reports flag them.

## `raw/ds_*.pdf`, `raw/ds_*.html`, `raw/dk_*.pdf`, `raw/cdx_*`

Dassault licence and 3DEXPERIENCE documents, and Datakit conversion and write
capability PDFs. Source for the phase-2 Datakit reports. `cdx_3ds_terms.txt` is an
empty fetch.

## `raw/ticket-search.json` (6.3 MB), `raw/forum-search.json` (11 MB)

OCCT issue-tracker and forum search dumps from the phase-1 open-source agent.
Confirms the negative: no OCCT ticket or forum thread about a CATIA reader or
writer.

## `raw/so/`, `raw/searches/`, `raw/b0*.html`, `raw/q0*.html`, `raw/me/`

Stack Exchange API dumps, per-query search captures, and agent working material
including a 168-entry scratch directory. Low value except as proof of what was
already searched. Read `../2026-09-06-p3-community-prior-art/` before repeating any
of it; that report logs which search engines and indexes returned nothing.

## `txt/` (40 files)

Stripped text of the web captures in `raw/`, so greps do not need an HTML parser.
Named to match the `raw/` file they came from.

## Fidelity notes

- `raw/uk_50ba.xml` is the CDPA section 50BA capture from legislation.gov.uk. Five
  `<CommentaryRef Ref="key-...">` anchors in it match the pattern GitHub push
  protection reports as a Mailgun API key. They are document-internal commentary
  identifiers, not credentials. The `key-` prefix in those five values is rewritten
  to `key_` so the repository can be public. The statutory text is untouched.
- Fetch failures are kept as empty or stub files instead of deleted, so a later
  agent sees that the query was attempted. See the stub list under
  `raw/cl_*.json` above.
