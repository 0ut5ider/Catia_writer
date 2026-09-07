# Late batch raw results (2026-09-06, session 2)

## ImHex / format RE methodology
- HN item 49508608: "Reverse Engineering Unknown File Formats with ImHex"
  https://news.ycombinator.com/item?id=49508608 | url: https://werwolv.net/posts/file_format_reverse_engineering/ | 2026-08-31 | 256 points
- Duplicate post 49496951 same day.

## Chinese group standard (what "ODSC-like" actually is)
- gddac.org.cn/nd.jsp?id=45 (广东省数字化学会, 2023-07-15): 《三维CAD数据模型和格式》团体标准征求意见, DISA 数字化工业软件联盟, online review platform http://116.63.173.155:31001/disa/ , deadline 2023-08-15, contact leimin@datalinkin.com.
- gddac.org.cn/pd.jsp?id=8: T/DISA 1011 三维CAD模型轻量化格式 (published standard).
- disa.org.cn/Content-371.html (JS page, same notice; fetch returned title only).

## archiveteam (via Wayback, direct connect fails from this host)
CATPart (web/20241218182710, page last modified 2020-04-11):
- Extensions .catpart; PRONOM x-fmt/439; Wikidata Q49416323
- Magic bytes 56 35 5F 43 46 56 32 = ASCII "V5_CFV2"
- "CATPart (CATIA Part Description/Model v5)... equivalent in version 4 is CATIA V4 Model"
- Sibling pages: CATDrawing, CATProduct, CATProcess, CATMaterial, 3DXML, cgr, CATIA V4 Project
CATIA V4 Model (web/20241218182710, last modified 2020-04-11):
- Extensions .mod, .model; PRONOM x-fmt/436; Wikidata Q49414097
- Sample files: grabcad Q&A link; Okino CATIA v4 importer doc link
- Links: Okino importer docs, 3ds.com

## OCCT CATIA/IRB verification - NEGATIVE
- GitHub Open-Cascade-SAS/OCCT tags V6_9_1..V8.x: no src/IRB, no CATIA module (checked 4 tag trees earlier).
- Wikipedia Open_Cascade_Technology (fetched 2026-09-06): Data Exchange "STEP, IGES, glTF, OBJ, STL, VRML supported natively... Other formats can be imported by using plug-ins" [ref: dev.opencascade.org/about/data_exchange; Datakit link]. No mention of IRB or CATIA anywhere.
- old.opencascade.com/content/catia-v4-import-datakit and /content/catia-v5-import-datakit: CATIA import is a commercial Datakit product.
- ddgs queries: 'opencascade "IRB interface"' 0 results; '"readirb"' garbage (unrelated); 'OCCT 6.5 "IRB" CATIA V4 source' nothing.
- files.opencascade.com / files.opencascade.org unreachable from this host (pre-6.9 tarballs not inspected - residual uncertainty).
- Conclusion: "OCCT documents CATIA V4 IRB format (irb_format_cxx)" not supported by any public source found. Treat as false/false-memory.

## cccp3d.ru
- Topic 74514 "Формат - CATIA" exists but every fetch (webfetch 403, curl 28KB) returns a JS bot-check page titled "Проверка". Wayback: no snapshots. Content unretrievable without a real browser.

## Reddit (Arctic Shift)
- posts/search?subreddit=CAD|reverseengineering|CATIA&selftext=catpart -> 0 rows; &title=reverse+engineering -> 0 rows (API healthy: unfiltered query returns posts). No CATIA-format threads in the 14-month default window.

## Parasolid XT manual (fetched)
- q-solid.com/Parasolid_Docs/xt_index.html: Siemens "Parasolid Transmit File Format" manual (V11.0 edition), published format, aimed at translator writers; PDFs under q-solid.com/Parasolid_Docs_V35/pdf/xt.pdf. Proves: official public spec exists => ecosystem of independent parsers.

## Crossref
- "Interactive reverse engineering of CAD models" -> Computer Aided Geometric Design, 2024-06, DOI 10.1016/j.cagd.2024.102339.
- ("CAD for Reverse Engineering" - CAD for Hardware Security book chapter 2023, DOI 10.1007/978-3-031-26896-0_15 - different sense of RE, noted.)

## arXiv SldprtNet (fetched)
- arXiv:2603.13098, submitted 2026-03-13, ICRA 2026. 242,000+ industrial parts, .step + .sldprt, encoder/decoder with 13 CAD commands (lossless structured-text round trip), 7-view composite renders, Qwen2.5-VL-7B generated + manually verified descriptions.

## blockfmt / Sam Partington - NEGATIVE
- '"blockfmt" OR "miscto" CAD binary format' (bing) 0 results; sampart GitHub repos: none matching; HackerNoon @sampart profile empty.

## Other URLs seen in raw greps (citable context)
- catiadoc.free.fr/online/cfyugrvs_C2/cfyugrvsexport.htm (mirrored CATIA help)
- docs.techsoft3d.com/exchange/2025.1.0/start/format/catia_v4_reader.html
- ansyshelp.../ref_cad/cadCatiaV4.html
- cadinterop.com/en/formats/cad-systems/catia-v4.html, catia-v5.html
- developer.rhino3d.com/guides/opennurbs/what-is-opennurbs/
- github.com/eryar/3DMViewer (opennurbs viewer)
- github.com/eryar? / pycatia examples (automation wrapper)
- aecmag.com/opinion/the-dwg-conundrum/
- en.wikipedia.org/wiki/.dwg, /wiki/Parasolid, /wiki/Onshape
- github.com/fougue/mayo (multi-CAD converter, OCCT+commercial readers)
- cadexchanger.com/catpart-to-gltf/, /catia-to-brep/, /parasolid/
