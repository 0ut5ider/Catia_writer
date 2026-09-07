# CATIA V5 Interop Without Reverse Engineering: Legal Routes and Risks

- Date: 2026-09-06
- Role: legal-research agent (opencode / Cerebo)
- Question asked: what are the legally authorized or low-risk routes to producing CATIA V5
  `.catpart`/`.catproduct` files, and what is the risk profile of pure reverse engineering?
- Model: claude (session model per harness)
- Status: research only. **Not legal advice.** This is a US/EU research memo for engineering
  planning, not an opinion of counsel.

---

## 1. Executive summary

Routes, ranked from lowest to highest residual legal risk:

1. **Licensed SDK route (lowest risk).** License Dassault's own interoperability components.
   Spatial (a Dassault subsidiary) sells **3D InterOp**, whose published capability statement is:
   native read/write of `CATPart`/`CATProduct` "without needing a CAD license"
   (verified live, spatial.com, 2026-09-06). This is the sanctioned, commercialized format-access
   channel: you pay for the parser, you ship a writer, you never reverse engineer anything.
2. **CAA component route (low risk, narrow).** Dassault licenses **CAA (Component Application
   Architecture)** as a "Development Tool Kit" under its Licensed Programs Terms. A CAA license
   lets you write code against CATIA's APIs. You must be a licensed CAA developer; distribution
   of components is governed by the CAA agreement. This produces files *through* CATIA rather
   than standalone writers.
3. **Interoperability-research route (medium risk).** Write your own writer by analyzing
   `.catpart` files you lawfully generated with a licensed copy of CATIA. Risk concentrates in:
   (a) the EULA's reverse-engineering ban (breach-of-contract exposure, verified verbatim below),
   (b) trade-secret exposure (mitigated if you only inspect files, not the program), and
   (c) US copyright fair-use posture is favorable under `Sega`/`Connectix` reasoning *for the
   analysis step*, but contract overrides fair use as a defense to breach in most US circuits
   (`Bowers v. Baystate`, Fed. Cir. 2003).
4. **Unsupervised clean-room reverse engineering (medium-high risk).** Same as 3 plus
   process discipline; still does not cure a contract breach if your "clean room" team ever
   signed the EULA or ran CATIA bound by it.
5. **Decompiling the CATIA program itself (highest risk).** The current Dassault/3DS EULA bans it
   by name, bans publishing benchmarks, and the Licensed Programs Terms add an anti-defeat clause
   for license/security mechanisms. DMCA §1201(f) *would* shelter circumvention done for
   interoperability analysis, but the EULA breach and trade-secret claims remain, and the EU
   decompilation right (Directive Art. 6) covers *programs*, not file formats.

What `.catpart` most likely is, legally: a **data file**. Ideas, principles, and interface
specifications embodied in a data format are not copyrightable (US: §102(b), `Atari v. Oman`
line; EU: `SAS v. WPL`, C-406/10, verified). The likely legal hooks are **contract** (the EULA)
and **trade secret**, not copyright or the DMCA. There is no TPM on an ordinary `.catpart`, so
§1201 anti-circumvention likely never engages at all.

---

## 2. The contract layer (verified primary sources)

### 2.1 Current 3DS EULA text (verified live 2026-09-06)

Source: `https://www.solidworks.com/support/license-agreement-ela` (HTTP 200). This is the
3DEXPERIENCE-era "3DS Offering" license agreement text that DS uses group-wide (SolidWorks is
DS; the CATIA-side agreement is the same template family: "3DS Offering", "Licensed Program",
"Online Services"). Verbatim clause:

> "Except to the extent permitted by applicable law, Customer shall not modify, adapt, reverse
> engineer, decompile, disassemble or otherwise translate all or part of any 3DS Offering, and
> shall not provide, disclose or transmit any results of tests or benchmarks related to any 3DS
> Offering to any third party."

Two separate obligations here, note:

- The RE/decompilation ban is softened by **"Except to the extent permitted by applicable law"**
  (which is what an Art. 6 decompilation right or a fair-use `§1201(f)`-style analysis leans on).
  US courts generally still enforce such clauses as contracts even where copyright law would
  permit the act (`Bowers v. Baystate`, §3.8 below).
- A **benchmark-results gag**. Converter vendors that publish "round-trip comparison vs CATIA"
  test data create independent breach exposure. Flag for marketing.

3DS retains "ownership in all intellectual property rights in all 3DS Offerings and all
modifications, or other derivative works thereof." (Same source, §4.)

### 2.2 CATIA-specific Licensed Programs Terms, LPT (verified via archived official PDF)

Source: `https://www.3ds.com/assets/Terms/LicensedProgramTerms/CATIA/CATIAuptoV5R20.pdf`
(DS's own hosted file, retrieved through Wayback `2023id_` snapshot; document footer:
"DS LPT - CATIA up to Version 5 Release 20 - April 2010"). Key provisions, verbatim in effect:

- **Deliverables / services clause ("USE FOR CERTAIN SERVICES").** Licensee may use CATIA to
  deliver to third-party end users "any deliverable generated specifically for said third party
  end user" (added-value engineering services). But Licensee "may not... use the Licensed
  Programs to develop software code for... general distribution" except through Development
  Tool Kits. Practical reading: **output files created in CATIA are yours to deliver; using
  CATIA as a code-development oracle for a shippable product is a contract breach.**
- **Outsourcing clause.** Third parties may operate licensed CATIA for you only if they are
  bound in writing to the license restrictions AND "such third party is not a competitor of any
  DS Group Company." A converter house is plausibly a competitor; contract-out translation-test
  infrastructure carefully (internal control, not an offshore BPO of your license).
- **Security mechanisms clause.** "Licensee may not take any steps to avoid or defeat the
  purpose of any such measures", covering license keys/administration software. This is the
  contractual anti-circumvention hook that reaches tools like floating-license spoofers. It
  does not naturally reach a `.catpart` data file (the file is not the license mechanism), but
  it is why you never touch the licensing stack itself.
- **No certification claims.** Licensee may not "represent or imply to any party that it is an
  authorized or certified provider of services for DS". Relevant to marketing a "CATIA
  compatible" product.

### 2.3 What we could NOT locate (honesty log)

- The live text of the umbrella "**Product Portfolio Terms and Conditions**" (PPTC) and the
  "**Common License and Installation Manual (CLIM)**" as a PDF are no longer publicly hosted.
  Wayback captures of `3ds.com/3ds/terms/*` are 404 snapshots; the live `3ds.com/terms` hub is a
  JS shell whose data endpoints returned 404/500 to direct probes. The SolidWorks-hosted group
  EULA (§2.1) is the best public proxy; assume the CATIA-side PPTC contains materially the same
  RE-ban and benchmark-gag language (identical defined terms).
- A current, CATIA-branded CAA license terms PDF is not public (only "CAA" specs sheets:
  `assets/Terms/LicensedProgramSpecifications/CATIA/CAA_V5R{18,19,20}.pdf`, fetched, contain
  only system requirements). Glossary Release 1 (fetched, official PDF) defines **Development
  Tool Kit** = Licensed Program "specifically designed for application or content development...
  identified with 'CAA' or 'ENOVIA Studio'". CAA terms are delivered through the sales channel.

### 2.4 The Spatial / 3D InterOp route (verified live)

- `https://www.spatial.com/solutions/cad-translation/3d-interop` (HTTP 200, 2026-09-06):
  3D InterOp "uses the CGM kernel and native APIs to read/write CATPart and CATProduct from
  CATIA and SolidWorks metadata **without needing a CAD license**." Spatial is a Dassault
  Systèmes subsidiary selling this as embedded C++ components (per-component royalty/licence).
  Glossary pages for `catpart` exist across languages under `spatial.com/glossary/...`.
- This *is* what "format licensing" looks like at Dassault: you license **the code that speaks
  the format**, not a paper format license. There is no public "CATIA format license program"
  or "CATIA compatible logo program"; no evidence either exists (zero verified hits; absence
  reported honestly).
- Practical implication: a converter vendor can embed 3D InterOp for CATIA I/O and stay fully
  authorized; the cost is per-seat/royalty economics and a dependency on the DS ecosystem for
  format updates.

---

## 3. US copyright and interoperability case law (citations verified via CourtListener API
unless flagged)

3.1 **Sega Enters. Ltd. v. Accolade, Inc., 977 F.2d 1510 (9th Cir. 1993)** (CL id-verified;
opinion 1992-10-20, amended 1993-01-06). Disassembly of object code to discover unprotected
functional requirements (interfaces) can be fair use where disassembly is the only way to get
them. Foundational support for: analyzing a locked interface by machine inspection is fair use
when the goal is unprotectable interoperability facts.

3.2 **Sony Computer Ent. v. Connectix, 203 F.3d 596 (9th Cir. 2000)** (verified). Intermediate
copies made to study/analyze unprotectable elements weigh toward fair use, especially
transformative final product. Cert. denied 531 U.S. 871 (2000) (verified).

3.3 **Sony Computer Ent. v. Bleem, 214 F.3d 1022 (9th Cir. 2000)** (verified). Adjacent
(ads/screenshots), but confirms the Ninth Circuit's tolerance for emulators at the time.

3.4 **Vault Corp. v. Quaid Software, 847 F.2d 255 (5th Cir. 1988)** (verified). §117 + misuse:
a shrinkwrap clause banning reverse engineering was preempted where it blocked analysis of an
uncopyrightable-as-such protection scheme. Important counterweight to §3.8, but its preemptive
logic is generally limited to uses copyright law affirmatively protects; post-DMCA courts have
narrowed Vault's reach (compare §3.6-3.7).

3.5 **Atari Games v. Nintendo, 975 F.2d 832 (Fed. Cir. 1992)** (verified). Clean-room doctrine
by negative example: Atari's teams improperly obtained Nintendo's source code from the Copyright
Office via a false patent-office representation; infringement judgment and loss of any
interoperability defense. Also **Atari Games v. Oman, 979 F.2d 242 (D.C. Cir. 1992)** (verified)
on Copyright Office deposit rules. Related: **Atari v. Nintendo, 897 F.2d 1572 (Fed. Cir. 1990)**
(verified).

3.6 **Chamberlain v. Skylink, 381 F.3d 1178 (Fed. Cir. 2004)** (verified; cert. denied 544 U.S.
923 (2005), verified). §1201 requires showing the access enabled by circumvention led to
infringement of a *copyrighted work*; a license key controlling access to a garage door opener
was not a §1201 violation absent an infringement nexus. Why DMCA-over-data-file claims fail
against honest interop: the file/data itself is usually unprotectable or licensed-by-sale.
(Superseded in part by later §1201 case law but the nexus requirement survives.)

3.7 **MDY Indus. v. Blizzard, 629 F.3d 928 (9th Cir. 2010)** (verified). Distinguishes
"access" controls vs "use" controls under §1201(b); bot program evading a game's client check
was circumvention of an access control to *the game* with sufficient nexus to code copies. If a
file format ever had an access-control wrapper (e.g., CATIA encrypted-save), MDY-style analysis
would govern; for plain `.catpart` there is no access control to defeat.

3.8 **Bowers v. Baystate Techs., 320 F.3d 1317 (Fed. Cir. 2003)** (verified). Contract banning
reverse engineering is enforceable **in addition to** patent/copyright rights; patent misuse
counterargument rejected. The controlling warning: fair use / Sega rights do **not** excuse
contractual RE-bans where you agreed to the contract. (See also ProCD below for enforceability
of shrinkwrap-style terms.)

3.9 **ProCD v. Zeidenberg, 86 F.3d 1447 (7th Cir. 1996)** (verified). Shrinkwrap/license terms
accepted post-purchase are enforceable; clickwrap and install-time EULAs follow. Assume a
CATIA EULA in a converter shop will bind even if "accepted" by a procurement clerk clicking.

3.10 **Davidson & Assocs. v. Jung, 422 F.3d 630 (8th Cir. 2005)** (citation verified; note:
CourtListener metadata mislabels the court as First Circuit; the same docket family includes
Davidson & Assocs. v. Internet Gateway, 8th Cir.). Users bound by click-through "no reverse
engineering" clause; breach enforced. Pattern: EULA RE-bans get enforced per ProCD/Bowers.

3.11 **Meshwerks, Inc. v. Toyota Motor Sales (10th Cir. 2008)** (verified, **528 F.3d 1258**;
earlier 509 F.3d 1163). **Correction to the task brief: the defendant was Toyota, not Ford.**
Holding: a 3D CAD model that is a faithful reproduction of a car carries (nearly) no original
expression and gets no meaningful copyright protection. Supports the position that **CAD data
of utilitarian objects is thin-copyright territory**, so the danger in data files is contract
and secrets, not copyright.

3.12 **Kewanee Oil Co. v. Bicron Corp., 416 U.S. 470 (1974)** (verified). Trade secret law is
not preempted; but the doctrine itself (and every state DTSA-adopted statute) holds that
information **derived from lawful reverse engineering of a product available on the market is
not misappropriated**. The catch for us: you can only "reverse engineer" what you lawfully
received, and if the receipt was conditioned on a no-RE contract, the misappropriation analysis
gets contaminated by contract claims.

3.13 **Apple Inc. v. Corellium, LLC** (11th Cir. 2022, affirming E.D. Va. jury verdict for
Corellium on fair use/DMCA): **could not be verified in this session** (CourtListener returned
zero hits for "Corellium" and no Wikipedia article exists; treat as reported but
unverified here). It *would* be the most on-point modern authority: building interoperable
virtualization from licensed ownership of the OS, with fair use covering the analysis copies.
Recommend counsel re-verify the citation (reported at 2022 WL ...) before relying on it.

3.14 **Apple Inc. v. Roese, 2d Cir. 2020** (as named in the task brief): **not found and
treated as unverified / probably mis-cited.** Searched: CourtListener opinions API (all courts,
court=ca2, reporter=F.4th/F.3d/Fed.Appx, case_name), CourtListener RECAP dockets, Wikipedia
search API, Internet Archive full-text search, OpenAlex. Zero hits for any Apple case captioned
"Roese". Do not cite it. If the underlying memory is "interoperability + fair use + Apple +
recent", the real cases are Apple v. Corellium (11th Cir. 2022, itself unverified here) or the
2d Cir.'s older Corley (Universal v. Reimerdes, 273 F.3d 2, 2001, verified by existence in
CL) which went the *other* way on §1201.

---

## 4. DMCA §1201 applied to `.catpart`

- **§1201(f) (reverse engineering) text verified** via Cornell LII `uscode/text/17/1201`
  (fetched 2026-09-06, verbatim (f)(1)-(3) extracted). (f)(1) allows a person who lawfully
  obtained the right to use a copy of a *computer program* to circumvent a TPM for the sole
  purpose of identifying/analyzing elements necessary to achieve **interoperability of an
  independently created computer program**, to the extent not infringing; (f)(2)/(f)(3) permit
  trafficking in the circumvention means when the sole purpose is enabling that analysis, or
  selling the interoperable product.
- The predicate act of §1201(a)(1) is **circumventing a technological measure that effectively
  controls access to a work**. An ordinary `.catpart` is a data file with a proprietary
  internal structure, not access-controlled. There is no TPM, so no §1201(a) hook. §1201(a)(2)/
  (b) (trafficking) are parasitic on circumvention, so they also fail.
- Where §1201 *could* engage: DS's **license administration / encryption features** (the LPT's
  "security mechanism" clause corresponds to real features: hardware locks, license keys,
  and encrypted/obfuscated storage). Defeating a license server check or an encryption-on-save
  protection is a §1201(a) access-control violation with real nexus (MDY/Corley framework), and
  no exemption covers commercial converter development.
- **Triennial rulemaking (1201(c)): corrected record.** The task brief said "37 C.F.R. §201.60".
  As of the eCFR snapshot of 2025-01-01 for Title 37 Part 201 (fetched via `ecfr.gov` API,
  verified), the classes are codified at **§201.40**, not §201.60 (there is no §201.60).
  Classes of interest, from the verified §201.40(b) list:
  - (8)-(12) device-software compatibility (phones, tablets, smart TVs, voice assistants,
    routers) - run apps; none touch CAD.
  - (13)-(17) maintenance/repair of lawfully acquired machines (motor vehicles, agricultural
    machinery, medical devices, wheelchairs): *diagnose, repair, or maintain* - this is where a
    hypothetical "unlock a machine controller" problem lives, not CAD writers.
  - (18) good-faith **security research** (accessing a computer to test with investigation and
    good-faith investigation/analysis; 2021/2024 additions).
  - (19)-(20) video-game preservation / library archival of programs.
  - **There is no general "interoperability" circumvention class.** None of the current classes
    exempts breaking a protection to write a CAD file. Conclusion: the §1201 exemption route
    is irrelevant here because §1201 itself is inapplicable to the file; do not rely on it.
- Practical rule: the analysis of `.catpart` bytes never requires circumvention, so §1201 is a
  non-issue *unless* your engineers also break the licensing stack "to understand" something.
  Keep it that way.

## 5. EU law: Directive 2009/24/EC (verified EUR-Lex full text, `CELEX:32009L0024`)

- **Art. 6 (decompilation), verbatim extracted.** The reproduction/translation right does not
  require authorisation where indispensable "to obtain the information necessary to achieve the
  interoperability of an independently created computer program with other programs",
  provided: (a) done by the licensee or a person having a right to use a copy (or on their
  behalf); (b) the information has not previously been readily available; (c) confined to the
  parts of the **original program** necessary. Paragraph 2: the information obtained may not be
  used for goals other than interoperability, given to others except as necessary, or used to
  develop/produce/market a program substantially similar in expression. Para. 3: three-step test
  (Berne).
- **The critical limit:** Art. 6 speaks of reproducing/ translating "the code" of **a program**.
  A `.catpart` is **data**, not a program. The Directive protects computer *programs* (Art. 1);
  its decompilation exception is a right against a program's rightholder. Reading files you
  already possess does not need Art. 6 at all (there is no restricted act in merely reading a
  data file you own); the Directive is simply the wrong shield for format analysis. Conversely,
  **decompiling CATIA's own code in the EU relies on Art. 6 and its strict conditions** (and
  UK equivalents, CDPA §50B(6)/§50BA for EU-retained law; UK analysis not re-verified here).
- **SAS Institute Inc. v World Programming Ltd., C-406/10 (CJEU Grand Chamber, 2012)** (full
  judgment fetched via EUR-Lex, `CELEX:62010CJ0406`): functionality of a computer program and
  programming languages are **not protected by copyright**; copyright in a program protects the
  expression, not the "functionality... nor the programming language nor the file formats" -
  the judgment expressly addresses the inability to monopolize file formats and data structures
  through program copyright. Strong EU support that the format facts in a `.catpart` are not a
  copyrightable asset you infringe by studying the file.
- **Navitaire Inc. v easyJet, [2004] EWHC 1725 (Ch)** (Proudman J): scripts/business rules of a
  reservation system not protected expression. **Not fetched** (BAILII bot-walled; r.jina.ai also
  refused). Cited from the known neutral citation; re-verify at BAILII before use.
- **Contract override:** Art. 5(3)/Recital 15 preserve *specific contractual provisions* on
  observation/study/testing "in contract, free of charge" and Art. 6's conditions are
  mandatory-law floors ("contractual provisions contrary to... decompilation... shall be null and
  void", Recital 16) **only for decompilation of programs**. EU does not give a right to ignore
  the EULA for data files, though an RE-ban that effectively locks out interoperability can
  attract Arts. 101/102 TFEU arguments (Recital 17 says the Directive is without prejudice to
  competition rules where a dominant supplier refuses interface information); DS is not
  obviously dominant, so competition law is a long shot, note honestly.

## 6. Clean-room methodology (what "clean" must mean here)

Verified anchor: **Atari v. Nintendo, 975 F.2d 832** (§3.5) - a "clean room" collapses when the
"clean" team has access to protected material it had no right to (there, deposited source code).
The method itself was implicitly accepted (Atari's own prior "Tenga" effort and the general
framework; see also Atari's *Oman* saga).

Operationally, for this project the discipline is:

1. **Source team** (inspect CATIA, capture format facts): may read `.catpart` files (they are
   yours), run the program to produce outputs, take notes/specs. May NOT receive source code
   dumps, memory dumps of running processes, or DS internal documents, and may NOT write the
   production code.
2. **Spec bridge**: only abstract interface specifications (field names, units, geometry
   semantics, topology relationships) pass the wall, written as functional requirements, never
   as code or transcribed dumps.
3. **Implementation team**: writes the writer from the spec only; never runs CATIA, never
   signs DS EULAs (contract exposure!), ideally staffed by people who never installed CATIA
   under license.
4. **Provenance record**: log every `.catpart` sample: who created it, with which licensed
   installation, when. Samples must be self-generated or from customers with rights to share.
5. **No DS confidential info in training data** if you use any model-based spec extraction:
   no DS docs, no DS code, no support-portal content.
6. **The residual hole (must say so)**: under `Bowers`/`Jung`, contract liability attaches to
   the *person/company bound by the EULA*. If your entire company is a CATIA licensee,
   the source team's very act of inspecting the program internals (not the files) breaches the
   EULA even with a perfect clean room downstream. Clean-room is an **anti-copyright/anti-secret
   device, not an anti-contract device**. The only contract-safe variants: (a) analysis
   confined to data files you generated (arguably outside "reverse engineer the Offering" since
   the file is not the Offering), or (b) a corporate structure where a non-licensee affiliate
   does the analysis (its own risks: single-enterprise/alter-ego arguments).

## 7. Output-file ownership and CAD-data copyright

- **No case law located** that squarely decides who owns a CAD file produced with licensed
  CATIA scripting (Automation API / macro). Absence reported honestly.
- Contract: the LPT (CATIA V5) *contemplates* you generating deliverables for third parties
  (§2.2), implying DS claims no ownership of user output. The ToU/LPT never asserts ownership of
  user data; DS claims rights in "3DS Offerings" and derivative works thereof (the offering's
  own code). Verbatim text on "user data" ownership was not present in the fetched LPT or ToU
  (searched; absent). Flag: the umbrella PPTC (non-public) may add a user-data clause; counsel
  with an actual contract copy should check.
- Copyright in the *data* itself: a `.catpart` containing geometry of a utilitarian object is
  like `Meshwerks` (§3.11): thin to no protection. The format's structural choices are ideas/
  methods (unprotectable, §102(b) analogue; `SAS` in EU). Your independently written writer
  emits the same facts; that is the entire theory of the converter business and it is
  copyright-resilient.
- Trade secrets: geometry facts in any `.catpart` you possess are trade-secret-safe to
  *reproduce* (they are the customer's own designs), and format facts learned by file inspection
  are classic "reverse engineering of a lawfully obtained article" (§3.12). Real secret risk is
  only: CAA/DS-internal specs (from ex-DS employees, leaked docs, or NDA'd portal access), and
  violating the EULA's confidentiality clause while probing. No-employees-with-DS-NDAs rule.

## 8. Mitigation program for converter vendors (the "everyone who sells this" checklist)

1. License 3D InterOp (Spatial) for CATIA read/write if budget allows; that erases steps 2-8.
2. If writing your own: use **your own licensed CATIA seats** only to *generate golden files*,
   keep seat records; never let licensed CATIA be a runtime dependency of your product; never
   ship/sell a product that requires defeating a DS security mechanism (LPT clause §2.2).
3. Clean-room the implementation team from the analysis team (§6), and paper it from day one.
   The record is the product; build the provenance log as you go, not in discovery.
4. Do not decompile the CATIA binary. Program internals are where the EULA ban, §1201 (if any
   TPM is present), and trade-secret claims all bite.
5. Do not publish DS benchmark comparisons (EULA benchmark gag, §2.1).
6. Do not imply DS certification/compatibility endorsement (LPT §2.2; also avoid "works with
   CATIA" logo styling without a program - none was found to exist publicly).
7. Customer-supplied `.catpart` files: obtain rights warranty + indemnity from customer,
   store separately, delete on request (secret-misappropriation hygiene).
8. Get the actual signed CATIA PPTC/EULA reviewed by counsel (the real text is not public; this
   memo's §2.1-2.2 is best-public proxy).
9. EU-facing products: if any program-level decompilation is ever done, document Art. 6
   compliance (indispensability, readily-available, confined scope, information quarantine)
   per-file, in real time.
10. No DS-alumni on format work without clean provenance of their prior NDAs; interview under
    privilege.

## 9. Residual risk table (for planning, not legal opinion)

| Claim theory | File-analysis route (no program RE) | Program decompile route |
|---|---|---|
| Copyright infringement (code) | very low (independent code) | low after Sega/Connectix fair use, **but** |
| Breach of EULA (RE-ban clause) | low-medium (file arguably not "Offering") | high (Bowers/Jung: enforceable) |
| DMCA §1201 | none engaged (no TPM on files) | medium (TPM on program+license) |
| Trade secret (DTSA/UTSA) | low (lawful RE of lawfully obtained article; no DS-internal info) | medium-high (CATIA internals arguably secret; Kewanee protects lawful RE only if no contract taint) |
| Contract: benchmark gag / certification | avoid by conduct | avoid by conduct |

## 10. Honesty and verification log

- **Verified this session (fetched, text extracted):** §2.1 EULA clause (live solidworks.com);
  LPT CATIA V5R20 (Wayback-hosted official PDF, pdftotext); Glossary Release 1 (same);
  Spatial 3D InterOp CATPart/CATProduct claim (live); 17 U.S.C. §1201(f) (LII); 37 CFR Part 201
  2025-01-01 edition (eCFR API; §201.40 classes, no §201.60); Directive 2009/24/EC Arts. 5-6
  (EUR-Lex HTML); SAS C-406/10 judgment (EUR-Lex HTML); case citations Sega, Sony/Connectix,
  Sony/Bleem, Vault, Atari x3, Chamberlain, MDY, ProCD, Bowers, Davidson, Meshwerks, Kewanee
  (CourtListener REST API, unauthenticated).
- **Could not verify:** Apple Inc. v. Roese (task brief's 2d Cir 2020 case; absent from
  CourtListener opinions + RECAP, Wikipedia, Archive.org fulltext, OpenAlex; recommend the
  brief's author re-check the name), Apple Inc. v. Corellium (reported, not found this session),
  Navitaire v easyJet (BAILII bot-walled), live CATIA PPTC/CLIM text (not publicly hosted),
  Dassault "format license program" or "CATIA compatible logo program" (no evidence of either;
  Spatial/CAA are the actual channels).
- **Search infrastructure failures this session (documented for the record):** Google/DDG/
  Mojeek/Ecosia/searx instances/Qwant all bot-walled or captcha; Bing RSS ignored queries;
  Casetext 410s; Wayback full-text API 429s; grep.app 403. Workarounds: CourtListener API,
  Wayback CDX + snapshot fetch, EUR-Lex, LII, govinfo/ecfr APIs, vendor live pages.
- Corrections made against the task brief: (a) Meshwerks defendant is Toyota, not Ford;
  (b) DMCA exemptions are at 37 C.F.R. §201.40 in the current codification, not §201.60;
  (c) Art. 6 Directive decompilation right covers programs, not data file formats.

---

## Appendix A: URLs used (primary evidence)

| Source | URL | Status |
|---|---|---|
| 3DS EULA (SolidWorks-hosted group template) | https://www.solidworks.com/support/license-agreement-ela | 200, text extracted |
| LPT CATIA up to V5R20 (official PDF via Wayback id_) | https://web.archive.org/web/2023id_/https://www.3ds.com/assets/Terms/LicensedProgramTerms/CATIA/CATIAuptoV5R20.pdf | 200, PDF extracted |
| DS Terms Glossary Release 1 (official PDF via Wayback) | https://web.archive.org/web/2023id_/https://www.3ds.com/assets/Terms/Glossary/GLOSSARY-Release1-April2010.pdf | 200, PDF extracted |
| Licensed Program Specifications index (CATIA/CAA specs) | web.archive.org CDX over 3ds.com/assets/Terms/* | 2,412 URLs enumerated |
| Spatial 3D InterOp | https://www.spatial.com/solutions/cad-translation/3d-interop | 200, quoted |
| 3ds.com site ToU (License Agreement reference) | https://www.3ds.com/terms-of-use | 200, extracted |
| 17 U.S.C. §1201 incl. (f) | https://www.law.cornell.edu/uscode/text/17/1201 | 200, (f) extracted verbatim |
| 37 CFR Part 201 (2025 ed.) | https://www.ecfr.gov/api/versioner/v1/full/2025-01-01/title-37.xml?part=201 | 200, §201.40 parsed |
| Directive 2009/24/EC | https://eur-lex.europa.eu/legal-content/EN/TXT/HTML/?uri=CELEX:32009L0024 | 200, Art. 6 verbatim |
| SAS v WPL C-406/10 | https://eur-lex.europa.eu/legal-content/EN/TXT/HTML/?uri=CELEX:62010CJ0406 | 200, verified |
| Case verification | https://www.courtlistener.com/api/rest/v4/search/?... (queries in §3) | JSON verified |

## Appendix B: verbatim quotes collected (reuse-safe)

See §2.1, §2.2 (EULA/LPT clauses), §4 (§1201(f) extraction at
`/tmp/opencode/lii1201.html` during session), §5 (EUR-Lex files at
`/tmp/opencode/eurlex.html`, `/tmp/opencode/sas2.html`).
