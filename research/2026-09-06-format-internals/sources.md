# Sources, accessed 2026-09-06

## Empirical (verified here)
- 5 real files hexdumped, this directory `samples/`:
  - https://raw.githubusercontent.com/glepore70/pronom-research/master/sample_files/c/catpart/{analysis,brepaccess,catconduit}.catpart (PRONOM test corpus clone of https://github.com/glepore70/pronom-research)
  - https://media.githubusercontent.com/media/Guilherme115/Motor-V6/master/Spur%20Gear11.CATPart (Git LFS media)
  - https://media.githubusercontent.com/media/Guilherme115/Motor-V6/master/Motor%20-%20V6%20(Assembly%20final).CATProduct
- GitHub code search (authenticated gh api): `"V5_CFV2"` 132 hits; `extension:catpart` 133 hits; `extension:catproduct` 23; `extension:catsettings` 0.

## Specifications / signatures
- DROID Signature File V125: https://www.nationalarchives.gov.uk/documents/DROID_SignatureFile_V125.xml (PRONOM CATIA x-fmt/436-440, fmt/1615, fmt/1714)
- DROID container-signature-20260119.xml: no CATIA OLE2 container mapping
- FIDO format_extensions.xml: no CATIA entries
- libmagic (cloned github.com/file/file, Magdir grepped): no CATIA entries
- Ivanti IDAC vNow API, CATIA V5 header layout: https://help.ivanti.com/ht/help/en_US/IDAC/vNow/api/Content/policies.htm

## Reverse-engineering reference
- cadmpeg: https://github.com/cadmpeg/cadmpeg ; crates.io `cadmpeg-codec-catia` 0.5.5 (2026-08-27, Apache-2.0)
  - docs/formats/catia.md (local copy: source-cadmpeg-catia-format-spec.md, CC-BY-4.0)
  - docs/layouts/catia.md (local copy: source-cadmpeg-layout-table.md; machine-checked from docs/layouts/catia.toml)
  - docs/formats/catia-coverage.md, catia-open-items.md, docs/format-support.md, LEGAL.md
  - crates/cadmpeg-codec-catia/src/{container,layout,variant,families/standard/topology}.rs (located via code search)

## .3dxml
- Wikipedia 3DXML, rev 2025-08-09: https://en.wikipedia.org/wiki/3DXML (ZIP+BOM XML, PRC, DSA license)
- PRC = ISO 10303-224; xeokit 3DXML loader docs: https://xeokit.github.io/sdk/docs/ ; GLC_Player (ASCII 3DXML viewer): https://sourceforge.net/projects/glc-player/
- DROID V125: no 3DXML signature (verified)

## Folklore instances (recorded to document the myth, not its truth)
- filext.com CATDRAWING magic page; docs.fileformat.com/cad/catpart/ (compound-file claims); Google AI-mode answer (via r.jina.ai proxy) claiming OLE2 streams such as `FarthestStreamedVersion`; CatThumbnail tool page http://catia2.cad.de/index.php/en/downloads/scripts-apps/382-catthumbnail-v1-2-1-en (V5_CFV2 + embedded JPEG thumbnail; supports V5_CFV2 header, not OLE2)

## Search method
- Working: `r.jina.ai` proxy over `lite.duckduckgo.com/lite` (dumps in /tmp/catia_re/q_*.txt); direct curl of APIs; authenticated `gh api search/code`
- Blocked/dead: Google, Bing (spam-poisoned RSS), Mojeek captcha, searx.be antibot, grep.app (Vercel checkpoint), PRONOM web search UI, StackExchange API (0 hits for catpart on reverseengineering)
