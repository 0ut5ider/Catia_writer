# CATIA V5 format internals (research report)

- Date: 2026-09-06
- Role: web research agent (research only, no product code)
- Question: what is known about the internal structure of CATIA V5 native files (.catpart, .catproduct, .catsettings, .3dxml) at a level sufficient to reverse-engineer and GENERATE valid files
- Model: anthropic claude (via opencode)

Every claim below carries a source and an access date (2026-09-06 unless noted). Confidence: **[V]** = empirically verified here on real files, **[S]** = well-sourced document, **[F]** = folklore / repeated without evidence.

## 1. Headline findings

1. `.CATPart`/`.CATProduct` are NOT OLE2/CFBF compound files. Real samples begin with ASCII `V5_CFV2`, contain no `D0CF11E0` signature, and PRONOM's OLE2 container-signature file has no CATIA mapping. **[V]** The widely repeated "Microsoft Compound File" description is folklore. **[F]**
2. The container is a "CATIA V5 compound" (magic `V5_CFV2`) with a header whose two big-endian u32 fields exactly locate a stream directory. Verified on 5/5 real files. **[V]**
3. The best public reverse-engineering reference is the `cadmpeg` project's `docs/formats/catia.md` (265 KB, CC-BY-4.0): byte-level, machine-checked, with a six-variant taxonomy. It is decode-only today (V5 -> STEP), and its CATIA support is rated L1, so treat it as a spec of what is *known*, not proof of easy write support. **[S]**
4. Generation of a CATIA-openable `.CATPart` from scratch means reproducing an object graph (`7C 0x` tagged records, topology spine, stream directory). Nobody has published a complete write recipe. The pragmatic generation routes remain STEP/IGES import or official SDKs. **[S]+[V]**

## 2. Outer container `V5_CFV2` (empirically verified)

Verified 2026-09-06 by hexdump of 5 real files: 3 small doc-sample parts from the PRONOM research corpus (`glepore70/pronom-research`), one real 481 KB `.CATPart` and one 381 KB `.CATProduct` (Git LFS media of `Guilherme115/Motor-V6`). See `samples/hexdump-verification.txt` and the sample binaries in this directory.

Layout (all integers big-endian unless noted):

| Offset | Size | Content | Evidence |
|---|---|---|---|
| 0 | 9 | ASCII `V5_CFV2\0\0` (PRONOM part/product signatures cover `56355F434656320000`) | [V][S] |
| 8 | 4 | `D` = directory offset, u32be | [V] |
| 12 | 4 | `P` = directory length, u32be; identity `D + P == file_size` holds on all 5 files | [V] |
| 16 | 8 | `ff ff ff ff ff ff ff ff` block | [V] |
| 24.. | - | zero padding, then segments and stream payloads | [V] |
| D..EOF | P | stream directory starting `CATIA_V5 CB0001\0`, ending `CB__END\0`; the last 2 bytes before `CB__END` echo the low half of `P` | [V] |

- Matches the Ivanti IDAC description (two u32 offsets, FF block, `CATIA_V5 CB0001`, size = off1+off2): https://help.ivanti.com/ht/help/en_US/IDAC/vNow/api/Content/policies.htm [S] and confirms it in exact byte positions. **[V]**
- PRONOM: x-fmt/439 `.catpart` (signature 239: `V5_CFV2\0\0` at BOF + `.CATPart`), x-fmt/440 `.catproduct` (348), x-fmt/438 `.catmaterial` (345), fmt/1615 drawing (1950: `V5_CFV2\0` + `CATDrwCont`), CATIA V4 x-fmt/436 (`CATIA   ` + `CATIA SOLUTIONS V4`), V3 fmt/1714 (`CATIA VERSION 3`). Source: DROID SignatureFile V125, https://www.nationalarchives.gov.uk/documents/DROID_SignatureFile_V125.xml [S]

### Stream directory
- Directory entries carry stream names as UTF-16LE with `00 00` terminator (verified via descriptor grammar). Names observed in real files: `MAIN`, `MainDataStream`, `Header`, `Describe`, `CATPreview`, `CATDocumentProperty`, `CATStorageProperty`, `CATPropertySets`, `Data`, `Format`, `TimeStamp`, `Project`, and `Cont_<hex>` per-container streams. **[V]**
- Descriptor grammar (extent table: per extent `phys_off`, `phys_len`, `log_len`, `log_off`, `flags`, all u32be; `logical_stream_length` at ds+0x0c; extent count at ds+0x50; validation rules; legacy vs standard descriptor forms): cadmpeg `docs/formats/catia.md` §3.4. **[S]**
- The outer logical stream `Data` carries model-container declarations (`01 00 03 00`, class name strings, and the 16-byte id whose last three BE u32 words form the `Cont_<w1>_<w2:08x>_<w3>` stream name). cadmpeg §3.1. **[S]** `Cont_` stream name fragments are visible in the verified hexdump. **[V]**
- `FINJPL  ` (two trailing spaces) marks named segments after the outer preamble; four-byte BE type word follows; segments live inside `[P,D)` region bounded per cadmpeg §3.3. Four `FINJPL` occurrences verified in `analysis.catpart` at 0x244b, 0x25d3, 0x2896, 0x2cca. **[V]**

### Nested inner `V5_CFV2`
- Real-world model files nest a second `V5_CFV2` sub-container inside the outer body: verified in `spur_gear.CATPart` at 381501, with its own header whose D=79599 (relative to the inner magic) points at a second `CATIA_V5 CB0001` directory at absolute 461100, while the outer directory sits at 471773. **[V]**
- Not all files have it: the 3 small PRONOM doc-sample parts have no inner container. cadmpeg treats this as one of six variant families (standard nested, FBB-only, E5-stream, zero-entity `a9 03`, float-packed inner-no-FBB, inner-body-without-directory). **[V]+[S]**

### Version stamps
- `analysis.catpart` contains ASCII `V5R24SP4HF0 built on 06-16-2014.20.00` in the `OSMX`/`CATOsmMetaData` area (string scan). **[V]**
- cadmpeg documents a `LastSaveVersion` summary field with `<Version>/<Release>/<ServicePack>/<BuildDate>/<HotFix>` delimited ASCII tuples; conflicting tuples do not define a governing version (docs line 82). **[S]**

## 3. Semantic payload (inside MAIN/MainDataStream)

Only cadmpeg documents this, at byte-marker level **[S]** (see `source-cadmpeg-catia-format-spec.md`, the full 2026-08 copy; and `source-cadmpeg-layout-table.md`):

- Segment/entity markers: `FINJPL` segments; `7C 02` source-schema catalog; `7C 05/08/09/0A` entity table, object-graph root, object records, tagged atoms; `7C D9` float data.
- Topology spine: face-boundary rows `30 xx 04 04 ff`; edge-table delimiter `10 24 04 ff ff 00 00 00`; vertex records `05 08 01` (15 bytes, 3×f32le XYZ); surface kind `00 33 <30-38>`; per-edge curve support `0x60`.
- Object-stream record families `a5/a8/b5 <frame_flag>`; freeform surface `a5 03 34`; freeform 3D curve `a5 03 32`; pcurves `CATPSpline`; analytic surfaces `b2 03 19/28/29/2a/2b/2d` (circle/cylinder/cone/sphere/torus/revolved); line profiles `b2/b3/b4 03 0e`.
- Expressions/parameters: full typed expression grammar and relation-entity framings documented (docs § on `RelationExpFct`, `ParserVersion`); units incl. `mm/in/deg`, functions, dimension algebra.
- External references in `.CATProduct`: atom sequences under `CATStorageProperty` naming `.CATPart/.CATProduct/.CATShape/.cgr` targets (cadmpeg §3.3).
- Honest caveats in cadmpeg's own docs: six variant families, `catia-open-items.md` lists unresolved structures, codec rated L1 (lowest support tier), decode-only to STEP. LEGAL.md: knowledge came from legally owned files plus public documentation; no vendor SDKs or decompilation.
- No other public source documents the semantic payload. Old OLE-adjacent blog lore, `file(1)` (zero CATIA magics; cloned and grepped 2026-09-06), and FIDO `format_extensions.xml` (zero entries) add nothing. **[S]**

## 4. `.catsettings`

- No PRONOM signature (DROID V125 has only the 7 CATIA formats listed above). No GitHub file samples or parser found. No public spec found. **[S/absent]**
- Community lore says it stores catalog/environment settings in the same CATIA compound family, but I found no citable source and no sample. **[F]** Treat as: same-container class as other V5 documents is *plausible but unverified*.

## 5. `.3dxml`

- A ZIP archive containing an XML "BOM" (bill of materials) file plus one or more 3D representation files, in either ASCII XML or binary PRC form; meshes as triangles/trifans/trisets or Gregory patches. Source: Wikipedia "3DXML", rev 2025-08-09, https://en.wikipedia.org/wiki/3DXML [S, medium authority]
- Binary representations are PRC = ISO 10303-224 (Product Representation Compact), a public standard also used by U3D and 3D PDF. **[S]**
- Dassault grants a yearly royalty-free license for the 3DXML format documentation, internal use only (Wikipedia citing the license text). **[S]**
- Open-source consumers that imply parseable structure: xeokit SDK has a 3DXML loader; GLC_Player reads ASCII 3DXML. **[S]**
- DROID V125 contains no 3DXML signature (grep, 2026-09-06). **[V]**
- Practical note: generating ASCII-mode 3DXML (ZIP + BOM XML + triangle/patch meshes) is feasible from published examples without any NDA spec; binary PRC requires the ISO 10303-224 standard. **[judgment]**

## 6. OLE2 folklore, traced

- The premise "catpart is a Microsoft Compound File Binary (D0CF11E0)" appears on file-extension sites (e.g. filext/docs.fileformat.com style pages, accessed 2026-09-06) and in a Google AI-mode answer claiming OLE2 streams like `FarthestStreamedVersion`. **[F]**
- Disproof: 5/5 real files start `V5_CFV2`, none contain `D0CF11E0` anywhere (see `samples/hexdump-verification.txt`); DROID `container-signature-20260119.xml` (fetched today) maps no CATIA extension inside OLE2; `file(1)` Magdir has no CATIA entries. **[V]**
- Probable origin: early `oletools`/POLE app lists and digital-preservation blogs loosely tagged CATIA among "compound file" users; V5 documents superficially resemble CFBF (directory of named binary streams). Speculation, flagged as such.

## 7. What generation would require (synthesis)

To write a `.CATPart` that CATIA opens you must emit, in order of hardening:
1. Valid outer container: header, `Data` stream declarations, FINJPL segments, CB0001 directory with consistent extents, `CB__END`, and the size identity. Fully spec'd (cadmpeg §3) and verified here. Achievable today. **[V][S]**
2. A directory-consistent stream set (`MAIN`, `MainDataStream`, `Header`, properties). Grammar known; per-stream content contracts partly known. **[S]**
3. The semantic object graph (entities, topology spine, geometry records, feature/parameter records). Marker-level spec exists (cadmpeg) but with open items; round-trip fidelity and version acceptance (R14..R32 differences, compact vs optimized save) are NOT documented anywhere public. This is the wall. **[S]**
4. Realistic alternatives confirmed by this research: generate STEP AP242 and let CATIA import; or use official 3DEXPERIENCE/ENA (CAA) licensing routes; or target ASCII 3DXML for downstream tools instead of native V5.

## 8. Sources

Full list with dates in `sources.md`. Raw evidence: `samples/` (5 binaries + `hexdump-verification.txt`), `source-cadmpeg-catia-format-spec.md`, `source-cadmpeg-layout-table.md`; more raw dumps in `/tmp/catia_re/` (DROID XMLs, search dumps).

## 9. Open items

- No public spec found for: compact-vs-optimized save semantics, R-version acceptance rules, `.catsettings`, `CATIA_V5 CB0001` descriptor fields at `ds+0x50` beyond extent count, and the `OSMX` early-block grammar beyond strings.
- A real R32 (2022+) native sample would test the variant families; only R24-era and unknown-version LFS files were reachable here.
