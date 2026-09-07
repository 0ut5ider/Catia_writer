Title: DATAKIT SDK: CATIA V5 Writer

URL Source: https://www.datakit.com/Doc_API_html/catiav5w.html

Markdown Content:
**[Supported versions and extensions](https://www.datakit.com/Doc_API_html/details.html#supportedversions) (3D) :**

| 3D Writer | Supported Versions | Supported Extensions |
| --- | --- | --- |
| CATIA V5 | R14, R19, R20, R21 and V5-6R2012 to V5-6R2026 | .CATPart, .CATProduct |

**[Supported Modules](https://www.datakit.com/Doc_API_html/supportedmodules.html) :**

: Processed: Not Processed: Partially Processed: Not Applicable

| Assemblies | BREP | Wireframe | Meshes | Notes/PMI/FDT | Metadata | RenderInfos | PhysicalMaterial | Machining Features | Assembly Constraints | UUID / PersistentName | Model Display | Drawings(2D) | Part Tree |
| --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- |
|  |  |  |  |  |  |  |  |  |  |  |  |  |  |

**[Datakit Libraries and usage](https://www.datakit.com/Doc_API_html/internaldepends.html) :**`LibCatiaV5Write``LibCatiaV5Read`

**Warning :**

CATIAV5 Doesn't support periodic surfaces and periodic curves.

 You cannot have an edge which has got the same start vertex as end vertex.

 So you have to split periodic surfaces and periodic curves.

**How to write assemblies :**

*   [How To Use Catia V5 Writer APIs for CATProduct writing](https://www.datakit.com/Doc_API_html/v5w_asm_how_to.html)

**General Mapping :**

*   [Catia V5 Write General Mapping](https://www.datakit.com/Doc_API_html/v5w_mapping.html)

**Sample Source Code :**

*   [Samples](https://www.datakit.com/Doc_API_html/v5w_samples.html)
