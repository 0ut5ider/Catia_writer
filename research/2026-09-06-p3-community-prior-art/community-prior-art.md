# CATIA V5 .CATPart/.CATProduct format: community prior art

> **Correction, 2026-09-07.** Four findings in this report did not survive a verification pass.
> Full detail in [`upstream-verification.md`](../2026-09-07-upstream-verification/upstream-verification.md) and
> [`container-invariant-sweep.md`](../2026-09-07-container-invariant-sweep/container-invariant-sweep.md).
>
> 1. Section 5 says open-source parsers: "None." That is wrong. `cadmpeg/cadmpeg` publishes a
>    byte-level CATIA V5 decoder plus a 265 KB format spec
>    (`../../2026-09-06-shared-corpus/raw/cadmpeg/catia.md`). This swarm's own
>    `format-internals.md` found it, so the miss was internal, not external. Web search failed to
>    surface a 32-star repo; the GitHub API found it in one call.
> 2. "contains the original filename with extension somewhere after the header" holds for 2 of 10
>    native samples in this repository, not all. Eight contain no `.CATPart` or `.CATProduct`
>    string in any case, including the three PRONOM-corpus samples used to validate the signature.
>    The `CATPart` token most files carry is class vocabulary (`FromCATPart`), not a name.
> 3. "The `*` wildcard in PRONOM byte sequences is a fixed 1-byte gap per occurrence" is wrong. In
>    PRONOM syntax `*` is a variable-length gap. The practical result is the same for these files,
>    though: the signature fails on 8 of 10 real files either way.
> 4. "Sample .CATPart never downloaded, so the PRONOM magic is not byte-verified on a real file" is
>    now closed. 10 native samples were swept on 2026-09-07. `V5_CFV2\0` at offset 0 holds 10/10,
>    and `directory_offset + directory_length == file_size` holds 10/10.


Research report. Date: 2026-09-06. Agent: opencode research session (model flashnext-w4a16-fp8ple).
Question: what does the public web actually know about the internal structure of CATIA V5
.CATPart/.CATProduct files, and about tools that read or write them without CATIA installed?

All raw search output is under `../2026-09-06-shared-corpus/raw/me/` next to this file. Claims below carry source URL, date,
and speaker. Anything the community merely guesses is labelled as such.

## Headline finding

**Nobody has published the file format, and the community mostly does not try.** The strongest
formal knowledge is two bytes-wide magic signatures in the UK National Archives PRONOM registry.
The strongest practical knowledge is "strings you can see in a hex/text editor" plus "which
commercial vendor ships an independent reader." Every reverse-engineering attempt found is either
a vendor trade secret (Ansys, Spatial/Okino) or a hobby string-extractor that stops at filename
recovery. No open-source parser of the native binary structure exists as of this research date.

## 1. What official Dassault Systèmes documentation says

- DS never published the CATIA V5 binary layout. No help mirror, user guide, or scripting manual
  contains a format description.
- Official V5 help mirrors exist and were crawled:
  - `catiadoc.free.fr` (mirror, undated hosting of V5-era help). Hosts the user guides and the
    "V5 Automation" scripting documentation: `CAAScdBase/CAAInfScriptHome.htm`, use cases like
    `CAAScdInfUseCases/CAAInfOpenDocument.htm` ("Opening an Existing CATIA Document", shows
    `CATIA.Documents.Open(...)` against a .CATPart). This is the public object model, not the
    file format.
  - `catia-v5-help.anarkia333data.center` (mirror). Its Infrastructure technical-article TOC
    (`basug_C2/basugat0000.htm` and sections 05, 06, 07, 08, 13, 30) covers printers, Power Input,
    fonts, DRM, parameters, Knowledgeware. **No file-format article exists.**
  - The DRM articles (`basugat0801.htm` "About DRM", `basugat0802.htm` "Producing a Cipher File")
    are official and useful negatively: encryption is an **opt-in** option
    ("Tools > Options > General > Digital Rights Management... Secure document on 'Save As'"),
    and the encrypted output is called a **cipher file**. So the recurring claim that CATPart
    files are "encrypted" is false for default files.
- PRONOM (TNA) marks the V5 formats "Disclosure: Full" (`x-fmt/439`), yet the only content is a
  signature; there is no DS submission with internals (changelog: added V45 2010-12-06, refined
  "following information submitted by Georgia Tech Research Institute", updated V101 2022-02-15).
- Wikidata items Q105849630 (CATIA V5 model) / Q105850575 (CATProduct) hold only extension and
  MIME-type claims; no magic-number property (P4603 absent).

## 2. The actual byte-level facts that are public

The authoritative public statement is the PRONOM signature repository (github.com/nationalarchives/pronom,
signatures/fmt/*.json, signatures/x-fmt/*.json; fetched as repo tarball to `../2026-09-06-shared-corpus/raw/me/pronom-main/`):

| PUID | Format | Signature (offset 0 unless noted) |
|---|---|---|
| `x-fmt/439` | CATIA Model (Part Description) v5, ext .catpart | `56355F434656320000*2E43415450617274` = ASCII `V5_CFV2\0\0`, gap, then `.CATPart` |
| `x-fmt/440` | CATIA Product Description v5, ext .catproduct | `56355F434656320000*2E43415450726F64756374` = `V5_CFV2\0\0` ... `.CATProduct` |
| `x-fmt/438` | CATIA Material Description v5, ext .catmaterial | `V5_CFV2\0\0` ... `.CATMaterial` |
| `fmt/1615` | CATIA Drawing v5, ext .catdrawing | `56355F4346563200*434154447277436F6E74` = `V5_CFV2\0` ... `CATDrwCont` |
| `x-fmt/436` | CATIA Model v4, ext .model/.mod | offset 80: `CATIA   ` + `CATIA SOLUTIONS V4{6}RELEASE ` |
| `fmt/1714` | CATIA Model File v3 | offset 0: `CATIA   *CATIA VERSION 3{11}RELEASE ` |

Live page confirmed: `https://pronom.nationalarchives.gov.uk/x-fmt/439` (retrieved 2026-09-06;
endian flag Little-endian; source "Digital Library Research Group / MIT Libraries").

What follows from this, and what does not:

- A V5 document file begins with the tag **`V5_CFV2`** followed by two NUL bytes, and contains the
  **original filename with extension** somewhere after the header. That is the entire public
  signature. The gap is unbounded: PRONOM does not say how far in the name sits.
- The `*` wildcard in PRONOM byte sequences is a fixed 1-byte gap per occurrence, so the name is
  separated from the header by an unspecified byte run.
- The SEO site docs.fileformat.com prints the same magic (`56 35 5F 43 46 56 32`). It is
  independently right here (probably copying PRONOM or a file-type DB); its other claims stay
  untrusted. file-extensions.com ("no published file signature or documented byte-level
  structure") is wrong against PRONOM and is the model for how bad the SEO layer is.
- The header is **not** `D0CF11E0`. The "CATIA files are OLE/compound files" theory found no
  support anywhere: `"CATIA" "structured storage"`, `"CATIA" "compound document" file`,
  `"D0 CF 11 E0" catpart OR catproduct`, `"catia" "compound file binary" OR "oletools"` all
  returned no matches on DuckDuckGo (see null-query list), and the BOF `V5_CFV2` signature is
  incompatible with a CFB header.
- file(1) magic: `Magdir/cad` (449 lines fetched, `../2026-09-06-shared-corpus/raw/me/file-cad-magic.txt`) has no CATIA
  entry. Sourcegraph `repo:github.com/file/file CATIA`: 0 files.
- PRONOM has **no** signature for .cgr, 3DXML, EPL, or EBA. Grep across all 2557 signature JSONs:
  only the six CATIA formats above.

## 3. What the community has actually observed in files (hex-level folklore)

Corroborated strings visible in text/hex editors:

- Stack Overflow Q45237882, "Catia CATProduct & CATPart File Formats", 2017-07-21, score 2,
  1292 views, **zero answers** (`https://stackoverflow.com/q/45237882`). Comment thread:
  - "You can find LASTSaveVersion by simply opening your CATIA files in an text editor... you can
    find also service pack, hot fix, FirstStreamed for V6 files and many other things..."
  - "In vb.net you can use InStr(strTmp, 'MinimalVersionToRead'). Idea is to read the binary
    file, search with InStr what you want and number how many characters you have to skip to
    find the version." (VB.NET answer-style comment, score 0.)
  - 2023 commenter: "I want to write a catpart file loader for WebGL library-threejs, but I don't
    find any file format spec online."
- Stack Overflow Q44952646 (2017-07-06, 0 answers, 455 views): notepad++ dump of a .CATPart
  showing `StorageProperty`, `DASSAULT-SYSTEMES   CATIA   041803P`, `LastSaveVersion` with the
  value NUL-masked, `CATDocumentProperty`, `CATSymbolProperty`, `CATOctetArray`,
  `GenericLocate`, `DocId`.
- Reddit r/CATIA, u/username___6, 2023-10-30 (thread [17k20mo]): version-check trick "open the
  file in notepad and search for 'v5r3'. If you find 'v5r31'... it's saved in the newer version."
  Consistent with the visible version strings above.
- GitHub `sobalvarro/CATProductFiles` (2022, C#, WinForms). Form1.cs:45-77 parses a .CATProduct
  as UTF-8 text: start marker `CATOctetArray`, end marker `\u0008FINJPL`, strips `;\u0001`,
  splits component records on `\u0001\u0004File`. Recovers component filenames only. README:
  "Code that extracts the file name of the components of a CATIA Product file (.CATProduct) by
  reading the file as a text." This is the only open code found that touches the binary
  structure, and it works purely by marker search.

Community inference level: these strings prove key-value-ish serialization and NUL-delimited
ASCII/CESU-8-ish names, plus an "octet array" section holding the product's reference list.
**No source found describes the chunking, object table, or object graph.** Nobody has published
that, at any level of confidence.

## 4. Tools that read CATIA V5 without CATIA installed

Direct vendor statements, most useful data collected in this research:

- **Ansys** (official help, Release 2024 R2,
  `https://ansyshelp.ansys.com/public/////////Views/Secured/corp/v242/en/ref_cad/cadCatiaV5stnd.html`):
  "The interface works in a Reader mode. **This is a stand-alone reader which does not require
  that the CATIA V5 system be installed.**" Supports V5R8 through 6R2023 (Linux) / 6R2024
  (Windows). Its caveat list is effectively a reverse-engineering report of what the format
  exposes: units read from file; hidden parts skipped; layers, color, publication names as
  attributes; no associativity; no parameters; fails on files made in Small/Big geometry scale;
  fails on pre-R8 files even re-saved; file names restricted to ISO-646; needs full path.
  A second Ansys page (2025 R1) documents `~CAT5IN` import up to 6R2022.
- **Okino** (`https://www.okino.com/conv/imp_catia5.htm`, site © 2026): "The importer is based on
  the actual CATIA v5 runtime DLLs and components from Dassault Système... **no reverse
  engineered libraries are used, as is often the case with other CATIA v5 importers.**" The DLLs
  come via **Spatial Corp** with per-year licence renewal. This is the only vendor statement
  that independent readers exist "often" in the market, unnamed. Okino also documents V4
  extension family: `.model`, `.exp`, `.session`, `.dlv` are CATIA V4 files.
- **Commercial SDK/viewer vendors** advertising CATIA V5 reading without CATIA (marketing-tier
  evidence, format-technical-free): CAD Exchanger (SDK + Lab, `cadexchanger.com/catia/`),
  HCL **Glovius** (V4 up to 4.5, V5 up to 6R2025, V6/3DX via V5 data, + 3DXML, CGR), CADmold,
  RapidPipeline, Okino PolyTrans, zw3d / CADBro / CADMonster (web conversion), London-secrets-type
  AI-slop sites (noise only).
- **Routes that still need a live CATIA**: `pycatia` and every VBA/macro approach (COM automation,
  e.g. pycatia issue #289, 2025-12-31 answer: loop CATProducts and `SaveAs` .stp); the Chinese
  tool "转转" `YESdontASKmeAgain-Engineer/CatiaStepConverter` (2026, README: "通过本机 CATIA V5
  自动化接口" = uses local CATIA automation). Okino's DLL route is DS-sanctioned, not
  independent.
- Autodesk Inventor "How to open CATIA files" article returned 403 (bot-blocked) at fetch time;
  not verified. Gap.

## 5. Open-source parsers

None. Negative search evidence:

- GitHub API repo search "catia": only COM wrappers (pycatia), the string extractor above, an
  XML-export parser (Lukex1/CATIA-Parser-XML, 2025), conversion front-ends. No binary parser.
- Sourcegraph (anonymous index): `file:.*\.CATPart$` 0 files; `repo:github.com/file/file CATIA`
  0; `CATOctetArray` 0 (index coverage caveat noted).
- PRONOM/DROID/Siegfried ship only the magic above; no library implements a reader.
- 010 Editor template repos searched (`q3-06` pending, Sourcegraph 0 hits): nothing found yet.

## 6. Non-English sources

Deliberate multilingual sweep (DDG, spaced): Russian (habr), Japanese (qiita), Korean, Spanish,
Italian, German, French, Chinese (csdn, zhihu). Results: only SEO converter farms, CATIA-usage
blogs (CSDN pycatia how-tos), 知乎 interop-format advice (2025-04: "Catia与NX间推荐使用.step或.jt"),
and Taobao/Gumroad-style paid-service noise. **Zero file-internals content in any language.**
Null queries are logged; the Chinese "破解" (crack/parsing) searches returned nothing usable.

## 7. Academic and standards material

- OpenAlex search "CATIA file format reverse engineering": top hits are all *geometric* reverse
  engineering (scan/point-cloud to CAD), e.g. "Reverse engineering modeling methods and tools: a
  survey" (CAD&Applications 2017). None touches file parsing. Semantic scholar and DiVA thesis
  probes returned unrelated theses. Exact-phrase DDG search `"Analysis of the CATIA file format"`
  found nothing.
- No standards-body or university course material on the format exists in the searched corpora.
- The PRONOM entry's provenance names Georgia Tech Research Institute (2010) as signature
  submitter; that is as close as academia got, and they submitted bytes, not structure.

## 8. What practitioners actually do without CATIA (Reddit full-history crawl)

Crawled every r/CATIA post 2014→2026 via Arctic Shift (2724 posts, `../2026-09-06-shared-corpus/raw/me/as/posts_all.json`,
keyword hits in `../2026-09-06-shared-corpus/raw/me/reddit_catia_hits.md`; comment trees of 9 threads in
`../2026-09-06-shared-corpus/raw/me/reddit_threads.md`). PullPush was IP-blocked; Arctic Shift comment-search timed out
(server-side), so comment coverage = threads selected from post matches.

- The universal answer to "convert/open CATIA without CATIA" is **conversion or paid viewer**, not
  parsing: "If u have solidworks or inventor, you can open it and save as a step"
  (u/No-Increase-1558, 2024-06-18); CADMonster web converter (u/starchickens, 2024-08-03);
  "zw3d or cadbro" viewers (2024-05-23); free DS 3DXML Viewer + asking the upstream engineer to
  export 3DXML/STEP AP242 with GD&T (2022-06, v7x5sx).
- "If you knew the encoding for CATPart files, could you open one up and manually reorder
  [parameters]?" (2024-09-25, 1fpgjx4): zero engagement with the encoding idea; all replies are
  in-CATIA workarounds. The question no one answers.
- "Does anybody know if it is possible to generate a CATProduct file without catia, where I can
  add the file references myself?" (2024-01-22, 19ctif0): one reply, a CATIA settings recipe.
- V4: "Are there any trustworthy third-party tools that can read V4 files without converting
  them into faceted surfaces?" (2026-02-11, 1r239nc): only answer is V4→V5 import as dumb solid.
- 3DXML as the native 3DEXPERIENCE/V6 format: "the native format in the background I was told was
  3DXML" (u/Pionosis, 2023-04-20, hearsay), V6-to-3DX translator compatibility (u/fofof,
  2023-04-20).

## 9. Adjacent formats and claims to distrust

- **.cgr**: no public spec, no PRONOM signature, no RE artifacts found. Okino/Glovius support it
  via licensed/undisclosed means. Gap.
- **3DXML**: zip container with XML parts (public behaviour), DS distributes free viewers; RE
  searches (`q2-28`) found nothing beyond general complaints. V6 cipher-3DXML exists (official
  help basugat0804).
- **EPL/EBA**: no evidence found anywhere in this corpus beyond the extension existing. Report
  honestly as an open gap; do not cite old folklore about them.
- **"CATIA V5 files are encrypted"**: false for default files; opt-in DRM only (section 1).
- **"Files are OLE compound documents"**: unsupported, contradicted (section 2).
- V4 is the only documented end of the family (PRONOM magics; Okino extension list; eng-tips
  2006 thread 166313 confirms drawing/part separation and .ig2 convention in V5 too).

## Queries that returned nothing (negative results, worth not repeating)

All run through spaced DuckDuckGo html (logs: `../2026-09-06-shared-corpus/raw/me/ddg-loop.log`, `ddg-loop2.log`,
`ddg-loop3.log`):

- `"CATIA" "structured storage"` → no match
- `"catpart" parser OR reader github` → no match
- `"CATIA" "compound document" file` → no match
- `"Document Services" "CAA V5" pdf` → no match
- `"D0 CF 11 E0" catpart OR catproduct` → no match
- `"catia" "compound file binary" OR "oletools"` → no match
- `"Analysis of the CATIA file format"` → no match
- `"CAA V5" "Document Services" use cases` → no match
- `"catpart" "step converter" dll runtime` → SEO only (3 hits, no content)
- `"catia" "technical modeler" redbook` → no match
- `"V5_CFV2" OR "V5_CDV2" catpart` → no match (string lives in PRONOM pages; bare `V5_CFV2`
  pending in queue 3)
- `"SM6" CATIA`, `"coreref" CATIA` → only Schneider Electric switchgear (the "SM6" theory is
  dead)
- site:qiita.com, site:habr.com, site:csdn.net, site:zhihu.com internals queries → nothing
  relevant
- taobao/gumroad paid parser probes → nothing relevant

## Collection failures (gaps in this research, stated plainly)

- Search engines degraded mid-session: DuckDuckGo began serving image CAPTACHAs (html and lite
  endpoints, code 9c39) from ~2026-09-06 18:40 UTC; Bing returned decoy results (sports news);
  Google returned JS shells; Mojeek/Startpage/Ecosia/Yandex/Baidu blocked; searx instances 429;
  Marginalia bot-wall. Queue 3 (filetype:catpart samples, V5_CFV2 web hits, 010 templates, CGR)
  is held until the captcha window passes.
- Sample .CATPart never downloaded, so the PRONOM magic is not byte-verified on a real file.
  3dicons.at and grabcad-style free samples unreachable from this network. A hex check of any
  real file is the top follow-up.
- archiveteam.org CATIA page unreachable (curl 000, webfetch transport error, no Wayback
  snapshot). PullPush Reddit mirror rate-limited this IP throughout. Eng-tips V4 thread
  (125382) blocked by Cloudflare, Save-Page-Now refused it twice (520). Autodesk CATIA-import
  article 403. GitHub code search needs auth; anonymous Sourcegraph misses small repos.
- r/CATIA comment trees cover only threads whose posts matched keywords; comment-level
  full-text search over the subreddit was not achievable (Arctic Shift timeouts).

## Prior art ranked (useful or not)

1. PRONOM signatures (authoritative, thin): header tag + embedded filename + V4 magics.
2. Ansys CATIA V5 Reader caveat list (vendor reverse engineering, behaviour-level, no bytes).
3. Hex-editor folklore: `V5_CFV2` tag, `LastSaveVersion`, `MinimalVersionToRead`,
   `CATOctetArray`/`FINJPL`/`\u0001\u0004File` reference list markers, visible v5rNN version
   string, DASSAULT-SYSTEMES tag, FirstStreamed (V6 streamed docs).
4. sobalvarro/CATProductFiles: the only working open code path (string markers, filenames only).
5. Okino/Spatial statement: DS runtime DLLs are licensable; other importers reverse-engineer.
6. Everything else: marketing pages claiming CATIA support (CAD Exchanger, Glovius, CADmold,
   RapidPipeline) with no format disclosure, and SEO junk worth citing only as evidence of the
   information vacuum.
