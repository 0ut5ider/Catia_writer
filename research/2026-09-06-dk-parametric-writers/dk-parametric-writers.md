# Parametric-native CAD formats: storage, open writers, and Datakit-to-CATIA V5 viability

- Date: 2026-09-07
- Role: web research agent (opencode session)
- Question: For each parametric-native format (.sldprt, .ipt, .par Solid Edge, .prt Creo/NX, .f3d, .model CATIA V4, .3dm), does the file store the parametric history, does an open-source writer exist, and which format can we generate today so that Datakit converts it to CATIA V5?
- Model: flashnext/flashnext-w4a16-fp8ple
- Raw data: `./raw/` in this directory.

## TL;DR verdict

| Format | Stores parametric history? | Open-source writer? | Verdict for our pipeline |
|---|---|---|---|
| .sldprt (SolidWorks) | Yes (features, sketches, parameters in proprietary streams; geometry is embedded Parasolid XT) | No. Readers only. | Unusable without a SolidWorks license (COM API). |
| .ipt (Inventor) | Yes (full feature tree; model geometry is embedded ACIS) | No. Readers only (free Apprentice DLL is read-only). | Unusable without an Inventor license. |
| .par (Solid Edge) | Yes (Parasolid payload plus feature data in a Compound File Binary container) | No. | Unusable without a Solid Edge license. |
| .prt (Creo / NX) | Yes (Creo: PSB container with feature data; NX: OPC/CFB container, embeds JT 9.x scene graph) | No. NXOpen requires an installed, licensed NX; Creo needs the licensed toolkit. | Unusable. |
| .f3d (Fusion) | Yes, verified in-file (Sketch/Feature/Revolve/SketchesRoot tables in the design segment stream; ShapeManager B-rep blobs separate) | No open writer. Closed writers exist: Fusion desktop API (`ExportManager.createFusionArchiveExportOptions`) and the paid APS Automation API for Fusion (cloud). | Usable only as a licensed/cloud generation path, not open source. |
| .model (CATIA V4) | Yes, in the V4 "specification" sense: V5's native import offers CATIA_SPEC (replayable parametric features) and CATIA_RESULT (dumb solid). | No. No public reader exists; even the best open effort validates only the MODEL header. | Unusable as a write target. |
| .3dm (Rhino) | No native feature history. Object history, layers, materials, blocks, user strings yes. | YES: rhino3dm (MIT). Verified end-to-end on this machine. | The only format where an open writer works today. Carries geometry plus recipe metadata, not feature history. |

Bottom line: no open-source tool writes a parametric-history-native file for any mainstream CAD kernel today. If the pipeline must be open and offline, generate `.3dm` with rhino3dm and put the build recipe in per-object user strings; the Datakit 3dm-to-CATIA V5 path delivers clean B-rep geometry but no editable features. If parametric editability inside CATIA V5 is mandatory, the format choice does not solve it; a STEP-based pipeline with a feature-preserving converter (Datakit's "intelligent" mode) or DS-native tooling is the better problem to attack.

## Evidence per format

### SolidWorks .sldprt

- History: features, sketches, and parameters live in proprietary streams. Geometry is an embedded Parasolid XT stream (`BlinkingSun/sldprt2step` extracts it: pure-Python XT reader, schema `SCH_13006`, converts SW parts to STEP).
- `schwitters/openswx` (18 stars, C++20, LGPL): reads SW files for metadata, properties, BOM, and preview images only. Handles both the OLE2 container (up to SW 2014) and the modern chunk container (2015+). No feature tree, no writer.
- `blussyya/sldprt-format-research`: a reverse-engineering knowledge base. Geometry is in `Contents/DisplayLists` streams; the face block layout is documented. Their `KNOWN_INVARIANTS.md` marks the `Config-0` partition as high-entropy and unreadable, so the feature/spec streams are not cracked.
- `SldprtNet` (arXiv:2603.13098, ICRA 2026, 242k part dataset): its encoder and decoder call the SolidWorks COM API, so it needs a licensed Windows SolidWorks install. No public code repository found.
- GitHub search for any .sldprt writer: nothing. Parasolid XT writers that exist (`khoanguyen-3fc/ps-parser`, `akiselev/xt-parser`) are read-only parsers, and a bare XT file is not a .sldprt anyway.

### Inventor .ipt / .iam

- `jmplonka/InventorLoader` (169 stars, FreeCAD workbench, GPL3): reads IPT/IAM via `olefile` (OLE2 container). The IPT file contains a full ACIS model representation; the workbench also imports SAT/SAB directly. Reader only.
- Autodesk Apprentice: a free, redistributable, read-only API for Inventor files. It cannot write.
- No open writer exists. Writing needs Inventor's COM/Python API on a licensed install.

### Solid Edge .par / .psm

- Container facts from `raw/format_support.md` (JFK-Solutions native-cad-viewer `FORMAT_SUPPORT.md`, the most current public per-format decode notes): .par/.psm are Compound File Binary documents with a display cache and a Parasolid payload; the project decodes metadata only.
- GitHub searches for Solid Edge par writers or parsers return nothing real. The SolidEdgeCommunity Reader sample predates modern formats and depends on the installed Solid Edge COM API.

### Creo .prt and NX .prt

- Creo: the modern .prt is a PSB container. The public viewer decodes it to display strips (`#UGC:2` tags) only. Feature and sketch data are inside, but no public parser exists. Writing requires the licensed Creo Open Toolkit or J-Link.
- NX: .prt is an SPLM/CFB container that embeds a JT 9.x scene graph (per `raw/format_support.md`). All public tooling is NXOpen (Python/C#), which runs only inside a licensed installed NX. The JT Open Toolkit writes JT, not .prt, and JT is tesselation plus PMI, not history.

### Fusion .f3d (primary evidence, this session)

I downloaded a real 2026-era archive (`isa-esc/CAD-training-projects`, Lollipop.f3d, 274 KB; saved in `raw/lollipop.f3d`) and unpacked it. Full listing: `raw/f3d_zip_listing.txt`.

Structure (modern generation, verified):

- Plain ZIP. Root folder `FusionAssetName[Active]/` holds segment folders: `FusionDesignSegmentType1`, `FusionBrowserSegmentType1`, `FusionACTSegmentType1`, plus `ProteinAssets.BlobParts`, `Breps.BlobParts`, `OGS.BlobFolder`, `Previews`.
- Geometry kernel: `Breps.BlobParts/*.smb` and `*.smbh` are `ASM BinaryFile4 / Autodesk Neutron / ASM 232.3.0.65535` files. "Neutron" is the internal name of the ShapeManager kernel. So .f3d stores ShapeManager B-reps directly, not FBX.
- Parametric data: `FusionDesignSegmentType1/BulkStream.dat` contains the serialized object tables, including the strings `FeatureMetaType`, `RevolveFeatureMetaType`, `SketchMetaType`, `SketchesRoot`, `FeatureOperationIdFlag` (see `raw/f3d_stream_strings.txt`). The design timeline and sketches are inside these streams. The stream format is proprietary and undocumented.
- `Properties.dat` is small JSON (`{"docstruct":{"version":"1.0.0","type":"part-design",...}}`). `*.protein` files are nested ZIPs (Fusion's old internal codename "Project Protein").
- The older generation reportedly paired an FBX with an "SMDB" database. I found no primary documentation for SMDB and no public schema. Treat that claim as unverified; it is irrelevant now because current exports use the structure above.

Writers:

- Inside Fusion (closed, free with the app, desktop GUI required): `ExportManager.createFusionArchiveExportOptions(path)` plus `exportMgr.execute(...)` writes .f3d. Verified in working scripts (`Simonlebucheron/f360_export_3dprint_file`) and in the API docs.
- Cloud: APS Automation API "Execute a Fusion Script" (Design Automation v3, Fusion-specific section: arguments, callbacks, "Running Without User Identity"). This runs real Fusion in Autodesk's cloud; billed in APS units. Fusion desktop license terms apply to the API; the API itself ships with every Fusion install, including personal use.
- Limits (verified by `max05210238/Fusion360-Archiver`, a maintained batch tool): the in-app API cannot export assemblies with linked external components as .f3d; those come out as .f3z (cloud Download action, optionally Zstandard-compressed per format_support.md). No headless mode exists on desktop.
- No open-source parser or writer for any part of the container.

### CATIA V4 .model

- Feature content: DS's documented V4-to-V5 path (mirrored help, quoted in `raw/catia_v4_to_v5_cati.txt`, cati.com 2020) shows two paste modes: `CATIA_SPEC` "will create part features in V5 that correlate to the model features in V4. This will give you a parametric model that can be edited", and `CATIA_RESULT` produces only the solid geometry, not editable. So V4 models carry a specification that V5 replays as features.
- Open source: none. GitHub code search for a CATIA V4 parser finds only commercial SDK documentation (HOOPS Exchange). JFK's viewer validates the `MODEL` header bytes and states the V4 B-rep records are not publicly decoded.
- Note: this is moot for us. Even if we could decode V4, generating a valid .model requires DS tooling. Its only pipeline role is as an input on the Datakit side.

### Rhino .3dm (the open writer, hands-on verified)

Environment: rhino3dm 8.32.2 in a local venv (`raw/` keeps the script `t3dm.py`, `test.3dm`, `v8.3dm`, `v5.3dm`).

Verified by writing and re-reading files:

- `rhino3dm.File3dm().Write(path, version)` works fully offline for archive versions 5, 7, and 8. Header: "3D Geometry File Format".
- Writable: NURBS curves, Breps (`CreateBox` etc.), meshes, extrusions, layers, instance definitions (blocks), named views, units, and per-object user strings.
- Render materials work: `Materials.Add` succeeds even though the stub file omits it; link objects with `ObjectAttributes.MaterialIndex` plus `MaterialSource`.
- User strings (`ObjectAttributes.UserStringCount/Set/UserStringNames`) give us a durable slot for a generator recipe (generator name, parameters, version) inside the file.
- Not available: no API to write `File3dmPlugInDataTable` (the table is exposed as an opaque read surface in both Python and .NET; a GitHub code search of `mcneel/rhino3dm` confirms no Add path), so we cannot embed a Grasshopper replay blob. No ActiveSnapshot API. Rhino's own object history is not written by rhino3dm.

Ecosystem:

- License: MIT. McNeel actively maintains it; official standalone writer samples ship in `mcneel/rhino3dm` developer samples (`SampleCreateCircleAndWriteTo3dmFile.py`, `SampleAddMaterial`, `SampleAddInstanceDefinition`).
- Production users of the standalone writer path: pyRevit (`pyrevitlib/rpw/extras/rhino.py`, wide AEC install base), plus McNeel's own samples and numerous AEC/CFD tools (e.g. `flexcompute/Flow360`).
- The parametric option in the McNeel stack is Rhino.Compute: it evaluates a real Grasshopper definition server-side on a licensed Rhino+GH server and returns results. That is a licensed service, not open source.

## Recommendation for the Datakit-to-CATIA-V5 pipeline

1. If "open source generation, no licenses" is the hard constraint: generate .3dm with rhino3dm. Deliver B-rep geometry with layers, materials, and a recipe in user strings. Expect Datakit to hand CATIA V5 clean but history-free solids. This is the only verdict table row that is "Yes" for an open writer.
2. If CATIA V5 must receive an editable feature tree from our files, no native-format route exists in open source. Two realistic options remain: (a) generate .f3d through the Fusion API on a licensed desktop instance or the APS Fusion cloud (then Datakit f3d-to-V5; the fusion-side geometry is ShapeManager B-rep, and whether features survive is a Datakit question, out of scope here), or (b) attack the STEP route with Datakit's feature-recovery mode, which is the industry-standard answer for this exact problem.
3. Do not plan on .sldprt, .ipt, .par, .prt, or .model as generation targets. Every write path needs the licensed authoring CAD, and no container is fully public.

## Search-method note (for the next agent)

Direct web search tools are unavailable here and search engines block `curl`. Working recipe: `curl "https://r.jina.ai/<url>"` for page text (rate limited, roughly 20 per minute), `https://r.jina.ai/https://www.google.com/search?q=...` for result pages (parse `### [` lines), and the `gh api search/code` plus `search/repositories` endpoints for code evidence. `web.archive.org` CDX queries timed out. `/tmp` is quota-full on this box; scratch lives in `~/scratch/dkpw/`.
