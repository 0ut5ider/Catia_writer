# CAD interchange formats as an alternative to reverse-engineering `.catpart`

- Date: 2026-09-06
- Agent: Cerebo (opencode session), model: anthropic claude (via opencode)
- Question asked: Can we skip reverse-engineering CATIA V5 `.catpart`/`.catproduct` files and instead
  require or produce standard interchange formats (STEP AP203/214/242, JT, 3DXML, IGES, glTF)?
  What does each format preserve, what is the legal/licensing position, what free tooling exists,
  and which path wins?
- Deliverable: answers below, then Caveats, then Raw sources with URLs, dates and verbatim quotes,
  then two validated STEP Part 21 examples.
- Companion file: `example-minimal-assembly.step` in this directory (hand-written AP214 assembly,
  validated with Open CASCADE 8.0.1, zero read errors).

## Verdict matrix

| Criterion | Native `.catpart` RE | STEP AP242 | STEP AP203/214 | JT | 3DXML | IGES | glTF |
|---|---|---|---|---|---|---|---|
| CATIA opens it | n/a (native) | yes (STEP is table stakes for CAD, S1) | yes (S1, S2) | yes, first-class in automotive (S8, S12) | yes (DS native, S9) | yes (legacy, dead since 1996, S10) | unlikely as CAD input |
| Assembly structure | full | full (NAUO mechanism, S2, S7) | full (AP214 CD) | full (JT structure + STEP B-rep V2, S8) | BOM + files (S9) | weak | no (scene graph only) |
| Exact B-rep geometry | full | yes, with precision caveats (S6) | yes | V2 embeds STEP B-rep (S8); V1 tessellated | Gregory patches / meshes (S9) | B-rep subset | no, mesh only |
| PMI / GD&T | yes | yes (AP242, S3, S11) | no/partial | partial | no | no | no |
| Feature tree / design intent | yes | no (S6 NIST quote: standards ignored design intent) | no | no | no | no | explicitly no (S13 glTF quote) |
| Spec access | none (proprietary, no public format spec) | ISO text paid; entity level free via S2/S7 tooling | same | ISO 14306 published (S8) | license from DS, internal use only (S9) | free (ASME) | free (Khronos) |
| Reading tools without CAD license | no | yes: pythonocc/cadquery-ocp, stepcode, FreeCAD (S14, S15, S16) | yes | partial: OCCT JT component (S17) | viewer only | yes | yes |
| Legal risk of third-party reading | high (EULA/circumvention) | low: open standard, open-source readers | low | low | medium: license terms (S9) | low | low |
| Effort for us | highest (binary RE, version churn) | low: validated reader already works here | low | medium | medium-high | low but format is dead | low |

Recommendation: require STEP (AP242 if PMI matters, AP214 CD otherwise) as the intake format.
Reading/writing STEP with `cadquery-ocp` already works in this environment and is proven here
by a hand-built assembly file that OCCT reads cleanly. Reserve native CATIA work for cases where
feature history is mandatory, and treat JT as the second choice for lightweight/automotive data.
Reverse-engineering the `.catpart` binary is unnecessary for geometry and structure, and it is the
only option that carries real legal risk.

## Q1. What formats exist and which versions matter

- STEP is ISO 10303, a family of parts. Part 21 is the plain-text file syntax (`ISO-10303-21;`
  header) (S5). Application Protocols define what can be exchanged: AP203 (configuration-controlled
  3D design), AP214 (automotive design, adds colors/geometry organization), AP242 (the successor
  that replaces AP203 and AP214) (S1, S4).
- AP242 is the current protocol: published 2014, and edition 2 (April 2020) added tessellated
  hybrids (curved triangles), textures, LODs, vertex colors, persistent IDs on geometry and
  additive manufacturing support (S1, S11).
- JT is an ISO-standardized format for 3D visualization and exchange: "In 2012 December, JT has
  been officially published as ISO 14306:2012 (ISO JT V1)" and V2 embeds STEP B-rep; JTIAP (2017)
  uses LZMA and specifies XT B-rep as recommended representation (S8).
- IGES is the pre-STEP US format, version 5.3 (1996) final, superseded in practice (S10).
- 3DXML is Dassault Systèmes' proprietary zip-based exchange format (S9).
- glTF is Khronos' runtime transmission format; meshes and scene graph only (S13).
- OCCT also exposes a native binary B-rep (`.brep`) which FreeCAD round-trips losslessly between
  OCCT-based tools (S16); it is a de-facto, not ISO, format.

## Q2. Can CATIA read/export these without conversion software?

Evidence for "yes" on STEP:

- STEP Tools (a vendor whose tools sit in CATIA/Teamcenter supply chains): "Nearly every major
  CAD/CAM system now contains a module to read and write STEP AP's" (S1).
- Theorem Solutions' converter line, sold against CATIA V5/3DEXPERIENCE data, translates
  "CATIA V5 ... JT and NX ... STEP ... SOLIDWORKS" both directions (S18).

For JT: JT is the automotive exchange format and the Wikipedia article ties it to OEM data
exchange, with STEP AP242/JT named for hybrid B-rep+tessellation exchange (S8). CATIA has offered
JT translators in 3D Exchange modules; I could not fetch a 3ds.com page from this environment
(3ds.com returned HTTP 500 to every path tried), so that part rests on secondary sources
(Caveats).

3DXML is Dassault's own format, so DS tools obviously handle it, but reading it outside DS tools
is the hard part (S9).

IGES import exists in every legacy CAD system including CATIA; development of IGES itself stopped
in 1996 (S10).

## Q3. What actually survives the export (structure, PMI, colors)

- Assembly structure is fully expressible in AP203/214/242 through
  `NEXT_ASSEMBLY_USAGE_OCCURRENCE` (NAUO) plus `PRODUCT_DEFINITION_SHAPE` and
  `CONTEXT_DEPENDENT_SHAPE_REPRESENTATION` with `ITEM_DEFINED_TRANSFORMATION` placements. OCCT's
  own translator: "assembly structure is recognized by NEXT_ASSEMBLY_USAGE_OCCURRENCE entities"
  (S2). A working 44-entity example is in Appendix B.
- The basic OCCT STEP translator deliberately limits itself: "Only geometrical, topological STEP
  entities (shapes) and assembly structures are translated by the basic translator"; colors,
  layers and attributes need the XDE/document-level translator (S2). So color/PMI survival depends
  on the exporter's option set, not just the format.
- PMI/GD&T is AP242 territory (S3, S11). AP203/214 do not carry annotation semantics.
- Feature history does not survive any of these: "standards for CAD data exchange ... were
  restricted to the exchange of pure shape information. These standards ignored the parameters,
  constraints, features, and other elements of 'design intent'" (NIST IR 7433, S6).

## Q4. Data quality issues in practice

- Numerical/precision mismatches: "Differences in the internal numerical accuracy of CAD systems
  was a major early cause of problems in the STEP-based exchange of B-rep models ... two points
  that are judged to be coincident by one system may have separate locations in another ...
  inconsistency between the geometry and the topology" (NIST IR 7433, S6). Exporters differ in
  unit scale and tolerance; expect sliver faces and broken sewn shells from cheap exporters.
- Structural bloat in Part 21: the Wikipedia article on Part 21 documents the criticism that the
  format cannot be read sequentially, that "assigning an RGB color code to an edge requires at
  least 6 other entities", that the same triangle can be encoded in several different ways, and
  that the specification is not freely available (S5).
- Version drift: an OCCT-built AP214 reader "translates ... STEP Application Protocol 214
  (Conformance Class 2) ... STEP Application Protocol 203 and some parts of AP242 are also
  supported", and writes "STEP AP 203 or AP 214" chosen by `write.step.schema` (S2). Even mature
  kernels implement part of AP242 only, so "we support STEP" from any vendor needs the AP and
  conformance class named.
- Concrete dialect traps found while validating our example (see Practical notes below): comment
  syntax and header placeholder styles vary between exporters (ST-Developer writes C-style
  `/* */` comments inside the header, S7; OCCT 8.0.1 flagged ISO-style `(* ... *)` comments in
  the DATA section and flagged one unresolved reference for compact empty FILE_NAME fields).

## Q5. Legal/licensing position

- STEP: ISO standard. Reading/writing it needs no license fee; free implementations exist
  (stepcode "formerly NIST's STEP Class Library", generates C++/Python from EXPRESS and reads
  "STEP Part 21 exchange files", S4; Open Cascade is LGPL-class; pythonocc/cadquery-ocp on PyPI,
  S14, S15). The ISO text itself is paid; the criticism that "the specification ... is not
  freely available" (S5) is real at text level, but the entity-level signatures needed to
  construct or interpret files are freely published by tool vendors (S7 schema pages).
- JT: openly published standard (ISO 14306:2012; S8). Original JT Open Toolkit hosted by Siemens;
  I could not reach its home page from this environment (Caveats).
- IGES: published ASME standard, no license issues; dead technology.
- 3DXML: proprietary. "Dassault Systèmes provides a yearly royalty free license to anyone
  requesting the 3DXML format documentation. This license however only permits internal works"
  (S9). That is the weakest licensing position of the group.
- glTF: free Khronos standard, but "glTF is not an authoring format. glTF deliberately does not
  retain 3D authoring information, in order to preserve runtime efficiency" (S13); irrelevant for
  engineering intake.
- `.catpart` itself: no public format spec; third-party parsing under CATIA's EULA plus
  anti-circumvention exposure. This is the only option in the table with meaningful legal risk,
  and it is the reason to prefer interchange intake.

## Q6. Does any of this preserve feature history?

No. See Q3/Q5 quotes (S6). AP242 edition 2's managed model based definition (MBE) and persistent
IDs (S11) keep associative references and annotation semantics on a modeled product, but do not
carry a CATPart feature tree. If the deliverable must contain the feature tree, the only formats
that carry it are CATIA's own (or parasolid-with-features in some NX contexts), which is exactly
why RE of `.catpart` is tempting and why we should instead negotiate intake (get STEP from the
supplier's export instead of their private binary).

## Q7. Free readers/writers (no CAD license)

- Python: `pip install cadquery-ocp` (verified working here, OCP namespace). Write path:
  pythonocc/CadQuery docs show `STEPControl_Writer` with
  `Interface_Static.SetCVal("write.step.schema", "AP214IS")` and CadQuery's
  `importStep(path, unit="M")` / `assy.export("out.stp", "STEP", mode="fused")` (S14, S15).
- C++/Python from EXPRESS: stepcode (S4).
- FreeCAD: reads/writes `.stp`, `.stpz` (zipped STEP), `.iges/.igs`, and native `.brep` (S16,
  Wayback capture of the current import/export table; base install has no JT/3DXML/CATIA row,
  those come from separate workbenches).
- OCCT itself ships the STEP translator (S2) and a JT component ("Read a JT file into a JT model,
  write a JT model into a JT file ... with the use of Open Cascade JT Import-Export", S17).
- Validation in this session: `STEPControl_Reader.ReadFile()` on all example files (S19 test log).

## Q8. Hand-writing STEP vs reverse-engineering `.catpart`

Hand-writing valid AP214 was done for this report: 44 entities, ~75 lines, and OCCT loads it with
`RetDone`, 1 root transferred, 1 shape, zero error lines (Appendix B + S19). Once you can hand
write it, you can generate it: emitting STEP text is a serialization problem with a clear grammar,
open readers to test against, and a paid-tool-free validation loop. Reverse-engineering
`.catpart` is a closed binary with per-version churn and legal exposure. Conclusion: generate
STEP, do not parse catpart.

## Practical notes from validation (Part 21 dialects, OCCT 8.0.1 via cadquery-ocp)

These come from controlled tests, one `ReadFile()` per fresh process, so counts are per file:

1. C-style `/* ... */` comments read cleanly everywhere tested (OCCT's own generated files,
   ST-Developer files like S7's `comments.p21`, and our example).
2. ISO-style `(* ... *)` comment lines in the DATA section produced `ERR StepFile: Incorrect
   Syntax: Fails Count: 5` on our first example (exactly the five comment lines), and the same in
   micro-tests both with `*)` closers. The final file switched to `/* */` and reads with zero
   errors. Treat the exact OCCT comment rule as a build quirk, not a spec claim, and test on the
   target reader.
3. `FILE_NAME` written compactly with empty placeholders
   (`('name','2026-09-06T12:00:00',('Cerebo'),(''),(''),'','')`) produced
   `ERR StepReaderData: Unresolved Reference: Fails Count: 1` on this OCCT build even in a
   two-entity template; switching to the IDA-STEP style of named, non-empty parameters (with
   `' '` for blank fields, as in the Wikipedia/IDA-STEP example in Appendix A) removed it.
4. Unit complex entities (`#5=(LENGTH_UNIT()NAMED_UNIT(*)SI_UNIT(.MILLI.,.METRE.));`) are fine,
   but do not let a comment-stripping regex near them: `\(\*.*?\*\)` matches inside
   `NAMED_UNIT(*)` and silently corrupts the unit lines (it did here).
5. Schema strings seen in clean files: `AUTOMOTIVE_DESIGN { 1 0 10303 214 2 1 1}` (wiki/IDA-STEP),
   `AUTOMOTIVE_DESIGN { 1 0 10303 214 1 1 1 1 }` (OCCT writer), our file uses
   `AUTOMOTIVE_DESIGN { 1 0 10303 214 3 1 1 }`; OCCT reads all three without complaint here.

## Caveats and unreachable sources

- 3ds.com (CATIA product pages and 3D Exchange docs) returned HTTP 500 to every path attempted
  from this environment, so CATIA's own supported import/export matrix is asserted only via
  secondary sources (S1, S8, S18). Before relying on a specific translator (e.g. CATIA reading
  JT natively today), confirm on a licensed CATIA install.
- pythonocc.org is currently parked/squatted (unrelated content); use PyPI packages and the docs
  mirror instead (S14).
- `dev.opencascade.org` now 301-redirects to `occt3d.com`, which serves the OCCT user guides
  (S2, S17). Old links in notebooks need updating.
- Forum-grade horror stories (prcforum, eng-tips, reddit) were all blocked (403/307/000). The
  data-loss evidence used here is instead NIST IR 7433 (S6) and the Wikipedia Part 21 criticism
  section (S5).
- FreeCAD-CAD/Cadd workbench (JT/3DXML/CATIA readers) could not be located as a current repo
  (FreeCAD-CAD GitHub path 404, Wayback empty); do not promise CATIA import from FreeCAD.
- JT Open Toolkit home page unreachable from here (sourceforge 403, no Wayback capture). Use OCCT
  JT component (S17) or Siemens' current hosting if JT work starts.

## Appendix A. Minimal valid AP214 file (verbatim from Wikipedia's ISO 10303-21 article, S5;
author Lothar Klein / LKSoft IDA-STEP; OCCT reads it with zero errors)

```step
ISO-10303-21;
HEADER;
FILE_DESCRIPTION(
/* description */ ('A minimal AP214 example with a single part'),
/* implementation_level */ '2;1');
FILE_NAME(
/* name */ 'demo',
/* time_stamp */ '2003-12-27T11:57:53',
/* author */ ('Lothar Klein'),
/* organization */ ('LKSoft'),
/* preprocessor_version */ ' ',
/* originating_system */ 'IDA-STEP',
/* authorization */ ' ');
FILE_SCHEMA (('AUTOMOTIVE_DESIGN { 1 0 10303 214 2 1 1}'));
ENDSEC;
DATA;
#10=ORGANIZATION('O0001','LKSoft','company');
#11=PRODUCT_DEFINITION_CONTEXT('part definition',#12,'manufacturing');
#12=APPLICATION_CONTEXT('mechanical design');
#13=APPLICATION_PROTOCOL_DEFINITION('','automotive_design',2003,#12);
#14=PRODUCT_DEFINITION('0',$,#15,#11);
#15=PRODUCT_DEFINITION_FORMATION('1',$,#16);
#16=PRODUCT('A0001','Test Part 1','',(#18));
#17=PRODUCT_RELATED_PRODUCT_CATEGORY('part',$,(#16));
#18=PRODUCT_CONTEXT('',#12,'');
#19=APPLIED_ORGANIZATION_ASSIGNMENT(#10,#20,(#16));
#20=ORGANIZATION_ROLE('id owner');
ENDSEC;
END-ISO-10303-21;
```

## Appendix B. Hand-written AP214 assembly example (validated, OCCT 8.0.1: RetDone, 1 root,
1 shape, zero errors). Also saved as `example-minimal-assembly.step`.

```step
ISO-10303-21;
HEADER;
FILE_DESCRIPTION(('Minimal AP214 assembly: bracket and plate in one assembly'),'2;1');
FILE_NAME(
/* name */ 'example-minimal-assembly.step',
/* time_stamp */ '2026-09-06T12:00:00',
/* author */ ('Cerebo'),
/* organization */ ('General'),
/* preprocessor_version */ ' ',
/* originating_system */ 'Hand-written AP214 example',
/* authorization */ ' ');
FILE_SCHEMA(('AUTOMOTIVE_DESIGN { 1 0 10303 214 3 1 1 }'));
ENDSEC;
DATA;
/* application context chain */
#1=APPLICATION_CONTEXT('core data for automotive mechanical design processes');
#2=APPLICATION_PROTOCOL_DEFINITION('international standard',
   'automotive_design',2010,#1);
#3=PRODUCT_DEFINITION_CONTEXT('part definition',#1,'design');
#11=MECHANICAL_CONTEXT('','mechanical',#1);
/* units */
#5=(LENGTH_UNIT()NAMED_UNIT(*)SI_UNIT(.MILLI.,.METRE.));
#7=(PLANE_ANGLE_UNIT()NAMED_UNIT(*)SI_UNIT($,.RADIAN.));
#9=(NAMED_UNIT(*)SI_UNIT($,.STERADIAN.)SOLID_ANGLE_UNIT());
#6=(GEOMETRIC_REPRESENTATION_CONTEXT(3)
   GLOBAL_UNCERTAINTY_ASSIGNED_CONTEXT((#8))
   GLOBAL_UNIT_ASSIGNED_CONTEXT((#5,#7,#9))
   REPRESENTATION_CONTEXT('',''));
#8=UNCERTAINTY_MEASURE_WITH_UNIT(LENGTH_MEASURE(0.000001),#5,'','');
/* products: assembly, bracket, plate; attribute order id, description, formation, context */
#20=PRODUCT('ASM001','assembly','',(#11));
#21=PRODUCT_DEFINITION_FORMATION_WITH_SPECIFIED_SOURCE('1','',$,#20,
   .NOT_KNOWN.);
#22=PRODUCT_DEFINITION('ASM001','',#21,#3);
#23=PRODUCT('BRK001','bracket','',(#11));
#24=PRODUCT_DEFINITION_FORMATION_WITH_SPECIFIED_SOURCE('1','',$,#23,
   .NOT_KNOWN.);
#25=PRODUCT_DEFINITION('BRK001','',#24,#3);
#26=PRODUCT('PLT001','plate','',(#11));
#27=PRODUCT_DEFINITION_FORMATION_WITH_SPECIFIED_SOURCE('1','',$,#26,
   .NOT_KNOWN.);
#28=PRODUCT_DEFINITION('PLT001','',#27,#3);
/* assembly structure: NAUO links parent PD to child PD, placement rides on the NAUO PDS */
#30=NEXT_ASSEMBLY_USAGE_OCCURRENCE('nauo1','bracket in assembly','',
   #22,#25,$);
#39=NEXT_ASSEMBLY_USAGE_OCCURRENCE('nauo2','plate in assembly','',
   #22,#28,$);
#31=PRODUCT_DEFINITION_SHAPE('','',#22);
#32=PRODUCT_DEFINITION_SHAPE('','',#25);
#40=PRODUCT_DEFINITION_SHAPE('','',#28);
#41=PRODUCT_DEFINITION_SHAPE('','',#30);
#42=PRODUCT_DEFINITION_SHAPE('','',#39);
/* shape representations: placements only, no B-rep geometry in this example */
#34=AXIS2_PLACEMENT_3D('placement',#35,#36,#37);
#35=CARTESIAN_POINT('',(0.,0.,0.));
#36=DIRECTION('',(0.,0.,1.));
#37=DIRECTION('',(1.,0.,0.));
#43=AXIS2_PLACEMENT_3D('placement',#44,#45,#46);
#44=CARTESIAN_POINT('',(50.,0.,0.));
#45=DIRECTION('',(0.,0.,1.));
#46=DIRECTION('',(1.,0.,0.));
#48=SHAPE_REPRESENTATION('asm_shape',(#34),#6);
#49=SHAPE_REPRESENTATION('bracket_shape',(#34),#6);
#50=SHAPE_REPRESENTATION('plate_shape',(#43),#6);
#51=SHAPE_DEFINITION_REPRESENTATION(#31,#48);
#52=SHAPE_DEFINITION_REPRESENTATION(#32,#49);
#53=SHAPE_DEFINITION_REPRESENTATION(#40,#50);
#54=CONTEXT_DEPENDENT_SHAPE_REPRESENTATION(#55,#41);
#55=REPRESENTATION_RELATIONSHIP_WITH_TRANSFORMATION('rr1','',
   ITEM_DEFINED_TRANSFORMATION('',#34,#34),#49,#48);
#56=CONTEXT_DEPENDENT_SHAPE_REPRESENTATION(#57,#42);
#57=REPRESENTATION_RELATIONSHIP_WITH_TRANSFORMATION('rr2','',
   ITEM_DEFINED_TRANSFORMATION('',#34,#43),#50,#48);
#58=PRODUCT_RELATED_PRODUCT_CATEGORY('assembly','',(#20));
#59=PRODUCT_RELATED_PRODUCT_CATEGORY('component','',((#23,#26)));
ENDSEC;
END-ISO-10303-21;
```

Validation log (fresh process per file):

```
$ python3 -c "
from OCP.STEPControl import STEPControl_Reader
r=STEPControl_Reader()
print(r.ReadFile('example-minimal-assembly.step'))
print('roots',r.NbRootsForTransfer(),'transferred',r.TransferRoots(),'shapes',r.NbShapes())"
IFSelect_ReturnStatus.IFSelect_RetDone
roots 1 transferred 1 shapes 1
(no error lines)
```

## Raw sources (all fetched 2026-09-06 unless noted)

- S1. STEP Tools, "What is STEP?" https://www.steptools.com/stds/step/ ; AP list page
  https://www.steptools.com/stds/step_2.html ; GD&T page
  https://www.steptools.com/stds/step_3.html ; overview "Nearly every major CAD/CAM system now
  contains a module to read and write STEP AP's"; STEP AP242 "was published in 2014"; NIST figure
  "cost the industry $90 billion a year" for data incompatibility (quotes per fetch). Also
  https://www.steptools.com/stds/step/step_1.html. Local copies: `/tmp/raw/step1.html`,
  `/tmp/raw/step3.html`.
- S2. Open CASCADE Technology, STEP Translator User Guide, via occt3d.com (redirect target of
  dev.opencascade.org): "Open CASCADE Technology: STEP Translator"; quotes used: reads AP214 CC2,
  "STEP Application Protocol 203 and some parts of AP242 are also supported", writes "STEP AP 203
  or AP 214 (Conformance Class 2)", `write.step.schema`, "assembly structure is recognized by
  NEXT_ASSEMBLY_USAGE_OCCURRENCE entities", "Only geometrical, topological STEP entities (shapes)
  and assembly structures are translated by the basic translator". Local: `/tmp/raw/occ_step.html`.
- S3. STEP Tools AP242/GD&T page (same fetch as S1): AP242 replaces AP203e2/AP214.
- S4. stepcode (formerly NIST STEP Class Library), GitHub README,
  https://github.com/sjames1958gm/stepcode or upstream: "generates C++ and Python from EXPRESS"
  (10303-11) and is "capable of reading and writing STEP Part 21 exchange files"; also Parts 22
  and 23 (SDAI). Local: fetched via webfetch.
- S5. Wikipedia, "ISO 10303-21" https://en.wikipedia.org/wiki/ISO_10303-21 , Criticism section
  (sequential reads; "assigning an RGB color code to an edge requires at least 6 other entities";
  multiple encodings of one triangle; "specification ... is not freely available") and the minimal
  AP214 example by Lothar Klein (LKSoft IDA-STEP) reproduced in Appendix A. Local:
  `/tmp/raw/wiki_ISO_10303-21.html`, `/tmp/raw/wiki_min.stp`.
- S6. NIST IR 7433 (Kim, Pratt, Iyer, Sriram, 2007), "Use of open-standard STEP data in digital
  manufacturing", https://nvlpubs.nist.gov/nistpubs/Legacy/IR/nistir7433.pdf (Wayback
  20250429201230): "standards for CAD data exchange ... were restricted to the exchange of pure
  shape information. These standards ignored the parameters, constraints, features, and other
  elements of 'design intent'"; "(e) Numerical Accuracy: Differences in the internal numerical
  accuracy of CAD systems was a major early cause of problems in the STEP-based exchange of B-rep
  models ... two points that are judged to be coincident by one system may have separate
  locations in another ... inconsistency between the geometry and the topology". Local:
  `/tmp/raw/nistir7433.pdf`, text `/tmp/raw/nistir7433.txt`.
- S7. STEP Tools AIM schema reference (free, entity-level):
  `https://www.steptools.com/stds/stp_aim/html/t_product_definition.html`
  (`id; description: OPTIONAL text; formation; frame_of_reference: product_definition_context`),
  `t_item_defined_transformation.html`, `t_next_assembly_usage_occurrence.html`,
  `t_product_related_product_category.html`. And ST-Developer comment dialect example:
  https://raw.githubusercontent.com/stepcode/stepcode/develop/test/p21/comments.p21 (header
  `/* Generated by software containing ST-Developer from STEP Tools, Inc. (www.steptools.com) */`).
  Local: `/tmp/raw/st_*.html`, `/tmp/raw/comments.p21`.
- S8. Wikipedia, "JT (visualization format)",
  https://en.wikipedia.org/wiki/JT_(visualization_format) : "In 2012 December, JT has been
  officially published as ISO 14306:2012 (ISO JT V1)"; "Main difference between V1 and V2 is the
  incorporation of a STEP B-rep as an additional B-rep segment"; JTIAP "LZMA ... specifies XT B-rep
  as recommended representation"; automotive OEM recommendation of STEP AP242 XML/JT. Local:
  `/tmp/raw/wiki_JT__visualization_format_.html`.
- S9. Wikipedia, "3DXML": "zip archive file that contains a BOM file and one or more 3D
  representation files"; "The surface data is stored as Gregory patches"; "Dassault Systèmes
  provides a yearly royalty free license to anyone requesting the 3DXML format documentation. This
  license however only permits internal works". Local: `/tmp/raw/wiki_3DXML.html`.
- S10. Wikipedia, "IGES": "exchange product data models in the form of circuit diagrams, wireframe,
  freeform surface, boundary (B-rep) or solid modeling (CSG)"; "After the initial release of STEP
  (ISO 10303) in 1994, interest in further development of IGES declined, and Version 5.3 (1996)
  was the last published standard." Local: `/tmp/raw/wiki_IGES.html`.
- S11. Wikipedia, "ISO 10303": "AP242 edition 2, published in April 2020, extends edition 1 domain
  by the description of Electrical Wire Harnesses and introduces an extension of STEP modelisation
  and implementation methods based on SysML ... optimized XML implementation method"; new features
  list "curved triangles, textures, levels of detail (LODs), color on vertex, 3D scanner data
  support, persistent IDs on geometry, additive manufacturing". Local: `/tmp/raw/wiki_ISO_10303.html`.
- S12. Wikipedia, "ISO 10303", AP242 intro: replaces AP203 and AP214, surface/geometric model + PMI
  (as used in the JT context for hybrid representation). Local as S11.
- S13. glTF 2.0 specification, Khronos registry, https://registry.khronos.org/glTF/specs/2.0/glTF-2.0.html :
  "glTF is not an authoring format. glTF deliberately does not retain 3D authoring information, in
  order to preserve runtime efficiency". Local: `/tmp/raw/gltf.html`.
- S14. pythonocc / cadquery-ocp via context7 docs for pythonocc-documentation and cadquery:
  STEPControl_Writer write pattern, `Interface_Static.SetCVal("write.step.schema","AP214IS")`;
  `importStep(path, unit="M")`, `assy.export("out.stp")`, export modes `fused/async`. Verified
  against `cadquery-ocp` 8.0.1 installed locally (OCP namespace, Python 3.14).
- S15. CadQuery GitHub/docs (context7): `importStep`/`exportStep` round trip, units.
- S16. FreeCAD wiki "Import/Export" (Wayback 20201124212706 of wiki.freecadweb.org/Import_Export):
  table rows for `.stp` and `.stpz`, `.iges/.igs`, `.brep` (import and export both directions; no
  JT/3DXML/CATIA in the base table). Local: `/tmp/raw/freecad_importexport.html`.
- S17. occt3d.com "JT Exchange" component page (meta description): "Read a JT file into a JT model,
  write a JT model into a JT file ... with the use of Open Cascade JT Import-Export". Local:
  `/tmp/raw/occ_jt_comp.html`.
- S18. Tech Soft 3D Spinfire Convert (Theorem Solutions technology) product page: translation
  solutions covering "3DEXPERIENCE, CATIA V5, CREO, JT and NX ... STEP ... SOLIDWORKS". Local:
  `/tmp/raw/spinfire.html` (fetched from techsoft3d.com).
- S19. Validation log: this session's OCCT tests (`OCP.STEPControl.STEPControl_Reader`) over the
  example files and micro-tests described in Practical notes; outputs quoted inline. Files under
  `/tmp/raw/` (`s_*.stp`, `c_*.stp`, `w_*.stp`, `z_*.stp`, `wiki_min.stp`, `occt_gen.stp`,
  `comments.p21`, `bis_*.stp`).
- S20. PDES Inc, "What is STEP?" https://pdesinc.org/step/ (general positioning, computer-sensible
  product data). Local: `/tmp/raw/pdes_step.html`.
- S21. prostep IVICoT homepage, https://www.prostep.org/en/ (industry consortium behind STEP/JT
  adoption; IP/licensing pages only as e-papers). Local: `/tmp/raw/prostep_en.html`.
