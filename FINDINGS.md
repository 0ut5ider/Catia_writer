# Findings and conclusions

Updated: 2026-09-07. Source: three research swarms (12 agents, then 7, both
2026-09-06) and a verification pass on 2026-09-07 in
`research/2026-09-07-upstream-verification/` and
`research/2026-09-07-container-invariant-sweep/`. Every bullet traces to an
evidence file in `research/`. Corrections are marked inline with their date.

## Executive conclusion

Do not reverse engineer the catpart format for writing. Build the pipeline:

```
CadQuery / pythonocc script (the parametric master)
  -> STEP AP214 XCAF (named assembly, colors) or ACIS .sat (analytic B-rep)
  -> Datakit converter (manual step, licensed)
  -> dumb but named CATPart/CATProduct
  -> pycatia/COM replays operations inside CATIA as real sketches + pads
  -> CATPart with a genuine, editable specification tree
```

Two independent routes to the same conclusion:
1. Writing native catpart from scratch means building on cadmpeg's
   decode-only spec, and the parametric feature layer is not documented by
   anyone. High cost, and the result is still a dumb part.
2. Even a perfect writer would not get history through Datakit. Feature
   history can only be created by a process running inside CATIA. That is the
   pycatia step.

The 2026-09-07 verification pass left this conclusion standing and changed three
things around it:

- The generator leg has a second option. cadmpeg ships semantic writers for STEP
  Part 21 (AP203/AP214/AP242, source-less documents, connected topology, product
  occurrences, colours, PMI) and IGES, under Apache-2.0. pythonocc-core is
  conda-forge only with a dead PyPI placeholder, so an Apache-2.0 Rust writer is a
  real alternative and a cross-check on the first writer.
- Detection code must not use PRONOM signatures. They match 2 of 10 real files
  here. Use the container invariant instead. Details below and in
  `research/2026-09-07-container-invariant-sweep/container-invariant-sweep.md`.
- One cheap experiment now decides whether the native route stays closed. See open
  question 0.

## Phase 1: the native format (research/2026-09-06-catia equivalents, `*-format-internals` etc.)

### What a .catpart actually is

- Magic: ASCII `V5_CFV2` + NUL. Not OLE2. The compound-storage claim floating
  around is folklore; no `D0CF11E0` anywhere in 10 native files (corrected
  2026-09-07, was: "newer saves use `V5_CFV4`", verified on 5 files). Current
  evidence: `V5_CFV4` appears in 0 of 10 native samples in any position, and the
  only source of that constant anywhere in the literature is line 36 of
  `KaiUR/Pycatia_Scripts`, `V5_MAGIC = (b'V5_CFV2', b'V5_CFV4')`. cadmpeg
  publishes a byte-accurate spec against release bands V5R8 to current and
  documents `V5_CFV2` only. Accept it as a magic to tolerate on input. Do not
  treat it as characterised and never branch write logic on it.
- Header: big-endian u32 at bytes 8 and 12 give directory offset and length,
  and offset + length equals file size exactly. Confirmed 10/10 across V5R14 to
  V5R30 on 2026-09-07, the strongest invariant in the format and the one to build
  on. Directory runs
  `CATIA_V5 CB0001\0` ... `CB__END\0` with `FINJPL` segment markers and
  UTF-16LE stream names. Typical parts nest a second `V5_CFV2` container
  around the real model streams. Observed pattern (2026-09-07): the inner
  container appears in CATParts carrying B-rep and in none of the 3 CATProducts,
  and `CB__END` appears once per container, so a hand-built `.catproduct` needs
  neither the inner container nor more than one sentinel.
- Corrected 2026-09-07: the PRONOM records are safe to cite and unsafe to depend
  on. x-fmt/439 (catpart) and x-fmt/440 (catproduct) are real, and fmt/1615 is
  CATIA Drawing (was: catsettings; confirmed against
  `nationalarchives/pronom` branch `develop`, `signatures/fmt/1615.json`). Both
  catpart and catproduct internal signatures end in the literal string
  `.CATPart`/`.CATProduct`, and 8 of 10 real files here contain no such string in
  any case, so the signature matches 2 of 10. The `CATPart` token most files do
  carry is class vocabulary (`FromCATPart`), not a filename. Detect with
  `V5_CFV2\0` at 0 plus `u32be(8) + u32be(12) == filesize` plus
  `CATIA_V5 CB0001\0` at the directory offset. Reproduce with
  `research/2026-09-07-container-invariant-sweep/pronom_signature_check.py`.
- Semantic payload is the CGM (CATIA Geometric Modeler) stream. CGM
  *semantics* are documented in mirrored CAA articles
  (maruf.ca/files/caadoc/CAAGobTechArticles/GeoObjects.htm). Only the byte
  encoding is secret.
- Version compat is encoded as a readable string, regex `V5R(\d+)SP(\d+)HF(\d+)`
  works on the header without CATIA (Pycatia_Scripts shows it). Qualified
  2026-09-07: it hits 8 of 10 samples. `Part1.CATPart` from the V5R14 era stores
  `CATIAV5R14` plus a separate `CATBuildLevel` key and no `SP`/`HF` fields, and
  `Print.CATProduct` carries no `V5R` sequence at all. A probe needs a second
  pattern such as `CATIAV5R(\d+)` and must treat "no version found" as normal.
  The same two files are the only ones where the `0x38..0x3F` header field reads
  `00000000 5f0d0a00` instead of `00000002 5f0d0a00`, so that field tracks the
  same old/new split and is not usable for release detection with 10 samples.

### The state of public knowledge

- cadmpeg (github.com/cadmpeg/cadmpeg, Rust, Apache-2.0, clean-room process)
  published a byte-accurate, CC-BY-4.0 spec of .CATPart including a
  machine-readable layout TOML and an open-items ledger. It decodes the
  standard nested container and geometry (their L1/L2 levels). Topology
  (L3+) and the feature layer are open problems. Copied into
  `research/2026-09-06-format-internals/source-cadmpeg-*.md`.
- No open catpart writer exists anywhere. Public OCCT, FreeCAD, assimp, VTK,
  Mayo all verified negative for catpart (checked source trees). Re-verified
  2026-09-07 against OCCT master mechanically: 35,642 tree entries, 0 paths
  containing `catia`. There is no reader, no writer and no build flag to look
  for, so stop spending agent time hunting for an OCCT CATIA module.
  FreeCAD reaches CATIA through the commercial ODA File Converter.
- cadmpeg's CATIA codec is decode-only, proven mechanically rather than inferred:
  its published API baseline for `cadmpeg-codec-catia` exports `detect`,
  `inspect_impl` and `decode_impl` and zero symbols matching `encode`
  (`research/2026-09-07-upstream-verification/raw/cadmpeg-api-baseline-catia.txt`).
  The same project does ship semantic writers for STEP Part 21 and IGES and
  partial writes for `.FCStd`
  (`research/2026-09-07-upstream-verification/raw/cadmpeg-write-support.md`).
  Repo status 2026-09-07: created 2026-07-10, pushed today, 48 stars (32 the day
  before), Apache-2.0 code plus CC-BY-4.0 docs.
- Only two independent native decoders exist: cadmpeg (open) and the closed
  ones sold by Datakit/HOOPS/CAD Exchanger/commercial OCCT DE.
- CATIA V4 `.model` (IRB) does carry replayable specs (V5's CATIA_SPEC paste
  rebuilds features from V4), but no public reader or writer exists. OCCT
  never shipped an IRB module; verified across OCCT trees 6.8 through 8.0.
  Treat the "OCCT documents V4 IRB" claim as false.

### Legal position (research/2026-09-06-legal-routes/, not legal advice)

- No TPM protects catpart files, so DMCA 1201 never engages on pure file
  analysis.
- Format facts observed in files are unprotectable ideas: SAS v WPL
  (C-406/10), Meshwerks v Toyota (528 F.3d 1258).
- The real exposure is contract. The current Dassault EULA bans reverse
  engineering, decompilation and benchmarking verbatim, and Bowers v.
  Baystate (320 F.3d 1317) means fair use does not excuse breach. Clean-room
  stops copyright and trade-secret claims, not contract. So: observe bytes,
  never the binary, and do not run the EULA.
- Authorized channels: Spatial 3D InterOp (Dassault subsidiary; reads AND
  writes native CATPart/CATProduct without a CAD license) is the de facto
  format license. There is no public "compatible logo" format-license program.

### Route reality check

- TransMagic EXPERT batch-writes native catpart with no CATIA present,
  mechanism undisclosed. That is what a real RE program looks like: years of
  work, then sold as a closed product.
- CATIA-side batch exists with a seat:
  `CATStart -run "CATDMUUtility -f x.stp -part out.CATPart"` converts STEP to
  catpart headless. pycatia (COM) covers everything else. Needs a licensed
  copy.
- 3DXML is one-way: ZIP + XML + PRC (PRC is the binary B-rep from
  ISO 10303-224). No tool re-saves it to catpart with anything parametric.
  It is not ISO 10303-237 (that was cancelled AP237).
- xdesign/xpr (3DEXPERIENCE) saw some public RE, but 3DX is not V5. Irrelevant
  unless Adrian moves platform.

## Phase 2: the Datakit route

### What Datakit writes into a CATPart (research/2026-09-06-dk-datakit-semantics/)

- The V5 writer API has no feature entry point. `CreateNode` makes
  GeometricSet/PartBody/MechanicalTool containers only. Published mapping:
  `Dtk_Body -> Imported Body`.
- Feature parsing exists only on the read side (CATIA, SolidWorks, NX, Creo,
  extra license) and dies at conversion. Even the flagship SOLIDWORKS-to-V5
  mapping converts cylinders and cones to NURBS with zero feature rows.
- Killer proof: Datakit writes CATParts "without requiring an external
  license". The writer never calls CATIA. A writer that never calls CATIA
  cannot create CATIA features. History is structurally impossible.
- The only history-aware commercial bridges (Theorem/XCAD) run CAA inside a
  licensed target CAD. Confirms the rule.
- Datakit 2026.3 inputs relevant to us: STEP up to AP242 E4, ACIS sat/sab
  (their ACIS kernel version listed per release), OCCT `.brep` up to 7.7.0,
  IGES, 3DXML, JT, plus the native CAD formats.

### Open writers that work today (research/2026-09-06-dk-writers-hands-on/, sandbox-verified, samples in its `samples/`)

| Writer | Writes | Evidence |
|---|---|---|
| ezdxf 1.4.4 (MIT) | DXF with layers/XDATA/3DSOLID, and real ACIS `.sat`/`.sab` via `ezdxf.acis` builder | a_box.sat is a valid ACIS 32.0 entity dump (body/lump/shell/face/loop/plane-surface), reload-verified |
| pythonocc-core 7.9.3 (LGPL) | STEP AP214 via XCAF with named assembly tree and colors | b_assy.step reopened and verified with an independent OCP build |
| CadQuery 2.8 (Apache-2.0) | Named `Assembly(...)` export to STEP | c_assy.step shows CQ-ASSY with named children |
| rhino3dm 8.32 (MIT) | `.3dm` offline: layers, names, user strings, instances, analytic B-reps | e_model.3dm, e_inst.3dm |
| build123d 0.11 | Parts only. `class Assembly` was removed upstream | Do not build on it for assemblies yet |
| pyiges, OpenJT, parasolid-kit, xt-parser, openswx | Readers or partial writers only. No usable open writer for IGES-as-semantics, JT, x_t, sldprt | verified negatives in dk-brep-writers and dk-parametric-writers. Corrected 2026-09-07 for IGES only: cadmpeg has a semantic IGES writer at ladder L9, byte replay plus source-less points, lines, conics, NURBS and trimmed sheet bodies. Not run here, so unverified in our sandbox |

Notes: pythonocc-core is conda-forge only, the PyPI name is a dead
placeholder. pythonocc trap: forgetting `STEPCAFControl_Controller.Init()` or
`Transfer(doc.Main())` writes an empty STEP silently and segfaults later.
ezdxf is broken on Python 3.14 (missing ezdxf.lldxf).
The negative on IGES was a Python-ecosystem result. cadmpeg is Rust, which is why
that swarm missed it and why an Apache-2.0 Rust STEP writer is worth a look before
we lock the pipeline to pythonocc.

### Where history actually comes from (research/2026-09-06-dk-history-survival/)

Ranked, from the evidence:
1. Replay our own operations inside CATIA with pycatia/COM. The tree is
   native and verifiable in minutes. Our generator script is the parametric
   master; the CATPart is the build artifact.
2. Vendor CAA bridges only if sources are native CAD with real trees.
3. CATIA feature recognition (lossy cleanup only).
4. Accept the dumb CATPart. This is the floor, not the goal.

### Transferable RE playbook (research/2026-09-06-community-knowledge/)

Only needed if the pycatia step ever dies and we must write native. Proven on
SLDPRT (openswx, sldprt-format-research, sldprt2step) and KOMPAS (habr 1068414,
466k-file clustering): identify container by magic/PRONOM, build a
differential corpus (empty, primitive, feature), keep an invariants database
with pass counts and a failed-hypotheses log, scan for IEEE-754 patterns and
validate against mass properties, round-trip to STEP for a free validator,
treat semantics as phase 2. The one real CATIA-format forum thread is
cccp3d.ru/topic/74514 (JS-walled, needs a browser). Zero CATIA threads exist
on reverseengineering.stackexchange.

## Phase 3: independent second opinion (7 agents, 2026-09-06)

Reported in `research/2026-09-06-p3-*`. Run blind against the same questions after
phase 1 and 2 were written, then audited on 2026-09-07.

Confirmed independently, so we can stop re-testing it:

- Native `.CATPart` writing from scratch is not viable. cadmpeg is L1 and has no
  encoder, and nobody publishes the feature layer.
- No interchange format carries feature history. STEP, IGES, JT, 3DXML and ACIS all
  land as dumb geometry. History has to be created inside CATIA.
- A hand-written minimal STEP AP214 assembly opens clean in OCCT with the product
  tree intact: `research/2026-09-06-p3-interchange-formats/example-minimal-assembly.step`.
  The assembly leg of the pipeline is not a research problem.
- Legal posture matches phase 1: no TPM on files, format facts unprotectable, the
  binding risk is the anti-RE clause in the Dassault EULA, and clean-room does not
  cure contract. `research/2026-09-06-p3-legal-re-constraints/` carries primary
  sources for 12 U.S. cases plus DMCA 1201, EU 2004/48 and UK CDPA ss.50A-50BA.

New, and useful:

- `research/2026-09-06-p3-catia-automation-writers/` prices the CATIA-side route:
  CAA development needs a Dassault support contract plus RADE seats, so pycatia over
  a normal seat is the only version of "drive CATIA" a small team can actually buy.
- `research/2026-09-06-p3-re-methodology/` gives an executable container-RE
  workflow: corpus of 3 files per variation, byte-diff to find the fields that move,
  invariants database with pass counts, failed-hypotheses log, STEP round-trip as a
  free validator.
- `research/2026-09-06-p3-community-prior-art/` maps the SEO misinformation layer,
  which is worth reading before trusting any web claim about this format. It found
  two sites asserting that no byte-level structure is documented, and one that
  invents a "CATIA binary structure" page wholesale.

Wrong, corrected in place with dated banners: `p3-community-prior-art` reported
zero open-source parsers (cadmpeg, which its own sibling report found), and two
reports repeated the idea that a V5 file embeds its own filename as a format rule
(2 of 10 files).

The process lesson is the expensive one. Within one swarm, one agent's headline
finding never reached the other six agents, and web search never surfaced a
32-star repository with a 265 KB format spec. Future research here needs a shared
findings file that agents read before writing conclusions, and must query the
GitHub API by topic and org rather than trusting a search engine.

## Open questions, ordered by what they unblock

0. Does CATIA accept a hand-patched `.CATProduct`? Take
   `research/2026-09-06-shared-corpus/raw/samples/Print.CATProduct` (14,975 B),
   change one part-number string and one placement term in place, and open it in
   CATIA V5. Byte offsets are already documented in
   `research/2026-09-06-shared-corpus/raw/samples/Print.CATProduct.matrix-version.txt`
   and `.streams.txt`. Cheapest possible native write is: copy the file, change the
   two strings, fix nothing else. If CATIA opens it, template-and-patch becomes a
   real route for assemblies, and assemblies are the half of the problem that needs
   no B-rep and no inner container (3 of 3 CATProducts here carry no inner
   container). If CATIA rejects it, the native route closes for good and the STEP
   plus pycatia pipeline stands alone. Added 2026-09-07. It needs a CATIA seat, so it
   waits for the same session that answers question 4.
1. Does Datakit's OCCT `.brep` input channel produce a cleaner CATPart than
   STEP? One manual A/B test. pythonocc writes .brep directly.
2. Do CadQuery/XCAF names and colors survive to the CATIA tree as named
   bodies/products? Needs one Datakit run plus a CATIA look.
3. Can ezdxf's SAT channel beat STEP on surface purity (analytic cylinders
   vs NURBS degradation)? Feed a_box.sat through Datakit.
4. pycatia prototype: open an imported CATPart, create a sketch and a pad,
   save, confirm the specification tree. Small script, big unknown resolved.
5. Does Datakit preserve any assembly structure (CATProduct tree) from STEP
   XCAF? Our bracket test should be an assembly to check this for free.
6. Is the STEP generator better in pythonocc or cadmpeg? Unverified either way
   today. cadmpeg is Rust and Apache-2.0 with declared AP203/AP214/AP242 targets;
   pythonocc is verified working in this sandbox. One bracket assembly written both
   ways and opened in CATIA settles it. Added 2026-09-07.

## Environment notes (this box)

- python3.14: ezdxf import fails. python3.11: venv needs
  `python -m venv --without-pip` then get-pip.py.
- /tmp/opencode disk quota is tight; do big installs under the project or
  clean up.
- CadQuery/pythonocc were verified in the sandbox by the hands-on agent on
  2026-09-06 using its own environment; see its scripts/ to reproduce.
- The 2026-09-07 verification scripts need only python3 and network:
  `bash research/2026-09-07-upstream-verification/verify_upstream.sh` re-pulls the
  cadmpeg API baselines, the OCCT tree, PRONOM and the Pycatia_Scripts constants.
  `python3 research/2026-09-07-container-invariant-sweep/container_sweep.py` and
  `pronom_signature_check.py` are offline and run from the repo root.
- `research/2026-09-06-shared-corpus/raw/me/pronom-main/` is a 13 MB, 2,853-file
  PRONOM signature dump and it is committed, which is 82% of the tracked files in
  this repository. It is re-downloadable from
  `github.com/nationalarchives/pronom`. Only 6 of its files are CATIA-relevant, and
  those are already extracted to `raw/pronom-catia-signatures.json` and
  `raw/pronom-catia-records.txt`. The 7 relevant signatures are `fmt/1615`,
  `fmt/1714` and `x-fmt/436` to `x-fmt/440`. Worth untracking if the repo ever
  needs to be small. Noted 2026-09-07, not done.
