# Programmatically Writing Native CATIA V5 Files (.CATPart / .CATProduct)

- Date: 2026-09-06
- Agent role: web research agent (Cerebo session)
- Question: What are the sanctioned, practical ways to generate native CATIA V5 files
  programmatically, using CATIA itself as the writer? What does each path cost (money,
  licenses, OS constraints), and what are the known traps?
- Model: flashnext/flashnext-w4a16-fp8ple

## TL;DR

CATIA itself must be the writer. Native `.CATPart`/`.CATProduct` are proprietary,
versioned, container formats (structured storage); no sanctioned third-party writer
exists. Five sanctioned writer paths:

1. **COM automation from another process** (`CATIA.Application` via pywin32/pycatia) on
   Windows, with a licensed, running CATIA V5. This is the practical path.
2. **In-context macros** (CATScript / VBA / `.catvba`) launched by `CNEXT -macro`.
3. **Batch (headless) mode**: `CNEXT -batch -macro ...` runs CATIA without UI and exits.
   Real headlessness on Windows, no X server or VNC needed.
4. **CAA V5 C++ (RADE license)**: `CATDocumentServices::New` etc. for true headless
   in-process creation. Heavyweight; license-gated.
5. **3DEXPERIENCE / "V6" is NOT a local file writer.** It creates platform objects
   (`3DPart` via `PLMNewService`, E70 license), not `.CATPart` files on disk.

Linux/Wine is hobbyist-grade only: intermittent license and rendering failures, no vendor
support. Practical recommendation: a Windows VM (or spare box) with any licensed CATIA V5
(2018+ fine), pycatia on Python ≥3.9, scripts run via `CNEXT -batch -macro` or attached
via `win32com`.

---

## 1. COM automation from another process (primary path)

### 1.1 The stack

- COM ProgID: `CATIA.Application`. Attach to running instance:
  `win32com.client.Dispatch("CATIA.Application")` (or `GetObject("", "CATIA.Application")`).
  Create: `CreateObject("CATIA.Application")`.
- **pycatia** (https://github.com/evereux/pycatia) is the maintained Python wrapper:
  365 stars, MIT, auto-generated from the V5Automation typelib of CATIA V5 R28,
  PyPI v0.10.1, 67 releases, latest releases current through 2026-03-26 (verified via
  `pypi.org/pypi/pycatia/json`). Requirements: Windows + Python ≥3.9 + running CATIA V5.
  Ecosystem exists: evereux/pycatia-tools (20★), SheydaKarimabadi/PyCATIA_Automation_Tutorial
  (15★), rk5novikov/PyCatia (8★), RiyanJamy/PyCatia (5★), mufi2/PyCatia-Drone-Final,
  KaiUR/Pycatia_Scripts, leonardozeng/CATIA_Python, pipelineinc/cv5com (Rust).

### 1.2 Minimum viable writer (pycatia)

```python
from pycatia import catia

application = catia()
documents = application.documents
part_document: PartDocument = documents.add('Part')
```
(verbatim from https://pycatia.readthedocs.io/en/latest/introduction.html)

### 1.3 Real geometry writer (pycatia, sketch → pad)

From `examples/example__hybrid_sketch__shape_factory__001.py` in the repo: points are
placed with `hybrid_shape_factory.add_new_point_coord(...)`, a sketch is created on
`part.origin_elements.plane_xy` via
`reference = parts.create_reference_from_object(plane_xy)`, edited with
`sketch.open_edition()` / `sketch_factory_2d.create_point(...)` / constraints, closed with
`sketch.close_edition()`, then padded via `shape_factory.add_new_pad(sketch, length)` and
`part.update()`.

### 1.4 VBA/CATScript equivalent (canonical CAA use-case, verbatim)

From `CAAScdPriUseCases/CAAPriPad.htm` (catiadoc.free.fr mirror of CAA docs):

```vb
Set oNewPartDocument = CATIA.Documents.Add("Part")
Set oPart = oNewPartDocument.Part
Set oFactory2D = oSketchFactory.CreateFactory(oSketch2D)
' ... sketch geometry ...
Set oPad = oPart.ShapeFactory.AddNewPad ( oSketch, 20.000000 )
oPart.Update
```

Creating documents (CAA `CAAInfCreateDocument.htm`):

```vb
Set oNewPartDocument = CATIA.Documents.Add("Part")
```

Products (`CAAPstAddNewProduct.htm`):

```vb
Set oProductDocument = CATIA.Documents.Add("Product")
Set oRootProduct = oProductDocument.Product
oRootProduct.PartNumber = "Root"
Set oNewProduct = oRootProduct.AddNewProduct("ChildProduct")
```

### 1.5 Assembly placement (no SPAWorkbench needed)

pycatia `example__product__002.py`: read with `product.position.get_components()`, write
with `product.move.apply((r11, r12, r13, tx, r21, ... tz))`, a 12-component
3×3 rotation + translation tuple. `Move.Apply / Move.SetComponents / Position.GetComponents`
confirmed in `pycatia/in_interfaces/move.py` and `position.py` (generated from InfInterfaces).

### 1.6 Known COM traps (all sourced)

- **Out-of-process `Documents.Add("Product")` is unreliable** (popup / PartNumber dialog
  can hang automation). Stack Overflow q/31998761 workaround: execute the creation
  in-process via
  `CATIA.SystemService.Evaluate(vba_code_string, 1, 'create_product', [arg])`.
  Also `CATIA.Visible = False` for invisible sessions.
- **Unsaved-children save dialog kills batch.** Saving a root `.CATProduct` whose parts
  are unsaved raises "This activates other save operations, do you want to continue?"
  (SO q/48190554, accepted answer). Correct pattern: save **leaf-first, bottom-up**, then
  save upward; set `CATIA.DisplayFileAlerts = False`. Accepted answer contains a full
  VBA dictionary-based bottom-up saver (see Raw sources).
- **Update before save**: every CAA use-case ends `oPart.Update`; a document "in error"
  still saves but exports downstream can fail. (Partially verified: update requirement is
  explicit in docs; the exact error-state save semantics I did not verify with a citable
  source. Treat as unverified.)
- Reddit r/CATIA "Automation API incomplete": some UI features are simply not exposed
  (e.g. BOM checkbox manipulation); community workaround patterns like
  `object.Parent.Parent` to reach target bodies exist, but some gaps are permanent.
- `.CATPart` vs `.catpart` case: unverified on Linux/Wine (CATIA is Windows-first; on
  case-sensitive filesystems reference resolution is reported fragile, no citable source
  found; treat as folklore until confirmed on a real box).

### 1.7 License checkout automation

pycatia `example__license_settings__001.py` (verbatim pattern):

```python
settings_controller = application.settings_controller
setting_controller = settings_controller.item("CATSysLicenseSettingCtrl")
from pycatia.system_management.interfaces.license_setting_att import LicenseSettingAtt
l: LicenseSettingAtt = LicenseSettingAtt(setting_controller)
print(l.get_license("AL3.prd"))  # 'Requested' | 'NotRequested'
l.set_license("AL3.prd", "Requested")
```

So workbench licenses (e.g. `AL3.prd` ~ Part Design family on DS keys) can be requested
programmatically before creating geometry. Server side is DSLS (`DSLS.lic`, TCP 4085,
per third-party ops doc quoted in Raw sources; hearsay-but-consistent).

## 2. Macro-in-context: CATScript / VBA / catvba

CAA `CAAInfInvoking.htm` (catiadoc mirror, verbatim forms):

```
CNEXT -macro E:\Users\Macros\MacroToRun.CATScript
CNEXT -macro myDocument.catvba myMacro
```

- `.CATScript` runs immediately on session start; `.catvba` requires a macro name.
- Scripts run inside the session, so `CATIA.Application` is the global `CATIA`.
- Same scripts also run interactively via Alt+F8 macro dialog.

## 3. Batch (headless) mode on Windows

From `CAAInfInvoking.htm`: "CATIA V5 can also be launched in batch mode... the batch mode
does not display any window and no display updates are performed. Once the macro has been
run, the CATIA V5 session is ended."

From v5vb.wordpress.com (official-adjacent CATIA blog), 2010-09-26 "Executing CATIA
scripts in batch mode", verbatim invocation shape:

```
CNEXT.exe -batch -env CATIA.V5R20.B20 -direnv C:\cv5env\CATEnv -macro "C:\path\job.CATScript"
```

Measured by the author: a drawing-generation job dropped from ~2.6 minutes to ~3 seconds.
Documented gotchas:
- On some setups the session exits after ~2 s if the macro arg is malformed.
- ENOVIA/login prompts break `-batch` (it cannot answer dialogs).
- Memory growth: author restarts the batch session every ~200 files.

`CATBatchMonitor.exe` and `CNEXT ... -nowindow` appear in a third-party ops skill doc
(Raw sources §R8) but I could not verify them in official docs; treat as unverified.

## 4. CAA V5 C++ (RADE): true headless writer

Official reference manual (via GitHub mirror lordkidd007/CAADoc,
`V5/generated/refman/ObjectModelerBase/class_CATDocumentServices_75551.htm`), verbatim:

> "Services to create, open and close documents. Role: All methods of this class must be
> used to create, open or close a document when no visualization is necessary. This is
> always the case in batch mode, but it is also possible in interactive mode... There are
> three methods for creating a (or several) new document(s) in the current session: New,
> OpenDocument, NewFrom."

Feature construction then uses PartInterfaces (`CATIPrtPart`, `CATIPrtFactory` pages
confirmed present in the same mirror). I verified the interfaces exist but did not verify
method-level C++ signatures; the COM route (§1) wraps the same factories and is far
cheaper operationally.

RADE economics (community-sourced, CADE FAQ, Raw sources §R9): building with CAA's `mkmk`
requires the CAA RADE license (license product "MAB"); manual Visual Studio compilation
of generated code works without it; without the framework `.dico` registration file a
component compiles but never instantiates. Academic RADE programs exist (university
licenses) but I found no current public price; RADE has historically been a paid,
per-developer license separate from a CATIA seat. Marked unverified.

## 5. 3DEXPERIENCE ("V6") is a different writer, not a file writer

scripting4v5.com, Emmett Ross, 2025-07-23, "Create a new part with V6 macro vs V5 macro"
(Raw sources §R6), substance:

- V5: `CATIA.Documents.Add "Part"` → a `.CATPart` file when saved.
- V6/3DEXPERIENCE: requires an **E70-class license**; creation goes through
  `PLMNewService`: `oNewService.PLMCreate "3DPart", oEditor3DShape` → the part is a PLM
  platform object in the 3DS platform, not a local file. Getting a `.CATPart` out is an
  export step (V5-interop export exists in the platform's product knowledge; the exact
  export call I did not verify from a citable source).

Conclusion: 3DEXPERIENCE (including xDesign and the ~$120/yr Maker portfolio tiers) is not
a scripted local `.CATPart` writer. For file-on-disk automation you want real V5 (or V5
data via a platform seat with V5 interoperability, unverified detail).

## 6. Linux without a Windows license seat: Wine reality check

- askubuntu q/155831 (2014): installer crashes unless the ISO is mounted via `gmountiso`.
- askubuntu q/237101: black-screen flicker fixed with Wine registry
  `[HKEY_CURRENT_USER\Software\Wine\X11 Driver] "UseXRandR"="N"` or `"ClientSideGraphics"="no"`.
- r/Ubuntu (Pulled via PullPush, 2022): V5R18 on Wine 6.0.3, license page greyed out;
  on Windows the `DSY_DISABLE_WININET=TRUE` workaround exists; no confirmed Wine fix.
- r/cad (2022-04) "Finally got CATIA running on Linux using wine": post body deleted,
  no recoverable detail. Anecdotes elsewhere claim v5.19 runs fine via Wine/CrossOver/
  PortingKit; several report specific features failing (text, rendering).
- No vendor support. For a generation pipeline this is a toy, not infrastructure.

## 7. Costs and licensing (numbers to re-verify before budgeting)

- GoEngineer buying guide (fetched 2026-09-06): standalone CATIA V5 perpetual ≈ **$15,200**
  plus ≈ **$3,300/yr** maintenance; term/rental ≈ **$6,600/yr**. The page renders mostly
  navigation via JS; numbers are from the fetched text but should be re-confirmed with a
  reseller quote.
- One seat = one concurrent user. DSLS license server can host floating seats; checkout is
  automatable (§1.7). No headless/server SKU of V5 exists; batch still consumes a seat.
- Maker/Student editions: could not fetch official current terms (search engines blocked,
  Wayback has no snapshots of the candidate 3ds.com URLs). Known constraints from prior
  knowledge, flagged: watermarked "non-commercial" files, no network/license-server use,
  and .CATPart output is version-locked. Do not build a pipeline on Maker Edition.
- CAA RADE: paid developer license, academic programs exist; no public price found.

## 8. Recommended pipeline for Adrian

Goal: agent generates parametric geometry, gets `.CATPart`/`.CATProduct` on disk.

1. Windows VM or spare box, licensed CATIA V5 (any release ≥ R2018; typelib is
   forward-compatible with pycatia's R28-generated API for core Part/Assembly/Inf).
2. Python ≥3.9 + `pycatia` (`pip install pycatia`); or raw `pywin32` if you want zero deps.
3. Generation job as a macro: either
   (a) attached mode: launch CATIA, `catia()` attaches, run Python, `save_as()`, quit; or
   (b) headless mode: emit a generated `.CATScript` that loads a JSON spec and builds
       geometry, run `CNEXT -batch -env ... -direnv ... -macro job.CATScript`.
4. Hygiene rules from §1.6: bottom-up saves, `DisplayFileAlerts=False`, always `Update`
   before save, restart the session every few hundred files, prefer
   `SystemService.Evaluate` for anything that pops dialogs.
5. Verification: reopen each output with `Documents.Open` + `Part.Update` +
   measure volume/mass; diff against expected params. (Volume/mass via
   `GetVolume`/inertia works headless.)

Cheapest wrong turn to avoid: trying to synthesize `.CATPart` bytes directly (reverse
engineering the container). The format is structured-storage with compressed versioned
feature history; even a byte-valid file is unsupported, unupgradeable, and CATIA-version
specific. Using CATIA as the writer costs one license seat and removes the entire class
of problems.

---

# Raw sources

Verbatim captures, with URLs and dates. Search-engine availability caveats in the final
section.

## R1. pycatia intro (https://pycatia.readthedocs.io/en/latest/introduction.html, 2026-09-06)

```python
from pycatia import catia

application = catia()
documents = application.documents
part_document: PartDocument = documents.add('Part')
```

## R2. pycatia sketch→pad example (github.com/evereux/pycatia,
examples/example__hybrid_sketch__shape_factory__001.py, key calls captured)

```python
origin_elements = part.origin_elements
reference = parts.create_reference_from_object(origin_elements.plane_xy)
sketch = hybrid_shape_factory.add_new_sketch()   # via sketch factory
sketch.open_edition()
factory_2D = sketch.open_manufacturing_mode()    # factory_2d.create_point(...) used
# ... factory_2D.create_point(x, y), constraints via factory_2D.add_constraint(...)
sketch.close_edition()
pad = shape_factory.add_new_pad(sketch, length)
part.update()
```

## R3. CAA pad use case (http://catiadoc.free.fr/online/CAAScdPriUseCases/CAAPriPad.htm)

```vb
Set oPad = oPart.ShapeFactory.AddNewPad ( oSketch, 20.000000 )
oPart.Update
```

## R4. CAA invoking/automation tech article
(http://catiadoc.free.fr/online/CAAScdInfTechArticles/CAAInfInvoking.htm)

- Out-of-process: `Set oCATIA = CreateObject("CATIA.Application")`;
  attach: `GetObject("", "CATIA.Application")`.
- `CNEXT -macro E:\Users\Macros\MacroToRun.CATScript`
- `CNEXT -macro myDocument.catvba myMacro`
- Batch: no windows, no display updates, session ends when the macro completes.

## R5. v5vb.wordpress.com 2010-09-26 "Executing CATIA scripts in batch mode"

```
CNEXT.exe -batch -env CATIA.V5R20.B20 -direnv C:\cv5env\CATEnv -macro "...\job.CATScript"
```

~2.6 min → 3 s per drawing; gotchas: 2-second silent exit on bad args, ENOVIA login
breaks batch, restart every ~200 files for memory.

## R6. scripting4v5.com 2025-07-23 "Create a new part with V6 macro vs V5 macro"

V5: `CATIA.Documents.Add "Part"`. V6/3DEXPERIENCE: E70 license required;

```vb
Set oNewService = CreateObject("PLMNewService")
oNewService.PLMCreate "3DPart", oEditor3DShape
```

Result is a platform 3DPart object, not a disk file.

## R7. SO q/48190554 accepted answer (STEP→native save; save-dialog mechanics)

> "When you do this, CATIA will complain that 'This activates other save operations, do
> you want to continue?' ... because you have to answer a dialog, it will prevent you from
> making a batch program. The right way to do this is to first save the leaf documents and
> then work 'up' the tree ... Then everything will be saved when you need it to be."

```vb
CATIA.DisplayFileAlerts = False
Set rootProdDoc = CATIA.ActiveDocument   ' as ProductDocument
rootProdDoc.SaveAs "C:\Temp\" & rootProd.PartNumber & ".CATProduct"
```

(Accepted answer continues with a `Scripting.Dictionary` bottom-up level-by-level saver,
branching on `TypeName(info.prod) = "Part"` for `.CATPart` vs `.CATProduct` suffixes.)

## R8. Third-party ops skill (alivirgo/Major-AI-Skills, skills/catia/SKILL.md, 2026-08-26;
UNVERIFIED details flagged)

```
CNEXT.exe -env CATIA_V5R32 -direnv "C:\ProgramData\DassaultSystemes\CATEnv" -nowindow
CNEXT.exe -batch -macro "C:\Scripts\BatchExport.CATScript"
CATBatchMonitor.exe            ' "headless operations" monitor
```

DSLS: `C:\ProgramData\DassaultSystemes\Licenses\DSLS.lic`, TCP 4085,
`DSLS_LICENSING_HEARTBEAT` registry value. Env files in
`C:\ProgramData\DassaultSystemes\CATEnv\*.CATEnv/.txt`. `-nowindow` and
`CATBatchMonitor` were not verifiable in official docs during this session.

## R9. CADE CAA FAQ (github.com/chenlei-gh/CADE, .agents/skills/catia-caa-dev/docs/guides/FAQ.md)

> "For mkmk compilation: Yes, you need CAA RADE license (MAB product). For manual VS
> compilation: No... Without Dictionary: Code compiles but component won't instantiate in
> CATIA!" Dictionary path: `Framework.edu/CNext/code/dictionary/Framework.edu.dico`.

## R10. CAA reference manual, CATDocumentServices
(github.com/lordkidd007/CAADoc V5/generated/refman/ObjectModelerBase/class_CATDocumentServices_75551.htm)

> "All methods of this class must be used to create, open or close a document when no
> visualization is necessary. This is always the case in batch mode... There are three
> methods for creating a (or several) new document(s) in the current session: New,
> OpenDocument, NewFrom."

## R11. License automation (pycatia example__license_settings__001.py)

```python
setting_controller = application.settings_controller.item("CATSysLicenseSettingCtrl")
l = LicenseSettingAtt(setting_controller)
if l.get_license("AL3.prd") == 'NotRequested':
    l.set_license("AL3.prd", "Requested")
```

## R12. Wine threads

- askubuntu q/155831: "Mount the ISO with GMOUNTISO and the installation won't crash :)"
- askubuntu q/237101 answers:
  `[HKEY_CURRENT_USER\Software\Wine\X11 Driver] "UseXRandR"="N"`; and
  `[HKEY_CURRENT_USER\Software\Wine\X11 Driver] "ClientSideGraphics"="no"`.
- r/Ubuntu via PullPush (2022): V5R18/Wine6 greyed license; `DSY_DISABLE_WININET=TRUE` is
  the Windows-side fix, Linux-side fix unknown.

## R13. Product placement (pycatia example__product__002.py + in_interfaces)

```python
components = product.position.get_components()
product.move.apply((r11, r12, r13, tx, r21, r22, r23, ty, r31, r32, r33, tz))
```

## R14. Out-of-process Product-add workaround (SO q/31998761)

```python
CATIA.SystemService.Evaluate(CREATE_PRODUCT_VBA_CODE, 1, 'create_product', [PART_NUMBER])
```

## Methodology and search log (honest)

Target ≥18 searches: met, 35+ distinct queries executed. Engine availability during this
session: DuckDuckGo html/lite, Brave, Mojeek, Ecosia, and public SearXNG instances all
bot-blocked; Bing RSS returned identical cached results for every query (unusable);
eng-tips.com, catiav5forum.com, cadfamily.com unreachable; PyPI html blocked by
Cloudflare (JSON API fine); Wayback has no snapshots for the candidate 3ds.com
maker/RADE URLs and the Siemens TCIC page. Working channels: GitHub API (repo search,
authenticated code search, contents/raw), Stack Exchange API, PullPush/Arctic Shift,
catiadoc.free.fr (CAA doc mirror), direct webfetch of pycatia docs/v5vb/scripting4v5/
goengineer/3ds.com.

Query list (abridged): DDG×2, Brave×4, Mojeek/Ecosia/SearXNG×3 (blocked), SE search×12
across stackoverflow/askubuntu/superuser (catia automation python, wine, batch, update
error, parameters excel, maker edition, 3dexperience catpart, license checkout,
knowledgeware, cnext options, udf instantiate; several returned 0 = SO has no content on
maker/license/knowledgeware topics), PullPush×4, Arctic Shift×3 (1 shape-error), GitHub
repo-search×5, GitHub code-search×9 (pycatia trees, cnext flags, CATDocumentServices,
CATIPrtFactory), Wayback CDX×6, plus ~15 direct page fetches.

## Open items (flagged unverified in-line)

1. Maker Edition current terms/price and version-lock watermark behavior.
2. Exact 3DEXPERIENCE→.CATPart interop export call.
3. CAA RADE current pricing/academic program.
4. Error-state save semantics precisely.
5. Extension case sensitivity on case-sensitive filesystems.
6. `-nowindow` / `CATBatchMonitor.exe` existence in official docs.
