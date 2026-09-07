# Generating valid .CATPart / .CATProduct files without reversing the CATIA V5 binary format

- Date: 2026-09-06
- Role: web research agent (research only, no project code; curl/jq/API queries used as tooling)
- Question: what practical routes exist to produce files CATIA V5 accepts as valid .CATPart/.CATProduct, without full reverse engineering of the V5 binary format? Verdict on 7 candidate routes.
- Model: anthropic claude (via opencode)

## Executive summary

| # | Route | Verdict |
|---|-------|---------|
| 1 | License + automation (pycatia / CATScript / CNEXT batch) | **Best route if any CATIA seat exists.** Proven, documented, produces true parametric native files. |
| 2 | Generate STEP elsewhere, convert to CATPart | **Strong.** Dassault ships an official command-line batch converter: `CATDMUUtility -f x.stp -part out.CATPart` (also `-product`, `-cgr`). Needs a licensed V5 install; geometry only, no parametric history. |
| 3 | Template mutation (byte-patch a sample CATPart) | **Partially possible, undocumented.** Empirically, part numbers, instance names, and container names are plaintext in the file, so renaming is plausible; but no public serialization spec, internal refs opaque, silent-corruption risk. Not recommended as a primary route. |
| 4 | 3DXML as an intermediate | **One-way only.** 3DXML cannot round-trip back to an editable CATPart. Also: the premise "3DXML is ISO 10303-237" is false (see Corrections). |
| 5 | CGR | **Not a part.** CGR is tessellated triangles (STL-like); CATIA reads it as lightweight reference, never as editable part. Official CLI (`CATDMUUtility -cgr`) and a commercial writer (Datakit) exist. |
| 6 | Hex-level format analysis | **Viable reconnaissance only.** Zero public format documentation or RE threads exist anywhere found. First-hand analysis here establishes the real container: magic `V5_CFV2`, not OLE/CFB. No usable serialization spec after this. |
| 7 | 3DEXPERIENCE / xDesign | **Dead end for file generation.** xDesign components are database objects ("physical products"), not local files; no public file spec. 3DX can export native V5 files, but that is just another licensed converter. |

**Killing fact found during research:** commercial multi-CAD SDKs (Datakit, CCE Intl ODX; CAD Exchanger for 3DXML) officially *write* `.CATPart`/`.CATProduct`. Datakit's published matrix: CATIA V5 Writer supports R14, R19-R21, V5-6R2012..R2026, BREP input, with documented limitations (no periodic surfaces/curves). This removes the need for RE entirely if a per-seat/royalty SDK license is acceptable and no CATIA seat is required.

- Datakit CATIA V5 Writer: <https://www.datakit.com/Doc_API_html/catiav5w.html>
- Datakit CGR Writer: <https://www.datakit.com/Doc_API_html/cgrw.html> (R14, R19)
- Datakit 3DXML Writer: <https://www.datakit.com/Doc_API_html/_3dxml.html>
- Datakit CATProduct writer how-to: <https://www.datakit.com/Doc_API_html/v5w_asm_how_to.html>
- CCE Intl "Open Data Exchange" (claims read+write Catia V4/V5/V6 native): <https://cceintl.com/development-tools/open-data-exchange-sdk/>
- CAD Exchanger (3DXML read/write, no native V5 write): <https://cadexchanger.com/convert-3dxml/>

## First-hand container analysis (new, primary data)

No public spec exists for the CATPart binary, so real files were downloaded and inspected directly.

Samples: <https://github.com/chanduj8351/CATIA-V5> (repo contains real .CATPart/.CATProduct files). Local copies: `raw/sample2.CATPart` (76,575 B), `raw/sample_assembly.CATProduct` (90,859 B).

1. **Magic bytes: `56 35 5F 43 46 56 32 00` = ASCII `V5_CFV2\0`.** Both part and product share this header. `CATIA` does not use OLE2/Compound File Binary: `olefile.isOleFile()` returns False (olefile 0.47). The internet folk-belief that CATPart is structured storage is wrong, and so are any plans built on olefile/MS-CFB tooling (e.g. oledump.py workflows).
2. Header is followed by a container table. Readable names in the sample part: `CATCompoundCont`, `CATContainer`, `CATProdCont`, `CATFeatCont`, `CATPrtCont`, `CGMGeom` (the CGM exact geometry model), `CATMFBRP`, `CATSeeBodyCont`, `CATBRepModeContainer`, `CATStdCont`, `CATCGRCont`, `CameraStartupContainer`, `AppliCont`, `V5USERID`, plus a build stamp `NOTHING-CNEXTINFOS-...V5R20SP0HF0 built` (writer release visible in-file).
3. Feature/object names are plaintext strings: `Part1`, `Sketch`, `PRTSketch`, `MechanicalPart`, `_PartNumber`, `_PartProperties`, `2DAxis_*`.
4. CATProduct stores its tree as readable records: `_PartNumber`, `_RefProduct`, `_InstanceName`, `Part2.1`, `_Position`, and link chains like `CtorToProd:Product!ProdToRep:Shape 1!RepToShape:Shape!Geometry:CKAEAAAAENFKDBDAE` (instance -> representation -> geometry with opaque per-object IDs).
5. Implication: the *envelope* is legible (container names, IDs, names, version). The *payloads* (serialized CAA objects, CGM geometry) are not specified anywhere public. Renaming part numbers/instances via careful byte-patching is plausible (fixed offsets, plausible length-prefix records) but unverifiable without a reference CATIA to test acceptance, and one bad offset silently corrupts the file. Route 3 stands or falls on having a CATIA to validate patched output.

Corroborating absence of public format knowledge:
- Stack Overflow <https://stackoverflow.com/questions/45237882/> "Catia CATProduct & CATPart File Formats": **zero answers**, only "no public docs" - stored in `raw/so-q-batch1.txt`.
- Stack Overflow <https://stackoverflow.com/questions/68160726/> "How does catia store file?" - open question, same void.
- reverseengineering.stackexchange.com: **0 results** for catpart/catia/3dxml/xdesign via API and site search (verified two ways, `raw/se-search.txt`).

## Corrections to the research premise (important)

1. **"3DXML is ISO 10303-237" is false.**
   - ISO 10303-237 is *AP 237 Fluid dynamics*, cancelled, its scope folded into AP 209 (Wikipedia ISO 10303 + List of STEP parts; official ISO part list <https://standards.iso.org/iso/10303/tech/step_titles.htm> fetched to `raw/step_titles.htm`, where no Part 237 remains and implementation methods are Parts 21/22/28 etc.).
   - STEP AP242 = ISO 10303-242 "Managed model based 3D engineering". Nothing there is 3DXML.
2. **3DXML is not an ISO standard at all.** ISO 19457 (the number suspected) is *Rolling bearings - Roller blocks* (ISO catalogue / distributors, see `raw/searches/iso-19457b.md`). 3DXML is a proprietary Dassault specification, published in 2005 with a royalty-free license limited to internal use, XSDs available; "Open format? No" (Wikipedia <https://en.wikipedia.org/wiki/3DXML>; 3DS press release <https://www.3ds.com/newsroom/press-releases/dassault-systemes-delivers-3d-xml-specifications-and-player>; 3D XML User Guide mirrors e.g. scribd 447080927).
3. **CATPart is not an OLE compound document** (empirical, above).

## Route-by-route detail

### Route 1 - License + scripting automation: RECOMMENDED when a V5 seat exists

- pycatia (<https://github.com/evereux/pycatia>, MIT, 365 stars; README in `raw/pycatia-readme.md`): Python COM wrapper; requires CATIA V5 running on Windows; self-described alpha. Examples: <https://pycatia.readthedocs.io/en/latest/examples.html> and `examples/example__hybrid_sketch__shape_factory__001.py` (creates sketch, constraints, Pad, saves .CATPart).
- True headless execution is documented: `CNEXT.exe -direnv <env> -env <env-id> -batch -macro script.CATScript`, batch mode has no UI and is materially faster than interactive: <https://v5vb.wordpress.com/2010-09-26/exec-scripts-in-batch-mode/> (fetched `raw/pages/v5vb-batch.md`); official docs `-batch` flag: <http://catiadoc.free.fr/online/basug_C2/basugbt0101.htm>; Batch Monitor: <http://catiadoc.free.fr/online/basug_C2/basugbt2301.htm>.
- License is the constraint: CATIA seats are expensive (DS buying guide <https://www.3ds.com/store/what-price-catia-comprehensive-buyer-guide>, cited from search `raw/searches/caa-license.md`); CAA RADE dev licensing exists but is also per-user (<https://www.maruf.ca/files/caadoc/CAAPdiTechArticles/CAAPdiVbtLicensing.htm>). Batch still consumes a license; there is no free headless writer.
- Output quality: real parametric parts (sketch + pad + parameters), identical to interactive work. This is the only route that yields *editable, feature-based* CATParts without a converter.

### Route 2 - Build STEP elsewhere, convert with Dassault's own batch converter

- Official documentation found: "Translating Files from the Command Line": **CATDMUUtility is a batch process enabling generation of .CATProduct, .cgr and .CATPart formats from STEP files**, via `CATStart.exe -env ... -run "CATDMUUtility.exe -f inputfile -part output.CATPart"` (also `-product` for STEP assemblies, `-cgr` for lightweight). <http://catiadoc.free.fr/online/dtlug_C2/dtlugbt0500.htm> (fetched `raw/pages/catiadoc-step-batch.md`). Same utility converts IGES (`-part`, `-cgr`): <http://catiadoc.free.fr/online/dglug_C2/dglugbt0500.htm> and Pro/E: <http://catiadoc.free.fr/online/dplug_C2/dplugbt0500.htm>.
- Generation side is free and solved: OpenCascade OCCT, stepcode, or even hand-written AP203/AP214 files produce valid STEP.
- Caveats (documented, not theoretical): import quality settings control healing (`http://catiadoc.free.fr/online/itfug_C2/itfugbt0101.htm`, troubleshooting page `itfugat0101.htm`); real failures exist: <https://stackoverflow.com/questions/75892587/> (AP203 geometry not read into CATIA), <https://www.eng-tips.com/threads/problem-when-importing-step-file-into-catia-assembly-combined-into-one-part-amp-partbody.512974/> (assembly collapses into one part); attribute mapping onto Physical Products in 3DX needs extra work (<https://3dswym.3dexperience.3ds.com/question/catia-user-community/how-to-mapp-attributes-during-step-import-in-3dx-native-catia-v6_2UuhFXNqScW4XL9WIAdukA>).
- Result: "dumb solid" CATPart - exact BREP, no feature tree, no parameters. Acceptable for downstream machining/inspection; not for design.

### Route 3 - Template mutation

- See "First-hand container analysis". Plaintext `_PartNumber` / `_InstanceName` strings mean a "clone a known-good file, rename it" workflow is technically within reach for CATProducts (the product tree is almost self-describing). CATPart payloads (CGM geometry, feature records) are not safely patchable blind.
- No tool, library, or writeup describing this was found on GitHub, Stack Exchange, Reddit, or the open web (searches `raw/searches/catpart-*.md`). Nobody has published success with it.
- Verdict: viable as a hack for product-level metadata **only if** output is validated against real CATIA; do not build a pipeline on it.

### Route 4 - 3DXML

- Container: ZIP with BOM XML + XML/binary representation files (Gregory patches, meshes); spec + XSD public since 2005 under a royalty-free internal-use license; viewers open source (GLC-Player). Wikipedia: <https://en.wikipedia.org/wiki/3DXML>.
- Writing 3DXML from scratch is legitimately feasible (XML + published schema; Datakit sells a writer). Reading *back into* CATIA as an editable part is the wall: "You cannot convert a published 3DXML back into an editable CATIA part - the parametric features and history live only in the source CAD file" (<https://www.file-extension.info/conversion/3dxml-to-catpart>, <https://file-extensions.com/docs/3dxml>; 3DS community thread <https://3dswym.3dexperience.3ds.com/question/catia-user-community/converting-file-from-3dxml-to-catpart_W2h78NQKTJye7iZ0OPzzug>, `raw/pages/swym-3dxml.md`).
- Verdict: 3DXML is an excellent *egress* format and a poor *ingress* path to .CATPart. Useless for this project's goal.

### Route 5 - CGR

- What it is: "CGR is a tessellated file format similar to STL... flat triangles, rather than exact surfaces and edges as would be in the CATPart file" - Rand 3D teardown <https://resources.rand3d.com/insights-from-within/extracting-geometry-from-cgr-files> (`raw/pages/rand3d-cgr.md`). CATIA treats .cgr as a lightweight reference (visualization), never an editable part; product views can be bound to cgr ("CGR view: only external appearance is used"): <http://catiadoc.free.fr/online/cfyugdr_C2/cfyugdr1012.htm>, cgr policy settings <http://catiadoc.free.fr/online/bascupst_C2/bascupst0800.htm>.
- Generation is easy and official (`CATDMUUtility -cgr`, Route 2 docs) or commercial (Datakit CGR Writer).
- Verdict: solves "display this product in CATIA", not "create a part". Also widely used *because* it is deliberately non-editable (OEM IP protection) - expect it to stay closed.

### Route 6 - Hex-level analysis of the V5 format

- Public corpus: empty (see Corroborating absence above). Bing/DDG sweeps found no blog post, gist, or paper serializing the CATPart container (searches saved under `raw/searches/`).
- First-hand baseline established here (magic `V5_CFV2`, container table, CGMGeom payload naming, plaintext name records). This is a real starting point where none was published, and the raw samples are kept for further work (`raw/sample2.CATPart`, `raw/sample_assembly.CATProduct`).
- The honest assessment: the container is 10% of the problem; the serialized CAA object model (features, parameters, constraints, CGM geometry) is the other 90%, is versioned (R14 -> R2026 differences visible in Datakit's version matrix), and DS has no incentive to document it. Effort beats value here because Routes 1/2/SDK already work.

### Route 7 - 3DEXPERIENCE / xDesign

- Official FAQ: "Components created in 3DEXPERIENCE apps like xDesign are saved as physical products in collaborative spaces" - there is no local xdesign document format to emit; exchange happens through import/export (3DXML, STEP, sldprt/sldxml, IGES): <https://dshelp-embed.3ds.com/2020x/english/xd_dashboard/SOLIDWORKS_XD_Tips.html> (`raw/pages/xdesign-faq.md`). 3DDrive stores files "in native formats", 3DSpace stores DB objects.
- No public spec for the platform wire/storage formats; RE search surface is even emptier than for V5.
- 3DX can *export native CATIA V5 files* (<https://community.3dcs.com/help_manual/saveas.htm>), i.e. another licensed converter exit, same category as Route 2.
- Verdict: no file-generation angle without buying into the platform; if on-platform, use its export instead of file RE.

## Recommended decision path

1. Have (or can borrow) a Windows + CATIA seat? -> **Route 1** (pycatia or CATScript under `CNEXT -batch`). Highest fidelity: parametric parts.
2. Seat available only for conversion, or pipeline should be geometry-only? -> **Route 2**: generate STEP with OCCT/stepcode, run `CATStart -run "CATDMUUtility -f x.stp -part out.CATPart"`. Officially supported.
3. No Dassault product allowed in the pipeline at all? -> **Commercial SDK write** (Datakit CATIA V5 Writer; verify version coverage and the periodic-surface limitation against your geometry; CAD Exchanger/CCE Intl as alternates). This is the only route that emits .CATPart on a machine with no CATIA.
4. Everything else (3, 4, 5, 6, 7) is dead or decorative for this goal.

## Method notes, limits, and blocked sources

- Search-engine outage on this network: Bing poisoned via every egress incl. r.jina.ai; DDG direct = CAPTCHA, Google/Ecosia/Qwant/Baidu blocked; SearXNG instances = Anubis. Working stack: Stack Exchange API 2.3, GitHub API, Wikipedia/Wikidata API, PullPush + Arctic Shift (Reddit), direct page fetches, and `r.jina.ai` proxy (which also unblocks DDG-lite and iso.org pages). All tooling: `raw/jsearch.sh`, `raw/parse_search.py`.
- Reddit evidence (round-trip pain, licensing gripes, STEP->CATPart workflows) in `raw/reddit-arctic.jsonl` (33 rows) and `raw/reddit-pullpush.jsonl` (90 rows).
- forum.freecad.org is Anubis-gated both directly and through the proxy (`raw/pages/freecad-3dxml.md`); its 3DXML threads were cited only via search snippets.
- Scribd copies of the 3D XML User Guide were located but not scraped (login-walled).
- Sample files come from a random public student repo; structure conclusions were verified on two files (one part, one product). A second corpus would firm up offsets, but the magic-bytes and not-OLE findings generalize (header + olefile check).

## Raw data manifest (same directory, `raw/`)

- `searches/*.md` - 20 DDG-lite result pages (verbatim); `search-urls.txt` - parsed URL/title/snippet index.
- `pages/*.md` - fetched evidence pages: `v5vb-batch.md`, `catiadoc-batchmonitor.md`, `catiadoc-step-import.md`, `catiadoc-step-batch.md` (the CATDMUUtility STEP->CATPart doc), `catiadoc-cmdline-translate.md` (IGES), `catiadoc-catdmu.md`, `datakit-catiav5w.md`, `datakit-cgrw.md`, `datakit-3dxmlw.md`, `datakit-v5writer.md`, `rand3d-cgr.md`, `xdesign-faq.md`, `swym-3dxml.md`, `freecad-3dxml.md` (Anubis page proving the block).
- `sample2.CATPart`, `sample_assembly.CATProduct` - real CATIA files inspected; headers/strings analysis in this report.
- `pycatia-readme.md`, `so-q-batch1.txt`, `so-batch1.json`, `se-search.txt`, `gh-search2.txt`, `reddit-arctic.jsonl`, `reddit-pullpush.jsonl`, `wiki-catia.txt`, `wiki-3dxml-fr.txt`, `wiki-iso10303.txt`, `wiki-stepparts.txt`, `step_titles.htm`, `iso-77133.txt`.
- `jsearch.sh`, `parse_search.py`, `pp.sh` - the research tooling used.
