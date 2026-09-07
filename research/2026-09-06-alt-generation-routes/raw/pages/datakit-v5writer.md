Title: How To Use Catia V5 Writer APIs for CATProduct writing

URL Source: https://www.datakit.com/Doc_API_html/v5w_asm_how_to.html

Markdown Content:
![Image 2: Logo](https://www.datakit.com/Doc_API_html/tetiere_ht.jpg)DATAKIT SDK V2026.3![Image 3](https://www.datakit.com/Doc_API_html/search/mag_sel.svg)[![Image 4](https://www.datakit.com/Doc_API_html/search/close.svg)](javascript:searchBox.CloseResultsWindow())

*   [Main Page](https://www.datakit.com/Doc_API_html/index.html)
*   [API Reference](https://www.datakit.com/Doc_API_html/annotated.html)

![Image 5: click to disable panel synchronisation](https://www.datakit.com/Doc_API_html/sync_on.png)

*   [▼](javascript:void(0))[DATAKIT SDK](https://www.datakit.com/Doc_API_html/index.html) 
    *   [▼](javascript:void(0))[API Guide](https://www.datakit.com/Doc_API_html/index.html) 
        *   [Welcome to Datakit API Help!](https://www.datakit.com/Doc_API_html/index.html#wcm) 
        *   [►](javascript:void(0))[What's New ?](https://www.datakit.com/Doc_API_html/rel_note.html) 
        *   [►](javascript:void(0))[Integrating SDK](https://www.datakit.com/Doc_API_html/all_samples.html) 
        *   [►](javascript:void(0))[Datakit API](https://www.datakit.com/Doc_API_html/howto.html) 
        *   [▼](javascript:void(0))[Readers and Writers details](https://www.datakit.com/Doc_API_html/details.html) 
            *   [►](javascript:void(0))[Supported versions and extensions](https://www.datakit.com/Doc_API_html/details.html#supportedversions) 
            *   [►](javascript:void(0))[Supported Modules](https://www.datakit.com/Doc_API_html/supportedmodules.html) 
            *   [►](javascript:void(0))[Readers Mapping](https://www.datakit.com/Doc_API_html/_sreaders.html) 
            *   [▼](javascript:void(0))[Writers Mapping](https://www.datakit.com/Doc_API_html/_swriters.html) 
                *   [►](javascript:void(0))[3DXML Writer](https://www.datakit.com/Doc_API_html/_3dxml.html) 
                *   [►](javascript:void(0))[3MF Writer](https://www.datakit.com/Doc_API_html/_3mfwriter.html) 
                *   [►](javascript:void(0))[ACIS 3D Writer](https://www.datakit.com/Doc_API_html/acisw.html) 
                *   [►](javascript:void(0))[CATIA V5 Writer](https://www.datakit.com/Doc_API_html/catiav5w.html) 
                *   [►](javascript:void(0))[CGR Writer](https://www.datakit.com/Doc_API_html/cgrw.html) 
                *   [►](javascript:void(0))[COLLADA Writer](https://www.datakit.com/Doc_API_html/colladaw.html) 
                *   [►](javascript:void(0))[FBX Writer](https://www.datakit.com/Doc_API_html/fbxw.html) 
                *   [►](javascript:void(0))[glTF Writer](https://www.datakit.com/Doc_API_html/gltfw.html) 
                *   [►](javascript:void(0))[IFC Writer](https://www.datakit.com/Doc_API_html/ifcw.html) 
                *   [►](javascript:void(0))[IGES Writer](https://www.datakit.com/Doc_API_html/igesw.html) 
                *   [►](javascript:void(0))[JT Writer](https://www.datakit.com/Doc_API_html/jtw.html) 
                *   [►](javascript:void(0))[NX Writer](https://www.datakit.com/Doc_API_html/ugw.html) 
                *   [►](javascript:void(0))[OBJ Writer](https://www.datakit.com/Doc_API_html/objw.html) 
                *   [►](javascript:void(0))[Parasolid Writer](https://www.datakit.com/Doc_API_html/xmtw.html) 
                *   [►](javascript:void(0))[PLM XML Writer](https://www.datakit.com/Doc_API_html/plmxmlw.html) 
                *   [►](javascript:void(0))[PDF-3D Writer](https://www.datakit.com/Doc_API_html/pdfw.html) 
                *   [►](javascript:void(0))[STEP Writer](https://www.datakit.com/Doc_API_html/stepw.html) 
                *   [►](javascript:void(0))[SOLIDWORKS Writer](https://www.datakit.com/Doc_API_html/sww.html) 

    *   [Deprecated List](https://www.datakit.com/Doc_API_html/deprecated.html) 
    *   [►](javascript:void(0))[API Reference](https://www.datakit.com/Doc_API_html/annotated.html) 

[•All](javascript:void(0))[Data Structures](javascript:void(0))[Namespaces](javascript:void(0))[Files](javascript:void(0))[Functions](javascript:void(0))[Variables](javascript:void(0))[Typedefs](javascript:void(0))[Enumerations](javascript:void(0))[Enumerator](javascript:void(0))[Friends](javascript:void(0))[Macros](javascript:void(0))[Modules](javascript:void(0))[Pages](javascript:void(0))

How To Use Catia V5 Writer APIs for CATProduct writing 

### Table of Contents

*   [the Document ID Notion](https://www.datakit.com/Doc_API_html/v5w_asm_how_to.html#v5w_doc_id_notion)
*   [The CATProduct writing step-by-step.](https://www.datakit.com/Doc_API_html/v5w_asm_how_to.html#v5w_asm_write_steps)
*   [Referencing existing files from a CATProduct](https://www.datakit.com/Doc_API_html/v5w_asm_how_to.html#v5w_asm_write_add_existing_files)
*   [The Virtual Component writing step-by-step.](https://www.datakit.com/Doc_API_html/v5w_asm_how_to.html#v5w_component_write_steps)
*   [Full Sample.](https://www.datakit.com/Doc_API_html/v5w_asm_how_to.html#v5w_asm_full_sample)

 You MUST ALWAYS close a Product/Component context - by calling [catiav5w::EndProduct()](https://www.datakit.com/Doc_API_html/namespacecatiav5w.html#a4c56b71729947412b4c9bc5271cae76a "Write effectively the Sub Product initialized by catiav5w::InitProduct.") or [catiav5w::EndVirtualComponent()](https://www.datakit.com/Doc_API_html/namespacecatiav5w.html#ac1238b1e47eb33c6f238c2329229e305 "End - and write - the virtual component initialized by catiav5w::InitVirtualComponent.") - before opening another context.

[catiav5w::InitProduct()](https://www.datakit.com/Doc_API_html/namespacecatiav5w.html#a698099acf905c9d068f977416f0c34b1 "Initialize a sub Product during CATProduct process.") / [catiav5w::InitVirtualComponent()](https://www.datakit.com/Doc_API_html/namespacecatiav5w.html#a08a28823e24f13b309a3526fb9eddaee "Initialize a virtual component during CATProduct process.") CAN'T be nested !!!

* * *

# [](https://www.datakit.com/Doc_API_html/v5w_asm_how_to.html) the Document ID Notion

The main idea of the Assemblies CATIA V5 Writing is to add instances of a previously written Document.

 For this, DATAKIT APIs introduce the Document ID notion.

 The first thing to do is to create Document Reference (DocID) giving a file fullpath and a reference name.

 It will result to a Document ID that you can use easily to add an instance into a CATProduct.

# [](https://www.datakit.com/Doc_API_html/v5w_asm_how_to.html) The CATProduct writing step-by-step.

*   First create Document IDs by [catiav5w::CreateCGRDocId](https://www.datakit.com/Doc_API_html/namespacecatiav5w.html#a2f3f68535afba2b041a989a7ec20d5cf "Create a CGR Reference and DocID related to a given CGR File.") or [catiav5w::CreateV4ModelDocId](https://www.datakit.com/Doc_API_html/namespacecatiav5w.html#a1c5bc3cb6340a740d919aa90279084a8 "Create a V4 Model Reference and DocID related to a given V4 Model File."): [Dtk_string](https://www.datakit.com/Doc_API_html/class_dtk__string.html) CATPartFileName = L"C:\\sample_files\\catiav5\\V5_sample.CATPart"; [Dtk_transfo](https://www.datakit.com/Doc_API_html/class_dtk__transfo.html) TransformationMatrix;   //First you have to initialize the CATIA V5 writer [catiav5w::InitWrite](https://www.datakit.com/Doc_API_html/namespacecatiav5w.html#a1fdce5cda848b1e2d0a87ad67ef24ef0)(L"C:\\LogFile.log", NULL);  //The ProcessPart is an user implemented function to create a part [Dtk_UUID](https://www.datakit.com/Doc_API_html/class_dtk___u_u_i_d.html) PartUUID = [ProcessPart](https://www.datakit.com/Doc_API_html/testlibcatiav5write_8cpp.html#afbc7fa6cdc116de4955729c6f3b88aba)(inOutputFile, L"essaiPart");  [Dtk_Size_t](https://www.datakit.com/Doc_API_html/define_8h.html#a9b49974b7430e6b7734b27657bf75af3) PartID, V4ID, CgrID, ProdID,ProdID2, ProdID3;  //We create Document Reference to the CATPart file  [catiav5w::CreatePartDocId](https://www.datakit.com/Doc_API_html/namespacecatiav5w.html#a4f661a03a577274e60983059935c99f8)(inOutputFile, L"PartFile", PartUUID, PartID);  //...and to a CGR file [catiav5w::CreateCGRDocId](https://www.datakit.com/Doc_API_html/namespacecatiav5w.html#a2f3f68535afba2b041a989a7ec20d5cf)("../SampleFiles/cgr/Engine.cgr", "CGRFile", CgrID);  //...and finally to a CATIA V4 '.model' file [catiav5w::CreateV4ModelDocId](https://www.datakit.com/Doc_API_html/namespacecatiav5w.html#a1c5bc3cb6340a740d919aa90279084a8)("../SampleFiles/v4/EngineComponent.model", "V4File", V4ID);   These functions create Reference link to an existing file. For CATIA V4 files, you can only reference '.model' files.

 At this time the CatiaV5 Writer can only reference CATPart written by the writer.

 The writer can't handle external CATPart references.

 So, to reference a CATPart file, you have to provide an additional parameter.

 This parameter is the CATPart UUID and it is given by the [catiav5w::InitPart](https://www.datakit.com/Doc_API_html/namespacecatiav5w.html#af5bae72d1a24331b0fca64dc90fcbe4a "Initialize the part") function. So you can call the CreatePartDocId function:
*   Once you have created the Part DocIds, you can create CATProduct file. For this you have to create a CATProduct context with the [catiav5w::InitProduct](https://www.datakit.com/Doc_API_html/namespacecatiav5w.html#a698099acf905c9d068f977416f0c34b1 "Initialize a sub Product during CATProduct process."). //we init a CATProduct context... [catiav5w::InitProduct](https://www.datakit.com/Doc_API_html/namespacecatiav5w.html#a698099acf905c9d068f977416f0c34b1)( L"..\\SampleFiles\\dtk\\SubProduct.CATProduct", L"SubProduct");  
*   Once the CATProduct context is created, you can easily add instances into it by the [catiav5w::AddInstance](https://www.datakit.com/Doc_API_html/namespacecatiav5w.html#a847ad8c1edaf5d8b7369b052a6e983a2 "Add an instance to a DocID into the Current (Sub/Root) CATProduct.") function. //...to insert a Part instance TransformationMatrix.[setOrigin](https://www.datakit.com/Doc_API_html/class_dtk__transfo.html#a418cf6193970c962140618fba7a740e1)( 0.0,0.0,0.0); [catiav5w::AddInstance](https://www.datakit.com/Doc_API_html/namespacecatiav5w.html#a847ad8c1edaf5d8b7369b052a6e983a2)(PartID, L"PartInstance", TransformationMatrix); //...a CGR instance TransformationMatrix.[setOrigin](https://www.datakit.com/Doc_API_html/class_dtk__transfo.html#a418cf6193970c962140618fba7a740e1)( 0.0,500.0,0.0); [catiav5w::AddInstance](https://www.datakit.com/Doc_API_html/namespacecatiav5w.html#a847ad8c1edaf5d8b7369b052a6e983a2)(CgrID, L"CGRInstance", TransformationMatrix); //...and a V4 instance TransformationMatrix.[setOrigin](https://www.datakit.com/Doc_API_html/class_dtk__transfo.html#a418cf6193970c962140618fba7a740e1)( 0.0,-500.0,0.0); [catiav5w::AddInstance](https://www.datakit.com/Doc_API_html/namespacecatiav5w.html#a847ad8c1edaf5d8b7369b052a6e983a2)(V4ID, L"V4Instance", TransformationMatrix);  
*   Finally you have to ends the CATProduct context - to explicitely write the CATProduct file - by the [catiav5w::EndProduct](https://www.datakit.com/Doc_API_html/namespacecatiav5w.html#a4c56b71729947412b4c9bc5271cae76a "Write effectively the Sub Product initialized by catiav5w::InitProduct.") function. This function will give you a resulting DocID to insert the CATProduct into multi level Assemblies. //we close the CATProduct context and retrieve the resulting DocID [catiav5w::EndProduct](https://www.datakit.com/Doc_API_html/namespacecatiav5w.html#a4c56b71729947412b4c9bc5271cae76a)(ProdID2);  

# [](https://www.datakit.com/Doc_API_html/v5w_asm_how_to.html) Referencing existing files from a CATProduct

You can reference existing or previously created files into a CATProduct for theses extensions:

| File Extension | Function |
| --- | --- |
| .CATPart | [catiav5w::CreatePartDocId](https://www.datakit.com/Doc_API_html/namespacecatiav5w.html#a4f661a03a577274e60983059935c99f8 "Create a Part Reference and DocID related to a given CATPart.") (const [Dtk_string](https://www.datakit.com/Doc_API_html/class_dtk__string.html "This is a high level string class.")&inPartFileName, const [Dtk_string](https://www.datakit.com/Doc_API_html/class_dtk__string.html "This is a high level string class.")&inPartName, Dtk_ID &outDocId) |
| .CATProduct | [catiav5w::CreateProductDocId](https://www.datakit.com/Doc_API_html/namespacecatiav5w.html#ae7bd55340756aa2144249c236f8b0cd0 "Create a Product Reference and DocID related to a given CATProduct.") |
| .cgr | [catiav5w::CreateCGRDocId](https://www.datakit.com/Doc_API_html/namespacecatiav5w.html#a2f3f68535afba2b041a989a7ec20d5cf "Create a CGR Reference and DocID related to a given CGR File.") |
| .model - V4 file - | [catiav5w::CreateV4ModelDocId](https://www.datakit.com/Doc_API_html/namespacecatiav5w.html#a1c5bc3cb6340a740d919aa90279084a8 "Create a V4 Model Reference and DocID related to a given V4 Model File.") |

# [](https://www.datakit.com/Doc_API_html/v5w_asm_how_to.html) The Virtual Component writing step-by-step.

The most important to know is that a virtual component ALWAYS belongs to a CATProduct context.

 So you have to cal [catiav5w::InitProduct](https://www.datakit.com/Doc_API_html/namespacecatiav5w.html#a698099acf905c9d068f977416f0c34b1 "Initialize a sub Product during CATProduct process.") prior calling [catiav5w::InitVirtualComponent](https://www.datakit.com/Doc_API_html/namespacecatiav5w.html#a08a28823e24f13b309a3526fb9eddaee "Initialize a virtual component during CATProduct process.").

 Moreover you can add a virtual component instance only into the same product context that his creation.

 So you can only call [catiav5w::AddVirtualComponentInstance](https://www.datakit.com/Doc_API_html/namespacecatiav5w.html#a2fbaa24b0c3a158affdfbdb5c94b3b96 "Add an instance to a DocID into the Current (Sub/Root) CATProduct.") prior the [catiav5w::EndProduct](https://www.datakit.com/Doc_API_html/namespacecatiav5w.html#a4c56b71729947412b4c9bc5271cae76a "Write effectively the Sub Product initialized by catiav5w::InitProduct.") call.

 This piece of code is correct:

//we init a CATProduct context...

[catiav5w::InitProduct](https://www.datakit.com/Doc_API_html/namespacecatiav5w.html#a698099acf905c9d068f977416f0c34b1)( SubProductFileName, "SubProduct");

//we start a virtual component prototype

[catiav5w::InitVirtualComponent](https://www.datakit.com/Doc_API_html/namespacecatiav5w.html#a08a28823e24f13b309a3526fb9eddaee)("VirtualSubComponent1");

TransformationMatrix.[setOrigin](https://www.datakit.com/Doc_API_html/class_dtk__transfo.html#a418cf6193970c962140618fba7a740e1)(0,0,150);

[catiav5w::AddInstance](https://www.datakit.com/Doc_API_html/namespacecatiav5w.html#a847ad8c1edaf5d8b7369b052a6e983a2)(PartID, L"PartInstance", TransformationMatrix);

//we end the component prototype

[catiav5w::EndVirtualComponent](https://www.datakit.com/Doc_API_html/namespacecatiav5w.html#ac1238b1e47eb33c6f238c2329229e305)(CompID1);

//now we had the component instance into the CATProduct

[catiav5w::AddVirtualComponentInstance](https://www.datakit.com/Doc_API_html/namespacecatiav5w.html#a2fbaa24b0c3a158affdfbdb5c94b3b96)(CompID1, L"CompInstance", TransformationMatrix);

//we close the CATProduct context and retrieve the resulting DocID

[catiav5w::EndProduct](https://www.datakit.com/Doc_API_html/namespacecatiav5w.html#a4c56b71729947412b4c9bc5271cae76a)(ProdID2);

...

...whereas this piece of code is wrong:

...

//we init a CATProduct context...

catiav5w::InitProduct( SubProductFileName, "SubProduct");

//we start a virtual component prototype

[catiav5w::InitVirtualComponent](https://www.datakit.com/Doc_API_html/namespacecatiav5w.html#a08a28823e24f13b309a3526fb9eddaee)("VirtualSubComponent1");

TransformationMatrix.[setOrigin](https://www.datakit.com/Doc_API_html/class_dtk__transfo.html#a418cf6193970c962140618fba7a740e1)(0,0,150);

[catiav5w::AddInstance](https://www.datakit.com/Doc_API_html/namespacecatiav5w.html#a847ad8c1edaf5d8b7369b052a6e983a2)(PartID, L"PartInstance", TransformationMatrix);

//we end the component prototype

[catiav5w::EndVirtualComponent](https://www.datakit.com/Doc_API_html/namespacecatiav5w.html#ac1238b1e47eb33c6f238c2329229e305)(CompID1);

//we close the CATProduct context and retrieve the resulting DocID

[catiav5w::EndProduct](https://www.datakit.com/Doc_API_html/namespacecatiav5w.html#a4c56b71729947412b4c9bc5271cae76a)(ProdID2);

[catiav5w::AddVirtualComponentInstance](https://www.datakit.com/Doc_API_html/namespacecatiav5w.html#a2fbaa24b0c3a158affdfbdb5c94b3b96)(CompID1, L"CompInstance", TransformationMatrix); //ERROR: Component instanciation is not it the same context as its creation... 

[catiav5w::InitVirtualComponent](https://www.datakit.com/Doc_API_html/namespacecatiav5w.html#a08a28823e24f13b309a3526fb9eddaee)("SubComponent2"); //ERROR this virtual component doesn't belong to any product 

[catiav5w::AddInstance](https://www.datakit.com/Doc_API_html/namespacecatiav5w.html#a847ad8c1edaf5d8b7369b052a6e983a2)(PartID, L"PartInstance", TransformationMatrix);

[catiav5w::EndVirtualComponent](https://www.datakit.com/Doc_API_html/namespacecatiav5w.html#ac1238b1e47eb33c6f238c2329229e305)(CompID2);

# [](https://www.datakit.com/Doc_API_html/v5w_asm_how_to.html) Full Sample.

[Dtk_UUID](https://www.datakit.com/Doc_API_html/class_dtk___u_u_i_d.html)[ProcessPart](https://www.datakit.com/Doc_API_html/testlibcatiav5write_8cpp.html#afbc7fa6cdc116de4955729c6f3b88aba)(const[Dtk_string](https://www.datakit.com/Doc_API_html/class_dtk__string.html)& inOutputFile, const[Dtk_string](https://www.datakit.com/Doc_API_html/class_dtk__string.html)&[inReferenceName](https://www.datakit.com/Doc_API_html/namespacecatiav5w.html#a409bd4b479edbf92359ec83a1b2e9ecb))

{

//You init the Part writer 

[Dtk_UUID](https://www.datakit.com/Doc_API_html/class_dtk___u_u_i_d.html) PartUUID = [catiav5w::InitPart](https://www.datakit.com/Doc_API_html/namespacecatiav5w.html#af5bae72d1a24331b0fca64dc90fcbe4a)( inOutputFile, [inReferenceName](https://www.datakit.com/Doc_API_html/namespacecatiav5w.html#a409bd4b479edbf92359ec83a1b2e9ecb) );

//you create a Geometrical Set

[catiav5w::CreateNode](https://www.datakit.com/Doc_API_html/namespacecatiav5w.html#a6077f5ab7ec19654ab451c82cb1fdcd6)([catiav5w::NodeTypeGeometricSet](https://www.datakit.com/Doc_API_html/namespacecatiav5w.html#a62c9c5da69caf82f4acffc1d5584f62ba0b65dcd441ac2de3c47c1fe2eabe8b8e), L"MyGeometricalSet");

//...and you insert a point

[Dtk_Entity](https://www.datakit.com/Doc_API_html/class_dtk___entity.html) TmpPoint = [Dtk_EntityPtr::DtkDynamicCast](https://www.datakit.com/Doc_API_html/class_dtk___smart_ptr.html#a33ab67e92120260f4db0e2cd0cd57711)( [Dtk_Point::Create](https://www.datakit.com/Doc_API_html/class_dtk___point.html#a2c70a07cd7597441ff7cae85f06724a0)(10.,20.,30.) );

[catiav5w::WriteEntity](https://www.datakit.com/Doc_API_html/namespacecatiav5w.html#acc38ca2a51338a47d1d6699085c5d73e)(TmpPoint);

//Finally you close the Geometrical Set...

[catiav5w::CloseCurrentNode](https://www.datakit.com/Doc_API_html/namespacecatiav5w.html#a5a473c0114dcb139059ddcb940824d5e)();

//...and the Part writer

[catiav5w::EndPart](https://www.datakit.com/Doc_API_html/namespacecatiav5w.html#afcc32dcc194737abc4e78ea6bae4a5e2)();

//you return the Part UUID

return PartUUID;

}

void[ProcessAsm](https://www.datakit.com/Doc_API_html/testlibcatiav5write_8cpp.html#a1bd2ec5a2777f034171b0cbf43faac39)()

{

[Dtk_string](https://www.datakit.com/Doc_API_html/class_dtk__string.html) CATPartFileName = L"..\\SampleFiles\\dtk\\V5_sample.CATPart";

[Dtk_string](https://www.datakit.com/Doc_API_html/class_dtk__string.html) CGRFileName = L"..\\SampleFiles\\cgr\\Engine.cgr";

[Dtk_string](https://www.datakit.com/Doc_API_html/class_dtk__string.html) V4ModelFileName = L"..\\SampleFiles\\v4\\EngineComponent.model";

[Dtk_string](https://www.datakit.com/Doc_API_html/class_dtk__string.html) SubProductFileName = L"..\\SampleFiles\\dtk\\SubProduct.CATProduct";

[Dtk_string](https://www.datakit.com/Doc_API_html/class_dtk__string.html) RootProductFileName = L"..\\SampleFiles\\dtk\\RootProduct.CATProduct";

[Dtk_transfo](https://www.datakit.com/Doc_API_html/class_dtk__transfo.html) TransformationMatrix;

//First you have to initialize the CATIA V5 writer

[catiav5w::InitWrite](https://www.datakit.com/Doc_API_html/namespacecatiav5w.html#a1fdce5cda848b1e2d0a87ad67ef24ef0)(L"..\\SampleFiles\\dtk\\V5W_LogFile.log", NULL);

//The ProcessPart is an user implemented function to create a part

[Dtk_UUID](https://www.datakit.com/Doc_API_html/class_dtk___u_u_i_d.html) PartUUID = [ProcessPart](https://www.datakit.com/Doc_API_html/testlibcatiav5write_8cpp.html#afbc7fa6cdc116de4955729c6f3b88aba)(CATPartFileName, L"testPart");

[Dtk_ID](https://www.datakit.com/Doc_API_html/define_8h.html#af81989144af13cad1cc9a5ac8f49a357) PartID, V4ID, CgrID, ProdID,ProdID2, CompID1, CompID2;

//We create Doceument References to the CATPart file 

[catiav5w::CreatePartDocId](https://www.datakit.com/Doc_API_html/namespacecatiav5w.html#a4f661a03a577274e60983059935c99f8)(CATPartFileName, L"PartFile", PartUUID, PartID);

//...and to a CGR file

[catiav5w::CreateCGRDocId](https://www.datakit.com/Doc_API_html/namespacecatiav5w.html#a2f3f68535afba2b041a989a7ec20d5cf)( CGRFileName, "CGRFile", CgrID);

//...and finally to a CATIA V4 '.model' file

[catiav5w::CreateV4ModelDocId](https://www.datakit.com/Doc_API_html/namespacecatiav5w.html#a1c5bc3cb6340a740d919aa90279084a8)( V4ModelFileName, "V4File", V4ID);

//we init a CATProduct context...

[catiav5w::InitProduct](https://www.datakit.com/Doc_API_html/namespacecatiav5w.html#a698099acf905c9d068f977416f0c34b1)( SubProductFileName, "SubProduct");

//we start a virtual component prototype

[catiav5w::InitVirtualComponent](https://www.datakit.com/Doc_API_html/namespacecatiav5w.html#a08a28823e24f13b309a3526fb9eddaee)("VirtualSubComponent1");

 TransformationMatrix.[setOrigin](https://www.datakit.com/Doc_API_html/class_dtk__transfo.html#a418cf6193970c962140618fba7a740e1)(0,0,150);

[catiav5w::AddInstance](https://www.datakit.com/Doc_API_html/namespacecatiav5w.html#a847ad8c1edaf5d8b7369b052a6e983a2)(PartID, L"PartInstance", TransformationMatrix);

//we end the component prototype

[catiav5w::EndVirtualComponent](https://www.datakit.com/Doc_API_html/namespacecatiav5w.html#ac1238b1e47eb33c6f238c2329229e305)(CompID1);

//we start another virtual component prototype

[catiav5w::InitVirtualComponent](https://www.datakit.com/Doc_API_html/namespacecatiav5w.html#a08a28823e24f13b309a3526fb9eddaee)("VirtualComponent1");

//we add the sub component instance...

 TransformationMatrix.[setOrigin](https://www.datakit.com/Doc_API_html/class_dtk__transfo.html#a418cf6193970c962140618fba7a740e1)( 0.0,0.0,0.0);

[catiav5w::AddVirtualComponentInstance](https://www.datakit.com/Doc_API_html/namespacecatiav5w.html#a2fbaa24b0c3a158affdfbdb5c94b3b96)(CompID1, L"VirtualSubComponent1_Instance1", TransformationMatrix ); 

//we close the component prototype

[catiav5w::EndVirtualComponent](https://www.datakit.com/Doc_API_html/namespacecatiav5w.html#ac1238b1e47eb33c6f238c2329229e305)(CompID2);

//we insert a Part instance...

 TransformationMatrix.[setOrigin](https://www.datakit.com/Doc_API_html/class_dtk__transfo.html#a418cf6193970c962140618fba7a740e1)( 0.0,0.0,0.0);

[catiav5w::AddInstance](https://www.datakit.com/Doc_API_html/namespacecatiav5w.html#a847ad8c1edaf5d8b7369b052a6e983a2)(PartID, L"PartInstance", TransformationMatrix);

//...a CGR instance

 TransformationMatrix.[setOrigin](https://www.datakit.com/Doc_API_html/class_dtk__transfo.html#a418cf6193970c962140618fba7a740e1)( 0.0,500.0,0.0);

[catiav5w::AddInstance](https://www.datakit.com/Doc_API_html/namespacecatiav5w.html#a847ad8c1edaf5d8b7369b052a6e983a2)(CgrID, L"CGRInstance", TransformationMatrix);

//...and a V4 instance

 TransformationMatrix.[setOrigin](https://www.datakit.com/Doc_API_html/class_dtk__transfo.html#a418cf6193970c962140618fba7a740e1)( 0.0,-500.0,0.0);

[catiav5w::AddInstance](https://www.datakit.com/Doc_API_html/namespacecatiav5w.html#a847ad8c1edaf5d8b7369b052a6e983a2)(V4ID, L"V4Instance", TransformationMatrix);

//...and the main component instance

 TransformationMatrix.[setOrigin](https://www.datakit.com/Doc_API_html/class_dtk__transfo.html#a418cf6193970c962140618fba7a740e1)( 0.0,1000.0,0.0);

[catiav5w::AddVirtualComponentInstance](https://www.datakit.com/Doc_API_html/namespacecatiav5w.html#a2fbaa24b0c3a158affdfbdb5c94b3b96)(CompID2, L"VirtualComponent1_Instance1", TransformationMatrix);

//we close the CATProduct context and retrieve the resulting DocID

[catiav5w::EndProduct](https://www.datakit.com/Doc_API_html/namespacecatiav5w.html#a4c56b71729947412b4c9bc5271cae76a)(ProdID2);

//we create another CATProduct context

[catiav5w::InitProduct](https://www.datakit.com/Doc_API_html/namespacecatiav5w.html#a698099acf905c9d068f977416f0c34b1)( RootProductFileName, "RootProduct");

//and we insert another time the a part instance - multinstancing management -

 TransformationMatrix.[setOrigin](https://www.datakit.com/Doc_API_html/class_dtk__transfo.html#a418cf6193970c962140618fba7a740e1)( 0.0,0.0,50.0);

[catiav5w::AddInstance](https://www.datakit.com/Doc_API_html/namespacecatiav5w.html#a847ad8c1edaf5d8b7369b052a6e983a2)(PartID, L"PartInstance2", TransformationMatrix);

//and two instances to the first CATProduct file

 TransformationMatrix.[setOrigin](https://www.datakit.com/Doc_API_html/class_dtk__transfo.html#a418cf6193970c962140618fba7a740e1)( 1000.0,0.0,0.0);

[catiav5w::AddInstance](https://www.datakit.com/Doc_API_html/namespacecatiav5w.html#a847ad8c1edaf5d8b7369b052a6e983a2)(ProdID2, L"SubProductInstance", TransformationMatrix);

 TransformationMatrix.[setOrigin](https://www.datakit.com/Doc_API_html/class_dtk__transfo.html#a418cf6193970c962140618fba7a740e1)( -1000.0,0.0,0.0);

[catiav5w::AddInstance](https://www.datakit.com/Doc_API_html/namespacecatiav5w.html#a847ad8c1edaf5d8b7369b052a6e983a2)(ProdID2, L"SubProductInstance", TransformationMatrix);

//finally we close the second CATProduct...

[catiav5w::EndProduct](https://www.datakit.com/Doc_API_html/namespacecatiav5w.html#a4c56b71729947412b4c9bc5271cae76a)(ProdID);

//...and the Main writter

[catiav5w::EndWrite](https://www.datakit.com/Doc_API_html/namespacecatiav5w.html#a53eebf3a44ce97b6c7855e91519ec716)();

}

Here a snapshot of the resulting V5 Assembly (from Full Sample)

![Image 6](https://www.datakit.com/Doc_API_html/cv5w_asm_v5_write_result.png)

[Dtk_ID](https://www.datakit.com/Doc_API_html/define_8h.html#af81989144af13cad1cc9a5ac8f49a357)

uint32_t Dtk_ID

**Definition:** define.h:688

[Dtk_transfo](https://www.datakit.com/Doc_API_html/class_dtk__transfo.html)

This is the Transformation dedicated class.

**Definition:** dtk_transfo.hpp:19

[catiav5w::InitVirtualComponent](https://www.datakit.com/Doc_API_html/namespacecatiav5w.html#a08a28823e24f13b309a3526fb9eddaee)

Dtk_ErrorStatus InitVirtualComponent(const Dtk_string &inReferenceName, const catiav5w::FileDescription &inFileDescription=catiav5w::FileDescription())

Initialize a virtual component during CATProduct process.

[catiav5w::AddVirtualComponentInstance](https://www.datakit.com/Doc_API_html/namespacecatiav5w.html#a2fbaa24b0c3a158affdfbdb5c94b3b96)

Dtk_ErrorStatus AddVirtualComponentInstance(const Dtk_ID &inDocId, const Dtk_string &inInstanceName, const Dtk_transfo &inTransfo, Dtk_ID &outInstanceId)

Add an instance to a DocID into the Current (Sub/Root) CATProduct.

[ProcessAsm](https://www.datakit.com/Doc_API_html/testlibcatiav5write_8cpp.html#a1bd2ec5a2777f034171b0cbf43faac39)

Dtk_ErrorStatus ProcessAsm(const Dtk_string &inResultDirectory, const Dtk_string &inInputFilesDirectory)

**Definition:** testlibcatiav5write.cpp:312

[Dtk_transfo::setOrigin](https://www.datakit.com/Doc_API_html/class_dtk__transfo.html#a418cf6193970c962140618fba7a740e1)

void setOrigin(const Dtk_pnt &O)

Set a new O center point.

[catiav5w::NodeTypeGeometricSet](https://www.datakit.com/Doc_API_html/namespacecatiav5w.html#a62c9c5da69caf82f4acffc1d5584f62ba0b65dcd441ac2de3c47c1fe2eabe8b8e)

@ NodeTypeGeometricSet

**Definition:** catiav5w.hpp:426

[ProcessPart](https://www.datakit.com/Doc_API_html/testlibcatiav5write_8cpp.html#afbc7fa6cdc116de4955729c6f3b88aba)

Dtk_ErrorStatus ProcessPart(const Dtk_string &inOutputFile, const Dtk_string &inReferenceName)

**Definition:** testlibcatiav5write.cpp:32

[Dtk_string](https://www.datakit.com/Doc_API_html/class_dtk__string.html)

This is a high level string class.

**Definition:** dtk_string.hpp:53

[Dtk_Size_t](https://www.datakit.com/Doc_API_html/define_8h.html#a9b49974b7430e6b7734b27657bf75af3)

size_t Dtk_Size_t

**Definition:** define.h:711

[catiav5w::WriteEntity](https://www.datakit.com/Doc_API_html/namespacecatiav5w.html#acc38ca2a51338a47d1d6699085c5d73e)

Dtk_ErrorStatus WriteEntity(const Dtk_EntityPtr &inEntity)

Write the entity provided in parameter.

[Dtk_UUID](https://www.datakit.com/Doc_API_html/class_dtk___u_u_i_d.html)

**Definition:** dtk_uuid.hpp:8

[catiav5w::CreateNode](https://www.datakit.com/Doc_API_html/namespacecatiav5w.html#a6077f5ab7ec19654ab451c82cb1fdcd6)

Dtk_ErrorStatus CreateNode(const NodeType &inNodeType, const Dtk_string &inNodeName=Dtk_string())

Create a node in the Specification Tree.

[catiav5w::InitProduct](https://www.datakit.com/Doc_API_html/namespacecatiav5w.html#a698099acf905c9d068f977416f0c34b1)

Dtk_ErrorStatus InitProduct(const Dtk_string &inFileName, const Dtk_string &inReferenceName, const catiav5w::FileDescription &inFileDescription=catiav5w::FileDescription())

Initialize a sub Product during CATProduct process.

[catiav5w::CreateCGRDocId](https://www.datakit.com/Doc_API_html/namespacecatiav5w.html#a2f3f68535afba2b041a989a7ec20d5cf)

Dtk_ErrorStatus CreateCGRDocId(const Dtk_string &inCGRFileName, const Dtk_string &inCGRName, Dtk_ID &outDocId)

Create a CGR Reference and DocID related to a given CGR File.

[catiav5w::inReferenceName](https://www.datakit.com/Doc_API_html/namespacecatiav5w.html#a409bd4b479edbf92359ec83a1b2e9ecb)

const Dtk_string & inReferenceName

**Definition:** catiav5w.hpp:447

[catiav5w::InitPart](https://www.datakit.com/Doc_API_html/namespacecatiav5w.html#af5bae72d1a24331b0fca64dc90fcbe4a)

Dtk_ErrorStatus InitPart(const Dtk_string &inOutputFile, const Dtk_string &inReferenceName, Dtk_UUID &outPartUUID, const catiav5w::FileDescription &inFileDescription=catiav5w::FileDescription())

Initialize the part

[catiav5w::EndVirtualComponent](https://www.datakit.com/Doc_API_html/namespacecatiav5w.html#ac1238b1e47eb33c6f238c2329229e305)

Dtk_ErrorStatus EndVirtualComponent(Dtk_ID &outDocId)

End - and write - the virtual component initialized by catiav5w::InitVirtualComponent.

[Dtk_SmartPtr< Dtk_Entity >::DtkDynamicCast](https://www.datakit.com/Doc_API_html/class_dtk___smart_ptr.html#a33ab67e92120260f4db0e2cd0cd57711)

static Dtk_SmartPtr< Dtk_Entity > DtkDynamicCast(const Dtk_SmartPtr< T2 >&p)

**Definition:** util_ptr_dtk.hpp:101

[catiav5w::AddInstance](https://www.datakit.com/Doc_API_html/namespacecatiav5w.html#a847ad8c1edaf5d8b7369b052a6e983a2)

Dtk_ErrorStatus AddInstance(const Dtk_ID &inDocId, const Dtk_string &inInstanceName, const Dtk_transfo &inTransfo, Dtk_ID &outInstanceId)

Add an instance to a DocID into the Current (Sub/Root) CATProduct.

[catiav5w::CreateV4ModelDocId](https://www.datakit.com/Doc_API_html/namespacecatiav5w.html#a1c5bc3cb6340a740d919aa90279084a8)

Dtk_ErrorStatus CreateV4ModelDocId(const Dtk_string &inV4ModelFileName, const Dtk_string &inV4ModelName, Dtk_ID &outDocId)

Create a V4 Model Reference and DocID related to a given V4 Model File.

[catiav5w::EndWrite](https://www.datakit.com/Doc_API_html/namespacecatiav5w.html#a53eebf3a44ce97b6c7855e91519ec716)

Dtk_ErrorStatus EndWrite()

Free the Catia V5 Writer

[catiav5w::CreatePartDocId](https://www.datakit.com/Doc_API_html/namespacecatiav5w.html#a4f661a03a577274e60983059935c99f8)

Dtk_ErrorStatus CreatePartDocId(const Dtk_string &inPartFileName, const Dtk_string &inPartName, Dtk_ID &outDocId)

Create a Part Reference and DocID related to a given CATPart.

[Dtk_Point::Create](https://www.datakit.com/Doc_API_html/class_dtk___point.html#a2c70a07cd7597441ff7cae85f06724a0)

static Dtk_PointPtr Create(const Dtk_Point &in)

Calls copy constructor to allocate a new object.

[catiav5w::EndProduct](https://www.datakit.com/Doc_API_html/namespacecatiav5w.html#a4c56b71729947412b4c9bc5271cae76a)

Dtk_ErrorStatus EndProduct(Dtk_ID &outDocId)

Write effectively the Sub Product initialized by catiav5w::InitProduct.

[catiav5w::CloseCurrentNode](https://www.datakit.com/Doc_API_html/namespacecatiav5w.html#a5a473c0114dcb139059ddcb940824d5e)

Dtk_ErrorStatus CloseCurrentNode()

close the current node previously created by catiav5w::CreateNode.

[catiav5w::EndPart](https://www.datakit.com/Doc_API_html/namespacecatiav5w.html#afcc32dcc194737abc4e78ea6bae4a5e2)

Dtk_ErrorStatus EndPart()

Free data allocated by catiav5w::InitPart

[catiav5w::InitWrite](https://www.datakit.com/Doc_API_html/namespacecatiav5w.html#a1fdce5cda848b1e2d0a87ad67ef24ef0)

Dtk_ErrorStatus InitWrite(const Dtk_string &inLogFile, Licence_dtk inLicFct, const WriteOptions &inOptions=WriteOptions())

Initialize the Catia V5 Writer

[Dtk_Entity](https://www.datakit.com/Doc_API_html/class_dtk___entity.html)

**Definition:** util_ent_dtk.hpp:371
