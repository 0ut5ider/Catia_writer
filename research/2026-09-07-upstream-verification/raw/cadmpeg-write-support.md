# cadmpeg write-support rows, extracted 2026-09-07

- source: github.com/cadmpeg/cadmpeg `docs/format-support.md`, local mirror `research/2026-09-06-shared-corpus/raw/cadmpeg/format-support.md`
- mirror md5: `5944f900b491717b821d6d2885bbb5d7`
- method: keep every `## ` section heading and every `**Write**` / `**Native write**` / `**Ladder**` line under it.


### Support ladder

### Autodesk Inventor `.ipt` and `.iam`
**Ladder: L1.** Structural detection requires directory evidence. The codec enumerates the complete CFB hierarchy, versioned databases, registry and revision tables, exact segment pairs, metadata tables, typed bulk records, OLE property sets, previews when present, Protein package entries and decoded catalog assets, and `UFRxDoc` external references. Optional or unknown segments remain named nativ
- **Write:** None. The codec has no encoder, replay path, or patch path.

### ASM/ACIS bare `.sat`/`.smt`/`.smb`/`.sab` streams
**Ladder: L3.** Detection, inspection, and decode cover the admitted binary and text branches. The codec transfers solved-record analytic, NURBS, topology, placement, and procedural carriers through `cadmpeg-asm` into connected B-rep when the stream yields surfaces, points, or faces. Header scale and tolerances populate the neutral document. Unknown SAB records retain source range, digest, and ker
- **Write:** None. The codec has no encoder, replay path, or patch path.

### Status terms

### FreeCAD `.FCStd`
**Ladder: L5.** The cumulative gate stops at L5; L9 write assertions pass individually and show as extras. Schema versions 2 and 3 and earlier layout bands are separate legacy profiles. The codec identifies them and refuses decode.
- **Native write:** Partial for the declared write envelope; individual write assertions pass as extras above L5. Schema 4/file 1 retained documents regenerate deterministically while preserving every unedited XML record and named side entry. Checked leaf property edits and side-entry replacements are supported. Recursive typed application graphs can be generated without a source archive. Writing 

### IGES
**Ladder: L9 for the IGES 4.0/5.0/5.1/5.2/5.3 ASCII mechanical/document envelope.** Semantic decode is resource-bounded, valid-IR output is admitted atomically, every non-null Directory Entry has retained identity and transfer accounting, and semantic output has target-version and independent-application gates. Binary, other ASCII versions, and extensions are separate envelopes. Binary is a read-o
- **Native write: Semantic.** An unchanged decoded document with an intact source baseline replays byte for byte. Source-less documents and edited documents can write standalone points, finite lines, circles, ellipse/parabola/hyperbola conic arcs, NURBS curves, planes, and NURBS support surfaces, one-face trimmed sheet bodies with Type 141/144 boundaries and NURBS parameter curves, and bounded Typ

### Rhino `.3dm`
**Ladder: L0.** Archive 2/3/4/50/60/70/80/90 and V2–V4 open at L1 and show as extras. Partial typed geometry, topology, presentation, and bounded source-less native writing show as extras above that L1 subset. V1 and archive 5 keep the codec at L0.
- **Native write: Bounded source-less regeneration.** Explicit archive 50, 60, 70, and 80 targets regenerate a narrowly writable IR. The writer does not consume `SourceFidelity` (`NotConsumed`). Writable families are point objects, grouped point clouds as free-vertex bodies, circles, native-canonical rational and non-rational NURBS curves, planes, native-canonical rational and non-rational NURBS s

### SolidWorks `.sldprt`
**Ladder: L4.** Unknown geometry carriers and topology cases block L5. Incomplete sketch constraints and feature families block L6.
- **Native write: Partial.** Unchanged IR with a retained source image writes byte for byte. Supported geometry edits can patch the native Parasolid partition when the entity graph and provenance remain stable. Retained writing can synchronize supported feature, sketch, parameter, configuration, active-configuration XML, and PMI edits and rejects structural edits it cannot safely rewrite. Modified

### Fusion 360 `.f3d`
**Ladder: L4.** Undefined geometry-carrier payloads block L5. Tolerant coedge, edge, and vertex records decode across their release-gated layouts and round-trip through retained and source-less native writing. Native writing shows as extras.
- **Native write: Partial.** An unchanged retained source archive writes byte for byte. The writer patches model points, common analytic and NURBS B-rep curves and surfaces, rational/non-rational pcurves, procedural caches, sketch geometry, constraints, history fields, design records, supported ACT GUID, channel, registry, and root fields, and supported appearance properties in their original reco
- **Write limits:** General writing requires a retained source archive and the original entity and record layouts. Source-less generation supports multiple placed bodies, regions, and shells with plane, cylinder, cone, sphere, torus, or rational/non-rational NURBS faces; multiple loops; shared radial edges; line, circle, ellipse, point-degenerate, or rational/non-rational NURBS edge curves; inline

### Siemens NX `.prt`
**Ladder: L2.** Connected B-rep on single-body, `RMFastLoad`-selected, and terminal-feature-lineage-resolved body images shows as extras. Feature and history transfer above that subset shows as extras until L4 coverage gates close. Unresolved multi-partition history keeps the codec at L2.
- **Native write: None.**

### CATIA V5 `.CATPart`
**Ladder: L1.** Geometry on the standard-nested band shows as extras. L3 requires connected topology across admitted files. Current topology depends on resolved trim, support, and endpoint assignments.
- **Native write: None.**

### Creo Parametric `.prt`
**Ladder: L1.** Incomplete model-space coverage across analytic and spline carrier families blocks L2. Exact plane components, selected cylinders, placed sketches, and native design records show as extras.
- **Native write: None.**

### STEP Part 21
**Ladder: L9.** Part 28 XML, Part 26 binary/HDF5, and AP242 BO-Model sidecars are outside the declared bands. ZIP packaging is an extra read profile for the `ISO-10303.p21` root; subsidiary graph composition is outside the declared band. AP203/AP214 mark constructs their schemas cannot carry as inapplicable. Part 21 exchange documents have no originating feature replay histories, sketch-constraint
- **Native write: Semantic.** The writer selects AP203 edition 1 or 2, AP214, or AP242 edition 1, 2, or 3 and declares the exact target schema. It emits source-less documents and typed edits for analytic and NURBS geometry, connected solid/sheet/wire topology, pcurves including 2D replicas, singular loops, rigid body placements, product occurrences, tessellation, visibility, layers, named colors, 

### Maintaining these profiles
