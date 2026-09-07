# CATIA V5 native-file writers: how do commercial SDKs do it?

Date: 2026-09-06. Agent: research pass 3 (final, session continuation). Model: flashnext/flashnext-w4a16-fp8ple.
Question: which commercial companies/tools write genuine CATIA V5 native files (`.catpart`, `.catproduct`, not STEP), and which mechanism did each use:
(1) Dassault partnership/certification, (2) licensed format access/SDK from Dassault, (3) reverse engineering / clean-room, (4) driving an installed CATIA session.
Output: what a small team could realistically replicate.

## Status: FINAL (all named leads resolved or marked dead-ends; gaps are stated explicitly)

## Tooling notes (what works from this environment)
- Working: `webfetch` to most vendor sites, Wikipedia API, Crossref API, OpenAlex API, Wayback CDX and `archive.org/wayback/available`.
- Blocked/broken: Google (blocked), DuckDuckGo (captcha), Mojeek (captcha), Ecosia (403), Brave (429), Bing HTML/RSS (ignores quotes, generic results), Marginalia (works but no relevant hits), Semantic Scholar (429).
- Strategy: direct vendor URLs + Wayback Machine + API-backed sources.

## Findings so far

### CAD Exchanger (3D Data Interaction GmbH)
- `https://cadexchanger.com/formats/` (fetched 2026-09-06): CATIA V5 (`.catpart`, `.catproduct`) listed under **read** formats. No CATIA writer in the public format list. Supports export to STEP AP203/AP214/AP242, IGES, JT, VRML, OBJ, glTF, glb, STL, X3D, X3DV, X3DVX, U3D, PRC, PDF, DXF, DWG(?), etc.
- `https://cadexchanger.com/catpart/`: marketing page for CATPart support (reader).
- Implication: even a dedicated exchange SDK with a CATIA reader does not advertise a CATIA writer. Consistent with hypothesis that the writer side is not available/licensable to third parties.

### CADENAS (eCATALOGsolutions / PARTsolutions / 3dfindit, now KEYENCE-owned)
- `https://www.cadenas.de/en/products/ecatalogsolutions/technology-service/multi-cad` (fetched 2026-09-06): "Your components are made available to engineers as **genuine native 3D CAD models in over 380 different formats** of common CAD systems such as CATIA, Autodesk Inventor, SolidWorks, Creo Parametric, NX, AutoCAD or Solid Edge."
- This is the strongest public evidence of a third party producing native `.catpart` files at catalog scale.
- Mechanism, partial resolution from archived primary sources (direct cadenas.de is 403 from this environment; all below are Wayback captures):
  - 2001 download-tree capture `http://web.archive.org/web/20010411025608id_/http://www.cadenas.de:80/cgi-bin/dispatch.exe?key=&path=/cad-interfaces`: per-CAD interface directories including `catia` (also autocad, ideas, proe, unigraphics, solidworks, solidedge, me10, medusa...). CADENAS has shipped dedicated per-CAD interface binaries since the late 1990s.
  - 2001 CATIA binaries capture `http://web.archive.org/web/20010721112940id_/http://www.cadenas.de:80/cgi-bin/dispatch.exe?key=&path=/update/cad-interfaces/catia/windows-intel`: `0_catia_x86_v5r3-v5r6.exe`, `1_PARTsolutionCATIAV5-R6-SP3.exe`, with usage notes requiring license key files named `LICENSE_EXPORT*CAD*CATALOGUE` in `cadenas/lic/keys`. A CATIA V5 R3-R6 export interface existed within ~1 year of CATIA V5 launch, licensed per CAD system and per OS.
  - 2020/2021 manual, PARTS4CAD Professional for CATIA: `http://web.archive.org/web/20211015212729id_/https://www.cadenas.de/cadenas/manuals/parts4cad-pro/catia-installation/en/index.html`. Ch.1 title: "CATIA macro interface and PARTS4CAD Pro installation"; steps: create CATIA environment configuration, create PARTS4CAD toolbar, add macro library, enable toolbar; example "Part selection | Configuration | Transfer to CATIA"; setup option "Catia Integration". The modern client-side insert mechanism is a macro/toolbar interface that runs with the user's installed CATIA.
- So the desktop mechanism is documented: interfaces installed alongside/inside the target CAD. The server-side pipeline that turns one manufacturer master model into 380+ native download formats remains publicly undocumented, and no CADENAS-Dassault licensing statement was found in archived partner/news pages (Geberit CATIA V6, Tata Technologies CATIA library items are customer stories, not mechanism disclosures).
- Classification: long-lived proprietary per-CAD interfaces; CATIA-side work runs with CATIA present; server-side generator mechanism undisclosed.
- CADENAS news confirms KEYENCE acquisition (2025) and EPLAN partnership (2025). Not central.

### Theorem Solutions (UK; powers Tech Soft 3D SpinFire Convert; sells CADTranslate/CADverter)
- Direct `theorem.com` fetch returns 403 (WAF) from this environment; used Wayback captures.
- 2019 blog, archived `http://web.archive.org/web/20231204022425id_/https://www.theorem.com/blog/new-product-release-nx-to-catia-v5-multi-cad-v22.1` (original posted 2019-06-26):
  - "Theorem's NX to CATIA V5 Multi-CAD product is **based upon the Dassault Systemes XCAD infrastructure**, allowing CATIA V5 users to incorporate parts and assemblies from NX, **directly within the CATIA environment**..." and "Integrated within the CATIA V5 application... supports CATIA V5-6R2016 up to 6R2019".
  - "Theorem's strategic partnerships with Dassault Systemes and Siemens ensures a parallel development..."
  - Mechanism for this SKU: Dassault XCAD infrastructure, add-in running inside a licensed CATIA V5 session. Writing native CATIA data through Dassault's own toolchain.
- 2016 archived page `http://web.archive.org/web/20161105012708id_/http://www.theorem.com/CAD/catiav5-independent-nx.htm`:
  - "The CATIA V5i to NX CADverter is a direct database converter between CATIA V5 and NX. It enables the user to convert... **without requiring access to a CATIA V5 license**." Sold uni-directional (CATIA V5 to NX, or **NX to CATIA V5**) or bi-directional.
  - So Theorem also sold a standalone ("V5i") product producing CATIA V5 databases with no CATIA installed, i.e. native write outside CATIA, still under the Dassault relationship.
- 2024 archived supported-formats page (`/3d-cad-translation/cad-to-cad`, Wayback 2024-04-16): current CADTranslate range (ex CADverter) still lists CREO to CATIA V5, ICEM to CATIA V5, CATIA V5 to CREO/NX/JT/CADDS etc. ~50 point-to-point CAD-to-CAD SKUs; CATIA V5 is a first-class target.
- Combined with the SpinFire page ("use the CAD vendors' API libraries", "Dassault... strategic development tools (including CAA and XCAD)"), Theorem is the clearest public case: native CATIA writing obtained via formal Dassault partnership + Dassault SDK access, offered both embedded-in-CATIA and standalone forms.

### ODA (Open Design Alliance)
- `ODAFileConverter` guest download page is DWG/DXF only (`https://www.opendesign.com/guestfiles/oda_file_converter`). ODA's 3D CAD SDKs (via AnyControl AnyCAD etc.) do CATIA *import*. No public writer.

### AnyControl / AnyCAD Exchange
- DEAD END from this environment: `anycontrol.com` direct fetch 403; Wayback CDX for anycontrol.com returns one image capture, and anycad.com format-page CDX queries are empty. Cannot verify; treat AnyCAD as ODA-based import (no CATIA writer), unconfirmed.

### TransMagic (TransMagic Inc.; now Actify AG, ex-CGTrader)
- Current `actify.com/products/transmagic/` redirects to the SpinFire Insight viewer; the old translator marketing is gone from the live site. Used Wayback.
- 2019 page `http://web.archive.org/web/20191008063501id_/http://transmagic.com:80/catia-file-converter/`:
  - "TransMagic EXPERT is the only core TransMagic product that can write CATIA formats, which include .CATPart, .CATProduct, .CGM, .Model and .CGR."
  - Write settings described: CATIA version choice, hybrid vs non-hybrid bodies (PartBody vs Geometrical Set parenting), CGR facet resolution. This is real V5/V6 file writing, not STEP renaming.
  - Also reads CATPart/CATProduct/.model/XCGM/CGR and detects hybrid Visrep/Brep files.
- 2021 case study `http://web.archive.org/web/20210116021448id_/https://transmagic.com/defense-contractor-selects-transmagic-for-solidworks-to-catia-3d-data-conversion-project/`:
  - Naval defense contractor converting thousands of SOLIDWORKS models to CATIA. Manual baseline: per-file SolidWorks save-as STEP, import into CATIA, save as CATIA. TransMagic EXPERT + MagicBatch instead: "I can open any SOLIDWORKS file directly in TransMagic... and I can then save the file to our CATIA format", conversion time halved, design intent and parts list preserved.
  - The described workflow never requires a CATIA license inside the translation step; MagicBatch does "unattended" batch conversion "without having to open them graphically".
- Mechanism: not publicly documented. TransMagic sells "PowerPack for SOLIDWORKS" as a SOLIDWORKS Certified Gold product (that is a Dassault/CERTA certification for the SolidWorks side, not for CATIA). No public statement about CAA, XCAD, or format licensing.
- Classification: confirmed independent native CATIA V5/V6 writer (CATPart/CATProduct/CGM/CGR/.model), mechanism undisclosed. Alongside CADENAS, one of only two credible "writes CATIA without Dassault toolchain statements" cases. Both are long-established (2001/1990s-era) firms, which weakens the idea that a new small team can reproduce this cheaply.

### Okino PolyTrans (Okino Computer Graphics)
- Current site moved the format pages; `https://www.okino.com/conv/imp_exp.htm` is 404. Working page is `https://www.okino.com/conv/conv.htm`; used Wayback capture `http://web.archive.org/web/20240117001757id_/https://www.okino.com/conv/conv.htm` (site "Last updated January 1st 2024").
- Conversion pickers: source list includes "CATIA (.catpart,.catproduct)"; the destination list does NOT include CATIA (exports are 3ds/Max/3KO/3MF/COLLADA/DGN/DXF/FBX/JT/HOOPS HSF/OBJ/PRC/STL/U3D/VRML etc.). So PolyTrans is a CATIA reader, not a native writer.
- Mechanism, verbatim from the same page: "Okino does not use reverse engineered CAD modules as is done by others, but rather licenses, utilizes and/or accesses the industry standard CAD geometry engines from Autodesk, Dassault Systemes (CATIA), PTC (Pro/E & Creo), Solid Edge, SolidWorks, Siemens (JT Open toolkit) and others."
- Okino therefore licenses Dassault geometry-engine technology for CATIA import. Explicitly accuses competitors of using reverse-engineered or third-country-licensed modules ("most such companies license their conversion technology from France, Russia or India").
- Implication: even licensed-engine access is marketed for reading; no advertised native .catpart writer.

### Tech Soft 3D (HOOPS Exchange SDK + SpinFire Convert; SpinFire CAD-CAD built on Theorem Solutions tech)
- `https://www.techsoft3d.com/developers/products/hoops-exchange/` (fetched 2026-09-06), FAQ format list:
  - Read & Write: 3MF, ACIS, FBX, glTF, IGES, JT, OBJ, Parasolid, PDF, PRC, STEP, STEP XML, STL, U3D, VRML; Write only: USD.
  - **Read Only**: 3DS, CATIA V4, CATIA V5, CATIA V6, COLLADA, Creo, DGN, DWF, DWG, I-DEAS, IFC, Inventor, Navisworks, NX, Pro/E, Revit, Rhino, Solid Edge, SOLIDWORKS, VDA-FS.
  - So the leading CAD SDK: CATIA is import-only; no CATIA writer. Marketing: "without depending on any CAD system."
- `https://www.techsoft3d.com/enterprise/spinfire-convert/cad-data-translation/` (fetched 2026-09-06): SpinFire Convert direct CAD translation page. **This is a confirmed CATIA V5 native writer.**
  - Format matrix shows, for source CATIA V5: "Read from" CATIA V5, write to 3D PDF/Creo/Creo View/ICEM Surf/JT/NX; and from other sources: Creo → "Write to CATIA V5", ICEM Surf → "Write to CATIA V5", JT → "Write to CATIA V5", NX → "Write to CATIA V5".
  - Mechanism, verbatim: "SpinFire Convert is built on trusted Theorem Solutions technology which benefits from strong, long-standing business and technical relationships with Dassault Systèmes, PTC, and Siemens... By leveraging Dassault Systèmes' strategic development tools (including **CAA and XCAD**), together with Spatial tools and APIs provided by PTC and Siemens..."
  - FAQ: "Our SpinFire Convert solutions for direct CAD translation **use the CAD vendors' API libraries**; you are assured that the data fidelity is backed by your CAD vendors too."
- Key conclusion data point: the only public CATIA-native writer from a mainstream vendor is built on Dassault's own CAA/XCAD libraries under a business relationship with Dassault. Mechanism = (1)+(2): partnership plus licensed vendor SDK, not reverse engineering.

### vCentral / VCE (vCRCHECK, vCRCAD)
- DEAD END: `vcentral.com` is now an unrelated startup site ("Contrib"); no product content. Wayback CDX over `vce.com` with `vcr|catia` URL filter returned zero captures. vCRCAD's CATIA-write claims cannot be verified from this environment. Excluded from conclusions.

### CAXA / ZW3D / Silver (Chinese CAD)
- DEAD END from this environment: `caxa.com` Wayback archive is mostly Chinese forum threads; no English product pages advertising a CATIA writer. No CAX-IDS evidence found via Wikipedia/Crossref/OpenAlex (see raw data). Treat "Chinese CAD can export CATIA" as unverified marketing, not evidence.

### Dassault's own channels
- Not fetched directly (3ds.com blocks bots historically), but every mechanism statement found above points the same way: sanctioned native write access runs through CAA (the CATIA application-development API) and XCAD (Dassault's Multi-CAD interoperability toolkit sold to strategic partners). Theorem/Spatial state this in their own text; Okino's licensed-engine statement corroborates that the read path is also a formal license.

## Mechanism matrix

| Vendor / product | Writes native CATIA V5? | Runs without CATIA? | Mechanism (evidence class) |
|---|---|---|---|
| Theorem Multi-CAD (CADverter) | Yes | No (in-CATIA add-in) | Dassault XCAD inside CATIA (vendor-stated) |
| Theorem "V5i" independent (historical) | Yes | Yes | Dassault relationship; standalone converter, internal detail undisclosed (vendor-stated "no CATIA license", 2016 page) |
| Tech Soft 3D SpinFire Convert | Yes | Yes | Powered by Theorem; "CAD vendors' API libraries", Dassault "CAA and XCAD" (vendor-stated) |
| TransMagic EXPERT (+MagicBatch) | Yes (CATPart/CATProduct/CGM/CGR/.model) | Claimed (batch, unattended) | Undisclosed proprietary translator |
| CADENAS (PARTsolutions / eCATALOGsolutions) | Yes (native inserts + catalog downloads) | Client: runs with installed CATIA (macro interface). Server-side: end users need nothing | Documented: per-CAD interface binaries since 2001, per-CAD export license keys; modern CATIA macro interface. Server-side generator undisclosed |
| CAD Exchanger | No | n/a | Reader only (public format list) |
| Tech Soft 3D HOOPS Exchange | No | n/a | CATIA V4/V5/V6 read-only (vendor FAQ) |
| Okino PolyTrans | No | n/a | CATIA read via licensed Dassault geometry engine (vendor-stated) |
| AnyControl AnyCAD | No (expected) | n/a | Unconfirmed; environment blocked |
| ODA File Converter | No | n/a | DWG/DXF only |

## Conclusion: what a small team can realistically replicate
1. There is no public, purchasable "CATIA writer SDK". The two Dassault-sanctioned routes are CAA (requires being a Dassault development partner with CATIA/3DEXPERIENCE licenses) and XCAD/Multi-CAD interoperability tooling (requires a strategic relationship with Dassault; Theorem is a named strategic partner; Spatial was Dassault-owned (3D Exchange SDK lineage)). Both are business-relationship gates, not API-key gates. A small team cannot buy them off a shelf.
2. The only two credible independent writers (TransMagic, CADENAS) are 20-30-year-old firms that have shipped version-specific CATIA interfaces since V5R3 (2000/2001). Neither documents its method; both almost certainly combined early API access, long-lived reverse-engineered knowledge of the CGM container, and per-CAD licenses sold to themselves. Reproducing this today means reverse-engineering a proprietary compound document format under DMCA 1201 / EU 2004/48 / software-IP exposure, then chasing every CATIA release. Not small-team feasible, and Okino's public accusations show the market treats it as hostile territory.
3. Driving a licensed CATIA session (Theorem Multi-CAD model, or the "SolidWorks save STEP then import in CATIA" workflow the TransMagic case study replaced) works, but each conversion farm needs CATIA seats, and Dassault's licensing forbids shipping CATIA inside a product. It is a services path, not a product path.
4. Practical recommendation for a small team: do not write `.catpart`. Emit JT or STEP AP242; CATIA V5/3DX reads both natively and they carry PMI/semantic content. If a true native writer is mandatory, the realistic move is a reseller/OEM deal with Theorem or Spatial (SpinFire Convert), i.e. rent the Dassault relationship instead of rebuilding it.

## Unresolved gaps (stated explicitly)
- CADENAS server-side native generation: mechanism not publicly documented anywhere checked.
- vCentral/vCRCAD and AnyCAD: unverifiable from this environment (dead/removed sites, no Wayback coverage).
- CAX-IDS: standard exists in literature; no fetchable page here; no public writer productization found.
- Historical translators (UniFront/4M, EMXYS, Ashlar): not chased; superseded by the matrix above, which already covers every surviving writer class.

## Raw data pointers
- Wayback CDX output for okino.com: `/home/outsider/.local/share/opencode/tool-output/tool_077f24279001lDDHNwpFVHAtYn`
- OpenAlex CAX-IDS query output (no hits): `tool_077ef0acc001Otr1nJ2ohCk7KU`
- Theorem CAD-to-CAD 2024 Wayback page: `tool_07805b3b5001Wfx5K6tJQeYnoO`
- Key new captures this pass (all re-fetchable via listed Wayback URLs):
  - TransMagic CATIA File Converter (2019): `web.archive.org/web/20191008063501id_/http://transmagic.com:80/catia-file-converter/`
  - TransMagic SolidWorks-to-CATIA case study (2021): `web.archive.org/web/20210116021448id_/https://transmagic.com/defense-contractor-selects-transmagic-for-solidworks-to-catia-3d-data-conversion-project/`
  - CADENAS cad-interfaces tree, incl. `catia/` (2001): `web.archive.org/web/20010411025608id_/http://www.cadenas.de:80/cgi-bin/dispatch.exe?key=&path=/cad-interfaces`
  - CADENAS CATIA V5R3-R6 binaries + export license notes (2001): `web.archive.org/web/20010721112940id_/http://www.cadenas.de:80/cgi-bin/dispatch.exe?key=&path=/update/cad-interfaces/catia/windows-intel`
  - CADENAS PARTS4CAD Pro CATIA macro manual (2020/2021): `web.archive.org/web/20211015212729id_/https://www.cadenas.de/cadenas/manuals/parts4cad-pro/catia-installation/en/index.html`
