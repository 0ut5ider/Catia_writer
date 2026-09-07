# Evidence notes (fetched 2026-09-06/07)

## 1. Datakit CrossManager (https://www.datakit.com/en/cross_manager.php, fetched 2026-09-07)

Verbatim quotes:

- "Does not require an external licence."
- "A CrossManager licence includes: the conversion engine, a reading module for each file
  format to be read, a write module for each format to be written."
- CATIA V5 3D: Reading "Version: R10 to V5-6R2026, Extension: .CATPart .CATProduct";
  Writing "Version: R14, R19, R20, R21 & V5-6R2012 to V5-6R2026, Extension: .CATPart .CATProduct".
- Output formats include: CATIA V5 3D, 3DXML, CGR, JT, STEP (AP203/AP214/AP242), Parasolid,
  ACIS, SOLIDWORKS 3D, UG NX 3D, PLM XML, PRC.
- "CrossManager CLI (Command Line Interface) will allow tight integration into your workflow
  (PLM, background services, scripts). It comes as a lightweight no-GUI executable that can
  run on various platforms, including Windows, Linux and macOS."

Interpretation:

- Datakit writes CATPart files WITHOUT a CATIA install or license. A writer that never calls
  CATIA cannot emit CATIA history objects, so output is B-rep/assembly/metadata into the
  CATIA container, not a live feature tree.
- No statement anywhere on the page that output contains parametric history or sketches.

## 2. Datakit homepage (https://www.datakit.com/, fetched 2026-09-07)

- "Extraction and writing of geometric data, (B-Rep, Mesh), tessellation data, metadata,
  PMI and feature data."
- "Over 50 native or standard 2D and 3D formats available, including parts, assemblies,
  PMI, features."

Interpretation: "feature data" is offered as data extraction. In SDK read contexts, feature
data means reading feature information from source files. Nothing says a written CATIA file
carries an editable feature tree. The phrase "Extraction and writing" is ambiguous; it is a
verified gap (open question to ask Datakit directly).

## 3. Theorem, CATIA V5 to JT (archived, raw/catia_v5_to_jt.html, 85723 bytes)

- "has been developed using the Dassault Systems CATIA V5 CAA Development Environment and
  therefore is integrated within an existing licensed CATIA V5 installation."
- CATIA CAA products "require access to a V5 license in order to run"; NX products use
  "Siemens NX Open tools."

Interpretation: the only commercially shipped cross-CAD bridge that touches CATIA feature
semantics is a CATIA-resident add-on running against a local licensed CATIA. That is the
structural limit of history-preserving translation: it needs the target CAD's own API.

## 4. theorem.com status (fetched 2026-09-06)

- theorem.com now redirects to Tech Soft 3D branding; acquisition FAQ lists
  CADTranslate/CADPublish/TheoremXR, no XCAD product.
- xcad.com: webfetch "Transport error", no DNS A record, RDAP registered, Wayback captures
  from 1998 are ~1 KB telecom-era pages. Not an available product today.

## 5. HOOPS Exchange (Tech Soft 3D)

- Earlier fetch of the docs index showed Feature Trees topics. The guessed deep URL
  `docs.techsoft3d.com/exchange/author/guide/features/feature_trees.html` returned 404 on
  2026-09-07; the read-only claim below is INFERRED, not quote-verified.
- Inference: HOOPS Exchange is an SDK for reading CAD files (including feature-tree
  metadata from native formats). No published capability writes feature trees INTO a target
  CATPart container, and Exchange does not run CATIA.

## 6. pycatia (GitHub, 2026-09-06)

- `evereux/pycatia`, 366 stars: Python wrapper over CATIA's V5 automation API.
- `PyCATIA_Automation_Tutorial` and other repos show scripted creation of sketches and
  part features from Python.
- Interpretation: a scripted build inside CATIA produces native, fully editable history,
  because the history is created by CATIA itself.

## 7. Search-engine blocklist (2026-09-06/07)

- DuckDuckGo HTML/Lite: bot challenge. Mojeek: JS captcha. SearxNG instances: anti-bot.
- Google via curl: empty. Bing RSS: irrelevant results.
- StackExchange API: 0 results for CATIA feature-tree queries onstackoverflow.com.
- stackoverflow.com direct question fetch: 403.
- Direct curl to datakit.com/TransMagic/TechSoft docs sometimes 200 with size 0; webfetch
  works. Wayback for some Theorem translate pages: 4644-byte stubs.
