# Datakit-ingestible CAD writers in open-source Python: hands-on verification

Date: 2026-09-06/07 (sandbox clock shows Sep 7)
Agent role: hands-on verification (write, reopen, inspect)
Question: which open-source Python writers can produce files Datakit can ingest, with maximum semantic richness (B-rep, assembly trees, names, colors, layers, metadata)?
Model: flashnext/flashnext-w4a16-fp8ple

## TL;DR results table

| Format | Library (version) | Writes? | Semantics achieved | Evidence | Verdict |
|---|---|---|---|---|---|
| DXF R2018 | ezdxf 1.4.4 | Yes | Layers+colors, LWPOLYLINE/CIRCLE/TEXT, INSERT+ATTRIB, XDATA, MESH, 3DSOLID embedding ACIS | `a_rich.dxf` 70,514 B, all round-trips pass | Use. Primary 2D/DXF path. |
| SAT (ACIS text) | ezdxf 1.4.4 | Yes | Real ACIS 32.0 B-rep (body/lump/shell/face/loop/plane-surface) | `a_box.sat` 4,174 B, header `700 0 1 0` + `@12 ACIS 32.0`, ezdxf re-`api.load` OK | Use. Only SAT writer on PyPI. |
| SAB (ACIS binary) | ezdxf 1.4.4 | Yes | Same body, binary container | `a_box.sab` 5,574 B, magic `ACIS BinaryFile(` | Use. |
| STEP AP214 | pythonocc-core 7.9.3 | Yes | Assembly tree + per-part names + colors, B-rep solids + fused/cut sketch | `b_assy.step` 62,453 B; `PRODUCT('BRACKET-ASSY',...)` + 2× `NEXT_ASSEMBLY_USAGE_OCCURRENCE`; independent OCP reopen shows ASSY/REF tree | Use when you need XCAF-level control. |
| STEP AP214 | cadquery 2.8.0 (OCP 7.9.3) | Yes | Same tree/names/colors via `Assembly.add(name=, color=)` | `c_assy.step` 51,128 B, OCP reopen: `'CQ-ASSY' [ASSY] -> 'BASE-PLATE' [REF], 'RISER' [REF]`; 4 COLOUR entities | Use. Friendliest high-level API. |
| STEP | build123d 0.11.1 | Parts only | Single solid or unnamed compound; **no Assembly class exists in 0.11.1** | `c_b123d.step` 32,851 B; grep: no `class Assembly` anywhere in package | Parts fine; assemblies: use cadquery or pythonocc. |
| IGES | pythonocc-core 7.9.3 (OCC) | Yes | Surfaces/wireframe + color records (entity 124) | `b_parts.iges` 46,656 B, header `Open CASCADE IGES processor 7.9` | Use. Only real IGES writer found. |
| IGES (read) | pyiges 0.3.4 | **No (reader-only)** | Parsed our OCC IGES: 183 items (48 Line, 2 CircularArc, 20 Face, 22 Loop, 2 EdgeList/VertexList, 2 Transformation) | `d_pyiges.py` output | Keep as independent validator; mesh needs `pyiges[full]` (geomdl+pyvista). |
| 3DM v7 | rhino3dm 8.32.2 | Yes (container) | Layers+colors, mesh, **B-rep solids** (`Brep.CreateFromBox`), object names, per-object user strings, units, instance definitions (blocks) as assembly-like tree | `e_model.3dm` 22,022 B reopen: 2 named layers, `BREP-BOX 6faces solid=True`, user string `PART=BRACKET-001` intact; `e_inst.3dm`: `PIN-BLOCK` idef + named instance with xform | Use for the 3DM row, with limits below. |
| JT | open source: none | No | n/a | GitHub search "JT writer/JT encoder/openjt" 2026-09-07: no maintained writer; OCCT JT Assistant fork `cbsghost/oce-jt` is reader-only, last push 2019 | Do not plan on JT from open source. Spec is free; implementations are not. |

## Environment

- Python 3.11.16 venv (`uv`-managed) at `/home/outsider/.cache/dk-writers-venv`; pythonocc-core via conda-forge env `/home/outsider/.cache/dk-writers-conda` (pip wheel is a dead 0.16 placeholder; conda only).
- cadquery ran in the pre-existing shared venv `/tmp/cqenv` (Py 3.14, cadquery 2.8.0, OCP 7.9.3.1.1). The 3.11 OCP wheel lacks `IVtkOCC`, which cadquery 2.8 imports at load time; the 3.14 wheel has it.
- `/tmp` is a quota-exhausted tmpfs here; all real work lived in `/home/outsider/.cache/dk-writers-work/` (`/tmp/dk-writers` is a symlink).

## Test details

### A. ezdxf: DXF + ACIS (pass)

One DXF carries: 3 colored layers, LWPOLYLINE, CIRCLE, TEXT, a block with ATTDEF rendered as INSERT with ATTRIB values (PART=BRACKET-001, REV=C), XDATA (app `DK_TEST`; string/real/int), a MESH, and a 3DSOLID whose ACIS body was built with `ezdxf.acis.api.body_from_mesh` + `export_dxf`. SAT and SAB written via `ezdxf.acis.api.save`/`save_sab`. Reopen checks all passed: entity counts, ATTRIB values, XDATA, ACIS body reloaded from both the DXF 3DSOLID and the standalone SAT.

Gotchas: `MeshBuilder` lives in `ezdxf.render.mesh`; `set_xdata` takes `(code, value)` tuples; `body.entities()` is a method.

### B. pythonocc-core: XCAF STEP + IGES (pass)

Model: two boxes fused, cylinder cut, sketch-L polyline extruded (the OCC 7.9 `BRepBuilderAPI_MakePolygon` two-point constructor + `Add` + `Close`). Assembly built on XCAF: `TopoDS_Compound` -> `shapeTool.AddShape(comp, True, False)` -> child labels -> `TDataStd_Name.Set(child_label, "BASE-PLATE")`, colors via ColorTool. STEP written with `STEPCAFControl_Writer` (name/color/layer modes on), schema AP214IS, write status 1 (Done). IGES via `IGESControl_Writer("MM", 11)`.

Proof (STEP text):

```
PRODUCT('BRACKET-ASSY','BRACKET-ASSY','',(#8));
NEXT_ASSEMBLY_USAGE_OCCURRENCE('2','BASE-PLATE',...);
NEXT_ASSEMBLY_USAGE_OCCURRENCE('3','L-GUSSET',...);
```

Independent reopen with the OCP bindings (different build than pythonocc) printed the same tree.

API drift found (OCC 7.9, both bindings): `XCAFDoc_ShapeTool` lost `AddChild/MakeAssembly/MakeIndependent/GetType/RootLabels`; static methods are `*_s`-suffixed; `STEPCAFControl_Writer.Transfer(doc)` takes the whole document (passing `doc.Main()` fails silently, write status 0, later segfault on reopen); `TDF_ChIterator` is now `TDF_ChildIterator`; pythonocc's `TDataStd_Name` has no Get/Find reader (binding gap; names verified from STEP text and OCP reopen).

### C. cadquery + build123d: STEP (pass with one gap)

cadquery: workplane feature chain (plate, through-hole, boss) exports clean AP214; `cq.Assembly(name=, add(name=, color=))` produces a named, colored tree that an independent OCP XCAF reader resolves as `'CQ-ASSY' [ASSY]` with two `REF` children. Also demonstrated STEP -> GLTF through cadquery (`b_assy.step` -> 8,048 B gltf + 17,544 B bin), so a mesh/web pipeline is covered too.

build123d 0.11.1: part export is clean AP214. But grep confirms **no `Assembly` class anywhere in the package**: assembly support was removed upstream. A `Compound([part1, part2.moved(...)])` exports multiple solids into one STEP, but without names, colors, or tree. Parts-only.

All STEP files from every writer carry `FILE_SCHEMA(('AUTOMOTIVE_DESIGN { 1 0 10303 214 1 1 1 1 }'))` (AP214).

### D. pyiges: reader, not writer

No writer API exists (`Iges(filename)` parses; no `write`). Used as a cross-validator: it parsed our pythonocc IGES into 183 typed items including Face/Loop/EdgeList/VertexList records. `read_as_mesh` needs the `full` extra (geomdl, then pyvista).

### E. rhino3dm: real .3dm with limits

Wrote v7 file: two colored named layers, two mesh objects with names and one carrying user string `PART=BRACKET-001`, plus a B-rep box (`Brep.CreateFromBox(Box(BoundingBox(...)))`). File magic `3D Geometry File Format` + version byte. Reopen: layers/colors/names/user string all intact, B-rep reopens as solid with 6 faces. Instance definitions (`InstanceDefinitions.Add` + `AddInstanceObject(InstanceReference, attrs)`) give blocks: `PIN-BLOCK` definition with a named transformed instance, reopened fine. Units preserved.

Limits: no free-form B-rep construction (analytic primitives only: box/cylinder/sphere/cone...), no STEP/IGES import, no file-level user-string writes (`File3dmStringTable` has only Delete/Count), no Notes setter. For complex B-rep inside .3dm you need real Rhino or OpenNURBS C++.

### F. JT: no open writer

GitHub searches (openjt, JT writer, JT encoder, JT file, 2026-09-07) find no maintained open-source writer. The OCCT "JT Assistant" exists only as a 2019-archived reader fork. The JT Open standard is publicly documented, but a from-scratch encoder is a C++ project, not a weekend Python task. Plan: deliver STEP/SAT/DXF/3DM and leave JT to commercial converters (which is, ironically, Datakit's own product line).

### G. ACIS/SAT on PyPI

`pypi.org/pypi/<name>/json` returns 404 for: acis, python-acis, satfile, satreader, opensat, pysat-file, acis-parser. ezdxf's built-in ACIS module is the only SAT/SAB writer. (OCCT does not speak ACIS at all; the commercial ACIS translators are what Datakit routes around.)

## Recommended generator stack

1. STEP AP214 with names/colors/tree: **cadquery** for authoring, its `Assembly` is one line per node. Drop to **pythonocc** XCAF when you need layer modes, free-form attribute injection, or OCC's exact writer settings. build123d only for parts.
2. SAT/SAB: **ezdxf** `ezdxf.acis.api.save`/`save_sab`.
3. DXF: **ezdxf** (layers, attribs, xdata, and optionally 3DSOLID-embedded ACIS in one file).
4. IGES: **pythonocc** `IGESControl_Writer`; validate with **pyiges**.
5. 3DM: **rhino3dm** for container semantics (layers, names, user strings, units, blocks) + mesh/analytic B-rep; expect real B-rep to come from elsewhere.
6. JT: skip in open source.
7. Mesh/web sidecar: cadquery `Assembly.save(..., exportType="GLTF")` (proven on a foreign STEP).

Install notes that matter: pythonocc-core is conda-forge only; cadquery 2.8 needs the OCP wheel variant with IVtk (the 3.11 build we hit lacked it); pyiges needs `pyiges[full]` for meshing.

## Reproduce

`scripts/` in this folder holds the exact tests: `a_ezdxf.py`, `b_pythonocc.py`, `c1_cadquery.py`, `c2_build123d.py`, `d_pyiges.py`, `e_rhino3dm.py`, `ocp_reopen.py` (shared independent reader). `samples/` holds every output file listed in the table plus run log `b_run.log`.

## Things worth remembering (surprises)

- build123d, the "modern cadquery successor", shipped 0.11.1 with assembly export deleted. The docs for 0.9-era tutorials that show `Assembly(name=...)` are now wrong for current pip.
- Two independent OCC binding projects (pythonocc conda build, cadquery-ocp pip build) both track OCCT 7.9, yet neither exposes a working `TDataStd_Name` read path in the assembly workflow; STEP text was the ground truth.
- The only open ACIS writer in the Python world lives inside a DXF library.
- `Transfer(doc.Main())` vs `Transfer(doc)`: one line difference, silent zero-output writer, segfault 30 seconds later. Instrument write status before debugging "empty STEP".
