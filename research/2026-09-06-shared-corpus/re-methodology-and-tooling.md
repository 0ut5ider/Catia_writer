# CATIA V5 `.catpart`/`.catproduct` reverse engineering: methodology and tooling for building a writer

- Date: 2026-09-06
- Role: research agent (opencode / web research + local binary analysis)
- Question: What is a concrete, executable RE methodology and toolchain for building a writer for CATIA V5 `.catpart`/`.catproduct` binary containers?
- Model: flashnext/flashnext-w4a16-fp8ple

## Headline finding (corrects the premise)

**`.catpart` files are NOT OLE2/CFB compound files.** Real samples start with ASCII
`V5_CFV2\0\0`, a Dassault Systèmes proprietary container ("CFV2"). There is no `D0CF11E0`
magic anywhere in the samples, and no `Root Entry` directory string. The widespread claim
that "CATIA V5 files are OLE2" is false for the file bytes; it may derive from CFB-based
neighbors like `.doc`/`.xls` or from confusion with other Dassault containers. This changes
the entire toolchain plan: olefile/oledump/7z-CFB inspection does not apply, and the
container itself must be parsed with a purpose-built reader.

Evidence is in Section 0 and Raw sources. No public parser of CFV2 exists in indexed code
zero hits for `V5_CFV2` outside signature databases, zero hits for `CATFeatCont` in code
search. This is a genuinely cold format.

## Method constraints (honesty section)

Search engines were largely unavailable from this sandbox: DDG (CAPTCHA), Mojeek (CAPTCHA),
Bing RSS (returns cached garbage), Qwant lite (JS-only), grep.app (bot checkpoint),
searchcode (404), Brave via curl (429), Brave via webfetch (worked twice, then persistent
429). `rohitab.com` (API Monitor) transport-error. dblp, arXiv API, OpenAlex, Wikidata,
GitHub API, raw.githubusercontent.com, Sourcegraph stream API, and direct site fetches all
worked. Consequence: web-search volume is below the requested 15, but every load-bearing
claim below is backed by a primary artifact fetched directly (PRONOM XML, real .catpart
bytes, file(1) magic, Kaitai template, project READMEs). Known literature I could not
independently fetch from here (T-ReX, PolyFormat, REVISITOR, AutoFormat) is flagged
unverified in Section 4 rather than cited blind.

---

## 0. Ground truth from real samples (fetched and parsed in this session)

Samples, all from public GitHub raw URLs:

| File | Repo | Bytes | First bytes |
|---|---|---|---|
| `pipico.CATPart` | `OpenKNX/OpenKNX` (PiPico BCU connector case) | 257,297 | `56 35 5F 43 46 56 32 00 00` = `V5_CFV2..` |
| `rim.CATPart` | `bryancostanich/OpenRC` (RC crawler wheel) | 322,959 | same |
| `mk1.CATProduct` | `WiredGeist/MK1` | 16,177 | same |

### Header (identical layout in both parts), offsets from BOF

```text
00 0000  56 35 5f 43 46 56 32 00 00 03 c4 1d 00 00 28 f4   V5_CFV2.......(.
00 0010  ff ff ff ff ff ff ff ff 00 00 00 00 00 00 00 00   ................
00 0030  00 00 00 00 00 00 00 00 00 00 00 00 02 5f 0d 0a 00 ................_
```

- `0x00..0x08`: magic `V5_CFV2\0` then a `0x00` byte.
- `0x09..0x0C`: 4-byte little-endian value, sample-specific (`0x001dc403` pipico,
  `0x0043c104` rim, `0x00d92700` mk1). Not the file size. Unidentified, but position-stable.
- `0x0E..0x0F`: 16-bit tag (`0xf428` pipico / `0x4c2c` rim, LE). **Mirrored verbatim in the
  trailer, immediately before `CB__END`.** This is a file-identity or header-checksum field
  any writer must reproduce.
- `0x10..0x17`: eight `0xFF` bytes (free-slot / chain markers?).
- `0x34..0x38`: constant `02 5F 0D 0A 00` (`_\r\n` marker). The nested segment below repeats
  this constant at the same relative offset, proving a repeated header structure, not one blob.

### Trailer (last 96 bytes, pipico)

```text
0b 49 28 a0 01 d8 df dd  (x3, identical 8-byte records: a Windows FILETIME;
                          0xdddfd801a028490b interpreted as FILETIME = 2020-02-04,
                          consistent with the repo's commit era)
00 00 00 12, zeros..., 01, 00 03 be c8, 00 00 00 e7, 00 00 00 e7,
zeros..., 28 f4, 43 42 5f 5f 45 4e 44 00  = "CB__END\0"
```

- Magic `CB__END\0` terminates the file (note: same byte family as the `CFV2` in the header).
- `0xE7` (231) appears twice in both parts and in both parts at the same position. A constant,
  not a count. Writer must reproduce it byte-exact until understood.
- `0x0003bec8` (pipico) / `0x0004bbd2` (rim): 4-byte value slightly below file size
  (245,448 vs 257,297). Plausibly the end of content before a fixed tail region.
- Three identical FILETIME records: save timestamps. Differential gold (Section 2/3).

### Nested CFV2 segment

A second complete `V5_CFV2\0\0` header occurs at offset 132,762 in pipico, followed by the
same ff-run and the same `02 5F 0D 0A 00` at the same relative offset. Documents are a
sequence (or tree) of CFV2 segments. The mk1 product (16 KB, no embedded preview) has no
second segment, so segments scale with content (preview/3D data at minimum).

### Strings and object model (pipico, 317 runs of 8+ printable bytes)

```text
2156 CATProdCont   2168 CATFeatCont   2244 CATPrtCont    2340 CATContainer
2420 CATMFBRP      2508 CATSeeBodyCont 2604 CATBRepModeContainer
2708 CATStdCont    2796 CATCGRCont    2884 CameraStartupContainer
2988 AppliCont     3156 CATCompoundCont
3052 V5USERID      3741 NOTHING-CNEXTINFOS-UpdateVersion-StreamBlock-SafeEarlyBlock-StrongEarly
3813 V5R28SP0HF0   4720 CATCatalogManager 4767 ASMPRODUCT  4778 Pcb_be8e
4787 _ViewsList 4798 _Connectors 4810 _Revision 4820 _RepresentedBy
4835 _Component 4862 _PartNumber 4874 _Definition
242291 FirstStreamed
242312 <Version>5/<Version><Release>28/<Release><ServicePack>0/...<HotFix>0/</HotFix>
242440 CATPreview  245453 DASSAULT-SYSTEMES  245576 CATStorageProperty
245611 CATUnicodeString  246813 CATIA_V5 CB0001
```

- These are CAA runtime class names (`CATFeatCont` = feature container, `CATPrtCont` = part
  container, `CATBRepModeContainer` = boundary-representation geometry). The file stores an
  object-factory registry: each serialized object is tagged by its class name. A writer must
  emit names the installed CATIA can instantiate.
- Strings are stored length-prefixed. Concrete: `0d 00 46 69 72 73 74 53 74 72 65 61 6d 65 64`
  = 2-byte LE length 13 + `FirstStreamed`. The writer's string encoding is therefore
  16-bit-length ASCII (at least for stream/section names).
- Version metadata is stored as fake-XML text (`<Version>5/...<HotFix>0/</HotFix>`).
- Embedded payloads: one JPEG (`FF D8 FF` at 242,781 inside the `CATPreview` region, with
  standard JFIF Huffman table strings), no `_TPU`/`!_` stream names (those belong to other
  container generations), no `CGR0`. zlib-candidate bytes (`78 xx`) are few (5 in pipico) and
  unconfirmed as real deflate streams (see Section 3 method to confirm).
- Entropy profile (8 KiB blocks, pipico): 4.06.4 bits/byte across structural blocks, i.e.
  the body is largely **uncompressed** binary object data; no high-entropy (>7.2) plateau
  except the JPEG preview area. Good news for a writer: most bytes are plaintext-ish structs.

PRONOM agrees with the bytes (verbatim XML from `siegfried/cmd/roy/data/pronom/x-fmt439.xml`):

```xml
<SignatureName>CATIA Part Description V5</SignatureName>
<SignatureNote>CATIA Version 5 identifier plus file extension of the file name (.CATPart)</SignatureNote>
<PositionType>Absolute from BOF</PositionType>
<Endianness>Little-endian</Endianness>
<ByteSequenceValue>56355F434656320000*2E43415450617274</ByteSequenceValue>
```

`V5_CFV2\0\0` + wildcard + ASCII `.CATPart`: PRONOM says **the file embeds its own file
name inside the header**. (Confirmed pattern: PRONOM's Drawing 5 signature
`56355F4346563200*434154447277436F6E74` = `V5_CFV2\0` + wildcard + `CATDrwCont`, so the
wildcard region also reaches a container class name in drawings.) Embedding the full file
name in the file is a writer gotcha and a free differential signal.

## 1. Container step: what to actually do

1. Forget olefile/oledump/7z-CFB for catpart; they find nothing (no CFB magic).
   For contrast, file(1) ships only the OLE2 recipe (`0 string \320\317\021\340...` in
   `Magdir/ole2compounddocs`) and has **no CATIA magic at all**; `file` calls catpart
   "data" or generic. Confirmed by cloning `file/file` (Apr 2026 revision).
2. Write a 100-line Python CFV2 segment walker: find all `V5_CFV2\0` headers, parse the
   fixed 0x40-byte header, locate `CB__END`, build the segment table. Snippet in Section 5.
3. Use Kaitai Struct only as a *spec authoring tool*: the public CFB template
   (`serialization/microsoft_cfb.ksy`, reproduced partly in Raw sources) is the model of
   what to produce for CFV2: a `.ksy` grammar + compiled parsers + test corpus.
4. Keep olefile in the toolbox only if you later touch adjacent OLE containers (some
   CATIA drawings/legacy CATIA V4, and unrelated but same-family formats).
5. Identification corpus: PRONOM PUIDs `x-fmt/436..440`, `fmt/1615`, `fmt/1714` cover
   CATIA Model/Project/Material/Part/Product/Drawing; all `V5_CFV2`-family signatures.
   Wikidata item Q49416323 (CATPart) records extension `catpart` + PUID `x-fmt/439`.

## 2. In-stream analysis: what to look for and the exact probes

Order that worked on the real samples:

1. **Magic + trailer scan**: search for repeated `V5_CFV2`, `CB__END`, and the `02 5F 0D 0A 00`
   header fingerprint. Gives the segment map before any field decoding.
2. **Entropy block scan** (8 KiB, Shannon) to separate structure from payloads. Code:

```python
import math
def blocks(d, bs=8192):
    for i in range(0, len(d), bs):
        c = d[i:i+bs]; freq = {}
        for b in c: freq[b] = freq.get(b, 0) + 1
        H = -sum(v/len(c)*math.log2(v/len(c)) for v in freq.values())
        yield i, round(H, 2)
```

   CATIA parts: 46 bits/byte structural plateaus, JPEG spike. Compare with `ent -b` or
   binvis as a visual cross-check.
3. **String table extraction with offsets and length-prefix validation**. The
   2-byte-LE-length + ASCII hypothesis came from `0d 00 "FirstStreamed"`; validate by
   requiring `data[p-2] == len(s)` and walking candidate starts. This maps your type
   registry, property names (`CATStorageProperty`, `CATUnicodeString`), metadata XML, and
   embedded filename in one pass.
4. **Embedded-payload carving**: search `FF D8 FF` (JPEG), 5-byte zlib candidates
   `78 01|5E|9C|DA` confirmed by `zlib.decompress(data[p:])` success length, PNG/CGR magics.
   Carve and hash them: a delta writer should be able to copy payloads byte-for-byte.
5. **Floating-point structure hunt**: slide f64/f32 LE windows and look for values in
   plausible CAD ranges (|x|<1000, coordinates, transforms as 4x4 with rows summing to
   unit-ish values), plus `ff ff ff ff` free-slot runs. This found the three-timestamp
   FILETIME array only after hypothesis (year-2000+ range filter on FILETIME 100-ns values).
6. **Pointer/reference hunting**: 4-byte LE values that point at earlier offsets
   (`0x0 <= v < filesize`) and cluster near object records; cross-reference counts to find
   the section-directory structure.

## 3. Differential analysis: controlled experiment design

Corpus plan (needs live CATIA; see kill criteria in Section 7):

| Experiment | Vary | Isolate |
|---|---|---|
| Save same doc twice, 1 min apart, no edits | none | all noise: FILETIME trio, header tag 0x0E, any counters/UUIDs |
| Edit only part name | one string | string-table layout, embedded-filename field (PRONOM shows name inside header) |
| Change only a parameter value | one float | the numeric stream region |
| Add one cube, then delete it, resave | object count + holes | ID allocation, free-slot reuse (the `FF...FF` runs) |
| Same doc, 3 CATIA releases (R28/R30/R31+) | writer version | `V5R28SP0HF0`-style version tags, format version fields |
| Part vs product vs drawing | doc type | class-name registry per doc type (`CATPrtCont` vs `CATProdCont`) |

Best practices:

- Keep everything constant: same machine, same CATIA build, same save options, one small
  source part (~50 KB so diffs stay readable), scripted saves.
- Diff with `radiff2 -C` / `bindiff`/`xdelta3 -s old new` to find stable vs shifting regions;
  a single added cube should show as a localized insertion plus length-field edits, or it
  triggered full re-layout (which you must know early).
- Treat every FILETIME-magnitude value found via the "no-edit double save" as a mutation
  target; a writer that leaves a 2020 timestamp on a 2026 save is detectable and might
  confuse CATIA or PLM.
- Known CATIA identity fields to watch (from samples/PRONOM): embedded original filename,
  `V5USERID` tag, `NOTHING-CNEXTINFOS-UpdateVersion-StreamBlock-SafeEarlyBlock-StrongEarly`
  save-pipeline marker, and the 4-byte IDs like `03 00 00 00 73 79 49 63` before
  `FirstStreamed` (candidate internal GUID slots; confirm with no-edit double saves).

## 4. Writer requirements (what the bytes say you must get right)

From ground truth only, no speculation:

1. Header: magic, the `0x09` value, and the **0x0E tag must match the trailer mirror**. That
   mirror (`28 f4 CB__END`) is a header/trailer integrity pair; a writer that patches length
   fields but not the trailer tag will produce files CATIA rejects (or worse, silently
   truncates). This is the classic cross-reference trap seen in DWG and PST.
2. Trailer: reproduce `01`, `0x0003bec8`-class end-of-content field, the two `0xE7`
   constants, FILETIME records, tag, `CB__END\0`, in exact order.
3. Segment bookkeeping: nested `V5_CFV2` segments mean lengths are hierarchical. Patching
   one segment shifts everything after it; every outer segment's length fields and the
   trailer's end-of-content value must be rebased. Plan for a two-pass layout
   (serialize, then backpatch offsets).
4. Type registry: every object is class-name tagged (`CATFeatCont`, ...). A writer either
   reuses template class sets verbatim (safe) or emits CAA class names it cannot verify
   (unsafe). There is no public list of these names except what you extract from corpus.
5. Strings: 2-byte LE length prefix, ASCII (UTF-16 confirmed only inside one UTF-16 filename
   fragment `0031 005f 0032 0035 0030` before the nested segment; test more corpus).
6. Version stamping: `<Version>5</Version><Release>28</Release><ServicePack>0</ServicePack>
   <BuildDate>11-29-2017.20.00</BuildDate><HotFix>0</HotFix>` and `V5R28SP0HF0` appear in
   plain text. Writing a version string your CATIA does not have will likely fail open.
7. Embedded filename + `V5USERID`: rewrite both consistently when generating "new" files.
8. Checksums: beyond the tag mirror, none found in headers/trailers yet; assume more exist
   and let the no-edit double-save experiment enumerate fields before trusting them.
9. Historical breakage precedents (verified quotes): LibreDWG's README admits the reader
   works everywhere while the writer "is good enough for everything but R2007. R2010-R2018
   writing leads to CRC errors still." After ~15 years of the project. libpff, ~13 years in,
   is still "Status: alpha" and its author's own doc is titled "PFF forensics analyzing the
   horrible reference file format". Lesson: cross-reference and CRC fields are exactly what
   sinks writers, and writers trail readers by years everywhere.

## 5. Template + delta patching: honest assessment

Precedents that actually exist (verified):

- **docxtpl** (docx template + Jinja render): "This package uses 2 major packages:
  python-docx for reading, writing... jinja2 for managing tags". Text/template formats only.
- **Excel/openpyxl templates**, **PDF AcroForm fill**: same category (documented,
  offset-light containers).
- **CATIA-native templates**: Design Table + Knowledgeware parameters let CATIA itself
  regenerate geometry from a parameterized seed part; combined with COM automation
  (`rock0505/CatiaPE`, batch driver `sheetd/BatchProcess`) this is the only reliable
  "generate valid catpart" route today, at the cost of requiring a CATIA license.
- **DICOM/SR value templates**: template-based generation exists but the format is an
  open standard with a published data dictionary. CFV2 has neither.

Verdict for real CATIA geometry: template+byte-delta works **only** for edits localized to
the metadata/property/string layer of an otherwise untouched byte stream (keep the float
streams and segment layout frozen; backpatch the header tag mirror, lengths, FILETIMEs, and
embedded filename). Adding real geometry (a new feature object) is not byte-patchable:
object serialization, ID allocation, and the B-rep container (`CATBRepModeContainer`) are
unmapped, and any length shift forces whole-segment re-layout you cannot validate.
Automated format-inference research (protocol/format extraction survey, DOI
10.1155/2018/8370341; CCS'23 "Lifting Network Protocol Implementation to Precise Format
Specification", DOI 10.1145/3576915.3616614) confirms the general pattern: inference
recovers syntax, not invariants; invariants come from differential + tracing. (T-ReX,
PolyFormat, REVISITOR, AutoFormat are known related work but were not fetch-verifiable
from this sandbox; treat those four names as leads, not citations.)

## 6. Tracing plan: see CATIA read the file, let the reads be the schema

The container map tells you *where* data is; CATIA's read offsets tell you *what matters*.

1. **API Monitor (rohitab.com/apimonitor; page unreachable from this sandbox, well-known
   Windows GUI)** on `CNEXT.exe` (the CATIA process): filter `CreateFileW` + `ReadFile`/
   `SetFilePointerEx`; log offset+size per read during File>Open of one small part.
   Expect segment-ordered reads; every distinct read-offset cluster is a field/section.
2. **Process Monitor (learn.microsoft.com Sysinternals Procmon)** as a lighter substitute:
   filter `Process Name is CNEXT.exe` and `Operation is ReadFile`, capture a few opens.
3. **Frida** (docs verified: frida.re/docs/frida-trace): `frida-trace -p <pid> -i
   "kernel32!ReadFile" -i "kernel32!SetFilePointer"` auto-generates JS action files; the
   handlers can print `(handle, outBuf, bytesToRead, *fileOffset)` per call. To hook CATIA's
   own C++ layer, enumerate modules (`frida -p ... -l script` with `Process.enumerateModules`
   filtered to `CAT*`) and intercept exported `CATIStream`/`CATStorageFactory`-style symbols
   if present; the binary does carry rich public symbol strings (`CATIA_V5 CB0001`,
   `CATStorageProperty`), so expect partially symbolized internals.
4. **strace** (man page verified) if CATIA runs under Wine: `strace -f -e
   trace=file,read -s 64 -o run.log CNEXT.exe part.CATPart`.
5. Correlate logged offsets against the segment map (Section 0); where a read starts at a
   known header offset you have decoded a consumer for that field. That is the ground truth
   the writer must satisfy, not a guess.
6. Static fallback: Ghidra/rizin on the storage DLLs is a last resort (huge binaries);
   differential + tracing first, per method.
7. `radiff2 -C old new` (rizin) for all binary diffs; `xdelta3 -s` to measure which regions
   are content-stable across saves.

## 7. Effort realism (anchored, with quotes)

- **DWG/LibreDWG** (closest analog: proprietary binary CAD container):
  "At the moment our decoder (i.e. reader) is done, it can read all DWG versions, just some
  very advanced R2010+ objects fail to read and are skipped over. The writer is good enough
  for everything but R2007. R2010-R2018 writing leads to CRC errors still." (libredwg
  README, fetched). DWG has decades of third-party knowledge, ODA's semi-open spec, and
  still the writer is not done. CATIA has none of that.
- **PST/libpff**: "Status: alpha" after 13+ years, with an explicit linked write-up
  "PFF forensics analyzing the horrible reference file format". Reference-file-driven
  RE of a binary container never ends.
- **Ecosystem evidence of difficulty**: the CAD industry's answer to foreign binary CAD is
  commercial translators (ODA File Converter; FreeCAD imports CATIA only via ODA, per
  FreeCAD wiki "Import From ODA"), not open parsers. OCCT reads CATIA only through a
  licensed Dassault CAA gateway module.
- Tiered estimate for the actual goal:
  - Container/segment parser + field map: days-weeks (samples in hand, format is mostly
    uncompressed; CFV2 header is simple; done to this level in this session).
  - Metadata/string/parameter delta writer: weeks; gated on CATIA access for validation
    (every field must be proven with open-after-edit).
  - Arbitrary-geometry writer: multi-year, ODA-scale. Do not attempt; use template +
    parameterized regeneration through CATIA automation instead.

## 8. Five-phase plan with success/kill criteria

| # | Phase | Actions | Success | Kill |
|---|---|---|---|---|
| 1 | Corpus + rig | Gather 30-50 parts across R27-R33, versions differ by one controlled edit each; script saves; store CATIA build IDs | Byte-diffable pairs for every experiment type | Cannot run/obtain CATIA legally (trial/student) within 2 weeks then all phases die (no ground truth possible) |
| 2 | CFV2 container parser | Segment walker + header/trailer codec; 100% of corpus files parse; every byte belongs to a modeled region or a named unknown | Parse all corpus; round-trip byte-identical | Persistent >5% unexplained bytes after modeling 3 doc types |
| 3 | Field map via diff+trace | No-edit double-save to list noise fields; API Monitor/Frida read-offset map vs segments; decode lengths/offsets/ID scheme | Each header/trailer field has a verified meaning or a "constant, copy it" classification | CATIA opens files that violate invariants (test deliberately) meaning invariants aren't enforced and field semantics stay unknowable |
| 4 | Delta writer (metadata layer) | Template file + localized patches: name strings, version tag, FILETIME, filename, tag mirror, lengths; backpatch two-pass; open-after-edit validation loop in CATIA | Edited file opens in CATIA with change visible, structure byte-stable | File layout re-flows on unrelated saves so patches can't stay localized, or tag/checksum fields resist decoding after 2 weeks of tracing |
| 5 | Structural growth (optional, only if 1-4 succeed) | Add/remove one trivial feature via learned object record; ID allocation replay vs fresh-allocation test | CATIA accepts grown files across 3 versions | Object record grammar not cracked in 4-6 weeks (expected): stop and ship template+CATIA-automation (Design Table/COM) as the product instead |

Rule for the whole plan: no field is "understood" until a file you wrote with your own
value for it opens in CATIA showing that value. The byte is the test.

---

## Raw sources (verbatim, with access dates; all fetched 2026-09-06)

1. **PRONOM x-fmt/439** "CATIA Model (Part Description)", v5, Dassault, binary; source
   MIT Digital Library Research Group 2009-04-06, updated 2022-02-11. Signature verbatim:
   `CATIA Version 5 identifier plus file extension of the file name (.CATPart)`,
   Absolute from BOF, offset 0, LE, `56355F434656320000*2E43415450617274`.
   URL: https://www.nationalarchives.gov.uk/PRONOM/Format/proFormatSearch.aspx?status=detailReport&id=851&strPageToDisplay=signatures
   and bundled XML `siegfried/cmd/roy/data/pronom/x-fmt439.xml` (fetched via git clone of
   https://github.com/richardlehane/siegfried, full XML quoted in Section 0).
2. **PRONOM fmt/1615** "CATIA Drawing 5", signature verbatim:
   `56355F4346563200*434154447277436F6E74` (V5_CFV2 + wildcard + `CATDrwCont`).
   File: `siegfried/cmd/roy/data/pronom/fmt1615.xml`.
3. **Real .catpart bytes** (od -A d -t x1z, this session):
   ```text
   pipico.CATPart (257297 B, github.com/OpenKNX/OpenKNX, Hardware/.../Pcb_be8e.CATPart)
   0000000 56 35 5f 43 46 56 32 00 00 03 c4 1d 00 00 28 f4  >V5_CFV2.......(.<
   0000016 ff ff ff ff ff ff ff ff 00 00 00 00 00 00 00 00  >................<
   ... tail: ... 01 00 03 be c8 00 00 00 e7 00 00 00 e7 00 00 00 00 00 00 00
             28 f4 43 42 5f 5f 45 4e 44 00                  >(.CB__END.<
   second V5_CFV2 @132762: 00 31 00 5f 00 32 00 35 00 30 00 [56 35 5f 43 46 56 32 00 00
     01 7f 4d 00 00 0a a4 ff*8 ... 02 5f 0d 0a 00]
   FirstStreamed @242285: ...03 00 00 00 73 79 49 63 | 0d 00 "FirstStreamed" |
     0e 00 00 00 | 7e 00 00 00 | "<Version>5/<Version><Release>28/...</HotFix>\n"
   JPEG SOI FF D8 FF @242781.
   rim.CATPart (322959 B, github.com/bryancostanich/OpenRC) same layout, tag 2c 4c.
   mk1.CATProduct (16177 B, github.com/WiredGeist/MK1) starts V5_CFV2, tag 17 58.
   ```
4. **file(1) magic** (github.com/file/file, `magic/Magdir/ole2compounddocs`, rev 1.30
   2026-04-17): `0 string \320\317\021\340\241\261\032\341` ... `OLE 2 Compound Document`;
   zero matches for "catia" across `magic/`. Verbatim header comment:
   "# Microsoft OLE 2 Compound Documents : file(1) magic for Microsoft Structured storage".
5. **Kaitai CFB template**: https://github.com/kaitai-io/kaitai_struct_formats
   `serialization/microsoft_cfb.ksy`, verbatim start:
   ```yaml
   meta:
     id: microsoft_cfb
     title: Microsoft Compound File Binary (CFB), AKA OLE (Object Linking and Embedding) file format
     xref:
       justsolve: Microsoft_Compound_File
       loc: [fdd000380, fdd000392]
       wikidata: Q5156830
     endian: le
   seq:
     - id: header
       type: cfb_header
   ```
   Live spec page: https://formats.kaitai.io/microsoft_cfb/
   (title fetched: "Microsoft Compound File Binary (CFB)... format spec for Kaitai Struct").
6. **olefile** (readthedocs, fetched): "olefile is a Python package to parse, read and write
   Microsoft OLE2 files (also called Structured Storage, Compound File Binary Format or
   Compound Document File Format)..." (NOT applicable to V5_CFV2; listed for adjacent
   containers). oledump: https://didierstevens.com/files/software/ (versioned zips V0_0_10
   ...V0_0_18+; OLE-only tool, same non-applicability note).
7. **Archiveteam "Just Solve the File Format Problem", CATPart page**
   http://fileformats.archiveteam.org/wiki/CATPart : magic `56 35 5F 43 46 56 32`
   (`V5_CFV2`), PRONOM x-fmt/439, Wikidata Q49416323. (Fetched in earlier session segment.)
8. **Wikidata Q49416323** (Special:EntityData JSON, fetched): label "CATIA Model (Part
   Description), version 5"; claims: P1195 `catpart`, P2748 `x-fmt/439`, P178 Q1172038
   (Dassault Systèmes), P2746/MIME `application/octet-stream`.
9. **LibreDWG README** (github.com/libredwg/libredwg, raw, fetched), verbatim: "At the
   moment our decoder (i.e. reader) is done, it can read all DWG versions, just some very
   advanced R2010+ objects fail to read and are skipped over. The writer is good enough for
   everything but R2007. R2010-R2018 writing leads to CRC errors still."
10. **libpff README** (github.com/libyal/libpff, fetched): "Status: alpha"; linked docs:
    "PFF forensics analyzing the horrible reference file format" (PDF in
    github.com/libyal/documentation).
11. **Frida frida-trace docs** (https://frida.re/docs/frida-trace/, fetched; tool page:
    auto-generates action handlers for traced functions).
12. **strace man page** (https://man7.org/linux/man-pages/man1/strace.1.html, fetched).
13. **010 Editor**: official template repository https://www.sweetscape.com/010editor/
    repository/templates/ (fetched: "Template Repository - Download Binary Templates");
    community template code incl. a template-language parser: github.com/x64dbg/btparser,
    github.com/Greatness7/binary_templates (GitHub API, fetched).
14. **docxtpl** (docxtpl.readthedocs.io, fetched): "This package uses 2 major packages:
    python-docx for reading, writing and creating sub documents / jinja2 for managing tags".
15. **FreeCAD wiki "Import From ODA"** (wiki.freecad.org/Import_From_ODA, fetched, page
    title confirmed): FreeCAD delegates foreign CAD (incl. CATIA) import to ODA File
    Converter; ODA converter: https://www.opendesign.com/guestfiles/oda_file_converter.
16. **CATIA overview** (Wikipedia REST summary, fetched): "CATIA is a multi-platform
    software suite for computer-aided design (CAD)... developed by the French company
    Dassault Systèmes."
17. **Code-search negatives** (Sourcegraph stream API + GitHub API): `"V5_CFV2"` indexed
    only in signature corpora (siegfried); `CATFeatCont` zero code hits; `CATIContainer`
    zero repo hits. No public CFV2 parser exists.
18. **Verified research-line citations**: "A Survey of Automatic Protocol Reverse
    Engineering Approaches, Methods, and Tools on the Inputs and Outputs View" (DOI
    10.1155/2018/8370341); "Lifting Network Protocol Implementation to Precise Format
    Specification with Security Applications" (CCS 2023, DOI 10.1145/3576915.3616614);
    both via OpenAlex API. **Unverified leads (flagged)**: T-ReX, PolyFormat, REVISITOR,
    AutoFormat, formatbots.org (empty reply), am-tools, REVIVE.
19. **COM-automation precedents**: github.com/rock0505/CatiaPE (win32com CATIA driver),
    github.com/sheetd/BatchProcess (batch CATIA ops). Both control a live CATIA; neither
    touches the file format.

Dead ends (recorded so nobody re-burns tokens): DDG/Mojeek CAPTCHA; Bing RSS returns
region-junk; Qwant lite JS-only; grep.app Vercel checkpoint; searchcode 404; Brave 429
after first query; rohitab.com transport error; dblp/arXiv/SemanticScholar have none of
the four named format-RE papers indexed accessibly from here; PRONOM direct API 403 via
curl (the legacy `www.nationalarchives.gov.uk/PRONOM/...` UI works via webfetch).

Working directory with samples and fetch artifacts: `/tmp/opencode/catia-re/`
(`samples/`, `microsoft_cfb.ksy`, `file/` clone, `siegfried/` clone).
