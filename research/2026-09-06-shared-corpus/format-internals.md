# CATIA V5 Native Formats: Binary Internals Research Report

- Date: 2026-09-06
- Agent role: web research (format internals)
- Question: what is the internal binary structure of CATIA V5 native documents (.catpart, .catproduct, related .cat*), to what depth is it publicly known, and can files be written from scratch without CATIA?
- Model: anthropic claude (via opencode)
- Confidence tags: **CONFIRMED** = backed by a primary source or byte analysis cited below; **SPECULATIVE** = reasoned, not yet evidenced.

All raw evidence is in `raw/` next to this file (`pronom-catia-records.txt`, `so/`, `cadmpeg/`, `samples/`).

---

## 0. Executive summary

1. **CONFIRMED: `.CATPart` and `.CATProduct` are not OLE/CFB files.** They begin with the ASCII magic `V5_CFV2\0` (bytes `56 35 5F 43 46 56 32 00`). A full-file scan of two real samples found zero occurrences of the OLE magic `D0 CF 11 E0 A1 B1 1A E1`. The widespread "catpart is a structured storage file" belief is wrong for V5 native files.
2. **CONFIRMED: the container is fully understood and machine-parsable today.** A big-endian directory offset/length pair at bytes 8..15 points to a trailing `CATIA_V5 CB0001` stream directory that ends with `CB__END`. Streams are named (`MainDataStream`, `SurfacicReps`, `Project`, `Data`, `CATPreview`, ...) and stored as physical extents. I parsed both real samples with ~60 lines of Python. `V5_CFV2` files can also nest a second `V5_CFV2` container (the standard CATPart does, for its BREP streams), and the outer body carries `FINJPL  `-marked named segments (project flags, summary information, JPEG preview).
3. **CONFIRMED: a serious open, clean-room, byte-level reverse-engineering of `.CATPart` exists: the cadmpeg project** (`github.com/cadmpeg/cadmpeg`, Apache-2.0 code, CC-BY-4.0 docs, active as of 30 Aug 2026). Its `docs/formats/catia.md` is a 265 KB format specification with a machine-checked layout table (`docs/layouts/catia.toml`), a Rust decoder, and an explicit open-items list of what is still unknown. It scores its CATIA codec at L1 (container/navigation) with L2 geometry extras on the standard nested band.
4. **CONFIRMED: exact record-level geometry serialization is known but incomplete.** Vertex, edge, face-spine, trim-mesh, and analytic surface/carrier record layouts are documented and decode real files. The design history (features, sketches, parameters) is only partially decoded, and `catia-open-items.md` lists ~60 unresolved semantics items.
5. **SPECULATIVE, then downgraded by evidence: writing a loadable `.CATProduct` or `.CATPart` from scratch is currently beyond any public implementation.** cadmpeg declares "Native write: None" for CATIA. The container layer is writable today; the record layer has load-bearing unknowns (extent flag bits, identity quotients, design-intent grammar). Realistic write strategies are: template byte-patching, viewer-only fakes, or switching to a documented interchange format (3DXML has a published specification; STEP/IGES are open and fully writable).
6. Precedent verdict: comparable proprietary formats have been RE'd much deeper by the same effort (SolidWorks to design-records level, NX to connected B-rep), so the ceiling for CATIA is a matter of corpus size and time, not of impossibility. See §7.

---

## 1. Q1: Is a .catpart an OLE structured-storage file?

**No, not in V5. CONFIRMED by three independent lines of evidence.**

- PRONOM (The National Archives, UK), record `x-fmt/439` "CATIA Model (Part Description) Version 5", internal signature: byte sequence `56355F434656320000` at absolute offset 0. That is ASCII `V5_CFV2\0\0`-style header (`V5_CFV2` + two NULs). Provenance of the record: "Digital Library Research Group / MIT Libraries", format source date 06 Apr 2009, disclosure "Full". Same scheme for `x-fmt/440` (`.CATProduct`), `x-fmt/438` (material description), `fmt/1615` (`.CATDrawing`, contributed by the J. Paul Getty Trust). See `raw/pronom-catia-records.txt`.
- Direct byte analysis of real files (this session, `raw/samples/`):
  - `Part1.CATPart` (112,111 bytes): magic `V5_CFV2\0` at 0; first bytes are not `D0CF11E0`; `d0cf11e0a1b11ae1` occurs nowhere in the file.
  - `Print.CATProduct` (14,975 bytes): same result.
- The `file(1)` magic database (v5.46 and current master) contains no CATIA entries at all, so the "OLE" claims online are folklore, not tool output (`raw/file-magdir-cad.txt`).

Nuance: `.CATProduct`/`.CATPart` *can* embed real OLE/CFB sub-objects? Not observed: no CFB magic in either sample. What *is* embedded is a JPEG preview (`FF D8 ... FF D9`, `JFIF`) and a rich property system using UTF-16LE strings (`CATStorageProperty`, `CATDocumentProperty`, `CATOctetArray`). The community OLE belief probably transfers from SolidWorks (which genuinely is CFB) or from CATIA V4-era/3DXML packaging. Old V4 model files have their own plain headers: at offset 80 `CATIA   ` plus `CATIA SOLUTIONS V4...RELEASE` (PRONOM `x-fmt/436`).

## 2. Q2: Container and serialization

All CONFIRMED against real bytes this session, cross-checked against cadmpeg §3 and the Ivanti file-type analysis note (see Raw sources; the Ivanti snippet independently gives the same offset-8/12 words and the `CATIA_V5 CB0001` string at the first offset).

### 2.1 Outer container (both .CATPart and .CATProduct)

```text
0x00..0x07  magic "V5_CFV2\0"
0x08..0x0B  directory_offset  (u32 big-endian)
0x0C..0x0F  directory_length  (u32 big-endian); invariant dir_off + dir_len == file_size
0x10..0x17  8 bytes: all ff in Print.CATProduct; 00 00 19 92 00 00 14 00 in Part1.CATPart (NOT a constant; cadmpeg never reads it)
0x18..0x37  32 zero bytes
0x38..0x3F  8 raw header flag bytes (not constant)
```

At `directory_offset` sits the string `CATIA_V5 CB0001\0`; the directory region ends with the token `CB__END`. Verified on both samples (e.g. `Print.CATProduct`: dir at 9855, len 5120, 9855+5120 = 14975 = file size; `CB__END` present).

### 2.2 Stream directory grammar

Per stream descriptor (found by self-consistency scan of the directory):

```text
ds+0x0c  logical_stream_length  u32 BE
ds+0x50  extent_count k         u32 BE
ds+0x54  k extents, 20 bytes each: phys_off u32BE, phys_len u32BE, log_len u32BE, log_off u32BE, flags u32BE
```

A logical stream is the concatenation of its physical extents in `log_off` order; `log_len == phys_len`, extents cumulative, `sum(log_len) == logical_stream_length`. Stream names are UTF-16LE, stored *before* the descriptor header, terminated by `00 00 00`. This grammar parsed both of my real files on the first attempt (`raw/samples/*.container-report.txt`). The meaning of the `flags` word is an open item (cadmpeg CR-02).

### 2.3 Stream inventory observed (real files)

- `Print.CATProduct` outer directory: `Data`, `Project`, `ProjectHeader`, `TimeStamp`, `Format`, `GesToler`, `Indexe`, `CATStorageProperty` (x several), `CATPropertySets`, `CATPreview`, plus container declaration streams named `<id>_<hex>_<id>` (`48b6aefe0_2c7_39d04d68_4ce`) and `>Cont_8b6aefe0_2c7_39d04d68_4ce`.
- `Part1.CATPart` inner container directory: `MAIN`, `MainDataStream` (largest, 5020 logical bytes: the geometry spine), `SurfacicReps` (1438 bytes: surface-of-representation roster), `Header`, `SceneGraph`, `Describe`, plus one `<hex-ish>` stream.
- cadmpeg §3.4 lists the same canonical names: `MAIN`, `MainDataStream`, `Header`, `SceneGraph`, `Describe`, `SurfacicReps`.

### 2.4 Nesting and FINJPL segments

- The standard `.CATPart` nests a second `V5_CFV2` container in the outer body: `Part1.CATPart` has inner magic at file offset 82572, its own dir delta/length (7072/4096), its own `CATIA_V5 CB0001` directory with `MainDataStream`/`SurfacicReps`. The inner `A/B` words have the same grammar as the outer. `Print.CATProduct` has no inner container (product documents do not carry a BREP spine of their own).
- The outer body is interleaved with segments marked `FINJPL  ` (six ASCII + two spaces) followed by a u32 BE type word and a primary name. Observed type words in real files: `0x0000008c`, `0x00000084`, `0x000000bc`, `0x000003a2`, `0x0000008e`, `0x01010001`, `0x01010002`, `0x01010003` family (project flags), plus the `CATSummaryInformation`/`CATPreview` segment whose JPEG is the model thumbnail. Segment bodies carry the atom-ish property records described in §2.5.

### 2.5 Property/value atom layer (both doc types)

Verbatim from `Print.CATProduct`: field-name atoms appear as UTF-16LE (`CATStorageProperty`, `CATUnicodeString`, `CATSymbolProperty`, `CATDocumentProperty`, `CATOctetArray`, `matrix`, `viewAngle`, `type`, `CreationDate`, `Identifier`, `OwnerName`) followed by value tags; f64 values appear as `e6 <8 LE bytes>` atoms (e.g. camera matrix components at 3689..3788, including `411.5017` at 3773). External document references are `CATStorageProperty` atoms whose `CATUnicodeString` payload ends in `.CATPart`/`.CATProduct`/`.CATShape`/`.cgr` (cadmpeg §3.3 gives the exact atom byte signature; independently matches the string dump in the Stack Exchange hex viewer in `raw/so/44952646-q.json`, which shows the same atoms plus absolute Windows paths). Doc identity/ref ids appear as strings like `D.e0ef6a8bc7020000784dd03911050000` (observed at 10092 in `Print.CATProduct`).

## 3. Q3: What serializes geometry and topology? (the record layer)

Source: cadmpeg `docs/formats/catia.md` (summarized; full spec + machine table in `raw/cadmpeg/`). All multi-byte ints LE (except marked BE lanes); lengths mm; angles radians; standard band stores coordinates as f32 (~1e-5 mm), object-stream/E5 bands store f64. CONFIRMED marker census on `Part1.CATPart`: `05 08 01` x19, `0x60`-prefixed rows x155, `e5 0d 03` x525, `00 33 3x` surface/curve kind markers (plane x6, cylinder x7, torus x1, line x19, circle x10), FBB face rows `30 04 04 ff` x14, standard edge delimiter `10 24 04 ff ff 00 00 00` x3. So a real part's spine layout matches the spec exactly.

- **Six variant families** detected by header/stream structure: standard nested `V5_CFV2` (FBB spine + edge tables + vertex table), FBB-only partial, E5 `0D 03` native record stream, zero-entity `a9 03`, float-packed object-stream (`a5/a8/b5` families), inner-body-without-directory. "No single universal freeform marker" (three separate NURBS storage classes).
- **Standard spine**: face outer-bound rows `((30|b0) 04 04 ff <4 raw>)` at stride 8 (face i = row i); counted edge tables `01 <kind> <count>` with big-endian handles (1/2/3-byte widths); vertex table `01 06` of 15-byte `05 08 01 <x><y><z> f32le` rows; per-face indexed triangle-mesh "trim records" (`01 0x4x ...`) whose triangle-edge cancellation recovers exact face boundaries and loop counts; `0x60 <tag u24le> ... <face_ref> <face_ref>` curve-support rows carrying analytic curves inline (circle = BE f32 center+radius, observed) and two-face incidence.
- **Analytic surfaces** (in `SurfacicReps` roster and consolidated streams): `00 33 32/33/34/35/38` = plane/cylinder/cone/sphere/torus kind markers, `00 33 36/37` = line/circle; `b2 03 19/28/29/2a/2b/2d` cylinder/cone/sphere/torus/revolution records; every face carries a 10xf32 trimmed-face AABB + bounding-sphere bounds block with a containment invariant (checked to 3 ulps).
- **Design history** (feature/sketch/parametric layer) lives in the outer preamble: `7C 02` source-schema catalogs, `7C 05/08/09/0A` entity tables and object graphs with UTF-8 schema names (`CATProdCont`, `CATFeatCont`, `Product1`, `_Component`, `_RefProduct`, `_PartNumber`, `PRTSketch`, ... all observed verbatim in my `Print.CATProduct` ASCII run dump), `7C 0B` visualization value blocks, formula/relation programs. This is the least-understood layer: schema-program semantics, sketch constraints, feature operation binding remain open items (DI-01..DI-29 in `raw/cadmpeg/catia-open-items.md`).
- Identity is layered into allocation / occurrence / geometry lanes; several identity quotients are unresolved, which is exactly what blocks robust *writing* (§6).

## 4. Q4: .CATProduct internal layout (tree, placements, references)

**CONFIRMED at container level** (my parse of `Print.CATProduct`, `raw/samples/Print.CATProduct.*`): same `V5_CFV2` outer container, no inner container; streams `Data` (1728 B, contains container class declarations), `Project`/`ProjectHeader`/`TimeStamp`, `CATPropertySets`, `CATPreview` (JPEG), `CATStorageProperty` streams. Product schema names appear verbatim as object-graph fields: `Product1`, `CATProdCont`, `_Component`, `_RefProduct`, `_PartNumber`, `_Connectors`, `_PubConnectors`, `_RepresentedBy`, `_ViewsList`, `_BagRepsList`, `_PrdVersion`, `Components`, `ParameterSet`, `VPGlobal`, `IsRoot`, `CATCompoundCont`. Placements are stored as `matrix` fields of f64 atoms (`e6 <f64le>`; the camera matrix decoded to plausible values, e.g. 0.9126 and 411.5017). External/linked document references: `D.<32 hex>` identity strings and `CATStorageProperty` targets ending `.CATPart`/`.CATProduct`.

**Known-depth caveat**: nobody publishes the full product-graph record grammar (occurrence ordering, id spaces across files, multi-instance sharing). cadmpeg marks "Product structure: None" for CATIA and its ladder puts Product support (components/occurrences/placements) at L7, above the current CATIA score. SPECULATIVE: the graph is walkable from the object-graph + schema catalogs the way `Part1.CATPart`'s BREP spine is, but it needs the same multi-file corpus work first.

## 5. Q5: Version records and version drift

- **No version field in the 64-byte header.** The `0x10..0x17` word pair varies between files (all-ff in the 2003-era product doc vs `00001992 00001400` in the part) and cadmpeg deliberately never reads it. SPECULATIVE: counts/counters of internal streams; do not treat as version.
- **Saved-by version is stored as text, not as a version word.** Observed in both samples: `DASSAULT-SYSTEMES` + `041803P` (the same string appears in the community hex dump: "DASSAULT-SYSTEMES CATIA 041803P"). cadmpeg §3.3 documents the `LastSaveVersion` summary field in the project-flags segment (`FINJPL` type `0x01010003`), with ASCII sub-fields delimited by `<Version>…</Version>`, `<Release>…`, `<ServicePack>…`, `<BuildDate>…`, `<HotFix>…`. So version identification = parse the summary segment, not the header. CONFIRMED.
- **Format-version drift of the container**: PRONOM shows V5 signatures stable across the R8..R3x era (single internal signature since 2009; `.CATDrawing` sig added 2022, V3 model sig 2022). V3/V4 models have entirely different headers (offset-80 strings, PRONOM x-fmt/436, fmt/1714). What *does* drift is the record layer: cadmpeg's six variant families behave differently by version band; the exact family<->CATIA-release mapping is unmeasured (SPECULATIVE: no public dataset correlates LastSaveVersion to variant family yet).

## 6. Q6: What would it take to WRITE files from scratch? Feasibility

The layered verdict:

1. **Container layer: writable now. CONFIRMED.** I reconstructed header, CB0001 directory, extents, names, FINJPL segmentation, JPEG preview embedding, and storage-property references from two real files. A writer must satisfy: header invariant `dir_off+len == size`; self-consistent extent chains with valid descriptor tails (a parser validates every extent); UTF-16LE name terminator grammar; `CB__END`; one uniquely-largest `MainDataStream`/`SurfacicReps` pair per stream directory (cadmpeg admits BREP streams only under that rule). Unknown: extent `flags` bit meanings (CR-02) and the unread `0x10..0x17` header word pair. Risk: CATIA itself may reject a file for unknown flag/header values; no public data on its strictness. SPECULATIVE.
2. **Geometry record layer: writable for a narrow band, with reservations.** The standard-nested spine (FBB rows, edge tables, `05 08 01` vertices, `0x60` supports, trim-mesh packets) has a full documented grammar and decode evidence; a *write-first* implementation of that band (cube/box primitives, analytic faces) is the highest-value unknown-resolution move (it forces the identity-quotient problems that reading can dodge). Load-bearing unknowns before any file is *guaranteed* CATIA-loadable: edge/vertex allocation-identity binding in ambiguous cases (SN items), orientation signs, pcurve attachment, the object-stream tag resolver. The honest current state per cadmpeg: "Native write: None. Round trip: None." for CATIA. CONFIRMED (from docs).
3. **Design-history layer: not writable.** Feature/sketch/parametric semantics are ~29 open items deep; a from-scratch writer would have to emit history records it cannot verify. Workaround (used elsewhere by cadmpeg): emit files *without* design history (pure BREP containers, "zero-entity"/mesh-only variants exist) or accept "unknown records survive opaquely" strategies.
4. **Pragmatic alternatives when the goal is "deliver a file CATIA opens", all CONFIRMED as routes**:
   - Template patching: take a real minimal `.CATProduct`/`.CATPart`, mutate bytes in place, re-fix directory extents. Feasible for tooling around a known corpus; not a general writer.
   - **3DXML**: zip of XML per a specification published by Dassault ("partially proprietary format with a specification published by Dassault Systèmes", file-extension.info; xeokit ships a format guide; zip + BOM + rep files confirmed by Okino/Spatial). The realistic "write something Dassault tools open" target.
   - Interchange: STEP AP203/214/242 and IGES remain the only fully documented, write-and-verify targets (cadmpeg scores both at its top level).

## 7. Q7: Precedents (other proprietary CAD formats reversed this way)

Primary dataset: the cadmpeg support ladder (levels: L0 parse, L1 navigate container, L2 placed geometry, L3 connected B-rep, L4 design records/features, L5 all shape data, L6 full design intent, L7 product structure, L8 full document, L9 semantic writer accepted by native apps). Current public scores, CONFIRMED from `raw/cadmpeg/format-support.md` (30 Aug 2026):

| Format | Level | Note |
|---|---|---|
| SolidWorks `.sldprt` | **L4** | features, sketches, parameters, configurations decoded from a CFB container by pure RE |
| Siemens NX `.prt` | **L2** | L3 extras on resolved body images; history transfer extras |
| Autodesk Inventor `.ipt/.iam` | **L1** | full CFB hierarchy enumerated (the contrast case for the "is catpart OLE" question: Inventor genuinely is CFB) |
| PTC Creo `.prt` | **L1** | partial placed geometry and topology already as extras |
| FreeCAD `.FCStd` | **L5** | not proprietary (zip+XML), reference for how far tooling got with a documented container |
| Rhino `.3dm` | **L0** | mitigated by the OpenNURBS library |
| ACIS `.sat`/binary streams | **L3** | |
| STEP / IGES | **L9** | open standards, semantic writers |

Precedent conclusions: (a) container-level RE of a "V5_CFV2-class" format is routine and fast once a corpus exists (Inventor, SolidWorks, NX all cracked their containers); (b) feature-history RE is the hard frontier everywhere (nobody is above L4 on a proprietary kernel format); (c) the CATIA gap is corpus and time, not method: cadmpeg explicitly states its format knowledge comes from "legally possessed CAD files and public documentation" and bans vendor SDK/decompiled knowledge, which is a reusable legal posture for the whole effort. Older, thinner precedents: catia2.cad.de's CatThumbnail (header sniff + JPEG extraction, 2000s-era); PRONOM/MIT/GettY signature records (detection only); a Stack Exchange question asking exactly this question with zero answers ("Catia CATProduct & CATPart File Formats", Dec 2017, viewed 1,539 times); filext.com quoting the same magic. The first open-source project to treat the records seriously is cadmpeg (crates.io `cadmpeg-codec-catia` v0.5.5, 27 Aug 2026).

## 8. Recommended next moves (dependency order)

1. Expand the sample corpus and run the existing parser (`raw/samples/*.py` logic, or `cargo run -p cadmpeg inspect`) over dozens of files from different CATIA releases; correlate `LastSaveVersion` with variant family (closes §5 drift, unblocks a version matrix).
2. Write-first experiment on the standard-nested band (cube): a generator from the documented grammar; any CATIA-openable output immediately kills the identity-quotient unknowns in §6.2. Verification difficulty: high (needs a CATIA install or a partner with one; viewer-only validation via e.g. 3DXML export is weaker).
3. Probe header edge cases: feed modified `0x10..0x17` words to free viewers/Dassault's free-trial CATIA to see what is validated (flags, header pair). Blast radius if wrong: small.
4. Mine the object-graph schema catalogs across more documents to map product-tree field semantics (§4) before writing any writer.
5. For productization, track cadmpeg upstream rather than duplicating: it is the only project resolving this format with public, byte-backed evidence and a legal posture to stay merged.

---

## Raw sources

Fetch/analysis log for this session, with the verbatim key content. Full dumps: `raw/` (see file pointers).

1. **PRONOM signature records** (official repo `github.com/nationalarchives/pronom`, files `signatures/x-fmt/436,437,438,439,440.json`, `signatures/fmt/1615.json`, `signatures/fmt/1714.json`; cloned to /tmp/opencode/pronom, formatted copy `raw/pronom-catia-records.txt`). Key verbatim fields (x-fmt/439): `signature.name: "internal"`, `byteSequence: "56355F434656320000"`, `positionType: "BOF"`, `offset: 0`; x-fmt/436: sequence `4341544941202020` "CATIA   " + "CATIA SOLUTIONS V4{6}RELEASE" at offset 80; provenance "Digital Library Research Group / MIT Libraries", `formatSourceDate: "06 Apr 2009"`, `formatDisclosure: "Full"`. fmt/1615 CATIA Drawing V5 (J. Paul Getty Trust), added v101 2022-02-15; fmt/1714 CATIA V3 model, v105 2022-06-29.
2. **file(1) magic DB**: `github.com/file/file` master clone (`/tmp/opencode/filed`) + local `/usr/share/misc/magic.mgc`: zero CATIA matches; `raw/file-magdir-cad.txt` shows the CAD magdir with CATIA absent.
3. **cadmpeg project** (`github.com/cadmpeg/cadmpeg`, clone at HEAD 74b83dec, 2026-08-30; docs mirrored to `raw/cadmpeg/`).
   - `README.md` verbatim: "Format knowledge comes from legally possessed CAD files and public documentation. Vendor SDKs, decompiled binaries, and confidential material are prohibited (LEGAL.md)." Format table: "CATIA V5 `.CATPart`: L1 ... SolidWorks `.sldprt`: L4 ... Siemens NX `.prt`: L2 ...".
   - `docs/formats/catia.md` (CC-BY-4.0), §3.1 verbatim: `0x00..0x07 magic = "V5_CFV2\0"`, `0x08..0x0B directory_offset = u32 BE`, `0x0C..0x0F directory_length = u32 BE`, `0x10..0x17 fill_ff = ff * 8`, `0x18..0x37 fill_00 = 00 * 32`, `0x38..0x3F hdr_flags = 8 raw bytes (not constant)`; "The two u32 fields form a big-endian directory offset and length pair: `directory_offset + directory_length == file_size`". §3.3: "`FINJPL  ` (two trailing spaces) marks named stream blocks... The `LastSaveVersion` summary field stores ASCII values delimited by `<Version>`/`/<Version>`, `<Release>`/`/<Release>`, `<ServicePack>`/`/<ServicePack>`, `<BuildDate>`/`/<BuildDate>`, and `<HotFix>`/`/<HotFix>`." Storage-property verbatim atom sequence: `34 12 "CATStorageProperty" 80 01 00 00 00 00 22 0c 00 00 00 34 01 01 00` + `34 10 "CATUnicodeString" a0 02 00 00 00 00` + `34 05 "CATIA" 9f a0 02 00 00 00 00` + `34 <length:u8> <ASCII target> 9f`, targets `.CATPart/.CATProduct/.CATShape/.cgr` are external references. §3.4 stream names verbatim: "The descriptor names include `MAIN`, `MainDataStream`, `Header`, `SceneGraph`, `Describe`, and `SurfacicReps`." §5 grammar and §12 units quoted in §3 above; §6/7 object streams and schema catalogs; `docs/formats/catia-open-items.md` (789 lines, DI/SN/OS/ZE/E5/FV/AT open items); `docs/format-support.md` ladder and scores table (quoted in §7); `docs/layouts/catia.toml` machine table (verbatim `outer_header` record in `raw/cadmpeg/`).
   - docs.rs/cadmpeg-codec-catia v0.5.5 (2026-08-27, Apache-2.0): "Detects the V5_CFV2 file signature, examines cataloged logical streams, identifies storage variants, and decodes record families ... L2 for standard nested layouts, L1 for others."
4. **Real files analyzed this session** (`raw/samples/`, downloaded 2026-09-06 from `catiadoc.free.fr/online/basug_C2/samples/`):
   - `Print.CATProduct`, 14,975 B, from `http://catiadoc.free.fr/online/basug_C2/samples/Print.CATProduct`. Output verbatim in `Print.CATProduct.container-report.txt` / `.streams.txt` / `.matrix-version.txt`: magic `b'V5_CFV2\x00'`; `dir_off 9855 dir_len 5120 D+L==size True`; `dir magic b'CATIA_V5 CB0001\x00'`; `CB__END` tail; descriptors incl. `desc@11163 name='Data' extents=1 loglen=1728`, `desc@12271 name='>Cont_8b6aefe0_2c7_39d04d68_4ce' ... loglen=448`; ASCII runs verbatim: `CATProdCont`@1804, `CATFeatCont`@1816, `Product1`@1962, `_Component`@2114, `_PartNumber`@2135, `_RefProduct`@2254, `DASSAULT-SYSTEMES`@3986 + `041803P`@4016, `FINJPL` segments @4303/4774/6846/9261, `CATSummaryInformation`@6863, `JFIF`@6910, `Print.CATProduct`@9218, `D.e0ef6a8bc7020000784dd03911050000`@10092, `matrix` field with f64 atoms at 3660..3788 (decoded `0.9126396634780657`, `411.5017395019531`). OLE magic found: no.
   - `Part1.CATPart`, 112,111 B, from `http://catiadoc.free.fr/online/basug_C2/samples/Part1.CATPart`. Verbatim (`Part1.CATPart.container-report.txt`): `outer dir_off 100847 dir_len 11264 D+L==size True fillff 0000199200001400`; `inner V5_CFV2 @ 82572 ... inner dir_off 89644 magic b'CATIA_V5 CB0001\x00'`; inner descriptors `MAIN`/`Describe`/`Header`/`SceneGraph`/`MainDataStream` (loglen 5020)/`SurfacicReps` (1438); marker census: `050801 x19, 60 x155, e50d03 x525, 003332 x6, 003336 x19, 003337 x10, 300404ff x14, 102404ffff000000 x3`; `OLE CFB @ -1`; `JFIF @ 3560`.
5. **Ivanti IDAC documentation** (`help.ivanti.com/ht/help/en_US/IDAC/vNow/api/Content/policies.htm`, custom file types), DDG-lite snippet verbatim: "V5_CFV2 is found at the beginning. A few 32-bit integer offsets follow (call them @off1 and @off2). Then an FF block of 8 bytes follows. At @off1 you find CATIA_V5 CB0001. File size is @off1 + @off2. These kinds of properties can usually be reverse-engineered using a HEX editor." Independently matches my byte analysis (off1 = directory_offset, off2 = directory_length).
6. **Stack Exchange** (api.stackexchange.com 2.3, bodies in `raw/so/`): Q 45237882 "Catia CATProduct & CATPart File Formats" (2017-12-12, score 8, 1539 views, zero answers: the community had no answer pre-2026). Q 44952646 (2017-11-30) body contains a notepad++ string dump of a real CATPart with verbatim tokens `StoragePropertyB(4Cont_0_e64_51890fa9_1ab4`, `DASSAULT-SYSTEMES CATIA 041803P`, `CATDocumentProperty`, `CATSymbolProperty`, `CATOctetArray`, `GenericLocate...DocId:File;CATPart);C:\Users\Public\...\CATPart`, `Features.feat`, `ProductModel.feat`, `MecMod.feat`, `CATHybridShape.feat`, `CATSummaryInformation ... LastSaveVersion 5/19/...` (UTF-16LE).
7. **3DXML**: xeokit SDK "3DXML Format Guide" ("A .3dxml file is a ZIP archive of XML documents... entries are normally DEFLATE-compressed"), Spatial glossary, Okino ("zip archive that contains a BOM ... and one or more 3D representation files"), file-extension.info ("partially proprietary format with a specification published by Dassault Systèmes").
8. **Detection/trivia**: filext.com CATDRAWING page quotes magic `56 35 5F 43 46 56 32 00 00` `V5_CFV2`; catia2.cad.de CatThumbnail: "The program first checks the file ending, then looks for a V5-Header ('V5_CFV2'). If both are OK, the JPeg signature is sought out by first looking for the string 'JFIF', and then the markers 'FF D8' and 'FF D9'."
9. **Search log**: successful queries: DDG lite `V5_CFV2`; DDG lite `"V5_CFV2" CATProduct`; DDG lite `.3dxml zip OPC unzip`; Stack Exchange API `catpart format` / `catpart binary`; GitHub repo API `catia`, `catpart`; local greps (PRONOM clone, file magdir, cadmpeg docs). Blocked/failed with evidence recorded in earlier journal: DDG html, Mojeek, ecosia, marginalia, metager, startpage, searx instances, Bing RSS/HTML (garbage), grep.app, GitLab search, searchcode; final two DDG lite queries (DCF, sldprt precedent) returned a bot captcha. DCF/CATFMT/OPC-for-native: no public primary evidence found; treat those names as unverified terminology (SPECULATIVE).
