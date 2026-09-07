# Datakit / Spatial 3D InterOp: what reaches a CATIA V5 CATPart, per source format

- Date: 2026-09-06
- Role: web research agent (fetch-only; search engine was CAPTCHA-blocked, all sources fetched by direct URL)
- Question: For each input format, what does the Datakit CATIA V5 writer actually produce in the CATPart? Does any input format carry parametric, feature, or sketch history into CATIA?
- Model: claude (opencode session, Cerebo)
- Product version examined: DATAKIT SDK V2026.3 (Doxygen docs at datakit.com), CrossManager/CrossCad product pages (datakit.eu), Spatial 3D InterOp product page (spatial.com), July 2026 release.

## Verdict

**No input format delivers feature, sketch, or parametric history into a Datakit-written CATPart.** The ceiling, for every source, is: B-rep geometry written as CATIA *Imported* objects (Imported Body / Imported Surface / Imported Curve / Imported Point), mesh as Cloud Body, plus assembly structure, names, colors, materials, and inert user metadata. The CATIA specification tree in the output contains only container nodes (GeometricSet, PartBody/hybrid body, MechanicalTool). No Part Design feature, no sketch, no driven dimension, and no formula is ever created. A converted part is editable in CATIA only as dumb geometry (healing, FreeStyle/Generative Shape, body replacement), not by editing feature history.

This is not a per-format gap. It is a property of the writer: the CATIA V5 write API has no entry point for features, and the official write mapping table has no mapping row for features. The read side *does* parse feature history from CATIA V5/V6, SOLIDWORKS, NX, and Creo, but that data model (Dtk_feat_*) has no write counterpart for CATIA, so it dies at conversion. Spatial 3D InterOp, the same engine sold to developers, states the same scope in its own words: exchange of "visualization, exact B-rep geometry and metadata."

For the pipeline goal (agent generates a source file that becomes an editable, feature-history CATPart), Datakit cannot satisfy it from any format. The only routes to spec-driven CATParts are CATIA-side automation (CAA C++ / COM / VBA / macro replay that creates Part Design specs natively) or manual/native CATIA authoring. Datakit remains the right tool for *dumb* geometry ingest at scale.

## 1. What the CATIA V5 writer can write

### 1.1 Writer API surface (evidence: `evidence/catiav5w.html`, V2026.3 `namespacecatiav5w`)

The complete CATIA V5 writer namespace exposes:

- `InitWrite`, `InitPart`, `InitProduct`, `WriteEntity(Dtk_Entity)`
- `CreateNode` with node types limited to: `NodeTypeGeometricSet`, `NodeTypePartBody` (hybrid body), `NodeTypeMechanicalTool`. Bodies may be created under PartBody and MechanicalTool nodes.
- Attributes: name, color/layer (`SetLayerData`), `Override*` attribute setters, named views (`WriteNamedView`)
- Metadata parameters: `AddDoubleParameter`, `AddIntegerParameter`, `AddBooleanParameter`, `AddStringParameter` (inert values; no formulas, no links to geometry)
- Assembly: `AddInstance`, `AddVirtualComponentInstance`
- Material (`Material`), file description (`FileDescription`)
- A `Pmi` sub-namespace (CATTPSPmi, CATTPSText, DrwLeader, RTFText) exists in the code, but the module matrix marks PMI as not processed for this writer (see discrepancy note in section 4)

There is no `AddFeature`, no sketch creation, no Pad/Pocket/Hole construction, no parameter-with-formula creation. The writer physically cannot emit Part Design specs.

### 1.2 Official write mapping (`evidence/v5w_mapping.html`)

Datakit element → CATIA V5 object:

| Datakit | CATIA V5 |
|---|---|
| Dtk_Body | Imported Body |
| Dtk_Body with Reference Plane | Reference Plane |
| (face) | Imported Surface |
| (edge/curve) | Imported Curve |
| (vertex) | Imported Point |
| Dtk_mesh | Cloud Body |
| assembly tree | CATProduct / instances |
| name, color, layer | V5 name / graphical attributes |

There is no mapping row for features, sketches, parameters-as-specs, or drawings. This is the definitive answer to "what does a converted CATPart contain": CATIA *Imported* geometry objects.

### 1.3 Writer module matrix, CATIA V5 row (`evidence/supportedmodules.html`, `evidence/matrix.json`)

| Module | Assemblies | BREP | Wireframe | Meshes | Notes/PMI/FDT | Metadata | RenderInfos | PhysicalMaterial | Machining Features | Asm Constraints | UUID/PersistentName | Views | Drawings(2D) | Part Tree |
|---|---|---|---|---|---|---|---|---|---|---|---|---|---|---|
| CATIA V5 writer | OK | OK | OK | OK | KO | OK | PP | PP | KO | KO | OK | KO | KO | OK |

"Part Tree OK" here means the container/hierarchy tree of section 1.1, not feature history: the module legend defines Part Tree as "Part construction tree, feature history and parameters" for *readers*, and the writer's own mapping table contradicts any stronger reading (see section 4).

## 2. What each source format carries in

Formats accepted for CATIA V5 output, per Datakit's own converter selector (datakit.eu, "all to CATIA V5 3D"): ACIS, CATIA V4, CATIA V5, CATIA V6/3DEXPERIENCE, DWG/DXF 3D, Fusion 360, IGES, Inventor, JT, Parasolid, PLM XML, ProE/Creo Parametric, Rhino, Solid Edge, SOLIDWORKS, STEP, UG NX. (Plus a Rhino-to-CATIA V5 CrossCad/Plug product, 1200 EUR, and SOLIDWORKS-to-CATIA V5 plug-in, 2500 EUR.)

Reader module states from the same matrix (OK processed / PP partial / KO not processed / NA not applicable), trimmed to the columns that change what lands in the CATPart:

| Source | Asm | BREP | Wireframe | Meshes | PMI/FDT | Mach.Features | Drawings(2D) | Part Tree (read) | What arrives in the CATPart |
|---|---|---|---|---|---|---|---|---|---|
| CATIA V5 | OK | OK | OK | OK | OK | OK | OK | OK | Imported Bodies + wires + PMI-free tree of containers; names/colors/materials. Feature history is read internally but not written. |
| CATIA V6 / 3DEXPERIENCE | OK | OK | OK | OK | OK | OK | OK | OK | Same as CATIA V5. |
| SOLIDWORKS | OK | OK | OK | OK | OK | OK | OK | PP | Imported Bodies; analytic surfaces are converted to NURBS (product mapping, section 3); names/colors kept; history lost. |
| NX/Unigraphics | OK | OK | OK | OK | OK | OK | OK | OK | Imported Bodies + structure; history read internally, not written. |
| Creo / ProE | OK | OK | OK | OK | OK | OK | OK | OK | Imported Bodies + structure; history read internally, not written. |
| Inventor | OK | OK | OK | KO | OK | KO | KO | PP | Imported Bodies + PMI-free attributes; no meshes, no features. |
| Solid Edge | OK | OK | OK | OK | PP | KO | OK | PP | Imported Bodies; partial PMI. |
| Fusion 360 | OK | OK | OK | KO | NA | KO | NA | NA | Imported Bodies only. |
| CATIA V4 | OK | OK | OK | OK | KO | KO | OK | KO | Imported Bodies + wires; 2D drawings dropped (writer Drawings KO). |
| Parasolid | OK | OK | OK | OK | NA | NA | NA | NA | Pure B-rep ingest; no metadata beyond names/colors. |
| ACIS | OK | OK | OK | NA | NA | NA | NA | NA | Pure B-rep ingest. |
| STEP | OK | OK | OK | OK | OK | PP | NA | NA | Imported Bodies + PMI-free structure; AP242 PMI readable but not writable to V5. |
| IGES | OK | OK | OK | NA | OK | NA | OK | NA | Surfaces/wires as Imported Surface/Curve; no solids guaranteed. |
| DWG/DXF 3D | OK | OK | OK | OK | OK | NA | OK | NA | 3D B-rep + wires; 2D drawing content dropped by the writer (Drawings KO). |
| JT | OK | OK | OK | OK | OK | NA | NA | NA | Imported Bodies + structure + PMI-free attributes. |
| PLM XML | OK | NA | NA | NA | NA | NA | NA | NA | Structure/metadata skeleton only; no own geometry module (NA). |
| Rhino | OK | OK | OK | OK | PP | NA | KO | NA | Imported Surfaces/Bodies; NURBS-native. |

Reading the table: the only per-format variation is *what geometry* (solids, loose surfaces, wires, meshes) and *which attributes* survive to the intermediate model. The writer then serializes that uniformly as Imported geometry. No column in the writer is ever better than B-rep-plus-attributes for any source.

## 3. Product-level mapping proof (SOLIDWORKS → CATIA V5, the best-endowed pair)

CrossCad/Plug product 94 mapping table (datakit.eu, "SOLIDWORKS 3D to CATIA V5"):

| Module | Input → Output |
|---|---|
| Assembly → Assembly | kept |
| Color, Name | kept |
| Plane → Plane | kept |
| Blend, Cone, Cylinder, Fillet, Extrusion, Offset, Revolution, Ruled, Sphere, Torus surfaces | all → **NURBS Surface** |
| Body → Body | kept (as imported) |

Even the flagship pair degrades analytic surfaces to NURBS and lists zero feature, sketch, or parameter rows. The Inventor→V5 and V5→V5 product pages publish no mapping table at all, and the SDK docs are the only complete source.

## 4. Feature reading exists; feature writing does not

- The SDK defines a rich read-side feature model: `Dtk_feat_sketch`, holes, threads, patterns, pockets, pads, revol, sweep, loft, shell (`evidence/../annotated` class list, V2026.3).
- "How to read features" (`evidence/howtofeat.html`): feature extraction is offered only for CATIA V5, CATIA V6/3DEXPERIENCE, NX, SOLIDWORKS, and requires a dedicated license. The SOLIDWORKS reader page lists a "Features Mapping" document under Detailed Mapping.
- No writer namespace for any target format (CATIA V5 included, and likewise SOLIDWORKS, NX writers) exposes feature construction. The feature model is read-only by design.

Document discrepancies, reconciled against the API and mapping pages:

1. Writer matrix "Part Tree = OK" vs mapping table with no feature rows. Resolution: the writer creates only GeometricSet/PartBody/MechanicalTool container nodes (section 1.1). "Part Tree" for the writer means structure, not history. The mapping table and the API, which are more specific, win.
2. Writer matrix "Notes/PMI/FDT = KO" vs the existing `Pmi` namespace (CATTPSPmi, text, leaders). Unresolved in the docs; the module matrix and the CrossManager mapping pages say KO, so treat CATIA V5 PMI write as unavailable. Do not plan a pipeline around it.

## 5. Spatial 3D InterOp says the same thing

Spatial acquired Datakit in 2021; 3D InterOp is the same engine for developers. spatial.com product page (fetched 2026-09-06):

- Scope sentence: "designed to exchange **visualization, exact B-rep geometry and metadata** from various CAD formats."
- "Native Data Translation: uses the CGM kernel and native APIs to read/write CATPart and CATProduct ... without a CAD license." Write output is CGM B-rep serialized into CATIA containers.
- "CAD Associativity: import stable CAD topological identifiers to allow your application to capture and track design changes to **regenerate downstream features**." That is the host application rebuilding its own features from topology IDs. It is not feature translation into CATIA's spec tree, and it requires a live host kernel, not a file converter.
- "3D InterOp generates native geometry for ACIS, CGM and Parasolid." Geometry only.
- No page in the set mentions writing parametric features into CATIA. PMI and metadata are the whole "beyond geometry" story.

## 6. Consequences for the pipeline

- Goal "agent emits format X, Datakit converts, result is a feature-history CATPart" is unreachable with this engine, for any of the 17 supported inputs.
- Best achievable with Datakit: clean B-rep CATPart (Imported Bodies) with correct assembly structure, names, colors, materials, and PMI read-side available for extraction into a sidecar. Parasolid or STEP are the cleanest generic inputs; SOLIDWORKS costs a NURBS degradation of analytic surfaces per the product mapping; native CATIA V5 source keeps the most attribute fidelity while still losing history.
- If spec-driven CATPart output is mandatory, the work must happen inside CATIA (CAA/COM automation building Part Design features) with the agent emitting a script/parameters rather than a CAD file. Datakit can still feed dumb references alongside.
- Related parallel research (not yet cross-checked): `docs/agents/2026-09-06-dk-parametric-writers/`, `.../dk-history-survival/`, `.../catia-catpart-reverse-engineering/`.

## 7. Sources

- `https://www.datakit.com/Doc_API_html/` (V2026.3): `supportedmodules.html`, `catiav5w.html`, `v5w_mapping.html`, `v5w_asm_how_to.html`, `howtofeat.html`, `howtoapi.html`, `solidworks.html`, `inventor.html`, `catiav5.html`, `details.html`, `annotated.html`, `namespacecatiav5w.html`
- `https://www.datakit.eu/en/product_search.php`; `/cad-convertors/all-to-catia-v5-3d/0-2-1.html`; `/cad-convertors/solidworks-3d-to-catia-v5-3d/94-solidworks-3d-to-catia-v5.html`; `/cad-convertors/catia-v5-3d-to-catia-v5-3d/2-2-1.html`; `/cad-convertors/inventor-to-catia-v5-3d/16-2-1.html`
- `https://www.spatial.com/solutions/cad-translation/3d-interop`
- Method notes: DuckDuckGo HTML search worked briefly then hit a bot CAPTCHA (code 9c39); direct curl to datakit.com became rate-limited (0-byte responses) after ~12 requests; webfetch remained reliable. All claims rest on fetched pages; nothing is inferred from marketing copy alone.

## 8. Evidence files

`evidence/` holds the raw fetched pages and the parsed matrix:

- `supportedmodules.html` (raw reader/writer matrix with OK/PP/KO/NA CSS classes)
- `matrix.json` (fully parsed reader and writer module matrices)
- `v5w_mapping.html` (CATIA V5 writer mapping table)
- `catiav5w.html` (writer module list + supported versions/extensions)
- `howtofeat.html` (feature read scope and license note)
- `details.html` (per-format version notes)
