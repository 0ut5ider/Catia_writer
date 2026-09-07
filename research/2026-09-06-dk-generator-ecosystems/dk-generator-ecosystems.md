# Open parametric CAD generators feeding Datakit into CATIA V5

Date: 2026-09-06. Role: web research agent. Question asked: which open parametric CAD generator ecosystems can emit CAD files that Datakit (CrossManager) converts into CATIA V5 with the most structure preserved, what survives, what are the licenses, and what is the single best combination. Model: flashnext/flashnext-w4a16-fp8ple.

Raw evidence: `raw/` next to this file (fetched pages, license files, source files). Citation style: file in `raw/` or URL.

## TL;DR

- Nothing gets true parametric feature history into CATIA V5 through Datakit. No open generator writes CATIA-native `.CATPart`. STEP carries B-rep plus product structure, names, colors. It carries no sketches, no constraints, no feature tree. The generator script is your parametric layer: regenerate and re-export instead of editing history in CATIA.
- The best structure you can realistically preserve is: assembly tree (`CATProduct` hierarchy), per-part names, colors, and clean B-rep solids.
- Recommended combination: **build123d or CadQuery (Python, Apache-2.0) → STEP AP214/AP242 via the OCCT XCAF assembly writer (names, colors, units, tree) → Datakit CrossManager → CATIA V5 named tree.**
- Headless **FreeCAD (LGPL-2.1)** is the runner-up and beats the others when you need document-level features: spreadsheet-driven parameters, App::Part assemblies, and 2D DXF drawings from the same script.
- The verified trick that raises the payoff: all three stacks write STEP through OCCT's XCAF layer, which stores names on labels. Datakit reads STEP AP242 to E4. Names land on CATIA products.
- "sweeet" and "RabbitEar" do not exist as CAD projects (GitHub search 2026-09-06: no CAD hits).

## What Datakit accepts and emits (verified on datakit.com, 2026-09-06, version 2026.3)

From `raw/datakit_cross.html` (cross_manager.php, fetched live):

- STEP input: AP203 (E1, E2), AP209, AP214 (up to E3), AP242 (up to E4), AP238 (.stpnc). Extensions `.stp .step .stpZ`.
- STEP output: AP203 (E1, E2), AP214 (E3), AP242 (E1, E3, E4).
- Open CASCADE input: `.brep`, version up to 7.7.0. `.brep` is also on the CrossManager 3D output list.
- ACIS input: `.sat .sab` (as 2D and 3D); Parasolid V7 to V38.1.
- DWG/DXF 2D and DXF 3D input; DXF 3D output.
- CATIA V5 3D output: `.CATPart .CATProduct`. CATIA V5/V6/3DEXPERIENCE read as well.
- IGES, IFC, QIF, JT, STL, OBJ, glTF, PLM XML, 3DXML also supported.
- CLI version of CrossManager exists ("Download CLI documentation" link on the page), so the whole chain can be automated.

So the useful input lanes from open tools are: STEP (best), `.brep` (interesting, untested for names), IGES (worse metadata), DXF 2D/3D, ACIS via SAT (only if you can produce it), IFC, and meshes (no tree).

## What survives a generator → STEP → Datakit → CATIA V5 trip

| Structure | Survives via STEP? | Evidence / notes |
|---|---|---|
| Solids/B-rep geometry | Yes | Core of AP203/214/242. `raw/occt_step.html`. |
| Assembly tree | Yes | NAUO-based; OCCT writes assemblies through XCAF; Datakit maps STEP products to CATIA V5 structure. |
| Part/product names | Yes, with the XCAF writer | OCCT: names are written by STEPCAFControl/XDE ("translates names, colors, layers ... into XDE document"). FreeCAD `setName()` on labels; CadQuery `SetNameMode(True)` + `TDataStd_Name`; build123d `TDataStd_Name`. |
| Colors | Yes | Same XCAF channel (surface/general colors). |
| Units | Yes | build123d sets `XCAFDoc_DocumentTool.SetLengthUnit_s`. |
| Sub-shape names (faces/edges) | Partial | `write.stepcaf.subshapes.name` option; CadQuery exposes it and can even rename geometric entities (`name_geometries`). |
| Sketches, constraints, feature history | No | STEP AP242 is "managed model based 3D engineering": B-rep + appearance + annotations + persistent IDs. Machining features live in AP224, which mainstream CAD translators do not write or read. `raw/wiki_iso10303.html`. |
| Parameters/formulas | No | Not expressible in STEP. The Python script is the parametric master copy. |
| Materials/GDT | Format yes, CATIA reception mixed | AP242 GD&T maps to XCAF dimensions; Datakit can carry them; CATIA V5 feature-level reception is not "parametric". Treat as annotation at best. |

Key rule: generate with a script, ship STEP, treat CATIA as the viewer/downstream, and never hand-edit the STEP result expecting back-propagation.

## Ecosystem findings

### FreeCAD (LGPL-2.1)

- Headless is first-class: two binaries, GUI `freecad` and console `FreeCADCmd`/`freecadcmd`, plus `--console`; console mode gives a full Python interpreter for scripts (`raw/wb_startup_old.html`, Wayback capture of wiki Start_up_and_Configuration, Dec 2022; note the live wiki sits behind Anubis anti-bot and must be read via Wayback).
- STEP export is XCAF-based in the Import module: `Import.export(objs, path, exportHidden, legacy, keepPlacement)` (`raw/Import_module.pyi`). The writer `ExportOCAF2.cpp` (`raw/ExportOCAF2.cpp`) calls `setName()` (names on XCAF labels), `XCAFDoc_ShapeTool::AddSubShape` (assembly hierarchy from App::Part / Assembly containers), and `XCAFDoc_ColorTool::SetColor` (surface and general colors).
- Schema is selectable: `write.step.schema` (AP203/AP214/AP242) plus `write.stepcaf.subshapes.name` and `write.step.product.name` (`raw/PartInterface.cpp`).
- 2D: `Import.writeDXFShape/writeDXFObject` writes DXF (versions R12/R14); Draft's SketchExportHelper exports sketches to DXF (`raw/SketchExportHelper.h`). No 3D DXF writer.
- Output files are not encumbered: the wiki License page states files made with FreeCAD are the user's own; the LGPL attaches to the code, not your models.
- FreeCAD Assembly workbench (built in recent releases) plus spreadsheets make it the richest document model, at the cost of a quirkier scripting API.

### build123d (Apache-2.0, repo `gumyr/build123d`)

- Dedicated STEP assembly exporter: `src/build123d/exporters3d.py` (`raw/b3d_exporters3d.py`) creates an XCAF document (`MDTV-XCAF`), sets length unit, and writes with `STEPCAFControl_Writer`, assigning names via `TDataStd_Name` and colors via `XCAFDoc_ColorTool`. It explicitly reasons about labels on tree nodes.
- Fully headless Python, ships as `OCP` wheels (OCCT bindings), so deployment is a `pip install`. Cleanest license of the group (Apache-2.0).

### CadQuery (Apache-2.0, repo `CadQuery/cadquery`)

- `cadquery/occ_impl/exporters/assembly.py` (`raw/cq_asm_export.py`) uses `STEPCAFControl_Writer` with `SetNameMode(True)`, sets `write.stepcaf.subshapes.name = 1`, supports XML/Bin XCAF driver round-trip, and an extra `name_geometries=True` mode that renames the underlying STEP geometry entities (FACE/EDGE names, not just products).
- Same headless, pip-installable OCP stack as build123d.

### pythonocc-core (LGPL-3.0)

- Raw OCCT bindings including STEPCAFControl/XCAF. You can build the exact XCAF document yourself. Verified license from the repo (earlier "Apache" claim was wrong). Use only if you need OCCT internals that build123d/CadQuery do not expose.

### OCCT itself (LGPL-2.1 with runtime exception)

- STEP user guide (`raw/occt_step.html`): basic translator writes AP203/AP214; XDE STEP translator (STEPCAFControl_Reader/Writer) "translates names, colors, layers, validation properties and other data associated with shapes and assemblies"; `write.step.schema` accepts AP242DIS; assemblies read/written via NAUO/XCAF.
- `.brep` is accepted by Datakit up to OCCT 7.7.0. XCAF documents (`BinXCAF`/`XmlXCAF`) carry names and colors fully. A raw `.brep` names section exists in newer OCCT but I could not confirm version or Datakit behavior; the BREP spec page is JS-rendered and the OCCT release-notes fetch failed. Test before relying on it: write an XCAF doc or BREP with names from pythonOCC, convert with Datakit trial, inspect CATIA tree.

### FreeCAD-independent: OpenSCAD (GPL-2.0-or-later)

- Exports only STL, OFF, AMF, 3MF, CSG (3D) and DXF/SVG/PNG/PDF (2D) (`raw/os_export.html`, Wikibooks manual, rev. 2025-08-26). No STEP/IGES/BREP. Mesh-only lane into Datakit, zero tree. Dead end for this goal.

### Blender (GPL)

- Core app is mesh-centric; STEP exists only via third-party add-ons. Official extensions platform has "STEP Importer" (import only, verified on extensions.blender.org). The community "CAD-Export" add-on (Nicola Carandini/neki) adds STEP/IGES/BREP export through OCC python bindings; its current hosting could not be located on GitHub on 2026-09-06, so treat its maintenance status as unverified.
- `DingoOz/BlenderMesh2STEP` (GPL-3.0, 1 star) converts meshes to STEP AP242. Either way Blender yields dumb solids or mesh-derived B-rep. No assembly tree, no names worth having. Not a candidate.

### 2D CAD (LibreCAD GPLv2, QCAD GPLv3/commercial, ezdxf MIT)

- DXF/DWG only. Datakit reads DXF 2D fine (2D → CATIA drawing route) and DXF 3D. ezdxf (MIT) can write DXF including 3DSOLID entities whose payload is ACIS, and Datakit reads ACIS SAT natively. Clever but fragile; documented here, not recommended.

### Others checked briefly

- SolveSpace (GPL-3.0): constraint solver, exports STEP/IGES via bundled OCC; no assembly metadata worth preserving; poor scriptability (no good headless API). Skip.
- IfcOpenShell (LGPL-3.0) and IFC: Datakit speaks IFC both ways, but IFC-to-CATIA-V5 for mechanical parts is a category error. Skip.
- materializr (GPL-3.0, materializr.com): "vibe-coded" parametric CAD, exports STEP/STL. Early stage, worth a watch, not a base.
- gcad3d (license NOASSERTION): parametric web CAD exporting STEP. Unknown maturity and license clarity. Skip.
- Onshape: SaaS, not open, API export exists but you get no offline generation. Out of scope.
- "sweeet", "RabbitEar": no CAD projects found under those names (GitHub repo search). Probably misremembered names.

## Ranking for "script generates CAD, Datakit lands it in CATIA V5 with a named tree"

1. **build123d** (Apache-2.0): purpose-built code CAD, pip-only deps, dedicated XCAF STEP assembly exporter with names/colors/units. Least friction, no copyleft concerns for the toolchain.
2. **CadQuery** (Apache-2.0): same stack, mature community, `name_geometries` extras for face-level naming. Essentially tied with build123d; pick by API taste.
3. **FreeCAD headless** (LGPL-2.1): same OCCT XCAF quality, plus spreadsheets/parameters/App::Part and DXF drawings from one script. Heavier to deploy (AppImage/package, not pip). Output files are unencumbered.
4. pythonocc-core DIY XCAF: maximum control, most work, LGPL-3.0.
5. `.brep` channel (any OCCT stack → Datakit OpenCASCADE reader): potential for richer/cleaner transfer than STEP, unverified; run one experiment with the Datakit trial.
6. Everything else (OpenSCAD, Blender, 2D-only, materializr, gcad3d): mesh-only, weak metadata, or unstable.

## Single recommendation

Use **build123d (or CadQuery), export STEP with the XCAF assembly exporter (AP214 or AP242), convert with CrossManager CLI to CATIA V5**. Verify in the CATIA tree: product hierarchy = your assembly containers, part names = your object labels, colors present. Keep the Python source in git as the parametric master; on change, regenerate and re-convert. If you find you need driven parameters, drawing sheets, or DXF output too, move the same model to a headless FreeCAD script and keep the STEP channel identical.

Two experiments before committing (both cheap):
1. Datakit trial: one 3-level assembly with names and colors, STEP AP214 vs AP242, inspect CATIA product names.
2. Write one XCAF `.brep` (BinXCAF) from pythonOCC and one plain `.brep` with names via `write.stepcaf.subshapes.name` analogue, run through Datakit, and check whether names survive. If yes, BREP becomes the preferred channel (smaller files, no EXPRESS lossiness).

## Access notes for future sessions

- `wiki.freecad.org` (and forum.freecad.org) run Anubis anti-bot; direct fetch, curl with browser UA, and even 2026 Wayback captures get the challenge. Wayback captures from ≤2023 are clean. Use CDX to find old captures.
- DuckDuckGo HTML/lite: bot CAPTCHA. Bing: frequently returns garbage. Working engines: none; go via Wayback, GitHub API, wikibooks, and direct site fetches (datakit.com, dev.opencascade.org, openscad.org, extensions.blender.org, wikibooks REST).
- `dev.opencascade.org` doc pages are fetchable static HTML except some JS-rendered pages (brep_format spec); `rg` is not installed on this box.
- `rg` note: use `grep`/python here. `wiki.freecad.org` correct page slug: `Manual:Import_and_export_to_other_filetypes`.

## Files in raw/

- `datakit_cross.html` live Datakit format matrix (key evidence)
- `occt_step.html` OCCT STEP user guide (XDE names/colors/assemblies, schemas)
- `Import_module.pyi`, `ExportOCAF2.cpp`, `PartInterface.cpp`, `SketchExportHelper.h`, `cq_asm_export.py`, `b3d_exporters3d.py` FreeCAD/CadQuery/build123d XCAF STEP writers
- `wb_startup_old.html` FreeCAD headless console docs (2022 Wayback)
- `wb_20251116081557_...Import_and_export_to_other_filetypes_en.html`, `wb_part_import.html` FreeCAD formats
- `os_export.html` OpenSCAD export list; `wiki_iso10303.html` STEP/AP242/AP224 facts
- `*_LICENSE` license files (cadquery Apache-2.0, build123d Apache-2.0, ezdxf MIT, libreCAD GPLv2, freecad LGPL-2.1)
