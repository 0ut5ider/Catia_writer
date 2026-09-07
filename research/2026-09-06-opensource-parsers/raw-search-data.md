# Raw research data: CATIA V5 open-source parsers

Companion to `catia-re-opensource-parsers.md`. Date: 2026-09-06.
Excerpts marked VERBATIM are copied exactly from fetched sources. Others are faithful summaries.

## 1. PRONOM signatures (VERBATIM from pronom.nationalarchives.gov.uk, fetched 2026-09-06)

x-fmt/439 "CATIA Model (Part Description)", version 5, ext `catpart`, disclosure Full:

```
Note: CATIA Version 5 identifier plus file extension of the file name (.CATPart)
Byte sequences:
  Min Frag Length: Absolute  from BOF: Offset 0  Max offset None
  Byte Sequence: 56355F434656320000*2E43415450617274
  Endianness: Little-endian
Changelog: Updated in V101 (15 Feb 2022); Added in V45 (6 Dec 2010)
```

ASCII decode: `V5_CFV2` + `00 00` + wildcard + `.CATPart`.
x-fmt/440 (catproduct) and fmt/1615 (catdrawing): same prefix, wildcard then embedded ASCII filename; fmt/1615 ends `434154447277436F6E74` = `CATDrwCont`.
Source JSON mirror: github.com/nationalarchives/pronom `signatures/fmt/1615.json`; Go port: richardlehane/siegfried `cmd/roy/data/pronom/fmt1615.xml`.

## 2. cadmpeg (fetched 2026-09-06 from main)

Repo metadata (VERBATIM fields): created 2026-07-10, pushed 2026-09-06, 32 stars, license Apache-2.0 code / CC-BY-4.0 docs, Rust workspace `crates/cadmpeg-*`, codec crate `crates/cadmpeg-codec-catia`.

`docs/layouts/catia.toml` (VERBATIM head):

```toml
schema = 1
format = "catia"
spec = "docs/formats/catia.md"
endianness = "little"
note = """
Covers the container headers and stream directory (§3), the `SurfacicReps`
roster rows and analytic surface records (§3.5, §5.8), the `0x60` curve-support
row (§5.5), the consolidated record framing families (§6), the outer schema
records (§7), the zero-entity `a9 03` framing (§8), and the E5 framing (§9).
§1 states the global rule: all multi-byte integers are little-endian unless
explicitly marked BE, and float coordinates are in millimetres. ...
"""

[[record]]
name = "outer_header"
parsed_by = "crates/cadmpeg-codec-catia/src/container.rs"
kind = "byte"
section = "3.1"
anchor = "0x00..0x07 magic = \"V5_CFV2\\0\""
size = 64
note = "`directory_offset + directory_length == file_size`. ..."

[[record.field]]
name = "magic"          offset = 0   type = "bytes[8]"  value = "V5_CFV2\u0000"
name = "directory_offset" offset = 8  type = "u32" endianness = "big"
name = "directory_length" offset = 12 type = "u32" endianness = "big"
name = "fill_ff"          offset = 16 type = "bytes[8]" (ff * 8)
```

`docs/formats/catia-coverage.md` (VERBATIM head + gate table summary):

```
The reader recognizes `V5_CFV2` part documents and classifies their geometry
storage as `standard_nested`, `fbb_only`, `zero_entity`, `e5_stream`,
`float_packed_inner_no_fbb`, `inner_no_directory`, or `unknown`.
The codec score is L1. Geometry on the `standard_nested` layout ... shows as extras.
```

Gates: L0 detection+metadata PASS; L1 container navigation PASS on recognized layouts; L2 points/analytic/NURBS PASS for standard_nested only; L3 topology INCOMPLETE; L4 features INCOMPLETE; L5/L6 INCOMPLETE. Color packets: `EB 01 R G B` (per-face) and `EC 03 R G B A` (body); dedup by RGBA; `EC` population must equal FBB face-row count to bind positionally.

`docs/formats/catia.md` (summary of sections §3-§9, fetched in full earlier):
- outer header above; trailing stream directory magic `CATIA_V5 CB0001\0` ... terminator `CB__END`; stream descriptor: logical length +0x0C, extent count +0x50; extents 20 bytes (offset/length u32 BE relative to inner `V5_CFV2` magic).
- nested inner `V5_CFV2` container; named logical streams incl. `MainDataStream`, `SurfacicReps`, `Data`; UUID stream names pattern w1_w2(8hex)_w3.
- `FINJPL  ` segments (8+2 bytes); type word `0x01010003` project-flags: `LastSaveVersion` between ASCII tags `<Version> </Version> <Release> <ServicePack> <BuildDate> <HotFix>`; JPEG preview `ffd8...ffd9`; external refs: `CATStorageProperty`/`CATUnicodeString`/`CATIA` + path ending `.CATPart`/`.CATProduct`/`.CATShape`/`.cgr`.
- geometry rows: `FBB` face rows; vertex row `05 08 01` 15-byte (3x float mm LE); `00 33 <kind>` surface markers; edge tables widths u8/u16be/u24be; `0x60` curve-support row; NURBS storage classes `a5 03 34/32/20`, `a8 <flag> ...`, `a9 03 ...`; E5 framing `0D 03`.
- identity: allocation / occurrence / definition layers; vertex ids positional.

`docs/formats/catia-open-items.md` (summary): unresolved - extent `flags` bit meanings; compact schema-program semantics; schema-role selectors; inline `7C09` reference roles; relation-result binding; release-band envelope.

`LEGAL.md` (summary): clean-room; no vendor SDKs, no decompilation, no SDK-derived constants; decoder changes need byte-backed provenance; corpus/ under CC0.

`docs/roadmap.md` line 63 (VERBATIM): native-format readers planned/claimed list includes `CATIA V5 .CATPart`. No CATIA write row anywhere; format-support matrix shows CATIA write "none" (STEP/IGES writers at L9).

## 3. KaiUR/Pycatia_Scripts/Utility_Scripts/Show_CATIA_File_Info.py (VERBATIM core, fetched 2026-09-06)

```python
V5_MAGIC    = (b'V5_CFV2', b'V5_CFV4')
...
def detect_version(data):
    if not any(data.startswith(m) for m in V5_MAGIC):
        return None, None, None
    m = re.search(rb'V5R(\d+)SP(\d+)HF(\d+)', data)
    if m:
        return int(m.group(1)), int(m.group(2)), int(m.group(3))
```

Header comment (VERBATIM): "Reads filesystem metadata and the embedded version tag from .CATPart, .CATProduct, .CATProcess and .CATDrawing files ... No CATIA session is required." Date 28.05.26.

## 4. sobalvarro/CATProductFiles Form1.cs (VERBATIM core, fetched 2026-09-06)

```csharp
//Read the product file and store as an UTF8 string
string productUTFText = File.ReadAllText(productFullFileName, Encoding.UTF8);
//Find the beginning of the CATOctetArray, that means the start of the portion where the components are listed
int octetArrayStart = productUTFText.IndexOf("CATOctetArray");
//Find the end of the CATOctet Array
int octetArrayEnd = productUTFText.IndexOf("\u0008FINJPL", octetArrayStart);
...
//Create a raw list by splitting the octet array on "[SCH][EOT]File Keyword
string[] docIdseparator = { "\u0001\u0004File" };
List<string> rawFileList = octetArray.Split(docIdseparator, StringSplitOptions.None).ToList();
```

## 5. OCCT public tree (fetched 2026-09-06)

`src/DataExchange` contains ONLY: TKBinXCAF, TKDE, TKDECascade, TKDEGLTF, TKDEIGES, TKDEOBJ, TKDEPLY, TKDESTEP, TKDESTL, TKDEVRML, TKRWMesh, TKXCAF, TKXSBase, TKXmlXCAF. No TKDECATIA / no catia dirs anywhere in repo (repo-wide search: incidental comment mentions only). `FA_CATIA`/`CatiaTo_occ` appear only in commercial Data Exchange product pages (opencascade.com / opencascade.wikidot.com/dataexchange).

## 6. Negative-result searches (all executed 2026-09-06, authed GitHub code search unless noted)

- `catia`/`catpart` in assimp/assimp: 0 hits (incl. README format list).
- `catia`/`catpart` in Kitware/VTK: 0 hits.
- `catpart` in FreeCAD/FreeCAD: 0 code hits (one STEP test asset mentions CATIA as author string).
- `catia` in file/file magic: 0 hits.
- repo search "libcatia", "catia-reverse", "open catalogue catia": 0 matching projects.
- code search `catpart` + writer/encoder/generate/write: no project writes catpart.
- repo search `.cgr` reader / CATIA V4 `.model` reader (public): none.
- npm registry search "catia": only unrelated packages.
- fougue/mayo supported formats (VERBATIM README list): STEP, IGES, BREP, DXF, OBJ, glTF/glb, VRML/X3D, STL, 3MF, AMF, PLY, TIFF - no CATIA.
- mlightcad/cad-viewer: DXF/DWG only.
- NVIDIA usd-convert-cad PyPI (VERBATIM): license "NVIDIA Omniverse Licensing Terms", "The wheel includes the converter command line, Python package, required native runtime components, and the canonical agent skill." Closed native kernel.

## 7. Other corroborating excerpts (VERBATIM)

KaiUR + transmagic + lepore magic (fetched 2026-09-06):

```
# transmagic.com/what-cad-format-do-i-have-here/
"CATPart V5 part and assembly files will start with V5_CFV2, and you can also tell
what release of V5 by searching on V5, for example – V5R20SP6HF16 built on 10-25-2011.11.21
... if you search on CATSummaryInformation or LastSaveVersion you will find the last saved
version, the release, service pack and minimal version to read."

# glepore70/pronom-research/lepore_magic
# CATIA V5 Data
# https://transmagic.com/what-cad-format-do-i-have-here/
0	string	V5_CFV2	CATIA V5 Data
!:ext	catpart

# abbaye/WpfHexEditorIDE CATPART.whfmt (claim checked and REJECTED):
# magic "V5.05..." = 56 35 05 00 00; contradicts PRONOM, cadmpeg, KaiUR, file-format/Docs
# (all: 56 35 5F 43 46 56 32). Treat whfmt as unverified prose.
```

HOOPS Exchange (Wayback 2017-07-04, VERBATIM fragment): support list "CATIA V4, V5 and V6 ... tessellated and B-rep data plus PMI".

3DXML open parsers: Terrev/3DXML-to-OBJ (35 stars), gxh-0808/3dxmlToGLtf (14 stars), z1130/convert_3dxml_to_fbx, xeokit/xeokit-convert - parse Dassault's zip+XML 3DXML to OBJ/glTF.

## 8. Access/tooling notes

- gh CLI authed as Construkted-Reality; code search worked; several anonymous API calls rate-limited (use auth).
- FreeCAD forum + wiki behind Anubis challenge; could not fetch thread bodies.
- techsoft3d.com / cadexchanger.com current pages 404 (domains restructured); used Wayback + wikidot mirror.
- DuckDuckGo html endpoint throttled intermittently; Bing used as fallback; DDG results quoted only where fetched directly.
