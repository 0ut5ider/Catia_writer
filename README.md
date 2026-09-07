# Catia_writer

Goal: generate native CATIA V5 `.CATPart`/`.CATProduct` files with editable,
sketch-driven history, from our own tooling.

Start with `FINDINGS.md`. It carries the conclusions from three research swarms
(12 agents then 7, both on 2026-09-06), a verification pass on 2026-09-07, and
the recommended pipeline. Every claim here is sourced in the agent reports.

## Layout

```
Catia_writer/
  README.md            This file. Folder map and conventions.
  FINDINGS.md          Conclusions, recommended pipeline, open questions.
  research/            One folder per agent. Report .md first, raw evidence after.
```

## Research index

Phase 1, can we reverse engineer the native format:

| Folder | Question the agent answered |
|---|---|
| `research/2026-09-06-format-internals/` | Real byte structure of .catpart/.catproduct. Verified hex dumps in `samples/`. |
| `research/2026-09-06-opensource-parsers/` | What open-source code reads catpart today. Found cadmpeg. |
| `research/2026-09-06-commercial-sdks/` | Who sells catpart writers and how they did it. |
| `research/2026-09-06-legal-routes/` | Legal exposure of RE vs contract risk. Case law with citations. |
| `research/2026-09-06-alt-generation-routes/` | Non-RE ways to produce catpart: automation, batch tools, 3DXML, CGR. |
| `research/2026-09-06-community-knowledge/` | Where RE knowledge lives. Transferable playbook from SolidWorks/KOMPAS efforts. |

Phase 2, Datakit route (Adrian has a Datakit converter license):

| Folder | Question the agent answered |
|---|---|
| `research/2026-09-06-dk-datakit-semantics/` | What Datakit writes into a CATPart per input format. Verdict: B-rep + metadata only. |
| `research/2026-09-06-dk-brep-writers/` | Open writers for interchange formats (ACIS, Parasolid, IGES, JT, STEP, V4). |
| `research/2026-09-06-dk-parametric-writers/` | Open writers for parametric-native formats (sldprt, ipt, prt, f3d, 3dm...). |
| `research/2026-09-06-dk-history-survival/` | Can feature history ever survive a format hop into CATIA. No. |
| `research/2026-09-06-dk-generator-ecosystems/` | Open parametric generators (FreeCAD, CadQuery, build123d, pythonocc) mapped by export capability. |
| `research/2026-09-06-dk-writers-hands-on/` | Sandbox test: what actually runs today. Generated sample files in `samples/`, scripts in `scripts/`. |

Phase 3, independent second opinion on the same questions, seven agents:

| Folder | Question the agent answered |
|---|---|
| `research/2026-09-06-p3-format-internals/` | Byte structure, version drift, variant families, RE precedent. Longest report; cites cadmpeg heavily. |
| `research/2026-09-06-p3-opensource-readers/` | Catalogue of everything that touches CATIA data in open source, and every commercial reader/writer. |
| `research/2026-09-06-p3-catia-automation-writers/` | What it costs to write native files by driving licensed CATIA (CAA, pycatia, batch seats, licensing). |
| `research/2026-09-06-p3-interchange-formats/` | Can STEP/JT/3DXML/IGES replace native RE. Includes a hand-written minimal AP214 assembly that OCCT reads clean. |
| `research/2026-09-06-p3-legal-re-constraints/` | DMCA 1201, EU and UK text-and-data/interop exceptions, contract risk, with primary sources in `raw/`. |
| `research/2026-09-06-p3-re-methodology/` | Concrete toolchain and workflow for container-level RE: corpus, diffing, instrumentation, validation. |
| `research/2026-09-06-p3-community-prior-art/` | What the public web actually knows, including the SEO misinformation layer and negative search evidence. |

Verification pass, 2026-09-07. Scripts you can re-run:

| Folder | What it settled |
|---|---|
| `research/2026-09-07-upstream-verification/` | cadmpeg is decode-only (0 encoder symbols); open-source OCCT has 0 `catia` paths; PRONOM `fmt/1615` is CATIA Drawing, not settings; `V5_CFV4` traces back to one constant in one third-party script; cadmpeg does ship semantic STEP and IGES writers. Corrects phase-1 and phase-3 claims. |
| `research/2026-09-07-container-invariant-sweep/` | Sweeps 10 native samples, V5R14 to V5R30, against the documented container invariants. Shows the PRONOM internal signature matches only 2 of 10 real files. |

Corrections are marked in place, dated, inside the affected report. The two phase-3
reports that were wrong about prior art carry a correction block at the top.

Plus `research/2026-09-06-shared-corpus/`: raw evidence shared across agents
(PRONOM signature dump including the 65 MB corpus, reverse-engineering case-law
captures, the cadmpeg docs mirror, search dumps, and the native sample files).
No report lives there. See its README before using it.

## Conventions for future agents

- New research goes in `research/<YYYY-MM-DD>-<slug>/` with the report named
  `<slug>.md` and raw data alongside it.
- Keep generated evidence files (hex dumps, sample CAD files, logs). They are
  worth more than prose.
- Update `FINDINGS.md` when a finding changes or an open question resolves.
  Mark corrections with the date.

## Quick facts, so nobody repeats the dead ends

- `.catpart` is not OLE2/compound storage. Magic is ASCII `V5_CFV2\0`, verified on
  10 native files spanning V5R14 to V5R30. `V5_CFV4` appears in 0 of them and traces
  to one constant in one third-party script. Tolerate it on input, never branch on it.
- The container invariant to build on: `u32be(0x08) + u32be(0x0C) == file_size`, true
  on 10/10 samples. Do not detect CATIA with PRONOM signatures; they match 2 of 10
  real files because they require an embedded `.CATPart` filename string that most
  files do not carry.
- cadmpeg (github.com/cadmpeg/cadmpeg) has the only public byte-accurate CATIA spec
  and the only open CATIA decoder. Rust, Apache-2.0, active. Decoder only for CATIA.
  It does ship semantic writers for STEP Part 21 and IGES, and partial writes for
  `.FCStd`, which is a second option for the generator leg of the pipeline.
- Open-source OCCT has no CATIA code at all: 0 paths containing `catia` in 35,642
  tree entries on master. FreeCAD reaches CATIA through the commercial ODA converter.
- Datakit's CATIA V5 writer has no feature-level API. It writes CATParts
  without a CATIA license, so it never calls CATIA, so it cannot write history.
  TransMagic EXPERT also writes `.CATPart`/`.CATProduct`; Spatial 3D InterOp does,
  but Spatial is a Dassault subsidiary.
- `pycatia` drives a licensed CATIA over COM. It is not a file parser.
- ezdxf 1.4.4 writes real ACIS `.sat` files. It needs Python < 3.14.
- This box: python3.14 (ezdxf broken on it) and python3.11 without ensurepip.
  /tmp/opencode quota is tight.
