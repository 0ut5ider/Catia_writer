Title: Running the CATDMUUtility Batch Process

URL Source: http://catiadoc.free.fr/online/dmnug_C2/dmnugat0401.htm

Markdown Content:
![Image 1](http://catiadoc.free.fr/online/icons_C2/common/atarget.gif)The CATDMUUtility is a batch process enabling the generation of cgr, 3dmap, hcg, wrl and NCGM formats from a CATIA file or from a MULTICAD file. It can also process files accessed in a PDM database, e.g. ENOVIA VPM or ENOVIA V5 VPM.
![Image 2](http://catiadoc.free.fr/online/icons_C2/common/ainfo.gif)All paths indicated in the CATDMUUtility command line must be absolute paths.
![Image 3](http://catiadoc.free.fr/online/icons_C2/common/awarning.gif)When using input data that contains references to a PDM system, it is imperative that you be connected to that PDM system while the CATDMUUtility process is running.
![Image 4](http://catiadoc.free.fr/online/icons_C2/common/anew.gif)[](http://catiadoc.free.fr/online/dmnug_C2/dmnugat0401.htm)The [-NavRep](http://catiadoc.free.fr/online/dmnug_C2/dmnugat0401.htm#hj-navrep) option enables you to generate Navigation Representations.
The -3dxml option enables you to generate 3D XML files for CATParts.
![Image 5](http://catiadoc.free.fr/online/icons_C2/common/ascenari.gif)1.   Prepare the Input file defining conversion parameters.
A typical computation parameters file looks like this:
**Example 1:**

CATDMUUtility -f inputfile -cgr outputfile1 [-nolod] [-sag value] [-3dmap outputfile2] [-vox value2] [-unit value3]

**Example 2:**

CATDMUUtility -l inputliste -db VPM -user username -pwd password -server servername

 -cgr -cache

**Example 3:**

CATDMUUtility -l inputliste -cgr -wrl -cache

**Example of input file:**

*   **Under WINDOWS**

"e:\New A\CRIC_BRANCH_1.CATPart"

 e:\B15doc\online\dmnug\samples\CRIC_BRANCH_1.CATPart

 e:\B15doc\online\dmnug\samples\GARDENAATOMIZER.model

*   **Under UNIX**

/usr/B05doc/online/dmnug/samples/CRIC_BRANCH_1.CATPart
![Image 6](http://catiadoc.free.fr/online/icons_C2/common/ainfo.gif)It is possible to use DLNames. The use of a DLName is indicated in the CATDMUUtility by the following string:**CATDLN://**
Examples:

UNIX:

*   CATDMUUtility -f CATDLN://TEST/model.model -cgr -cache

Windows:

*   CATDMUUtility -f CATDLN://TEST\model.model -cgr CATDLN://model.cgr
*   CATDMUUtility -f CATDLN://TEST\model.model -cgr e:\tmp\model.cgr
DLNames are supported for CATIA file definition in the CATDMUUtility. For more information on DLNames, see the Infrastructure Guide, [_Administrating Data Using the DLName Mechanism_](http://catiadoc.free.fr/online/basil_C2/basilcuDLNameBatch01.htm)_._
However, DLNames are supported only for CATIA files, i.e. in order to indicate a .txt file as an input parameter, it is necessary to supply an absolute path, e.g.
> CATDMUUtility -l /tmp/list.txt -cgr -cache
> 
> 
> (CATDMUUtility -l CATDLN://TEST/list.txt -cgr -cache would not work.)

The .txt file, of course, can contain DLNames, e.g.

> CATDLN://TESTDLN/model.model
> 
>  /tmp/users/mypart.CATPart
> 
>  CATDLN://DLN/mycgr.cgr
![Image 7](http://catiadoc.free.fr/online/icons_C2/common/ainfo.gif)Note: Special characters []  identify optional parameters.

 Please find below the different options available input, output:
![Image 8](http://catiadoc.free.fr/online/icons_C2/common/ainfo.gif)If you specify an extension in the output file name which isn't the correct extension for the output 

 option used, the correct extension is added to the output filename. The only exception to this feature is the -box output option, with which you can choose any extension you wish.
Example: 

 If you type: CATDMUUtility -f .../MyPart.CATPart -cgr .../MyResult.CATPart

 the resulting output file will be: .../MyResult.CATPart.cgr
### Input Options
**-f** : Input file with appropriate extension. A path must follow the option.
It is now possible to convert a V4 cgr file to a V5 cgr file. The -f input file should be a V4 cgr file and the -cgr output file should specify the name of what will be the new V5 cgr file. The -f option is mandatory, the -cache option cannot be used for the conversion of cgr files.
**-l** : Input list of model with **-f,** or database identifiers with **-db** option (note: the **-cache** option is mandatory in case the database identifiers are used). 
**-db**: Input database type: For processing data stored in a PDM database. For details on using the -db option, see [Accessing Data in a PDM Database](http://catiadoc.free.fr/online/dmnug_C2/dmnugat0411.htm).

> It is mandatory to use either:
> 
> 
> *   the **-l**option
> *   for database type ENOVIA VPM, the **-coid**,**-compid**,**-catenv**and**-cattab**options
> *   for database type ENOVIA V5 VPM, an appropriate identifier
> 
> 
> You cannot use the **-f** option with the -db option.

Generic example for CATDMUUtility:

CATDMUUtility -db VPM -user $user_db -pwd $pwd_db -server $server_name -coid $coid_nb -compid $compid_nb -cattab $table_name -catenv $env_name -cgr (if you want to tessellate into a cgr) $output_file_path or -cache (if you want the outputfile to be placed in the cache)
**-coid** : Input identifier of the ENOVIA VPM data to convert. 

 The **-db**, **-compid**, **-catenv** and **-cattab** options are mandatory.
**-compid** : Input identifier of the ENOVIA VPM data to convert. 

 The **-db**, **-coid**, **-catenv** and **-cattab** options are mandatory.

**-catenv** : Input identifier of the ENOVIA VPM data to convert. 

 The **-db**,**-coid**, **-compid** and **-cattab** options are mandatory.

**-cattab** : Input identifier of the ENOVIA VPM data to convert. 

 The **-db**, **-coid**, **-compid** and **-catenv** options are mandatory.
### Output Options
**-cgr** : Output file for cgr corresponding to the input file.A path must be indicated after the option. If no output file name is mentioned, output file will be generated in input file directory.
**-jpg** : Output file for jpg corresponding to the input file. The input file can be of format CATPart, model or cgr. This option cannot be used with  -db, -cache or -mp options. If no output file name is mentioned, output file will be generated in input file directory.
The following options are now available for specifying jpg output. These options can only be used with the **-jpg** option. 
**-xsize** : Specifies the horizontal size of the generated jpg file in pixels. An integer value is required.

**-ysize** : Specifies the vertical size of the generated jpg file in pixels. An integer value is required.

> Note: The default jpg size is 140 pixels * 120 pixels. Accordingly, if only one of the two parameters is specified, the other parameter be valuated to its default size.

**-camera** : Specifies the camera (viewpoint) used to generate the jpg file. A camera name is required. The specified viewpoint can be a standard view or a camera. A viewpoint name containing blanks should be surrounded by quotation marks, e.g. -camera "* iso".

> Examples:
> 
> 
> -camera "* iso"
> 
>  -camera "Camera 1"

**-viewmode** : Specifies the view mode {shading, shadingedges, wireframe, material}. A mode name is required.

> - shading for display shading representation 
> 
>  - shadingedges for display shading with edges representation
> 
>  - wireframe for display wireframe representation 
> 
>  - material for display material representation

**-bk** : Specifies the background color of the generated jpg file. The color can be either white of the background color currently defined via Tools > Options > General > Visualization:

> Examples:
> 
> 
> -bk 0 (specifies the currently defined background color)
> 
> -bk 1 (specifies a white background)
**-hcg** : Output file for hcg corresponding to the input file. A path must be indicated after the option, if no path is specified the output will be written into the cache by using-cache option. If no output file name is mentioned, output file will be generated in input file directory.
**-NCGM** : Output file for NCGM corresponding to the input file. A path must be indicated after the option, if no path is specified the output will be written into the cache by using the

-cache option. If no output file name is mentioned, output file will be generated in input file directory.

**-3dmap**: Output file for 3dmap corresponding to the input file. A path must be indicated after the option, if no path is specified the output will be written into the cache by using -cache option. If no output file name is mentioned, output file will be generated in input file directory.

**-wrl** : Output file for vrml corresponding to the input file. A path must be indicated after the option,if no path is specified the output will be written into the cache by using -cache option. If no output file name is mentioned, output file will be generated in input file directory. Note: In batch mode, as there is no editor, the wrl file will not contain any viewpoints.

**-product**: Output file for CATProduct documents generation from an assembly (MultiCAD or CATIA). The linked documents will be computed if -cgr, -3dmap ... options are specified.

Example:

```
CATDMUUtility -f E:\Assembly.asm 
     -product E:\Assembly.CATProduct 
     -cgr -cache
```

**-box** : Switch to generate the bounding box corresponding to the input file. The **-f** option is mandatory. If the input file is not a cgr file, then the -cgr option is necessary. This option is not compatible with the -cache option.

Examples:

```
CATDMUUtility -f e:\tmp\mycgr.cgr 
     -box e:\tmp\mycgr.cgr
```
**-vps** : Output file for vps corresponding to the input file.
The voxel size value can be specified using the –vox option. If the option –vox is omitted, the voxel size value will be retrieved from the CATSettings (default value = 5mm). The minimum voxel size value is 1mm.

The vps files accuracy can be specified using the –vpssag option. If the –vpssag option is specified, vps files are generated with the voxel size and triangle accuracy. If the option is omitted, computation is performed with only voxel size.

Example:

```
CATDMUUtility -f e:\tmp\mypart.CATPart -vps –vox 10 –cache 
     -vpssag
```
**-3dxml** : Output file for 3D XML. The generation of a 3D XML file is only possible for input file of type .CATPart.
Example:

`CATDMUUtility -f e:\tmp\mypart.CATPart -3dxml –cache`
![Image 9](http://catiadoc.free.fr/online/icons_C2/common/anew.gif)**[](http://catiadoc.free.fr/online/dmnug_C2/dmnugat0401.htm)-NavRep** : Output file for Navigation Representations corresponding to the input file.A path must be indicated after the option. If no output file name is mentioned, output file will be generated in input file directory (NavReps cannot be generated into the cache). It is possible to use CATProducts and CATParts both from file and database.
### Computing Options
**-mp** : CATDMUUtility batch will be launched in multi-process mode. Multi-process parameters must be set in : [Tools > Options > Digital MockUp > Multiprocess Settings](http://catiadoc.free.fr/online/bascudmn_C2/bascudmn0500.htm). The -l and -cache options are mandatory.
Example: CATDMUUtility -l e:\tests\lists\list1.txt -cgr -cache -mp
**-timeout** : -timeout time: set the time out. After this time, child processes will be killed, on the assumption that they've entered a CPU loop. Available with multi-process mode (-mp) only.
![Image 10](http://catiadoc.free.fr/online/icons_C2/common/ap2.gif)**-process** number_of_processes : set the number of child processes. Available with multi-process mode (-mp) only.
**-filter** : -filter <filter.txt> : . This option is only available if the input file is a model, CATPart or CATProduct. The output file must be a cgr, wrl or hcg. The file  filter.txt is a list of filter rules. See [Using Visualization Filters](http://catiadoc.free.fr/online/basug_C2/basugbt2402.htm).
**-apps** : Enables eventual access to V4 comment pages and V4 layers and filters in visualization mode : {com | lnf} 
> The type of appended data must follow the -apps option:
> 
> 
> *   com for V4 comment pages
> *   lnf for V4 layers and filters
> *   all for V4 comment pages, layers and filters
> 
> 
> The **-cgr** and **-cache** options are mandatory.
[**-vox** : Switch to generate 3map with a specified voxel value. Its use is mandatory after -3dmap option. A float value is required. **-sag** : Optional switch to generate cgr with a specified sag value. A float value is required. Default value is defined in the settings.](http://catiadoc.free.fr/online/dmnug_C2/dmnugat0401.htm)
Note: The sag option does not work with certain V4 models (e.g. solids).
**-sagon**: Optional switch enabling you to re-generate a cgr with a specified sag value. A float value is required. Available only with the -cache and -sag options. Works only for input files that are .CATPart or .model. The default value is defined in the settings.

 Previously, if you modified the sag value, the cgr was not updated in the cache.
Example:

CATDMUUtility -f e:\tmp\model.model -cgr -sag 0.2 -cache

 Then CATDMUUtility -f e:\tmp\model.model -cgr -sag 0.4 -cache

 In the cache, you would find your cgr still had a sag value of 0.2.

Now, if you modify the sag value using the -sagon option, CATDMUUtility will take the new value into account.

CATDMUUtility -f e:\tmp\model.model -cgr -sag 0.4 -sagon -cache

 In the cache, you will find your cgr now has a sag value of 0.4
**-keepsag**: Activate this switch to re-tessellate a cgr, keeping the same sag value. The **-force** option is mandatory when using -keepsag. You should **not** use **-sag** option with -keepsag.
If cgr doesn't exist, it is created with default sag value ( settings ).

Examples :

CATDMUUtility -f e:\tests\CATPart\cylinder.CATPart -cgr e:\tmp\keepsag.cgr -keepsag -force 

 CATDMUUtility -f e:\tests\CATPart\cylinder.CATPart -cgr -cache -keepsag -force 

 CATDMUUtility -l e:\tests\list\list.txt -cgr -cache -keepsag -force
**-nolod** : Optional switch to generate CGR without Level Of Detail (LOD) 
**-unit** : Optional switch to compute in the appropriate unit { mm, cm, m, inch, foot }

 Default value is input millimeter : mm

**-cache** : Optional switch to generate files directly in the cache directory (note: this option is mandatory if you are using the -l option).
**-log**: Store all the error messages in a log file. If no log file is specified, CATDMUUtility creates one in the temporary directory
Examples :

CATDMUUtility -f e:\tmp\model.model -cgr -cache -log e:\tmp\logfile.txt CATDMUUtility -f e:\tmp\model.model -cgr -cache -log

**-force**: Rebuild the output file if the option is activated (You have generated an output file, and you want to update it : use the -force option) Limitation : Only available with -cache option

Examples :

Test 1 : CATDMUUtility -f e:\tmp\model.model -cgr -cache

 It generates a cgr file in the cache, (at 12h00min).

 Then : CATDMUUtility -f e:\tmp\model.model -cgr -cache -force

 It rebuilds a cgr file in the cache (at 12h02min).

If the options are different, CATDMUUtility takes it into account :

Test 2 : CATDMUUtility -f e:\tmp\model.model -cgr -sag 0.2 -cache

 This generates a cgr file in the cache, with a sag of 0.2

 Then CATDMUUtility -f e:\tmp\model.model -cgr -sag 0.6 -cache -force

 It forces the generation of a cgr file in the cache, with a sag of 0.6

Test 3 : CATDMUUtility -f e:\tmp\model.model -3dmap -vox 20 -cache

 This generates a 3dmap file in the cache, with a voxel size of 20 mm.

 Then CATDMUUtility -f e:\tmp\model.model -3dmap -vox 10 -cache

 This forces the generation of a 3dmap file in the cache, with a voxel size of 10 mm.
**Note:**The contents of the input file list for the ENOVIA VPM database must be formatted as follows: 
> COID1 COMPID1 CATENV1 CATAB1
> 
>  COID2 COMPID2 CATENV2 CATAB2
> 
>  ...
![Image 11](http://catiadoc.free.fr/online/icons_C2/common/awarning.gif)To use this option, make sure you work with the Cache system. For this:

 select Tools>Options>Infrastructure>Cache Management
![Image 12](http://catiadoc.free.fr/online/icons_C2/common/ainfo.gif)For more detailed information, see the _Infrastructure User's Guide,_[_Cache Management_](http://catiadoc.free.fr/online/bascupst_C2/bascupst0100.htm).
1.   Run the following shell to start the batch process:

**On UNIX**:

*   Place yourself in the following directory:

 cd $install_path/code/command
*   Run the command:

./catstart -run "CATDMUUtility -f inputfile -cgr outputfile1"

**On Windows**:

*   Write a shell script containing the following lines:

cd $install_path\code\bin

 CATDMUUtility -f inputfile -cgr outputfile1
*   Run the shell.

Note: The $install_path is the path of the installation directory or folder. For more information on installing DMU, see the _Installation User's Guide_.
A user interface is now available for running the CATDMUUtility batch.
1.   In the menu bar, select Tools > Utility.

 The Batch Monitor dialog box appears.

![Image 13](http://catiadoc.free.fr/online/dmnug_C2/images/dmuutility1NLS.gif)

1.   Select the CATDMUUtility batch from the proposed list.

> A dialog box will appear in which you can enter the same information you would otherwise have entered in a line command:
> 
> 
> *   Input documents
> *   Output options
> *   Output location
> *   Advanced options (accessed by clicking Advanced button)

![Image 14](http://catiadoc.free.fr/online/dmnug_C2/images/dmuutility2NLS.gif)

1.   Click the Save button to save all input data in an XML file for later use.

2.   Click the Run button to run the batch job immediately.

3.   In the Batch Monitor dialog box, click the Processes tab to monitor the batch job execution.

![Image 15](http://catiadoc.free.fr/online/dmnug_C2/images/dmuutility3NLS.gif)

For more information on using the Batch Monitor, see the _[Infrastructure User's Guide, Basic Tasks, Running Batches, Running Batches Using the Batch Monitor](http://catiadoc.free.fr/online/basug\_C2/basugbt2301.htm)_.
![Image 16: aendtask.gif (1477 bytes)](http://catiadoc.free.fr/online/icons_C2/common/aendtask.gif)

Note: For supported Multi-CAD formats, see the sections _Requirements_ and _Methodologies and Advice_ in the corresponding documentation:
