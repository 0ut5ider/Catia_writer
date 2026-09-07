# Catia_writer

Goal: generate native CATIA V5 `.CATPart`/`.CATProduct` files with editable,
sketch-driven history, from our own tooling.

Start with `FINDINGS.md`. It carries the conclusions from two research swarms
(12 web-research agents, 2026-09-06) and the recommended pipeline. Every claim
here is sourced in the agent reports.

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

Plus `research/2026-09-06-shared-corpus/`: raw evidence shared across phase-1
agents (PRONOM signature dump, reverse-engineering case-law captures, search
dumps). See its README before using it.

## Conventions for future agents

- New research goes in `research/<YYYY-MM-DD>-<slug>/` with the report named
  `<slug>.md` and raw data alongside it.
- Keep generated evidence files (hex dumps, sample CAD files, logs). They are
  worth more than prose.
- Update `FINDINGS.md` when a finding changes or an open question resolves.
  Mark corrections with the date.

## Quick facts, so nobody repeats the dead ends

- `.catpart` is not OLE2/compound storage. Magic is ASCII `V5_CFV2\0`
  (newer files `V5_CFV4`). Verified on five real files.
- cadmpeg (github.com/cadmpeg/cadmpeg) has the only public byte-accurate
  .CATPart spec. Decode only. No writer.
- Datakit's CATIA V5 writer has no feature-level API. It writes CATParts
  without a CATIA license, so it never calls CATIA, so it cannot write history.
- `pycatia` drives a licensed CATIA over COM. It is not a file parser.
- ezdxf 1.4.4 writes real ACIS `.sat` files. It needs Python < 3.14.
- This box: python3.14 (ezdxf broken on it) and python3.11 without ensurepip.
  /tmp/opencode quota is tight.
