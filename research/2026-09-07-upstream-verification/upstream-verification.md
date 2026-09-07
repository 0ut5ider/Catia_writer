# Upstream verification pass and swarm-3 audit

- Date: 2026-09-07
- Role: verification pass over a third research swarm's claims, run in the terminal
  after that swarm returned
- Question asked: which load-bearing claims in this repository and in the 2026-09-06
  swarm-3 reports hold up against upstream sources, and what does swarm 3 add that
  the first two swarms missed
- Model: flashnext/flashnext-w4a16-fp8ple

Re-run everything with `bash verify_upstream.sh`. Raw output lives in `raw/`.

## 1. Verified claims

### 1.1 cadmpeg exists, is active, and its CATIA codec has no encoder

`cadmpeg/cadmpeg` on GitHub: created 2026-07-10, pushed 2026-09-07, Apache-2.0 for
code plus a separate CC-BY-4.0 docs licence, Rust, 48 stars on 2026-09-07 (32 on
2026-09-06). See `raw/cadmpeg-repo.json.txt`.

The public API surface is generated per crate. `raw/cadmpeg-api-baseline-catia.txt`
lists every exported symbol of `crates/cadmpeg-codec-catia`. It contains `detect`,
`inspect_impl` and `decode_impl`. It contains zero symbols matching `encode`. That is
positive evidence for "decode only", not an inference from the absence of a blog post.
Compare `raw/cadmpeg-api-baseline-step.txt`, which is 8,715 bytes against CATIA's
1,803 bytes, because the STEP crate does expose an encoder path.

### 1.2 cadmpeg ships semantic writers for the interchange side

From the repo's own `docs/format-support.md`, extracted to
`raw/cadmpeg-write-support.md`:

| Codec | Ladder | Native write |
|---|---|---|
| CATIA V5 `.CATPart` | L1 | None |
| STEP Part 21 | L9 | Semantic: AP203 e1/e2, AP214, AP242 e1/e2/e3, source-less documents, connected solid/sheet/wire topology, pcurves, rigid body placements, product occurrences, tessellation, layers, named colours, PMI |
| IGES | L9 | Semantic: byte replay plus source-less points, lines, conics, NURBS, planes, trimmed sheet bodies |
| FreeCAD `.FCStd` | L5 | Partial: regenerates retained documents deterministically and can generate typed application graphs without a source archive |

Consequence for the pipeline in `FINDINGS.md`: the generator leg does not have to
depend on pythonocc-core, which `dk-writers-hands-on` records as conda-forge-only with
a PyPI placeholder that is dead. An Apache-2.0 Rust library emits the STEP or IGES file
that Datakit ingests. This does not replace pythonocc if we stay in Python; it removes a
licensing and packaging problem, and it gives us a second writer to cross-check the first.

### 1.3 Open-source OCCT contains no CATIA code at all

`raw/occt-master-no-catia.txt`: Open-Cascade-SAS/OCCT master has 35,642 tree entries and
0 paths containing `catia`, checked 2026-09-07. This corroborates `FINDINGS.md` for the
V4 IRB case and extends it to CATIA V5: there is no reader, no writer, and no build flag
to look for. The widely repeated claim that OpenCascade or FreeCAD opens CATIA files is
false; FreeCAD reaches CATIA through the commercial ODA File Converter.

Do not spend another agent-hour looking for an OCCT CATIA module.

### 1.4 Container invariants hold across a real corpus

See the sibling report `../2026-09-07-container-invariant-sweep/container-invariant-sweep.md`.
Summary: on 10 native samples spanning V5R14 to V5R30, the cadmpeg invariant
`directory_offset + directory_length == file_size` holds 10/10, and no file is OLE2/CFB.

### 1.5 PRONOM signature identity

`fmt/1615` is **CATIA Drawing** version 5 (`.catdrawing`), confirmed against
`nationalarchives/pronom` branch `develop`, `signatures/fmt/1615.json`. See
`raw/pronom-fmt-1615.txt`. `FINDINGS.md` listed it as catsettings. Corrected there.

## 2. Claims that do not hold

### 2.1 `V5_CFV4` is an unconfirmed constant, not a verified newer magic

`FINDINGS.md` and `README.md` state that newer saves use `V5_CFV4`. The only source in
this repository is one constant in one third-party script:
`KaiUR/Pycatia_Scripts` line 36, `V5_MAGIC = (b'V5_CFV2', b'V5_CFV4')`
(`raw/kaiur-magic-constants.txt`). Evidence status:

- 0 of 10 local native samples contain the byte string `V5_CFV4` anywhere in the file.
- cadmpeg's byte-accurate spec documents `V5_CFV2` only, and admits release bands
  V5R8 through current. A newer container magic would be a visible fact to a project
  that publishes a coverage ledger.

Conclusion: accept `V5_CFV4` as a constant to tolerate on input, since the script
author presumably saw such a file. Do not treat it as characterised, and never branch
write logic on it. Corrected in `FINDINGS.md` and `README.md`.

### 2.2 The release-version regex is not universal

`FINDINGS.md` says the regex `V5R(\d+)SP(\d+)HF(\d+)` reads the release from the header.
It works on 8 of 10 samples. The two failures are informative:

- `Part1.CATPart` (V5R14 era) has no `SP`/`HF` fields at all. Its tag reads
  `CATIAV5R14` followed by a `CATBuildLevel` key.
- `Print.CATProduct` contains no `V5R` byte sequence anywhere.

So a version probe needs a second pattern, something like `CATIAV5R(\d+)`, and must treat
"no version found" as a normal case rather than an error. A CATProduct can be version
silent even when the parts it references are not.

The same file is also the only sample where the `ff * 8` field at `0x10..0x17` is not
all `0xff`, which suggests the older header band differs slightly from what cadmpeg
documents for the current band. cadmpeg's own spec marks release-band coverage as open.

### 2.3 Swarm-3 report corrections

Two reports in the swarm-3 set (now `../2026-09-06-swarm3-community-prior-art/` and
`../2026-09-06-swarm3-opensource-readers/`) need corrections that were applied in place:

- `community-prior-art.md` states that no open-source parser of the native binary
  structure exists. That is false. cadmpeg had published a 265 KB byte-level CATIA spec
  nearly two months earlier and that swarm's own `format-internals.md` found it. The
  agent web-searched and never queried the GitHub API by topic or org. Corrected in
  place with a dated banner.
- `opencascade-and-open-source-readers.md` names Datakit CrossManager as the only
  non-Dassault writer of native `.CATPart`/`.CATProduct`. Swarm 1 found two more:
  TransMagic EXPERT batch-writes native catpart, and Spatial 3D InterOp is a Dassault
  subsidiary that reads and writes native files without a CAD licence. Corrected in place.

The pattern to remember: within one swarm, one agent's headline finding never reached the
other six agents. Future swarms need a shared findings file that agents read before
writing conclusions, or at minimum a cross-check pass like this one.

## 3. Process insight for future agents

Web search does not surface low-star research repositories. cadmpeg had 32 stars, a
proper spec, and an active commit history, and it stayed invisible to six agents running
varied queries. What found it: querying `api.github.com/repos/<org>/<repo>`, the
`git/trees?recursive=1` endpoint for file listings, and `docs/api-baseline/` for a
mechanical answer to "does this project have a writer". Use
`api.github.com/search/repositories?q=<topic>` directly rather than hoping a search
engine indexes a README.

## 4. New result that changes a plan decision

The cheapest experiment that decides whether the native route is alive is not in
`FINDINGS.md`'s open questions. Take `Print.CATProduct` (14,975 B), patch one part
number string and one placement matrix term in place, and open it in CATIA V5. Byte
offsets for both are documented in
`../2026-09-06-shared-corpus/raw/samples/Print.CATProduct.matrix-version.txt` and
`.streams.txt`. If CATIA accepts a hand-patched CATProduct, a template-and-patch writer
for assemblies becomes a real option, and assemblies are exactly the half of the problem
that needs no B-rep. If CATIA rejects it, the native route closes and the STEP plus
pycatia pipeline in `FINDINGS.md` stands as the only route. Added to `FINDINGS.md` as
open question 0.
