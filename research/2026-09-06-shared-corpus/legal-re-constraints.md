# Legal constraints on reverse engineering CATIA V5 files and shipping a third-party reader/writer

Date: 2026-09-06. Researcher: Cerebo (opencode session), model flashnext/flashnext-w4a16-fp8ple.
Question: What legally blocks reading/writing CATIA V5 `.catpart`/`.catproduct` files and shipping a third-party converter, per primary sources?

Method note: every quotation below was retrieved by this session into `raw/` (HTML/PDF, mostly Wayback snapshots) or `txt/` (stripped text). Files are listed in "Raw sources". Items that could not be verified are flagged **[unverified]**. This is research, not legal advice.

---

## 1. The Dassault Systèmes license side

**Finding: DS's published Licensed Programs Terms do not contain an express "do not reverse engineer" clause. The general anti-reverse-engineering EULA is not published; it lives in the signed master "Agreement" and the installer EULA, which are not publicly hosted.** What IS public (retrieved verbatim):

- `txt/ds_catia_v5_lpt.txt` = "Licensed Programs Terms for CATIA – V5 Release 20" (DS public PDF, April 2010). It "incorporates by reference" a master Agreement that DS does not publish. Relevant published clauses:
  - Services restriction: licensed code may not be used to provide "services to third parties" or for "general distribution" of code (a service-bureau / SaaS-style clause).
  - Outsourcing clause: third parties you let use the software must not be "a competitor of any DS Group Company".
  - Security clause: you must not defeat or circumvent the "lock" (license-key enforcement) or authentication keys, nor let others do so.
- `txt/ds_consumers_ost.txt` (3DEXPERIENCE consumer offering-specific terms, 2022): commercial use of consumer editions is capped (revenue threshold of USD 2,000/yr). No RE clause here either.
- `txt/ds_3dexp_2017.txt` (3DEXPERIENCE R2017x licensed-programs addendum): no "reverse engineer" wording.
- A 2007 website Terms of Use (`raw/ds_tou2007.html`) prohibits RE of *website content*, not of the software.

Consequence: the contract analysis must assume a classic EULA-style clause exists (installer EULA/signed Agreement, text not public). The classic clause form is visible in the Vault v. Quaid license quoted at `txt/op_vault.txt`: the license grants use "only on a single machine" and forbids the licensee to "decompile or disassemble ... the program ... for any purpose". Courts treat such clauses as ordinary contract terms (section 4). A CATIA license clause of that type constrains only whoever signs it (the licensee). It does not bind a third party who never buys the software and never signs. That distinction drives the whole risk model.

An important corollary: a DS licensee (an employee or contractor who installs CATIA to study file behavior) who reverse-engineers under that contract breaches it, even where copyright law would allow the RE (section 4). Clean analysis therefore separates: (a) strangers analyzing a file (no contract), (b) licensees analyzing files (contract bites), (c) licensees using CATIA's own automation APIs to read/write their own files (usually fine, but see the competitor clause on outsourced work).

## 2. Copyright status of the file format vs. the code

- The program code itself is protected, source and object code alike: Apple v. Franklin, 715 F.2d 1372 (3d Cir. 1983) (`txt/op_franklin.txt`: object code is a "copy" because the CPU can only follow instructions written in object code); Apple v. Formula Int'l, 725 F.2d 521 (9th Cir. 1984) (`txt/op_formula.txt`: OS programs protected, though copying them onto disks for resale is still assessed under ordinary infringement rules).
- What a file format IS: a data structure plus a naming/syntax convention. Under 17 U.S.C. 102(b) and 101 ("method of operation") interfaces and formats fall outside protection. Key holdings retrieved:
  - Lotus v. Borland, 49 F.3d 807 (1st Cir. 1995), `txt/op_lotus.txt`: "the Lotus menu command hierarchy is uncopyrightable subject matter" as a method of operation (Breyer, J., concurring, stressed that copying it was necessary to let users keep their macros and skills).
  - Engineering Dynamics v. Structural Software, 46 F.3d 408 (1st Cir. 1995), aff'g 785 F. Supp. 576 (E.D. La. 1992), `txt/op_edsi.txt`: the district court held the input and output file formats (the SPACS data cards and output lists) to be unprotectable methods of operation, and the First Circuit affirmed while expressly assuming arguendo that the formats were protectable, so the plaintiff could not complain about that ruling; the input format was also held to merge with the idea of describing a structure. This is the closest precedent to a CAD file format and it went the format's way, on independence grounds: EDSI independently rewrote its own elements after studying the published formats, which is why its program survived the merger analysis, and it survived because it "rewrote" the format, not because file formats are categorically free.
  - SAS v. World Programming, C-406/10 (CJEU Grand Chamber, 2 May 2012), `raw/eu_sas_wpl.html`: Directive 2009/24 Art. 1(2) quoted: "Protection in accordance with this Directive shall apply to the expression in any form of a computer program. Ideas and principles which underlie any element of a computer program, including those which underlie its interfaces, are not protected". The CJEU held that neither the functionality nor the programming language nor the data file format is protected as the expression of a program. Same logic applies to the EU for reading the format's schema.
  - Sega v. Accolade, 977 F.2d 1510 (9th Cir. 1992), `txt/op_sega.txt`: the gateway sentence for the whole field: "where disassembly is the only way to gain access to the ideas and functional elements embodied in a copyrighted computer program and where there is a legitimate reason for seeking such access, disassembly is a fair use of the copyrighted work, as a matter of law."
  - Sony v. Connectix, 203 F.3d 596 (9th Cir. 2000), `txt/op_connectix.txt`: intermediate copies made during reverse engineering were fair use; the summary language retrieved from the headnote: "finding fair use where defendant made intermediate copies of [Sony's] copyrighted software program and, by reverse engineering, created defendant's own software program which emulated" it. The district court's contrary ruling was reversed.
  - Sony v. Bleem, 214 F.3d 1022 (9th Cir. 2000), `txt/op_bleem.txt`: even taking screenshots of Sony games for side-by-side ads was fair use; a converter that merely reads the format is much less invasive.
  - Atari Games v. Nintendo, 975 F.2d 832 (Fed. Cir. 1992), `txt/op_atari_fed.txt`: RE for interoperability can be fair use, but Atari LOST because it obtained the lockout source code from the Copyright Office on a false "needed for defense" representation and used it. Lesson: the clean-hands doctrine is the real enforcement risk in RE cases; document provenance of every sample and every document consulted. (The earlier N.D. Cal. 1992 Atari opinion that introduced the clean-room lesson **[unverified/full text not retrieved]**; the point is standard but not quoted here from a retrieved source. The related 897 F.2d 1572 opinion (`raw/op_atari_dc.html`, mislabeled) is a procedural Fed. Cir. opinion.)
  - Interop-driven file RE with a clean-room defense succeeded in Davidson & Assocs. v. Jung, 422 F.3d 630 (8th Cir. 2005) (`txt/op_davidson.txt`: bnetd devs reverse-engineered the Battle.net protocol "by necessity ... to learn Blizzard's protocol language"; the RE itself was a copyright fair-use win for the devs; they lost on the EULA contract breach instead).

Bottom line: reading or describing a `.catpart` format, and independently re-implementing it, is well-covered by precedent. What is NOT covered is copying DS's code or literal data tables into a reader, and what is fact-dependent is whether a writer that reproduces DS's exact internal structures copies protectable creative expression (an unresolved boundary; see the EDSI rewrite pattern).

## 3. Anti-circumvention law and the interoperability exceptions

None of this binds you if the file is not access-controlled, and `.catpart` files are not encrypted. CATIA's licensing lock is a different measure (see below).

- DMCA 17 U.S.C. 1201, `raw/us_1201.html` / `txt/us_1201.txt`:
  - 1201(a)(1) bars circumventing "a technological measure that effectively controls access to a work"; 1201(a)(2)/(b) bar trafficking in circumvention tools.
  - 1201(f) "Reverse Engineering" exception, retrieved text: a person who lawfully obtained the right to use a copy of a program "may circumvent a technological measure ... in order to identify and analyze those elements ... necessary to achieve interoperability of an independently created computer program with other programs"; the knowledge acquired may be "delivered or made available to the person's own independently created programs" and may be shared with others "when doing so is otherwise necessary to achieve interoperability", but only to the extent it does not itself facilitate infringement ("sole purpose of achieving interoperability" framing; 1201(f)(2), (f)(3)(A)).
  - This is squarely the reader/converter scenario: analyzing a program (CATIA or the file) to achieve interoperability of an independently created program.
- EU Directive 2009/24/EC (codifying 91/250), `raw/eu_directive.html`:
  - Art. 5(1): acts necessary for use "in accordance with their intended purpose" by a lawful user need no authorization "in the absence of specific contractual provisions".
  - Art. 5(3): observing, studying or testing "the functioning of a program in order to determine the ideas and principles which underlie any element of the program" needs no authorisation and cannot be contracted out of (no specific contractual provision "can be held to be incompatible with this exception").
  - Art. 6(1): decompilation (reproduction + translation to obtain the information necessary to achieve interoperability of an independently created program) needs no authorisation, subject to the classic conditions: prior attempt to obtain interfaces on reasonable terms, information limited to parts needing decompilation, and the information may not be used for acts restricted without authorisation (notably "for the development, production or marketing of a computer program substantially similar in its expression").
  - Recital (15) retrieved verbatim: "any contractual provisions contrary to the provisions of this Directive laid down in respect of decompilation or to the exceptions ... should be null and void".
- UK implementation, `txt/uk_50b.txt`, `txt/uk_50c.txt`, `txt/uk_50ba.txt` (CDPA 1988):
  - s.50B Decompilation: "It is not an infringement of copyright for a lawful user of a copy of a computer program expressed in a low level language (a) to convert it into a version expressed in a higher level language, or (b) incidentally in the course of so converting the program, to copy it", with the same Art. 6 conditions and the "not ... read as extending" limits.
  - s.50C other lawful-user acts; s.50BA observation/study/test (cannot be overridden).
- Germany, UrhG 69e (`txt/` copy): matches Art. 6 ("Handlungen ..., die erforderlich sind, um die Informationen herzustellen, die zum Herstellen unabhängig geschaffener ... Programme erforderlich sind"), with the same no-abuse limits. 69a(5): ideas and principles underlying interfaces are not protected (SAS logic).

Practical note on the two locks: DS's enforcement mechanisms are (a) the license-key system protecting the software (anti-circumvention would bite only if you broke that lock to run CATIA without authorization; you don't need it, a licensed or trial copy suffices for lawful analysis), and (b) nothing on the files. The DMCA/EU/UK anti-circumvention risk for this project is near zero because no access control on the target work (the file) is circumvented.

DMCA misuse cases retrieved:
- Lexmark v. Static Control (6th Cir. 2004, 387 F.3d 522, `txt/op_lexmark2.txt`): DMCA attacked as an IP-leverage tool against a compatible-product maker; the court noted 1201 bars circumvention of measures that "effectively control access" and 102(b) keeps ideas/methods of operation free; Static Control prevailed (and in the later Supreme Court case, Lexmark v. Static Control, 572 U.S. 118 (2014), `txt/op_lexmark.txt`, Static Control won standing too).
- Chamberlain v. Skylink (Fed. Cir. 2004, 381 F.3d 1178, `txt/op_chamberlain.txt`): 1201(a) claim rejected for lack of "the critical nexus between access and protection": "Chamberlain neither alleged copyright infringement nor explained how the access provided by the Model 39 transmitter facilitates the infringement of any right that the Copyright Act protects."
- Corley (2d Cir. 2000, 273 F.3d 429, `txt/op_corley.txt`): fair use is not a defense to 1201(a) circumvention, but that case involved breaking an access control (CSS) to enable piracy. It does not fit an unencrypted file, and 1201(f) exists precisely for interop.

## 4. Contract: the enforceability of the anti-RE clause

- If you never sign, no bite. If you license CATIA to do the RE, Davidson v. Jung (bnetd) is the warning: 8th Cir. enforced the EULA/TOU RE prohibition and awarded for breach "even though the reverse engineering itself was lawful under copyright". `txt/op_davidson.txt` quotes the EULA/TOU clickwrap ("I Agree" button) and the breach award.
- Bowers v. Baystate (Fed. Cir. 2003, 320 F.3d 1317, `txt/op_bowers.txt`): a "do not reverse engineer" clause in a signed license is enforceable; jury awarded $3.8M for contract breach. Federal Circuit expressly held contract and copyright are separate, no preemption.
- The contrary view at district level (Vault v. Quaid, E.D. La. 1987, `txt/op_vault.txt`) held the shrinkwrap RE ban unenforceable (misuse/preemption); the Fifth Circuit affirmed the invalidity of the clause but the case was superseded by the later line; treat Bowers/Davidson as the modern rule.
- EU/UK: Art. 6 + Recital 15 + s.50B mean such clauses are null and void against lawful-user decompilation for interoperability. Germany 69e likewise mandatory.
- Effect: a US project must not do its RE under a signed CATIA license with the analysis team; an EU project has stronger statutory protection. The practical mitigation everywhere is: use an evaluation/trial copy under its own terms only for black-box observation of outputs, or better, never run CATIA at all for RE (work from sample files only), or use a clean-room team that never sees CATIA or DS docs (see section 6).

## 5. Trade secrets

- Files in circulation are not secret; DS publishes the reader-writer ecosystem via interchange formats and sells access to the format only via CAA licenses. Under DTSA/UTSA, independent discovery and reverse engineering of lawfully obtained products are lawful means of acquisition. No retrieved case shows DS suing a format reader on secret grounds.
- Where it bites: an ex-employee or CAA licensee who leaks source or unpublished interface specs (that is why Dassault Systemes v. Childress exists: 663 F.3d 832 (6th Cir. 2011), `raw/cl_ds_cases.json` metadata: jurisdiction over a former DS engineer tied to source-code disputes; full text behind a paywall, **[full text not retrieved]**). Clean-room discipline is the answer, plus not accepting any leaked material.

## 6. DS's enforcement history, and how the incumbents do it

Retrieved facts:
- CourtListener case-name search for Dassault (`raw/cl_ds_cases.json`, 18 hits): the copyright/interop fights are Autodesk v. Dassault Systèmes SolidWorks, 685 F. Supp. 2d 1001/1023 (N.D. Cal. 2009) (the IMSI/DXF translation dispute, with DS as defendant; full texts not retrievable, **[metadata only]**), and Dassault v. Childress (above). No retrieved case shows DS suing a neutral file-reader vendor. Dassault v. Tata **[unverified]** (search engines unusable this session).
- DS runs an anti-piracy/licensing-compliance program (page referenced from 3ds.com ethics/compliance materials; page content **[not retrieved]**).
- Incumbent converter vendors (all third parties, none licensed by DS for the native formats, to the extent of public evidence):
  - Okino (`raw/okino_conv.html`): Conversion3D/TransMagic-family page lists "CATIA (.catpart, .catproduct)" among supported formats.
  - ODA (`raw/oda_about.html`; site is now a JS SPA, 2012/2016 Wayback copies retrieved contain no quotable anti-RE disclaimer), CAD Exchanger (`raw/cadex_about.html`, also SPA), Tech Soft 3D HOOPS (`raw/tsoft_hoops.html`), Spatial (`raw/spatial_about.html`) advertise CATIA import; verbatim legal-position statements were not server-rendered and could not be extracted. Their long-standing, unlitigated market position is itself the best evidence of what the field tolerates: independent readers built from observed file behavior, sold as interoperability products.
  - Autodesk acquired DataTranslation (the CGS/OCC-lineage translators) in 2016 **[unverified this session: press page not retrievable]**.
- Open source: GitHub API search (this session, `raw/gh_search.json`, `raw/gh_search2.json`): "catpart" 49 repos, none a mature reader; "catia parser" 1 repo (XML-based). The previously known MIT `kkoziarski/catia-parser` repo is gone (API 404; user exists with 22 repos, no CATIA; no Wayback snapshot). Public open-source `.catpart` parsing is effectively absent, which is a market fact and also a legal signal: nobody has needed to litigate this.

## 7. Clean room, CAA, and DS's own publications

- The Atari Fed. Cir. ruling (section 2) sets the bar: any DS code or DS-internal documentation entering the implementation is a clean-hands disaster. A defensible process: team A (reads sample `.catpart` files, may run licensed CATIA only on a dedicated machine under terms it does not sign for project purposes; documents observed structure in specs owned by the company), team B (writes the reader only from team A's specs, never touching DS software or code). This is the pattern the Atari court blessed in dicta and Connectix effectively endorsed (independent final product).
- CATIA V5's CAA APIs and published help make large parts of the object model public (feature tree, topological data model, `3dxml`/JT/STEP export paths). Using CAA documentation to learn semantics is a fair-use-scale act; the format's "ideas and principles" (its entity taxonomy) are not protected (Art. 1(2) quote, section 2).
- Interchange route: exporting STEP AP242/JT/3DXML through CATIA is contract-safe for a licensee, and readers of STEP/JT (open ISO specs) have no RE problem at all. This is why option (f) in the table is the low-risk baseline.

## 8. Patents and trademarks

- Patents: Google Patents XHR queries this session (`raw/pat_ds2.json`: assignee Dassault + catia, total 98; `raw/pat_ds3.json`: object-oriented database cluster, total 99). DS patents cover implementation techniques (e.g., US10275942B2 compression of a 3D modeled object, prio 2013; US10347040B2 hybrid streaming, prio 2015; EP3032495B1 texturing a 3D modeled object, prio 2014). I did not find a retrieved patent claiming the `.catpart` serialization itself; V5 (1994-1999) era patents have expired 20 years from filing regardless. Patent risk for a reader today is modest and concentrated in newer features (3D via CATIA V6/3DEXPERIENCE formats), not the V5 container format. This is a coverage gap, not an all-clear; a targeted patentability search is cheap to repeat.
- Trademarks: DS's public trademarks policy page exists (`raw/ds_trademark.html`, Wayback 2010 copy; current site is a JS shell). Saying "reads CATIA V5 files" descriptively is nominative fair use: New Kids on the Block v. News America, 971 F.2d 302, 308 (9th Cir. 1992), quoted in Network Automation v. ASC (9th Cir. 2013, slip op. No. 10-55840, `txt/op_network_auto.txt`; reported at 748 F.3d 880, reporter cite from memory, slip op retrieved): use is permitted where "the product requires use of the trademark to identify it", only as much as necessary, no suggestion of sponsorship. Use "works with CATIA", not a CATIA-looking logo or "official".

## 9. Jurisdictional exposure, ranked

1. US: contract (Davidson/Bowers) is the leading real risk if anyone on the project signs a DS license and does the RE under it; DMCA is near-zero (no access control circumvented; 1201(f) covers the rest); copyright on the format is favorable (102(b), Lotus/EDSI/SAS logic, Sega/Connectix fair use).
2. EU: strongest position. Art. 5(3) study right and Art. 6 decompilation right are mandatory law; RE-for-interop contracts are null and void; SAS CJEU confirms formats/functionality unprotected. Germany 69e mirrors.
3. UK: same via s.50B/50BA/50C.
4. Where the plaintiff can find you: DS sues in US and France. France enforces the directive's mandatory exceptions (L.122-6-1 CPI equivalent), but French courts also guard authors' moral rights; irrelevant for file reading.

## 10. Risk-graded options

| # | Option | Legal basis | Main residual risk | Notes |
|---|--------|-------------|--------------------|-------|
| a | Read-only parser for `.catpart`/`.catproduct` (sample-file RE, clean room) | 102(b); Sega/Connectix fair use; 1201(f); Art. 5(3)/6; s.50B | Low. Keep clean hands (Atari); no copied literals; never under a signed DS EULA for the RE team | Market has done this for 20 years without litigation |
| b | Writer producing new files that CATIA opens | Same as (a) plus: reproducing DS's creative internal structures could be expression (EDSI boundary) | Medium-low. Prefer minimal valid structure + round-trip testing on licensed evaluation copies | The unresolved doctrinal edge |
| c | Commercial writer/converter as product (Okino/ODA model) | (a)+(b) plus trademark fair use (New Kids via Network Automation) | Medium. Add trademark wording review; consider indemnity | No retrieved case against such a vendor |
| d | Publish the format spec | Pure speech; nothing in DS's published terms reaches non-licensees | Low; reputational/cease-and-desist noise possible | Spec published from RE of files is protected (Sega: ideas not protected) |
| e | Drive CATIA itself via CAA/COM automation (user must own CATIA) | User's own license; DS's automation APIs exist for this (see sibling report `catia-automation-writers.md`) | Low contract risk if user is the licensee; competitor clause only affects outsourced service bureau use | Not a product for non-CATIA users |
| f | Interchange formats only (STEP/JT/IGES; user exports once) | Open ISO specs; zero DS code contact | Near zero | The safe floor; also a good compliance fallback ("we read STEP") |

Recommended default: (a) now, (c) with clean-room evidence trail, (b) behind it, (f) always as fallback. Never: running cracked CATIA, using leaked CAA source/specs, or letting the RE team sign and breach an EULA.

---

## Raw sources

Case texts (Wayback snapshots of law.justia.com / casetext.com, downloaded 2026-09-06; stripped text in `txt/`):

| File | Case | Citation |
|------|------|----------|
| raw/op_sega.html → txt/op_sega.txt | Sega v. Accolade | 977 F.2d 1510 (9th Cir. 1992) |
| raw/op_lotus.html → txt/op_lotus.txt | Lotus v. Borland | 49 F.3d 807 (1st Cir. 1995) |
| raw/op_connectix.html → txt/op_connectix.txt | Sony v. Connectix | 203 F.3d 596 (9th Cir. 2000) |
| raw/op_bleem.html → txt/op_bleem.txt | Sony v. Bleem | 214 F.3d 1022 (9th Cir. 2000) |
| raw/op_formula.html → txt/op_formula.txt | Apple v. Formula Int'l | 725 F.2d 521 (9th Cir. 1984) |
| raw/op_franklin.html → txt/op_franklin.txt | Apple v. Franklin | 715 F.2d 1372 (3d Cir. 1983) |
| raw/op_atari_fed.html → txt/op_atari_fed.txt | Atari v. Nintendo | 975 F.2d 832 (Fed. Cir. 1992) |
| raw/op_atari_dc.html | Atari v. Nintendo | 897 F.2d 1572 (Fed. Cir. 1990, procedural) |
| raw/op_edsi.html → txt/op_edsi.txt | Engineering Dynamics v. Structural Software | 46 F.3d 408 (1st Cir. 1995) / 785 F. Supp. 576 |
| raw/op_davidson.html → txt/op_davidson.txt | Davidson v. Jung (bnetd) | 422 F.3d 630 (8th Cir. 2005) |
| raw/op_bowers.html → txt/op_bowers.txt | Bowers v. Baystate | 320 F.3d 1317 (Fed. Cir. 2003) |
| raw/op_chamberlain.html → txt/op_chamberlain.txt | Chamberlain v. Skylink | 381 F.3d 1178 (Fed. Cir. 2004) |
| raw/op_corley.html → txt/op_corley.txt | Universal v. Corley | 273 F.3d 429 (2d Cir. 2000) |
| raw/op_lexmark.html → txt/op_lexmark.txt | Lexmark v. Static Control (SCOTUS) | 572 U.S. 118 (2014) |
| raw/op_lexmark2.html → txt/op_lexmark2.txt | Lexmark v. Static Control (6th Cir.) | 387 F.3d 522 (6th Cir. 2004) |
| raw/op_vault.html → txt/op_vault.txt | Vault v. Quaid (E.D. La.) | 655 F. Supp. 750 (1987); aff'd 847 F.2d 255 (5th Cir. 1988) |
| raw/op_network_auto.html → txt/op_network_auto.txt | Network Automation v. Advanced System Concepts | 9th Cir. 2013, No. 10-55840 (slip op; reported at 748 F.3d 880); quotes New Kids 971 F.2d 302 |

Statutes and official texts (live downloads, same day):
- raw/us_1201.html / txt/us_1201.txt: 17 U.S.C. 1201 incl. (f) via law.cornell.edu.
- raw/eu_directive.html: Directive 2009/24/EC full text via eur-lex (CELEX 32009L0024); Art. 5, Art. 6, Recital 15 quoted.
- raw/eu_sas_wpl.html: CJEU C-406/10 SAS v. WPL (pdf-derived HTML, eur-lex).
- txt/uk_50b.txt, txt/uk_50c.txt, txt/uk_50ba.txt: CDPA 1988 ss.50B, 50C, 50BA via legislation.gov.uk. s.50E not retrieved (section repealed/moved by 2003 regs; circumvention now ss.296ff., not quoted).
- txt/urhg_69e.txt: UrhG 69e, 69a via gesetze-im-internet.de.

DS terms (Wayback + live, same day):
- raw/ds_catia_v5_lpt.pdf → txt/ds_catia_v5_lpt.txt: Licensed Programs Terms, CATIA V5R20, 2010 (3ds.com fileadmin, Wayback).
- raw/ds_3dexp_2017.pdf → txt/ds_3dexp_2017.txt; raw/ds_consumers_ost.pdf → txt/ds_consumers_ost.txt: 3DEXPERIENCE terms.
- raw/ds_lpt.html, raw/ds_lps.html, raw/ds_licensed_programs.html, raw/ds_tou2007.html, raw/ds_trademark.html (Wayback 20100621083929): 3ds.com terms/trademark pages.
- raw/cdx_ds_files.txt, raw/cdx_ds_fa.txt: Wayback CDX harvests of 3ds.com fileadmin (523 terms files; mining result: master EULA not publicly hosted).

CourtListener API results (anonymous, throttled 5/min): raw/cl_ds_cases.json (caseName:(Dassault), 18 hits incl. Autodesk v. DS SolidWorks 685 F. Supp. 2d 1001; full texts behind WAF/paywall **[not retrieved]**); raw/cl_*.json for each case above.

Patents: raw/pat_ds2.json (assignee:"Dassault Systemes" catia, 98 results), raw/pat_ds3.json (99 results) via patents.google.com/xhr/query; representative numbers quoted in section 8.

Vendors: raw/okino_conv.html (lists CATIA .catpart/.catproduct support), raw/oda_about.html, raw/cadex_about.html, raw/tsoft_hoops.html, raw/spatial_about.html (SPA shells; quoted wording not server-rendered); raw/gh_search.json + raw/gh_search2.json + raw/gh_repo.json + raw/gh_kkoz.html (GitHub API; kkoziarski/catia-parser deleted, 404 live and in Wayback).

Unverified items (do not cite as fact): Apple v. Brightstar; CD Maps v. MetaMap; Dassault v. Tata; Atari N.D. Cal. 1992 opinion; Oracle v. Google 593 U.S. 1 (2021) (not fetched this session); Autodesk/DataTranslation 2016 acquisition date.
