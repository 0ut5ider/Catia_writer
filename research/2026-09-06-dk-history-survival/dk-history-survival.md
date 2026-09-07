# Can Datakit-fed CAD become an editable CATIA V5 model with history?

Date: 2026-09-06/07. Agent: Cerebo (opencode research session). Question from Adrian:
programmatic CAD sources converted toward CATIA V5. The deliverable must be editable with
history and sketches, not a dumb B-rep. Does any format-based route deliver that, what is
the real ceiling, and what are the fallbacks?

Verdict and fallbacks first. Raw quotes and files: `raw/evidence-notes.md` and the raw
directory beside it.

## Verdict

No format converter puts a live feature tree into a CATPart. This is structural, not a
quality gap in Datakit.

- A feature tree is private, versioned data inside the target CAD's container, editable
  only through the target CAD's own API. Translators write geometry (B-rep or mesh),
  assembly structure, PMI, and metadata into the target container. They do not reconstruct
  parametric operations, because those exist only in the source's semantics and map to
  target ops one kernel at a time.
- The only shipped bridges that touch CATIA feature semantics run inside a licensed CATIA
  install. Theorem's CATIA-to-JT page is explicit: it "has been developed using the Dassault
  Systems CATIA V5 CAA Development Environment and therefore is integrated within an
  existing licensed CATIA V5 installation," and CATIA products "require access to a V5
  license in order to run."
- Datakit's CATIA V5 writer proves the inverse. CrossManager writes .CATPart for versions
  "R14, R19, R20, R21 & V5-6R2012 to V5-6R2026" and "does not require an external licence."
  A writer that never opens CATIA cannot emit CATIA history objects. Its output is a valid,
  geometry-complete CATPart: editable in the sense that you can add features on top, not
  editable in the sense of an upstream sketch/pad tree.
- Where the history actually lives: in your generator. The sources are programmatic, so the
  parametric intent already exists as code. That reframes the problem. The route to a
  native CATIA tree is replaying that intent through CATIA's automation API, not feeding
  files to a translator.

Confidence: high on the ceiling (vendor pages, quotes in evidence-notes.md). Medium on the
exact contents of Datakit's "Extraction and writing of ... feature data" line, since it
reads as an SDK read-side capability. One email to Datakit closes that gap. See Open
questions.

## The ceiling, per route

| Route | Best realistic CATIA V5 result | History? |
|---|---|---|
| Datakit CrossManager/SDK STEP/Parasolid → CATIA V5 | Valid CATPart, B-rep bodies, assembly tree, metadata/PMI | No |
| Theorem CADTranslate (CAA) NX/Creo/SolidWorks → CATIA | Named features in the tree for supported pairs, runs inside CATIA with a local V5 license | Partially, for supported pairs; source must itself carry a feature tree |
| CATIA-native STEP AP242 import, FreeStyle/DMU reconstruction | Geometry plus recognized features where reconstruction succeeds | Lossy reconstruction |
| pycatia/CAA replay of the generator's own operations | Native sketch/pad/pattern tree, created by CATIA | Yes, fully |
| JT/3DXML/PLM XML as carriers | Geometry, PMI, semantics; CATIA reads PMI | No tree from these |

## Ranked fallbacks

Ranked as Adrian's rules require: dependency order, verification difficulty, subtle-bug
risk, blast radius. Not by effort.

1. Replay the build inside CATIA (pycatia or CAA). Emit a replay script from the same
   program that emits the B-rep: sketches, pads, pockets, patterns, via CATIA's automation
   API. The tree is native because CATIA builds it; no translator is in the loop.
   Verification is easy: open the part and edit a parameter. Risk concentrates in API
   coverage for exotic geometry (B-spline lofts, surface ops), where the fallback is
   build-that-piece-as-dumb-brep and feature the rest.
2. If, and only if, the real sources turn out to be native CAD files with their own trees,
   a vendor bridge that runs inside CATIA (Theorem-style CAA, or Dassault's own exporters).
   Needs a local CATIA license per seat. It cannot help pure programmatic sources, which
   have no source tree to translate.
3. CATIA-side feature recognition on the imported B-rep (FreeStyle, Generative Shape
   Editor, design reconstruction). Lossy and interactive. Treat it as cleanup for the
   pieces route 1 cannot replay, not as a pipeline.
4. Semantic-carrier experiment: write PMI/PLM XML or STEP AP242 semantics from the
   generator, ask Dassault and Datakit in writing whether any import reconstructs
   features. Unverified as of 2026-09-07; it is cheap to ask and cheap to test.
5. Accept the dumb CATPart. Editable as a downstream shape: added features, boolean
   operations, measurements all work; only the upstream tree is gone. This is the floor,
   not a goal.

Route 1 is the recommendation because it is the only one that converts the thing you
already have (parametric intent in code) into the thing you want (a native CATIA tree),
and it is the only one verifiable in minutes on a real part.

## 30-minute test plan

1. Datakit offers a CrossManager trial (account/test_licenses.php). Convert one STEP to
   CATPart, open in CATIA, inspect the specification tree. Expect: bodies, no features.
   This confirms or kills the whole format route in one sitting.
2. pycatia proof of concept: one sketch, one pad, one dimension change, re-run. Expect a
   green tree that replays. This confirms the recommended route.
3. One email to Datakit with the exact question: "Does the CATIA V5 write module ever emit
   feature/history objects, or only B-rep and metadata?" Their answer settles the last
   ambiguity.

## Open questions

- Datakit's "Extraction and writing of ... PMI and feature data" sentence: which formats
  accept written feature data? Their marketing does not say CATIA history; ask them.
- CATIA V5's own FreeStyle-to-solid reconstruction quality on representative parts is
  undocumented here. Doc fetches failed; it needs a hands-on test, not a citation.
- STEP AP242 managed model subtypes and PLM XML feature semantics: whether any CATIA
  import path materializes them is unverified.

## Dead ends and blocks

- XCAD: the classic "preserves design history" story. xcad.com has no DNS A record,
  webfetch returns Transport error, Wayback shows 1 KB telecom-era pages. theorem.com
  redirects to Tech Soft 3D and its acquisition FAQ lists no XCAD. The product line
  appears defunct; nothing to buy.
- TransMagic: curl 200 with zero bytes, no fetchable claims. Not evaluated.
- Search engines all blocked for this session: DuckDuckGo bot challenge, Mojeek captcha,
  SearxNG anti-bot, Google empty via curl, Bing irrelevant. StackOverflow via API returned
  zero hits for the feature-tree queries; direct question pages 403. Findings rest on
  vendor pages and archives, which is the right source class for capability claims anyway.
- The guessed HOOPS Exchange feature-tree doc URL 404'd on recheck; the read-side-only
  claim about Exchange is marked as inference in evidence-notes.md.

## Files

- Final report: `docs/agents/2026-09-06-dk-history-survival/dk-history-survival.md` (this file).
- Raw evidence: `docs/agents/2026-09-06-dk-history-survival/raw/evidence-notes.md` plus
  archived Theorem HTML (key file `catia_v5_to_jt.html`, 85 KB, CAA/license quote).
