Title: STEP: Import

URL Source: http://catiadoc.free.fr/online/itfug_C2/itfugbt0101.htm

Markdown Content:
![Image 1](http://catiadoc.free.fr/online/icons_C2/common/atarget.gif)This task shows you how to import to a CATPart or CATProduct document 

 the data contained in a STEP AP203 / AP214 file.
It is also possible to insert a STEP file as an existing component in a CATProduct.
![Image 2](http://catiadoc.free.fr/online/icons_C2/common/ainfo.gif)Regarding AP214, both STEP AP 214 IS and STEP AP 214 DIS files are read.[](http://catiadoc.free.fr/online/itfug_C2/itfugbt0101.htm)
The level of Recommended Practices published by the CAx Implementor Forum applied by the translator at import and export are the following :
The table entitled [What about the elements you import ?](http://catiadoc.free.fr/online/itfug_C2/itfugbt0101.htm#ix-STEP:imported%20elements)

 provides information on the entities you can import. 

 You can find further information in the Advanced Tasks: 
*   [Trouble Shooting](http://catiadoc.free.fr/online/itfug_C2/itfugat0101.htm#hj-import),
*   [Best Practices](http://catiadoc.free.fr/online/itfug_C2/itfugat0102.htm#hj-import),
*   [FAQ](http://catiadoc.free.fr/online/itfug_C2/itfugat0103.htm#hj-import),
*   [VBScript Macros](http://catiadoc.free.fr/online/itfug_C2/itfugat0104.htm#ix-STEP:import%20VBScript%20macros).

and in the Customizing [STEP Settings](http://catiadoc.free.fr/online/bascuitf_C2/bascuitf0100.htm#hj-import) chapter.

Statistics about each import operation can be found in the [report file and the error file](http://catiadoc.free.fr/online/itfug_C2/itfugbt0101.htm#ix-STEP:report%20file).
![Image 3](http://catiadoc.free.fr/online/icons_C2/common/ascenari.gif)1. Depending on your configuration: Click the Open icon![Image 4](http://catiadoc.free.fr/online/icons_C2/images/I_OpenP2.gif) or select the File > Open command. The File Selection dialog box is displayed. or Insert/Existing component command[](http://catiadoc.free.fr/online/itfug_C2/itfugbt0101.htm). The File Selection dialog box is displayed. 2. Set the .stp or .step extension in the Files of type field. [](http://catiadoc.free.fr/online/itfug_C2/itfugbt0101.htm) This displays all .stp or .step files contained in the selected directory : ![Image 5](http://catiadoc.free.fr/online/itfug_C2/images/bt053NLS.gif) 3. Select the .stp or .step file of your choice (MoldedPart.stp, in our example) and click Open.
![Image 6](http://catiadoc.free.fr/online/icons_C2/common/ainfo.gif)What is then displayed depends on the contents of the STEP file. 

*   For the File/Open command:
    *   If the STEP file contains a normalized assembly structure, 

 a CATProduct document is created.

    *   If the STEP file does not contain any geometrical and topological data, 

 the components will be visible only in the Specification Tree.

    *   If the STEP file contains also geometrical and topological data, 

 all the components will be present in the Geometry Space and in the Specification Tree.

    *   If the STEP file contains only geometrical and topological data, a CATPart document is created.

> The geometrical elements of the faces, which could not be transferred, 
> 
>  are created in the NO SHOW space. In the NO SHOW space, you can 
> 
>  visualize the Surface supports and the 3D Curves).

*   For the Insert/Existing component command: 
    *   if the STEP file contains no assembly information, it is converted to a CATPart,
    *   if the STEP file contains assembly information, it is converted to a CATProduct 

 referencing several CATPart documents.

> The resulting document is inserted in the current CATProduct document, 
> 
>  and the graphic window is updated (specification tree and geometry).
![Image 7](http://catiadoc.free.fr/online/icons_C2/common/awarning.gif)*   The reference to the STEP file is lost, so any update of the STEP file will have no effect 

 in the CATProduct.
*   For both commands: 
    *   The reference planes are hidden.
    *   A Geometrical Set is always created. It may be empty:
        *   it will contain the valid surfaces imported, if any.
        *   it is empty if there is no valid surfaces, e.g. when the element imported is a solid, 

 or when all surfaces are invalid.
        *   invalid surfaces are sent to a specific Geometrical Set (FaceKO#xxx)
Several STEP options can be customized: 
*   [Continuity optimization of curves and surfaces,](http://catiadoc.free.fr/online/bascuitf_C2/bascuitf0100.htm#ix-STEP:continuity%20optimization%20of%20curves%20and%20surfaces) to optimize curves and surfaces.
*   [Validation Properties](http://catiadoc.free.fr/online/bascuitf_C2/bascuitf0100.htm#ix-STEP:validation%20properties), to check the quality of the transfer.
*   [Groups (Selection Sets)](http://catiadoc.free.fr/online/bascuitf_C2/bascuitf0100.htm#ix-STEP:groups%20(selection%20sets)), to activate/de-activate the transfer of groups mapped with Selection Sets.
*   [Detailed report](http://catiadoc.free.fr/online/bascuitf_C2/bascuitf0100.htm#ix-STEP:detailed%20report), to set the level of details of the transfer log.
![Image 8](http://catiadoc.free.fr/online/icons_C2/common/aendtask.gif)
