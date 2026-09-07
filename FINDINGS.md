# Findings and conclusions

Updated: 2026-09-06/07. Source: two research swarms, 12 agents, all reports in
`research/`. Every bullet traces to an evidence file there.

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

## Phase 1: the native format (research/2026-09-06-catia equivalents, `*-format-internals` etc.)

### What a .catpart actually is

- Magic: ASCII `V5_CFV2` + NUL. Newer saves use `V5_CFV4`. Verified on 5 real
  files (`research/2026-09-06-format-internals/samples/`). Not OLE2. The
  compound-storage claim floating around is folklore; no `D0CF11E0` anywhere.
- Header: big-endian u32 at bytes 8 and 12 give directory offset and length,
  and offset + length equals file size exactly. Directory runs
  `CATIA_V5 CB0001\0` ... `CB__END\0` with `FINJPL` segment markers and
  UTF-16LE stream names. Typical parts nest a second `V5_CFV2` container
  around the real model streams.
- PRONOM signatures exist: x-fmt/439 (catpart), x-fmt/440 (catproduct),
  fmt/1615 (catsettings). Useful for safe detection.
- Semantic payload is the CGM (CATIA Geometric Modeler) stream. CGM
  *semantics* are documented in mirrored CAA articles
  (maruf.ca/files/caadoc/CAAGobTechArticles/GeoObjects.htm). Only the byte
  encoding is secret.
- Version compat is encoded as a readable string, regex `V5R(\d+)SP(\d+)HF(\d+)`
  works on the header without CATIA (Pycatia_Scripts shows it).

### The state of public knowledge

- cadmpeg (github.com/cadmpeg/cadmpeg, Rust, Apache-2.0, clean-room process)
  published a byte-accurate, CC-BY-4.0 spec of .CATPart including a
  machine-readable layout TOML and an open-items ledger. It decodes the
  standard nested container and geometry (their L1/L2 levels). Topology
  (L3+) and the feature layer are open problems. Copied into
  `research/2026-09-06-format-internals/source-cadmpeg-*.md`.
- No open catpart writer exists anywhere. Public OCCT, FreeCAD, assimp, VTK,
  Mayo all verified negative for catpart (checked source trees).
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
| pyiges, OpenJT, parasolid-kit, xt-parser, openswx | Readers or partial writers only. No usable open writer for IGES-as-semantics, JT, x_t, sldprt | verified negatives in dk-brep-writers and dk-parametric-writers |

Notes: pythonocc-core is conda-forge only, the PyPI name is a dead
placeholder. pythonocc trap: forgetting `STEPCAFControl_Controller.Init()` or
`Transfer(doc.Main())` writes an empty STEP silently and segfaults later.
ezdxf is broken on Python 3.14 (missing ezdxf.lldxf).

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

## Open questions, ordered by what they unblock

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

## Environment notes (this box)

- python3.14: ezdxf import fails. python3.11: venv needs
  `python -m venv --without-pip` then get-pip.py.
- /tmp/opencode disk quota is tight; do big installs under the project or
  clean up.
- CadQuery/pythonocc were verified in the sandbox by the hands-on agent on
  2026-09-06 using its own environment; see its scripts/ to reproduce.
