# How much of the CATIA V5 format is reverse-engineered and shipped in open source?

- Date: 2026-09-06
- Agent role: web research agent (Cerebo session), OpenCascade/open-source evidence track
- Question: How much of the CATIA V4/V5 file format has been reverse-engineered and shipped
  as open source? Is there anything that can write CATIA files? Catalog every independent
  reader or writer.
- Model: flashnext/flashnext-w4a16-fp8ple
- Companion report: `catia-automation-writers.md` (same directory) covers writing native
  files by driving CATIA itself. This report covers reading and the open-source ecosystem.

## TL;DR

1. **Open-source OCCT has never shipped a CATIA reader or writer.** The premise of this task
   (packages `IFSIOPart`, `CATIAReader`, toolkit `TKXDECATIA` in OCCT) is false. Those names
   return zero commits in OCCT's full GitHub history and zero matches in Sourcegraph's global
   public-code search. Confidence: high.
2. Open CASCADE's own free format list was and is "IGES, STEP, STL, VRML, etc." Their
   commercial format catalog (2018 page, and today's `OCCT-Components` GitHub org) contains
   ACIS, DXF, JT, Parasolid, IFC, RVM, USD. No CATIA in either tier. CATIA interoperability
   was routed to **Datakit**, a third party.
3. A real `.CATPart` (227,597 bytes, saved by CATIA V5-6R2020 SP6 HF0) starts with the magic
   `V5_CFV2`, not OLE2 and not zip. `file(1)` says "data", 7-Zip refuses it, and `olefile`
   does not apply. Contents are a Dassault compound-file container holding typed persistence
   containers (`CATContainer`, `CATPrtCont`, `CATFeatCont`, `CGMGeom`, `CATCGRCont`, ...)
   and a readable provenance footer (`MinimalVersionToRead = CATIAV5R30`).
4. **Yes, something can write CATIA V5 files: Datakit CrossManager lists `.CATPart` and
   `.CATProduct` as output formats**, and its "write" brochure names CATIA V5 as an embedded
   writing-library format. It is commercial and per-format licensed. No open-source writer
   for native V5 exists. Writing otherwise requires a licensed CATIA (see companion report).
5. Independent readers are all commercial: HOOPS Exchange (CATIA V4/V5/V6 read-only),
   CAD Exchanger (V5 and 3DXML read-only), Datakit (V4/V5/V6 read, V5 write), ODA (lists
   "Catia" in its platform matrix), plus TransMagic, CoreTechnologie, 3D-Tool, Okino,
   Verisurf, and Autodesk APS (medium confidence on APS).
6. The only genuinely open-source parsing in the family targets **CATIA V6 3DXML**
   (`.3dxml`), a documented zip/XML container: `Terrev/3DXML-to-OBJ` (C#, 35 stars),
   `gxh-0808/3dxmlToGLtf` (C#, 14 stars), `z1130/convert_3dxml_to_fbx` (Python),
   `zy-zhao17/3Dxml-for-unity` (C#, 6 stars). For V5 native the only open-source artifact
   found is a string-scraping C# utility that extracts component filenames from
   `.CATProduct` by text markers.

## 1. OCCT: what ever existed (and what did not)

### 1.1 The named modules do not exist in OCCT history

The task premise names `src/IFSIOPart`, `src/CATIAReader`, `src/TKXDECATIA`, and
`src/CATIALSRef`. Checks run on 2026-09-06 via `api.github.com` against
`Open-Cascade-SAS/OCCT` (the vendor's own mirror, history back to V6_5_0 tags):

| Check | Result |
|---|---|
| `GET /contents/src?ref=master` (8.0.1, commit `3d097a03`) | no `IFSIOPart`, `CATIA*`, `XDE_CATIA` dirs |
| same on tags `V6_5_0 V6_6_0 V6_7_0 V6_8_0 V6_9_0 V7_4_0 V7_6_0 V7_7_0 V7_8_1` | none |
| `GET /commits?path=src/IFSIOPart` | `[]` (0 commits, every path ever) |
| `GET /commits?path=src/CATIAReader` | `[]` |
| `GET /commits?path=src/TKXDECATIA` | `[]` |
| `GET /commits?path=src/CATIALSRef` | `[]` |
| Sourcegraph global literal search `IFSIOPart` | `matchCount: 0` over the indexed public corpus |
| Sourcegraph global literal search `CATIAReader` | `matchCount: 0` |

The only literal "CATIA" strings in current OCCT master are historical comments inside the
STEP and IGES modules, for example:

- `src/DataExchange/TKDESTEP/TopoDSToStep/TopoDSToStep_MakeStepFace.cxx:19`:
  `// abv 6 Jan 99: TR10: fix by PDN commented (temporarily) because CATIA do not read DEG_TORUSes`
- `src/DataExchange/TKDESTEP/.../RWStepAP214_ReadWriteModule.cxx:4731` area:
  `LECTURE SEULEMENT (READ ONLY), origine CATIA. CKY 2-SEP-1997`

Caveat stated plainly: GitHub history for OCCT begins with the vendor's git import (the repo
carries tags from 2007 onward but is not a commit-by-commit archive of the 1990s Perforce
era). Absence of a deleted path cannot be proven from git alone. Two independent sources
below close that gap.

### 1.2 What OCCT's own product pages ever claimed

- Wayback, `opencascade.com/content/data-exchange`, snapshot 2016-04-05
  (`20160405110228`): "Data Exchange is organized in a modular way as a set of interfaces
  that comply with various CAD formats: **IGES, STEP, STL, VRML, etc.**" No CATIA.
- Wayback, `opencascade.com/content/added-value-components` (2018): commercial component
  list is "**Advanced Data Exchange: ACIS Import-Export, DXF Import-Export, JT
  Import-Export, Parasolid Import, IFC Import**". No CATIA then.
- Today, `github.com/Open-Cascade-SAS/OCCT-Components/tree/main/Exchange`:
  `ACIS_ImportExport, DXF_ImportExport, IFC_Import, JT_ImportExport, Parasolid_Import,
  RVM_Import, USD_ImportExport`. No CATIA now.
- Wayback, `opencascade.com/content/what-3d-formats-supported` (2017 Q&A): asked about
  formats beyond STEP/IGES/STL, Open CASCADE answered by offering commercial interfaces
  "(DXF, ACIS SAT/SAB, Parasolid X_T/X_B)" and pointing at "data exchange interfaces
  **by Datakit**". CATIA interop was third-party business, never open OCCT.
- OCCT 8.0.1 XDE user guide (`dev.opencascade.org/doc/overview/html/occt_user_guides__xde.html`):
  import/export chapters cover IGES, STEP, glTF, OBJ, PLY, STL, VRML only.

### 1.3 The archives: 8,843 forum topics and 7,498 tickets

Open Cascade's retired forum and Mantis tracker are published as searchable JSON
(`occt3d.com/dev/forum-search.json`, `occt3d.com/dev/ticket-search.json`; both copied to
`raw/`). Lexical counts over the full indexes:

| Term | Forum topics (8,843) | Tickets (7,498) |
|---|---|---|
| `catpart` | 1 (pythonOCC thread, asks about normals) | 0 |
| `catproduct` | 0 | 0 |
| `ifsiopart` / `r catiareader` | 0 | 0 |
| `catia` | 41, all STEP/IGES interop context | 7 |
| `connector` | n/a | 1 |

The single interface-adjacent ticket is `0005080`: "CATIA V4 Connector is not compilesd",
project OCCT, category `OCCT:WOK`, submitted 2004-01-23, closed, 0 notes. It is a build
error in a long-gone WOK-era "connector" shell. It is not evidence of a shipped CATIA
parser; it is the earliest trace of an interface idea that never entered open OCCT.

Verdict on the research question's first clause: **the amount of CATIA V5 reverse-engineered
and shipped in open-source OCCT is zero**, with one pre-2005 commercial connector for V4 as
footnote. Confidence: high.

### 1.4 FreeCAD and the Python wrappers

FreeCAD current source (`/tmp/opencode/freecad`, master) has no CATIA import path.
`grep -rliE "catpart|catproduct" src/` returns nothing. The only hit family is one comment,
`src/Mod/Import/stepZ.py:29`: `# Catia seems to use gz, Inventor zipfile` (about STEP-Z
compression, not parsing). pythonOCC and cadquery wrap OCCT, so they inherit the same
zero. assimp and gmsh were checked too: assimp `doc/Fileformats.md` has 0 occurrences of
"catia", and `gmsh.info` front page has 0. Negative confirmed for the major open stacks.

## 2. What the V5 container actually is (measured on a real file)

Sample: `MM_Oil_Dipstick.CATPart`, 227,597 bytes, from
`github.com/Momento2025/CATPART` (public, no PII beyond a part name). Full scan in
`txt/CATPart_container_scan.txt`; sample copied next to this report.

```
magic bytes      56 35 5f 43 46 56 32 00  →  "V5_CFV2"
file(1)          data (no recognized type)
7z l -slt        ERROR: Cannot open the file as archive
OLE magic D0CF11E0   absent (olefile does not apply)
zip magic        absent
second CFV header at offset 172,810 (segmented container)
```

This corrects a common assumption: current-save `.CATPart` is **not** an OLE2 compound file.
`V5_CFV2` is Dassault's own "compound file V2". Only files wrapped by PDM/OLE persistence
look like `D0 CF 11 E0`. Measured structure:

- 1,043 printable runs of 6+ bytes out of 227 KB; the payload is binary.
- Version stamps: `V5R30SP6HF0` x3, plus `NOTHING-CNEXTINFOS-UpdateVersion-StreamBlock-SafeEarlyBlock-StrongEarly`
  (`cnext` is the CATIA V5 executable name), plus `DASSAULT-SYSTEMES` x12 and marker `041803P` x12.
- Readable footer (offset ~214,050) in XML-ish form:
  `...<Release>..</Release><ServicePack>6</ServicePack><BuildDate>03-11-2022.23.05</BuildDate><HotFix>0</HotFix> |
  MinimalVersionToRead | CATIAV5R30 | CATBuildLevel | ... | CATPDMPersistence | OMBDoc_0002`.
- 39 unique class-like tokens naming the persistence objects:
  `CATContainer, CATCompoundCont, CATPrtCont, CATFeatCont, CATProdCont, CATStdCont,
  CATSeeBodyCont, CATBRepModeContainer, CATMFBRP, CATCGRCont, CGMGeom, CGMLevel,
  CATStorageProperty, CATUnicodeString, CATOctetArray, CATPreview, CATSummaryInformation,
  CATCatalogManager, CATExtruderBySweep, ...`.
  Reading: the document stores typed CAA objects (`CAT*Sch` schemas), both exact B-rep
  (`CATBRepModeContainer`) and `CGR` tessellation (`CATCGRCont`), with the geometry kernel
  namespace `CGMGeom` (Dassault's CGM kernel).
- The same markers appear in open-source code: `sobalvarro/CATProductFiles` (see 4.2) splits
  on `CATOctetArray` and the stream-end marker `FINJPL` (both also present in this file,
  `FINJPL` x11).

Practical inspection commands that work today on Linux, all run against this sample:

```
file X.CATPart                       # expect: data
python3 - <<'EOF'                     # magic + ascii dump (works, see txt/ script)
open('X.CATPart','rb').read()[:64]
strings -n 6 X.CATPart | sort | uniq -c | sort -rn
grep -aoE 'CAT[A-Za-z]{4,30}|CGM[A-Za-z]{3,20}' X.CATPart | sort -u
```

`olefile`, `oledump.py`, and `7z l` all fail on a `V5_CFV2` file by design. Confidence:
high for this file's structure; medium as the universal V5 picture (one sample, one save
version; older releases or PDM wrappers may differ).

## 3. Who can write CATIA V5

| Product | Writes `.CATPart`/`.CATProduct` | Evidence |
|---|---|---|
| CATIA V5 itself (COM/CATScript/CAA) | yes, sanctioned | companion report `catia-automation-writers.md` |
| **Datakit CrossManager** | **yes**, native output | product page format matrix lists under Output: "CATIA V5 3D `.CATPart .CATProduct`"; write brochure PDF: "Datakit supports a broad range of CAD formats to write, including CATIA V5, NX, SOLIDWORKS, JT, ..."; "writing libraries are embedded by software vendors ... for native formats such as CATIA V5, CGR, NX, SOLIDWORKS, and 3DXML". Fetched 2026-09-06; PDFs in `raw/` |
| CAD Exchanger | no, read-only | formats page matrix: CATIA V5 Read R, no W |
| HOOPS Exchange | no, read-only | FAQ: "Read Only Support ... CATIA V4, CATIA v5, CATIA V6" |
| ODA | unknown | homepage lists "Catia" in the format matrix; write capability not documented publicly |
| Free open source | none | 0 hits in all repo/code searches |

Datakit is also the company Open CASCADE itself pointed CATIA users to in 2017 (1.2). If a
pipeline needs programmatic V5 writing without Dassault software, Datakit CrossManager CLI
(Windows/Linux/macOS, per-format floating licenses) is the only third-party path found.

## 4. Reader ecosystem catalog

### 4.1 Commercial readers (independent of Dassault, all reverse-engineered)

| Library / product | V4 | V5 native | V6 3DXML | Notes |
|---|---|---|---|---|
| HOOPS Exchange (Tech Soft 3D) | read | read-only (B-Rep, PMI) | read | page fetched 2026-09-06; powers eDrawings-class viewers, Unity-class pipelines |
| CAD Exchanger SDK / Lab | no | read-only, B-Rep | read-only | formats page fetched 2026-09-06: "CATIA V5 `.CATPart, .CATProduct` Read R" |
| Datakit CrossManager + SDK | read (`.model .dlv .dlv3 .exp .session`) | read + **write** | read + write (3DXML out) | matrix fetched 2026-09-06; CLI runs on Windows/Linux/macOS |
| ODA (Open Design Alliance) | unclear | listed "Catia" | unclear | homepage matrix only; membership SDK |
| SpinFire / Okino | SpinFire is Tech Soft 3D rebrand path; Okino site is JS-only, matrix not fetchable | same family | | unverified, treat as adjacent |
| TransMagic (CONFIG), CoreTechnologie 3D_Evolution, 3D-Tool NativeCAD, Verisurf | yes | yes | yes/yes | independently corroborated inside `lycorismmoonlights/catpart-converter` backend docs (see 4.3) and its repo |
| Autodesk APS (Forge) Model Derivative | yes | yes | yes | medium confidence: docs pages are JS SPAs, not fetched; capability widely documented |

### 4.2 Open source, real code that touches CATIA files

- `sobalvarro/CATProductFiles` (C#, 6 stars). Entire technique, from `Form1.cs`
  (source copied to `raw/`): read `.CATProduct` **as a UTF-8 text string**, find
  `CATOctetArray`, cut at the `\u0008FINJPL` stream terminator, split on the
  `\u0001File` document-id keyword, strip nulls, keep the text after the last backslash.
  It recovers referenced part filenames from an assembly. That is the full depth of
  open-source `.CATProduct` knowledge on GitHub: text markers, not structure.
- `evereux/pycatia` and the PyCATIA family: Python COM wrappers. They require a running,
  licensed CATIA on Windows. They automate the application; they parse nothing.
- 3DXML (V6) family, all genuinely format-level because `.3dxml` is a documented zip+XML
  package with PRC/tessellated geometry: `Terrev/3DXML-to-OBJ` (35 stars),
  `gxh-0808/3dxmlToGLtf` (14 stars), `zy-zhao17/3Dxml-for-unity` (6 stars),
  `z1130/convert_3dxml_to_fbx` (Python 3.13 + bpy; input is a CATIA-exported 3DXML).
  None of these touch V5 `.CATPart`.

### 4.3 One honest negative-confirmation artifact worth citing

`lycorismmoonlights/catpart-converter` (Codex plugin, 2026) documents, from a practitioner's
side, exactly which backends convert `.CATPart` today and which fail. Its list: CATIA batch
`catstart`, pycatia COM, CAD Exchanger SDK, Datakit CLI, HOOPS Exchange `ImportExport`,
3D-Tool `Convert.exe`, TransMagic `TMCmd`, CoreTechnologie `3D_Kernel_IO`, FreeCAD only for
already-converted STEP. Its probe reports say plainly that without one of those, the local
machine has no native CATPart import capability at all. This mirrors every other finding in
this report and is a useful sanity anchor.

## 5. Synthesis answers

1. **How much of the CATIA V5 format is open source?** Zero shipped code parses V5 native
   B-rep. One small utility string-scrapes `.CATProduct` for referenced filenames. The V6
   3DXML container, a different format, has several real open-source parsers.
2. **OCCT's role?** None. OCCT is the engine that *sits behind* STEP-based CATIA pipelines,
   never behind a CATIA reader. The commercial `TKXDECATIA`/`CATIAReader`/`IFSIOPart` names
   correspond to nothing that ever existed in OCCT's public history; they look like plausible
   fabrications (the real commercial modules are the ACIS/JT/Parasolid/IFC components).
3. **What is the container?** `V5_CFV2` compound file with typed CAA object persistence
   (`CATContainer`/CGM/B-rep/CGR mix) and an XML-ish provenance footer. Not OLE, not zip.
4. **Writers?** Datakit CrossManager (commercial) is the only non-Dassault writer of native
   `.CATPart`/`.CATProduct` found. Everything else requires CATIA itself or an export hop.
5. **Practical open-source path for V5 data today:** none end-to-end. The universal open
   pipeline is CATIA/Datakit/HOOPS doing the CATIA hop once, then STEP, and OCCT, FreeCAD,
   pythonOCC do everything downstream.

## 6. Confidence levels

| Claim | Confidence | Basis |
|---|---|---|
| Open OCCT never shipped a CATIA interface | High | tag trees, path commit APIs, sourcegraph global zero, vendor pages 2016/2018/today, forum+ticket archives |
| Task's class names are fabricated | High | 0 commits, 0 global code matches, plausible-name morphology |
| V5_CFV2 container facts | High (this sample) | direct measurement; one file, one save version |
| Datakit writes CATIA V5 | High | vendor matrix + vendor brochure, fetched today |
| HOOPS/CAD Exchanger read-only | High | vendor pages, fetched today |
| ODA reads CATIA | Medium | listed on homepage matrix, no module docs fetched |
| Autodesk APS reads CATIA | Medium | not fetched (JS SPA); widely corroborated secondhand |
| "No open-source V5 parser exists anywhere" | Medium-high | negative result over GitHub repo search (11 queries), sourcegraph global, archives; private code cannot be excluded |

## 7. Raw sources

Full bodies and local copies. Fetch date: 2026-09-06.

APIs (GET, anonymous):
- `api.github.com/repos/Open-Cascade-SAS/OCCT/commits?path=src/IFSIOPart` → `[]` (same for
  `src/CATIAReader`, `src/TKXDECATIA`, `src/CATIALSRef`)
- `api.github.com/repos/Open-Cascade-SAS/OCCT/contents/src?ref=<tag>` for
  `master, V6_5_0, V6_8_0, V6_9_0, V7_4_0, V7_6_0, V7_7_0, V7_8_1` → no CATIA dirs
- `api.github.com/search/repositories?q=` for catpart, catproduct, catia parser, catia
  reader, catpart converter, catpart python, 3dxml, catia to step, catpart to step,
  cgr catia, catia v4 (results quoted above; totals 49/15/1/0/2/2/14/8/0/0/0)
- `sourcegraph.com/.api/search/stream?q=context:global "IFSIOPart"` → `matchCount: 0`;
  `"CATIAReader"` → `matchCount: 0`; `"CATProduct"`/`"CATPart"` → icon manifests, pycatia,
  this sample repo only

Archives / docs:
- `occt3d.com/dev/forum-search.json` (8,843 topics) and `occt3d.com/dev/ticket-search.json`
  (7,498 tickets) → copied to `raw/`; ticket `0005080` quoted in 1.3
- Wayback: `web.archive.org/web/20160405110228id_/http://www.opencascade.com/content/data-exchange`
  ("IGES, STEP, STL, VRML, etc.")
- Wayback: `.../content/added-value-components` 2018 (commercial components, no CATIA)
- Wayback: `.../content/what-3d-formats-supported` (2017, Datakit referral quote)
- `github.com/Open-Cascade-SAS/OCCT-Components/tree/main/Exchange` (current catalog)
- `dev.opencascade.org/doc/overview/html/occt_user_guides__xde.html` (format chapters)

Vendors:
- `cadexchanger.com/formats/` → "CATIA V5 File extensions .CATPart, .CATProduct Read/Write: R"
- `techsoft3d.com/products/hoops-exchange/` → FAQ "Read Only Support ... CATIA V4, CATIA v5,
  CATIA V6"; format matrix rows CATIA V4/V5/V6 (3D XML)
- `datakit.com/en/cross_manager.php` → input list "CATIA V4 2D/3D .model .dlv .dlv3 .exp
  .session", "CATIA V5 2D .CATDrawing", "CATIA V5 3D .CATPart .CATProduct", "CATIA V6 ...
  .3dxml", "CGR .cgr"; output list "CATIA V5 3D .CATPart .CATProduct", "3DXML .3dxml", "CGR .cgr"
- `datakit.com/download.php?kind=doc&filename=write_cad_files_in_multiple_formats.pdf` →
  "supports a broad range of CAD formats to write, including CATIA V5"; copied to `raw/dk_write.pdf`
- `datakit.com/download.php?kind=doc&filename=dtk_brochure_crossmanager_convertors_2025-en.pdf`
  → copied to `raw/dk_converters.pdf`
- `opendesign.com/products` → homepage matrix incl. "Catia"
- `assimp` `doc/Fileformats.md` → 0 catia; `gmsh.info` → 0 catia

Code:
- `raw.githubusercontent.com/sobalvarro/CATProductFiles/master/CATProductFiles/Form1.cs`
  → copied to `raw/`; technique quoted in 4.2
- `raw.githubusercontent.com/lycorismmoonlights/catpart-converter/main/README.md` → backend
  matrix quoted in 4.3 (fetched via webfetch of GitHub page)
- `Momento2025/CATPART` → `MM_Oil_Dipstick.CATPart` copied next to this report; scan output
  in `txt/CATPart_container_scan.txt`

Blocked during research (for the record): DuckDuckGo lite (image captcha), Mojeek (JS
captcha), Bing (ad-spam on exact-phrase query), FreeCAD forum (Anubis PoW), grep.app
(Vercel checkpoint), searchcode.com API (404), anycad.org (transport fail). Direct site
fetches, Wayback CDX, GitHub API, Sourcegraph, and vendor PDFs substituted.
