
===== as/c_12t85m8.json (7 comments)
[2023-04-20 u/Pionosis] 3DExperience is built such that you don't need to worry about files as they are simply server entries to be worked on. However the native format in the background I was told was 3DXML. And yes 3DX can work with 3DXMLs totally fine
[2023-04-20 u/fofof] Yes! They are the same format. There is some compatibility mapping between versions though - especially if your data has fancy stuff like composites, electrical, etc… Which way are you trying to go? V6 to 3DX?
[2023-04-20 u/Intelligent-Lab8688] Thanks for the quick response! To be more specific, I work with a CAE software which has a translator for CATIA V6 3dxml file. I was wondering if the same translator should work for a file coming from 3DExperience.
[2023-04-20 u/fofof] Yeah, that should work the same for both.
[2023-04-20 u/Intelligent-Lab8688] Thanks for your input.
[2023-04-20 u/Beowuwlf] It should work the same as long as you aren’t using any custom data or anything
[2023-04-21 u/lulzkedprogrem] 3Dxml format can be read by 3DExperience.

===== as/c_17k20mo.json (2 comments)
[2023-10-30 u/bryansj] It sounds like maybe you've moved or renamed the files and the recent selections are invalid. You can simply use Open and browse to it again. Or drag the file into the CATIA window. Or double-click the file. Or insert existing component.
[2023-10-30 u/username___6] Maybe you should tell what the error says. Usual reason: The file was saved in the newer version and CATIA doesn't support opening a file in previous versions. To confirm, open the file in notepad and search for "v5r3". If you find "v5r31", "v5r32" or "v5r33", it's saved in the newer version. You can ask the creator to save the file in lower version, or export as step.

===== as/c_19ctif0.json (1 comments)
[2024-01-22 u/BarkleEngine] Try these settings: Tools>Options>General: uncheck "Load Referenced Documents" Tools>Options>Infrastructure>Product Structure> General: Work with the cache system Tools>Options>Infrastructure>Product Structure>Product Visualization: Do not activate default shapes on open. And construct your assemblies leaf subassemblies first and work up the assembly.

===== as/c_1cj2ccz.json (2 comments)
[2024-05-03 u/bryansj] I have yet to use this, but I've booked marked it for when that day comes. [https://wikifactory.com/pricing/](https://wikifactory.com/pricing/)
[2024-05-23 u/Much_Possible_2108] Unfortunately no but zw3d or cadbro good works viewer or different fotmats support.

===== as/c_1diplrm.json (2 comments)
[2024-06-18 u/El-MIRAGE16] send me the catpart
[2024-06-18 u/No-Increase-1558] If u have soldworks or inventor, you can open it and save as a step Or open it with catia and save it step

===== as/c_1ejcjrp.json (8 comments)
[2024-08-03 u/starchickens] Try the service [https://cadmonster.org](https://cadmonster.org) The conversion speed is not very fast (sometimes the file arrives in a few hours), but it supports various unusual file formats
[2024-08-03 u/leperfectbaguette] thanks for the answer. i'll try to see if it works :)
[2024-08-03 u/leperfectbaguette] seems to be that the file is not actually a .model file according to cad monster
[2024-08-03 u/burgd] .model is a catia v4 file. It should open. You can also try tools-utility V4toV5 converter not sure what license it's tied to though.
[2024-08-04 u/Stripe_Show69] You can right click copy the name from the tree and paste special into a part body.
[2024-08-04 u/bryansj] OP doesn't have CATIA.
[2024-08-04 u/bryansj] As this .model is from, I'm assuming, a game then developer just used the .model extension for models and has nothing to do with CATIA. It is probably something like a Blender file renamed.
[2024-08-05 u/3DExperience] What type of file would you like it converted to?

===== as/c_1fpgjx4.json (5 comments)
[2024-09-25 u/Pirhotau] Try to drag and drop parameters. When I have a lot of parameters, I usually create geometrical sets and put parameters in. In this way, I can rename each geometrical set and group parameters.
[2024-09-25 u/Ape_of_Leisure] [Creating sets of parameters](http://catiadoc.free.fr/online/kwrug_C2/kwrugat1006.htm) Right click on the parameter and you can reorder/place as you like. I usually create sets of parameters and group them by categories.
[2024-09-26 u/Lukrative525] I'm so glad I came here to ask, thanks!
[2024-09-26 u/Lukrative525] Thanks for the help, and great link!
[2024-10-16 u/skill_lync] Hey, In CATIA V5, you can reorder parameters in the Specification Tree to better organize them. Here's how to do it: Reordering Parameters in CATIA V5 1. Open Your Part File: Launch CATIA V5 and open the part containing the parameters you want to reorder. 2. Access the Parameters: Go to the Parameters section in the Specification Tree. This is typically found in the left pane. 3. Select Parameters: You can select multiple parameters by holding down the \`Ctrl\` key and clicking on them, or click and drag to select a range. 4. Reorder Parameters: you can, - Right-click on a parameter and choose Cut. - Right-click on the desired location in the tree and select Paste. This effectively moves the parameter to the new location. 5. Grouping Related Parameters: Consider using a naming convention to group related parameters together. For example, prefixing similar parameters can help keep them vi

===== as/c_1r239nc.json (1 comments)
[2026-02-11 u/bryansj] CATIA V5 can open them as a dumb solid (step like). Just import them into an assembly and measure.

===== as/c_v7x5sx.json (7 comments)
[2022-06-08 u/fofof] I can't speak for viewing GD&T in Fusion360 or Solidworks but if you have a relatively new version of CATIA and the right licenses you can export the part into STEP AP242 format that will contain the GD&T.
[2022-06-08 u/xDecenderx] You can also save it has a 3dxml file and use a free viewer to view the gD&t, if it was set up correctly.
[2022-06-09 u/king-charles-king] Do you have a preference to a viewer?
[2022-06-09 u/king-charles-king] I wish I could do that… unfortunately the engineers giving me the files would rather not put in the effort to do that no matter how much I beg
[2022-06-09 u/xDecenderx] The dessault free one is what we used at work for non catia users.
[2022-06-10 u/king-charles-king] Do you happen to know if it’s “3DXML Viewer”? Or what’s the name of it?
[2022-06-10 u/xDecenderx] That is the name, they didn't get really creative with giving it a fancy name. https://www.3ds.com/products-services/3d-xml/downloads/
