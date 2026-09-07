# Open-source writers for CAD interchange formats (ACIS, Parasolid, IGES, JT, STEP, CATIA V4)

- Date: 2026-09-06/07
- Role: research agent (Cerebo session, opencode)
- Question: for each interchange format, what does it carry beyond raw B-rep, and which open-source writers exist that produce files a commercial converter (Datakit) accepts as input for conversion to CATIA V5?
- Model: anthropic claude (via opencode)

## TL;DR

| Format | Open writer? | Verdict |
|---|---|---|
| STEP (.stp) | YES, several, mature | The real answer. OCCT (IGES/STEP, XDE) or cadmpeg (AP242, PMI, layers, colors, assembly). |
| IGES (.igs) | YES, several | OCCT IGESControl/IGESCAFControl, cadmpeg (FreeCAD-verified writer), aerocaps (Python, GPL). |
| ACIS (.sat/.sab) | NO | Read-only OSS (rwsat, cadmpeg ASM codec). Spec for SAT > 7.0 not published. |
| Parasolid (.x_t/.x_b) | NO | Read-only OSS parsers. Writing x_t requires a licensed Parasolid kernel. |
| JT (.jt) | NO (OSS) | Only readers in OSS. JT Open Toolkit writes JT but is proprietary-licensed (free, with source). |
| CATIA V4 (.model/.exp) | NO | Nothing open found, read or write. IRB is proprietary. |

Bottom line: an open-source "semantic" pipeline to CATIA V5 via Datakit means **writing STEP (XDE, AP203/214/242) or IGES**. SAT/x_t/JT/CATIA V4 are dead ends without proprietary SDKs.

---

## 1. STEP (ISO 10303-21, AP203/AP214/AP242)

### What it carries beyond B-rep
- Product/assembly structure (NAO / representation_relationship_with_transformation), per-product names and descriptions.
- Colors, layers, validation properties, names, and some GD&T via XDE-level translation (OCCT user guide, STEP section, line 57 of `occt_step.md` in `raw/`: "Other kinds of data such as colors, validation properties, layers, GD&T, names and the structure of assemblies can be read or written with the help of XDE tools: STEPCAFControl_Reader and STEPCAFControl_Writer").
- pcurves including 2D replicas, tessellation, visibility, transparency (cadmpeg STEP profile).
- No feature replay histories or sketch-constraint systems in any Part-21 AP: cadmpeg's ladder doc states this explicitly ("Part 21 exchange documents have no originating feature replay histories, sketch-constraint systems, or assembly mates"). STEP carries geometry + structure + presentation, not parametric intent.

### Open writers
1. **OCCT** (`Open-Cascade-SAS/OCCT`, C++, LGPL-2.1 with exception, latest V8_0_0, ~2.8k stars, very active)
   - `STEPControl_Writer` for shapes; `write.step.schema` selects AP214 CD (default), AP214 DIS, AP203 (`raw/occt_step.md` lines 985-987). `write.step.assembly` ON/Auto writes nested compounds as real STEP assemblies.
   - `STEPCAFControl_Writer` (XDE/OCAF) writes names, colors, layers, validation properties, assembly structure.
   - AP242: reading is "some parts" (doc line 49); the user guide's write schema list does not include AP242 as a target. Treat OCCT as an AP203/AP214 writer with partial AP242 read.
   - Consumed from Python via `pythonocc-core` (verified `src/SWIG_files/wrapper/STEPCAFControl.pyi` and `IGESCAFControl.pyi` exist) or via FreeCAD (`Part.export` to `.step/.stp`, which uses the same OCCT translator; XDE-level export in FreeCAD via App::Part tree naming).
2. **cadmpeg** (`cadmpeg/cadmpeg`, Rust, Apache-2.0, very active; verified `docs/format-support.md`)
   - STEP is their L9 format. "Native write: Semantic. The writer selects AP203 edition 1 or 2, AP214, or AP242 edition 1, 2, or 3 ... emits source-less documents ... topology, pcurves including 2D replicas, rigid body placements, product occurrences, tessellation, visibility, layers, named colors, surface transparency, and semantic or presentation PMI where the selected application protocol carries them." Round-trip verified by self-decode; optional external validators (verify-step-occt.py, verify-step-gmsh.py).
   - This is the most protocol-coverage-honest open STEP writer found (only writer claiming AP242 ed1-3 write), but it is young and self-verified rather than third-party-verified for STEP.
3. **brepkit** (`andymai/brepkit`, Rust, AGPL-3.0, active): STEP export "stable" per README; IGES export experimental/lossy (analytic surfaces skipped, circular/elliptic edges approximated as polylines). AGPL is a trap for any closed tooling.
4. **monstertruck-io** (`virtualritz/monstertruck`, C, Apache-2.0): STEP read+write in its own engine; IGES read-only. Niche.
5. **parasolid-kit** (see Parasolid section): reads x_t and writes AP242 STEP for a verified subset - useful as a Parasolid-in / STEP-out bridge.

### Notes for Datakit->CATIA V5
Datakit's own homepage: "Constant commitment to STEP standardisation"; SDK does "Extraction and writing of geometric data (B-Rep, Mesh), tessellation data, metadata, PMI and feature data" with "Over 50 native or standard 2D and 3D formats ... including parts, assemblies, PMI, features" (fetched 2026-09-07, `raw/` note). STEP is the input format Datakit is most invested in. Assembly structure + names written by an XDE STEP writer should surface as a V5 product structure; colors/layers should survive. Feature-level editability will not (no Part-21 AP carries features).

## 2. IGES (.igs/.iges)

### What it carries beyond B-rep
- Directory Entry attributes: layers, colors, thickness/weight - translated by OCCT via XDE (`raw/occt_iges.md` line 59); names via XDE too (line 10).
- Global Section administrative data: author, company, product, receiver, units, date/time (OCCT writer params `write.iges.header.*`).
- No assembly structure semantics (IGES has no NAO equivalent; there are 408 subfigure / drawing practices and Type 308 Sublist, 402 Layer, 314 Color, 406 Property forms). 2D: drawing entities (text 156/406, views 5xx) - geometry is plain curves/surfaces.
- Effectively: dumb B-rep + presentation attributes (layer/color/name).

### Open writers
1. **OCCT `IGESControl_Writer`** (LGPL-2.1+exception) - writes Face or BRep mode, unit + header metadata configurable; `IGESCAFControl_Writer` adds layers/colors/names. The classic choice; this is what FreeCAD's `Part.export`/`Import.export` uses.
2. **cadmpeg** (Apache-2.0) - IGES is an L9 format with a documented writer profile: writes points, lines, conic arcs, NURBS curves/surfaces, planes, Type 141/144 trimmed sheets with pcurves, Type 186/502/504/508/510/514 manifold B-rep solids, Type 120 revolved and Type 122 ruled constructions, Type 190 planes, analytic families via Type 192/194/196/198; targets IGES 4.0/5.0/5.1/5.2/5.3; refusal-based loss model. Independent verification: FreeCAD import acceptance on GitHub Actions (run 31923613047: 11/11 manifest files, 37/37 valid shape imports). The best-documented open IGES writer found.
3. **mlau154/aerocaps** (Python, GPL-3.0, ~2 stars, last push 2025-08-15) - genuine IGES 5.3 writer: `IGESGenerator` (start/global/directory/parameter/terminate), entities LineIGES(110), CircularArcIGES(100), RationalBSplineCurveIGES(126), CurveOnParametricSurfaceIGES(122), CompositeCurveIGES(142), BoundaryCurveIGES, trimmed surfaces 144, transformation 124, global_params. Has 2D curve machinery. Small project, no external-acceptance evidence.
4. **Rod-Persky/pyIGES** (Python, AFL-3.0, 16 stars, dormant since 2020) - writes via `IGESGeomLib`: points, lines, arcs, circles, torus/sphere, polylines, composite curves, planes, curve-on-surface, trimmed parametric surface (144), transformation, view/drawing/property entities, Type 414 circular array, groups, rational B-spline surfaces (128), spline curves, general note (text). README is honest: "hasn't been tested as to work with other cad programs beyond an IGES viewer program".
5. **@thi.ng/iges** (TypeScript, Apache-2.0, npm, monorepo codeberg.org/thi.ng/umbrella) - "IGES 5.3 serializer for (currently only) polygonal geometry, both open & closed" (npm metadata, `raw/`). Fine for meshes-as-iges, not B-rep.
6. **andymai/brepkit** IGES export: experimental, planar+NURBS only, approximated analytic edges. Skip if correctness matters.
7. (Historical) **pyiges** (`pyvista/pyiges`, MIT, active, PyPI 0.3.4): verified READ-only (README + all PyPI wheels 0.1.1-0.3.0 inspected). The original writer project (remsdtv/pyiges) is gone; wayback has no capture. GitHub code search for `IGES110` writer classes found only `cfsengineering/Pentagrow` (app-embedded IGES writer, GPL CAM framework).

## 3. ACIS (.sat/.sab/.smt)

### What it carries beyond B-rep
Per Wikipedia's ACIS article (fetched 2026-09-07, `raw/` note): user-defined data (attributes) attachable at any model level; model history ("begin history data marker ... old entity records needed for history and rollback" is an optional part of the save file); product ID and units in the header (required since 6.3); save-version targeting for backward compatibility. Entities can be named; groups used for layer-like grouping. So ACIS-in principle carries name/attribute/group/history semantics, and Datakit does extract attribute data from SAT.

### Open writers: none found
- SAT file format spec was publicly available only for version 7.0 (circa 2001) ("ACIS Text File Format Reference Manual"); newer SAT versions' specs are not published (Wikipedia: "Thus reading of modern SAT files requires either using native ACIS library or reverse engineering of the format"). Writing modern SAT from scratch means reversing a live, versioned binary/text format - nobody has published a writer.
- Searches that came back empty: GitHub code search `api_save_to_sat_file` (the ACIS API function), `"OpenACIS"` (only unrelated ACI/Abaqus hits), repo search `sat writer`, `acis export`. Wayback CDX for spatial.com/openacis and sourceforge/openacis: zero captures. "OpenACIS-2.0" (the ~1998-2000 ACIS 2.0 source donation) could not be located anywhere current; treat as unrecoverable.
- **cadmpeg** has a serious ASM/ACIS *decoder* (`ASM BinaryFile4/8`, `ACIS BinaryFile` save-format 217/218, SAT/SMT text): "Write: None. The codec has no encoder, replay path, or patch path." (verified in `docs/format-support.md`).
- **orbingol/rwsat** (C++, BSD-3-Clause, 2019): SAT reader + spline extraction for a mesh viewer. Reader only.
- Adjacent: cadmpeg's Fusion `.f3d` codec (kernel: "ASM, derived from ACIS") does partial source-less native writing, but the output is an F3D container, not `.sat`.

Verdict: writing SAT requires an ACIS/Spatial license (commercial). No open path.

## 4. Parasolid (.x_t/.x_b)

### What it carries beyond B-rep
Attributes (named user attributes on any entity via `attribute`), named entities/sets, groups/feature tree (in native part files; transmit files x_t/x_b carry a snapshot: topology + geometry + attributes + colors, but not the feature history - history lives in the native .par). x_t is schema-versioned text (SCH_nnnnn blocks).

### Open writers: none found
- **monozukuri-ai/parasolid-kit** (Rust+Python, MIT, 1 star, pushed 2026-09-07, pre-alpha): "experimental, schema-aware parser for Parasolid X_T and X_B transmit files ... read-focused". Notably it *exports validated STEP AP242* for a verified OCCT-subset with a provenance sidecar: a useful x_t-in/STEP-out bridge.
- **akiselev/xt-parser** (Rust, WIP): "from-scratch, native Rust implementation of the Parasolid XT format ... does not link to Parasolid"; generated schema crates (SCH_13006, SCH_30100/37102); differential testing against a *private* `parasolid-rs` oracle. Parser only.
- **parasolid-core** crate: schema-aware X_T/X_B parser, 0.1.0-dev. Parser only.
- Searches that came back empty: code search `"x_t writer"`, `write_x_t`, repo search parasolid writer/generator. The Siemens Parasolid Transmit API (which writes x_t) ships only with a licensed kernel.

Verdict: dead end for open writing, same as ACIS. x_t -> STEP via parasolid-kit is the one usable open move.

## 5. JT (.jt)

### What it carries beyond B-rep
JT is segment/attribute-tree based: LODs (tessellation-first), B-rep segment optional, PMI (annotation 3D/2D, semantic + characteristic), visual attributes (colors), structure with node transformations, metadata segments, and JT 9/10 lost-edge/B-rep topology. It is presentation/PMI-rich; B-rep is the optional part.

### Open writers: none found
- The **JT Open Toolkit** (jt-open.org SDK, C++) reads AND writes JT and ships source, but under a proprietary free-license agreement - not OSI open source, registration-gated download. This is the standard way to write JT; flag it as "source-available, proprietary license" rather than open.
- OSS is read-side only: **cbsghost/oce-jt** (GPL-2.0, JT Assistant fork on OCCT 6.8 lineage, 2019; mirrored as **liamsi/jt-opencascade.org** - the JT Assistant from OCCT news, a reader), **3drepo/3drepobouncer** (AGPL-3.0, in-house JT parser for reverse engineering, active).
- Verified OCCT never ships JT: no JT toolkit in OCCT 7.7, 7.8, 8.0, or OCE 6.8.0/OCE-0.18.3 git trees. (Historic JT Reader existed as a separate "JT Assistant" patch under GPL, read-only; "OpenJT", a SourceForge project sometimes cited, is unfindable: zero GitHub repos, zero Wayback captures of a sourceforge project page. Treat as a ghost.)
- Searches empty: `"JT Open"`, `jt-open`, `openjt` (only an unrelated Chinese SpringBoot demo named jt-open), gitee/codeberg/gitlab/bitbucket sweeps.

Verdict: no open writer. If JT output is genuinely needed, the JT Open Toolkit is the only free route, license-permitting.

## 6. CATIA V4 (.model/.exp, IRB)

- No open reader or writer exists. IRB is a proprietary Dassault format; the IRB readers in the wild are Datakit/EODA commercial SDK modules.
- Correction of an earlier hypothesis in this project: OCCT never had a CATIA V4 module. Verified by git-tree listing of `tpaviot/oce` tags `official/6.8.0` and `OCE-0.18.3` (the old OCCT 6.x lineage forks): zero paths matching `irb|catia`, while `iges` matches 3064 paths. GitHub code search `irb_format_cxx`/`readIrb` also empty.
- Verdict: dead end; only Dassault/Datakit-class commercial tooling.

## 7. Adjacent options worth knowing (not in the six formats)

Datakit lists SOLIDWORKS, Fusion, Inventor, NX, Creo, CATIA as inputs, and these native containers are the only ones that carry *feature* semantics:
- **cadmpeg writes SolidWorks `.sldprt`** (L4, "Native write: Partial"): patches/ regenerates native Parasolid blocks, Keywords feature history (extrude/revolve/sweep/loft/fillet/chamfer/pattern/hole operation families), sketch geometry, parameters, configurations, PMI on edited/source-less supported IR. Read side is impressively deep (feature tree, sketch profiles, equations, configurations).
- **cadmpeg writes Fusion `.f3d`** (L3-partial): source-less generation of multi-body ASM B-rep with typed history, sketch geometry + constraints, design records.
These are Apache-2.0 and the only open code found that writes *feature history* into any CAD container. Completely untested against Datakit ingest, and their own docs mark the write profiles "Partial". Worth an experiment if CATIA V5 feature trees (not just named solids) are the actual goal.

## 8. Top-3 open writers to build on

1. **OCCT STEP via XDE** (`pythonocc-core` or FreeCAD; LGPL-2.1+exception). Most converter-proven path; writes assembly structure, names, colors, layers; Datakit's flagship standard. Use `STEPCAFControl_Writer` + `write.step.schema AP214` (default) or AP203.
2. **cadmpeg** (Rust, Apache-2.0). The only open writer claiming AP242 ed1/2/3 output incl. PMI, layers, named colors, and 2D-replica pcurves; also the best-verified open IGES writer (FreeCAD acceptance runs). Young; validate output against Datakit before committing.
3. **OCCT IGES** (`IGESControl_Writer`/`IGESCAFControl_Writer`; or `mlau154/aerocaps` in pure Python GPL as a fallback). For the cases where a target wants IGES: geometry + layer/color/name attributes only, no assembly semantics.

ACIS, Parasolid, JT, CATIA V4: no open-source writers exist. If those formats are mandatory, it needs commercial SDKs (Spatial 3D ACIS Modeler, Siemens Parasolid, JT Open Toolkit for JT).

## Method and dead ends

- Working channels: GitHub API via `gh` (repos/code search), raw.githubusercontent, PyPI/npm/crates registries, StackExchange API (returned empty - effectively blocked), webfetch for datakit.com and Wikipedia API. Blocked/blocked-ish: DuckDuckGo (captcha), Bing (junk), Mojeek, searx instances (429), Ecosia (403), sourceforge (403/404), FreeCAD forum (Anubis), Wayback CDX queries for spatial.com/openacis + sourceforge/openacis (zero rows).
- All maturity claims come from fetched READMEs/docs (stored in `raw/`), registry metadata, or git-tree listings, checked 2026-09-06/07.
- Converter-acceptance evidence beyond cadmpeg's own FreeCAD-acceptance runs: not obtainable from this machine (search engines blocked, SE API empty). Anything about "Datakit accepts X" is stated as expectation, not field-tested report - test with a real converter before betting on it.
- Wrong hypothesis killed with data: "OCCT had a CATIA V4 IRB reader removed in 6.9". OCE/6.8 trees have no IRB/CATIA paths; OCCT never supported CATIA. (This belief probably came from the commercial OpenCascade/Datakit overlap; the number that killed it: 0 matches for `irb|catia` in 56,299 paths of the official/6.8.0 tree vs 3,064 for `iges`.)

## Raw data in this folder (`raw/`)
- `occt_iges.md`, `occt_step.md` - OCCT master user guides (writer params, XDE semantics).
- `cadmpeg_format_support.md` - cadmpeg support ladder incl. IGES/STEP write profiles and SAT "Write: None".
- `parasolid-kit_readme.md`, `xt-parser_readme.md` - Parasolid readers, x_t -> AP242 bridge.
- `pyIGES_README`, `pyIGES_GeomLib.py` - pyIGES writer entity classes.
- npm metadata for `@thi.ng/iges` (see inline JSON in report).
- Wikipedia ACIS extract, Datakit homepage text (fetched; inline quotes in report preserve the claims).
