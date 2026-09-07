# CATIA & adjacent CAD native-format RE: community knowledge map and transferable playbook

- Date: 2026-09-06
- Role: web-research agent (Cerebo/session-2 continuation)
- Question: Where does community reverse-engineering knowledge about CATIA and adjacent CAD native formats live, and which methodologies have demonstrably succeeded for other proprietary CAD formats?
- Model: flashnext/flashnext-w4a16-fp8ple
- Raw data: `raw/` alongside this file (search-en-catia.md, search-caxids-std.md, search-cn-ru.md, search-transferable.md, search-people-method.md, crossref.md, github-readmes.md, openswx-readme.md, search-late-batch.md)

## Executive summary

1. There is no open community reverse-engineering CATIA. reverseengineering.stackexchange.com has zero CATIA threads; no open-source CATPart parser exists; the only genuine forum thread found (cccp3d.ru, Russian) is bot-walled with no Wayback copy. CATIA knowledge lives in (a) byte-identification records (PRONOM/archiveteam), (b) mirrored official documentation (maruf.ca, catiadoc.free.fr) which documents the CGM object model, not the byte layout, and (c) commercial readers (Datakit, Okino, CAD Exchanger, Tech Soft 3D).
2. The transferable playbook is rich and current: SolidWorks SLDPRT (2011 personal RE -> 2025-2026 active multi-repo effort), Parasolid (vendor-published XT spec), Rhino 3dm (OpenNURBS), DWG (OpenDWG/ODA), КОМПАС-3D (2026 Habr writeup, 466k-file corpus), and the ImHex community's format-RE workflow.
3. Two premises in the tasking did not survive verification and should be treated as false memory: "CAX-IDS / ODSC Open Data Standard for CAD" (not findable under those names anywhere; the closest real things are the Chinese DISA group standards, STEP AP242/CAX-IF, and the Open Design Alliance) and "OCCT documents the CATIA V4 IRB format" (no IRB module in any inspectable OCCT version; CATIA import is the commercial Datakit plugin).

## Area 1: CATIA itself

| Source | Date | What it proves |
|---|---|---|
| https://reverseengineering.stackexchange.com/search?q=CATIA (+ SE API 2.3, same query) | checked 2026-09-06 | Zero results. The main RE forum has no CATIA content; the community simply is not there. |
| https://fileformats.archiveteam.org/wiki/CATPart (via Wayback 2024-12-18; page rev 2020-04-11) | 2020/2024 | CATPart magic = ASCII `V5_CFV2` (hex 56 35 5F 43 46 56 32), PRONOM x-fmt/439, Wikidata Q49416323. The only public byte-level anchor for CATPart; the container name is "CFV2". |
| https://fileformats.archiveteam.org/wiki/CATIA_V4_Model (via Wayback 2024-12-18) | 2020/2024 | CATIA V4 Model = `.mod`/`.model`, PRONOM x-fmt/436, Wikidata Q49414097, with sample-file links (grabcad Q&A) and Okino importer references. |
| https://www.nationalarchives.gov.uk/PRONOM/x-fmt/436 and .../439 | ongoing | Machine-readable binary signature records for CATIA V4/V5; the starting point for any detector. |
| https://www.maruf.ca/files/caadoc/CAAGobTechArticles/GeoObjects.htm (+ Curves.htm, Surfaces.htm, CAATobTechArticles/TopoModel.htm) | mirror, undated | Unofficial mirror of official "CATIA Geometric Modeler" CAA technical articles: the CGM object model (objects, curves, surfaces, topology) is documented for free. The *semantics* target is mapped; only serialization is missing. |
| http://catiadoc.free.fr/online/cfyugrvs_C2/cfyugrvsexport.htm | mirror, undated | Full mirrored CATIA user/export documentation; mirrors of vendor help are how CATIA knowledge survives publicly. |
| https://cccp3d.ru/forum/topic/74514 ("Формат - CATIA") | thread, undated | The only real "RE the CATIA format" forum thread found in any language; JS bot-check ("Проверка") blocks all non-browser fetches and no Wayback snapshot exists. Needs a real browser to mine. |
| https://tony-bro.com (CGM blog series, zh) | 2010s | Chinese hobbyist writing about CGM geometry concepts; thin, conceptual, no byte layout. |
| https://docs.fileformat.com/cad/catpart/ | SEO era | Example of the shallow SEO "format description" genre around CATPart: no technical depth; do not expect content there. |
| https://cadinterop.com/en/formats/cad-systems/catia-v4.html and catia-v5.html | fetched 2026 | Vincent Simon (CAD Exchanger) per-system format notes: V5 = CGM kernel; documents which vendors can read what, version traps. Commercial but the best public map of the V4/V5/CATProduct/CGN landscape. |
| https://docs.techsoft3d.com/exchange/2025.1.0/start/format/catia_v4_reader.html ; https://ansyshelp.ansys.com/.../ref_cad/cadCatiaV4.html ; https://www.okino.com/conv/imp_catia4.htm ; https://cadexchanger.com/catia-to-brep/ | 2024-2025 | Commercial readers for CATIA V4 exist and are productized; their docs describe observable behaviors (entity types, limitations) usable as a semantic oracle. Nobody publishes byte-format knowledge. |
| github.com/deltabomb? no: pycatia (https://github.com/etaii? use: https://github.com/mkrusaka? actual: pycatia on PyPI) | 2026 | All "python + catia" code found is CAA/COM automation wrapping (pycatia): it reads models *through a licensed CATIA instance*, not bytes. No parser exists. |

(pycatia canonical repo: https://pypi.org/project/pycatia/ - automation wrapper, proof that the community path to CATIA data is "drive the real CAD", not parse the file.)

## Area 2: "CAX-IDS / ODSC" - negative result, and the real standards landscape

- Negative: "CAX-IDS" and "ODSC Open Data Standard for CAD" return nothing on Google/Bing/Brave/DDG (EN + CN + RU), Crossref, or Semantic Scholar. Treat the name as misremembered.
- https://www.disa.org.cn/Content-371.html and http://www.gddac.org.cn/nd.jsp?id=45 (2023-07-15) | 2023 | China's DISA (数字化工业软件联盟) drafted a group standard 《三维CAD数据模型和格式》 (3D CAD data model and format) with a 30-day public comment round; this is the closest real "open CAD data format standard" movement outside STEP.
- http://www.gddac.org.cn/pd.jsp?id=8 | 2023 | Published related standard T/DISA 1011 《三维CAD模型轻量化格式》 (lightweight CAD format). Proves China is standardizing exchange formats, likely for CATIA-free toolchains.
- https://www.ap242.org/ ; https://www.mbx-if.org/home/cax ; https://benchmark.ap242.org/ | ongoing | STEP AP242 is the actual open exchange standard; CAX-IF/MBx maintains it and benchmark.ap242.org publishes public compliance test reports per CAD system. Methodology value: a public test-corpus + compliance-report oracle.
- https://www.dhs.gov/sites/default/files/2024-10/24_1015_cad-to-cad_factsheet.pdf ; NIST STEP model libraries on mbx-if | 2024 | Government CAD-to-CAD interoperability testing reports: public, per-format, pass/fail matrices.
- https://doi.org/10.1016/j.compind.2007.12.002 ("Standardized data exchange of CAD models with design intent", Computer in Industry) and https://hal.science/hal-02981783 (review of CAD visualization standards in PLM) | 2008/2020 | Academic surveys of the exchange-standard space; useful bibliography, no byte RE.

## Area 3: Transferable success stories (the core evidence)

### SolidWorks SLDPRT (best analog to CATIA)
| Source | Date | What it proves |
|---|---|---|
| https://heybryan.org/solidworks_file_format.html | ~2011 | Earliest public SLDPRT RE: container = OLE2 structured storage; explored with libgsf `gsf cat/list`; geometry in `Contents/DisplayLists__ZLB`; methodology = graduated corpus (empty part -> single primitive -> extrude -> feature). |
| https://github.com/schwitters/openswx | 2025-09..2026-08 active | Production-grade outcome 14 years later: pure C++20 reads SLDPRT/SLDASM/SLDDRW with no SolidWorks. Two containers: <=2014 OLE2 (`D0 CF 11 E0 A1 B1 1A E1`), 2015+ proprietary chunk format located by byte-scanning for marker `14 00 06 00 08 00`. Extracts configurations, mass properties, previews. |
| https://github.com/blussyya/sldprt-format-research (+ sldprt-research-dump) | 2026 | The methodology artifact to copy: `knowledge/KNOWN_INVARIANTS.md` (INV-001 modern geometry lives in Contents/DisplayLists; INV-002 face-block layout with float32[vertexCount*3] positions/normals; 593/595 faces across 4 models validate the layout), `EXPERIMENT_LOG.md`, `FAILED_HYPOTHESES.md`; stated rule "syntax before semantics, never guessing meanings"; LLM-assisted loop ("kinda vibecoded"). |
| https://github.com/BlinkingSun/sldprt2step | pushed 2026-09-02 | Pure-Python SLDPRT -> STEP AP214: proves the round-trip milestone is reachable without vendor code. |

### Parasolid (the vendor-published-spec case)
| Source | Date | What it proves |
|---|---|---|
| http://www.q-solid.com/Parasolid_Docs/xt_index.html and .../Parasolid_Docs_V35/pdf/xt.pdf | V11.0 manual, V35 mirror | Siemens publishes the full Parasolid "transmit" (XT) byte format manual for translators. A published spec creates an ecosystem of independent parsers (CATIA's absence is the counterfactual). |
| http://13thmonkey.org/~boris/...Parasolid XT Format Reference PDF (2006 copy) | 2006 | Long-standing unofficial mirror; format docs circulate privately for 20+ years. |
| github.com/khoanguyen-3fc/ps-parser ; github.com/monozukuri-ai/parasolid-kit ; github.com/deGravity/verisolid , /parasolid_frustrum | 2025-2026 | Active independent XT parsers/checkers/fingerprinters; a second healthy parser community next door (NX is Parasolid-based, like Teamcenter data). |

### Rhino 3dm, DWG, КОМПАС-3D, Onshape
| Source | Date | What it proves |
|---|---|---|
| https://github.com/mcneel/opennurbs + https://developer.rhino3d.com/guides/opennurbs/what-is-opennurbs/ | ongoing | Rhino's format documented and shipped as open C++ source by the vendor; community viewers exist (github.com/eryar/3DMViewer). Vendor-aliance model #1. |
| https://en.wikipedia.org/wiki/.dwg ; https://aecmag.com/opinion/the-dwg-conundrum/ ; Open Design Alliance (opendesign.com) | ongoing | The canonical RE-then-standardize arc: DWG was reverse-engineered by third parties, then OpenDWG/ODA took over spec maintenance; Autodesk tolerates an ecosystem. |
| https://habr.com/ru/articles/1068414/ (fafnir999) | 2026-08-10 | Best end-to-end documented version-identification methodology for a closed CAD format: two containers (v16+ ZIP with UTF-16 FileInfo ini; older binary with `KF` magic + big-endian 4-byte format code at offset +2); 466,000-file corpus scraped from c-stud.ru / alldrawings.ru; cluster magics against release chronology; 95% version ID; libmagic Magdir seeds; explicitly human+LLM workflow. |
| https://github.com/fafnir999/cadver | 2026 | Tool output of that work: 51 КОМПАС KF format codes, command-line version detector. |
| https://en.wikipedia.org/wiki/Onshape | 2026 | Architecture contrast: Onshape is a versioned feature-stream database, no "native file" to RE; shows what CATIA-style opaque single-file blobs are the exception to. |

## Area 4: Academic work

| Source | Date | What it proves |
|---|---|---|
| DOI 10.1016/j.cagd.2024.102339, "Interactive reverse engineering of CAD models", Computer-Aided Geometric Design | 2024-06 | Semantics-level RE is an active peer-reviewed field (recovering construction history from geometry), i.e. the layer above byte RE. |
| https://arxiv.org/abs/2603.13098 "SldprtNet", ICRA 2026 | 2026-03-13 | 242k+ industrial parts shipped as .step AND .sldprt with a lossless encoder/decoder over 13 CAD commands: a working large-scale SLDPRT parsing toolchain exists in academia. |
| https://spatial.engr.wisc.edu/.../2003-2.pdf (B-rep SE) ; https://arxiv.org/abs/2608.04955 | 2003 / 2026 | B-rep representation-learning lineage: how to consume decoded B-reps once you have them. |
| Negative | 2026-09 | No Crossref/Semantic Scholar hits for "CAX-IDS"; Semantic Scholar API 429-limited unauthenticated, so scholar sweep was Crossref-primary. |

## Area 5: Tools and methodology sources

| Source | Date | What it proves |
|---|---|---|
| https://werwolv.net/posts/file_format_reverse_engineering/ (HN https://news.ycombinator.com/item?id=49508608, 256 pts) | 2026-08-31 | The closest thing to a published playbook for unknown binary formats (by ImHex's author): entropy/structure triage -> ImHex + Pattern Language structs -> differential analysis -> incremental decoder; community expectations mirror what blussyya does manually. |
| https://github.com/WerWolv/ImHex-Patterns | ongoing | Community-written binary format definitions repo: the pattern for publishing format knowledge as executable structs. |
| https://zoo.dev/learn/a-practical-overview-of-cad-file-formats (zoo.dev blog) | 2025-05 | Current taxonomy of CAD containers (OLE vs zip vs chunked streams); orientation layer before byte work. |
| https://github.com/file/file/blob/master/magic/Magdir/cad | ongoing | libmagic's CAD signature file: the seed labels for any corpus (fafnir999 built on exactly this). |
| libgsf (`gsf cat/list`), python `olefile` | ongoing | The OLE2 exploration toolkit from the heybryan thread; applies to any pre-2015 SolidWorks or similar OLE containers (including legacy CATIA? no evidence - CFV2 is not OLE). |
| Negative | 2026-09 | 010 Editor template library: no CAD format templates surfaced in any query; that community is elsewhere (ImHex patterns + GitHub). |

## Area 6: People / accounts to follow

- blussyya (GitHub) - SLDPRT invariant knowledge base; posts method docs, not just code.
- schwitters (GitHub) - openswx author; deepest public knowledge of SW's post-2015 chunk container.
- BlinkingSun (GitHub) - sldprt2step; geometry extraction path.
- khoanguyen-3fc, monozukuri-ai, deGravity (GitHub orgs/repos) - active Parasolid XT parsing community.
- fafnir999 (GitHub + Habr, ru) - corpus-based magic/version identification; writes up full method.
- WerWolv (GitHub, werwolv.net) - ImHex; format-RE workflow and pattern tooling.
- Vincent Simon / CAD Exchanger blog (cadinterop.com) - per-CAD-system format notes; closest thing to a maintained "format landscape" doc.
- PDES Inc (pdes.com) and CAX-IF (ap242.org) - AP242 standards commentary and public compliance tests.
- maruf.ca maintainer - keeps official CAA/CATIA tech articles searchable; catiadoc.free.fr likewise.
- Negative: Sam Partington "blockfmt" could not be verified (no GitHub repos under sampart, HackerNoon @sampart empty, queries for blockfmt/miscto/blockdump all empty). "pr0fbook" not found either. Both names likely garbled; do not cite.

## Negative results and dead routes (recorded so nobody repeats them)

- RE.SE: 0 CATIA results (site search + SE API).
- "CAX-IDS"/"ODSC standard": not findable under those names on Google/Bing/Brave/DDG (EN/CN/RU), Crossref, Semantic Scholar.
- OCCT IRB: no src/IRB or CATIA module in any inspectable OCCT tag (V6_9_1 -> V8); Wikipedia says native exchange = STEP/IGES/glTF/OBJ/STL/VRML, CATIA via commercial Datakit plugin; "readirb" queries return nothing. Pre-6.9 OCCT tarballs unreachable (files.opencascade.com down for us) - small residual uncertainty.
- cccp3d.ru topic 74514: JS bot-check; no Wayback copy; needs a real browser.
- Arctic Shift: no catpart/RE-title posts in r/CAD, r/reverseengineering, r/CATIA within default window.
- Search routes that are dead from this host: DDG lite, Mojeek (captcha), Marginalia (empty), public searx instances, Bing RSS (junk), old.reddit JSON, grep.app, Habr search (JS SPA), dev.to-style full-text engines; Semantic Scholar API 429s; working stack = ddgs python (google/bing/brave, region params), GitHub REST (unauth), Crossref, HN Algolia, PullPush, Arctic Shift (unfiltered), Wayback.

## Transferable playbook (synthesis)

1. Check for a published or mirrored spec first. Parasolid XT and 3dm/OpenNURBS show vendor-published formats create parser ecosystems; when absent (CATIA), look for mirrored official help (maruf.ca, catiadoc.free.fr): it documents semantics (CGM object model) even when bytes are undocumented.
2. Identify the container before anything else. Magic bytes + PRONOM/file/cadver records: CATPart = `V5_CFV2`, SW = OLE2 then marker-scanned chunks, КОМПАС = `KF`+code, modern Chinese CAD = zip. Never assume OLE twice; test per format, per era.
3. Build a differential corpus: author empty -> single primitive -> extrude -> fillet -> assembly files, and harvest bulk corpora from model-sharing sites (fafnir999's 466k files from c-stud.ru/alldrawings.ru is the ceiling example). One-feature deltas localize byte regions; version-chronology clustering of magics/codes identifies eras.
4. Adopt the invariant-database discipline (blussyya): every claim is a numbered invariant with a tested-file count and pass rate (593/595); keep EXPERIMENT_LOG.md and FAILED_HYPOTHESES.md; rule "syntax before semantics, never guess meanings". Treat format knowledge as a test suite, not prose.
5. Use float32/float64 scans against known geometry to find the geometry layer, and validate against oracles you can get legitimately: mass properties and preview/tessellation data (openswx validates extraction by mass properties; thumbnails approximate tessellation ground truth).
6. Reach a round-trip milestone early: decode -> STEP (sldprt2step path). STEP gives you a free validator (OCCT/FreeCAD) and a public compliance yardstick (benchmark.ap242.org).
7. Keep semantics (features/history) as phase 2, using academic interactive-RE approaches (10.1016/j.cagd.2024.102339) after geometry is reliable.
8. Publish as a knowledge-base repo, not just code; it attracts corpus donations and works well LLM-assisted (both blussyya and fafnir999 explicitly ran human+LLM loops).
9. Legal posture: byte observation + interoperability is the community's actual path (DWG precedent); never touch vendor API code under NDA (CAA docs are the semantic map, the CAA SDK headers are the contamination boundary).
10. CATIA-specific entry points: CFV2 chunk structure around the `V5_CFV2` header; UUID/identifier inventory via strings; CGM semantics from mirrored CAA tech articles; cccp3d topic 74514 via a real browser; commercial readers (Tech Soft 3D/Okino/CAD Exchanger) as behavioral oracles.
