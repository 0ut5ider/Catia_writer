Title: Translating Files from the Command Line

URL Source: http://catiadoc.free.fr/online/dtlug_C2/dtlugbt0500.htm

Published Time: Thu, 31 May 2012 13:34:56 GMT

Markdown Content:
![Image 1](http://catiadoc.free.fr/online/icons_C2/common/atarget.gif)This procedure describes how to run the CATDMUUtility batch program to import STEP files from the command line.

 The CATDMUUtility is a batch process enabling the generation of .CATProduct,.cgr and CATPart formats from STEP files.
![Image 2](http://catiadoc.free.fr/online/icons_C2/common/ainfo.gif)Some STEP entities are not converted to V5. Click [here](http://catiadoc.free.fr/online/dtlug_C2/dtlugbt0200.htm#ix-Step%20entities%20that%20are%20not%20converted) for more information.
The following examples show typical arguments and command switches passed to the [CATDMUUtility](http://catiadoc.free.fr/online/dtlug_C2/dtlugbt0500.htm) batch:
Converting a STEP part to a V5 cgr file
[CATStart.exe -env CATIA.V5R10.B10 -direnv C:\Documents and Settings\user\Application Data\DassaultSystemes\CATEnv -run "](http://catiadoc.free.fr/online/dtlug_C2/dtlugbt0500.htm)CATDMUUtility -f InputPartFile -cgr OutputCgrFile"
Converting a STEP part to a V5 CATPart file
[CATStart.exe -env CATIA.V5R10.B10 -direnv C:\Documents and Settings\user\Application Data\DassaultSystemes\CATEnv -run "](http://catiadoc.free.fr/online/dtlug_C2/dtlugbt0500.htm)CATDMUUtility -f InputPartFile -part OutputPartFile.CATPart"
Converting a STEP assembly to a V5 CATProduct file
[CATStart.exe -env CATIA.V5R10.B10 -direnv C:\Documents and Settings\user\Application Data\DassaultSystemes\CATEnv -run "](http://catiadoc.free.fr/online/dtlug_C2/dtlugbt0500.htm)CATDMUUtility -f InputProductFile -product OutputCATProductFile.CATProduct"

![Image 3](http://catiadoc.free.fr/online/icons_C2/common/ainfo.gif)## Options

Input and output options that can be used with CATDMUUtility are described below.
### [Input Options](http://catiadoc.free.fr/online/dtlug_C2/dtlugbt0500.htm)
**-f**Input file with appropriate extension. A path must follow this option. For STEP parts and assemblies, the file extension should be .prt.
### [Output Options](http://catiadoc.free.fr/online/dtlug_C2/dtlugbt0500.htm)
**-cgr**Output file for cgr corresponding to a part input file.
**-part**Output file for CATPart corresponding to a part input file.
**-product**Output file for CATProduct corresponding to the STEP assembly input file.
### [Other options](http://catiadoc.free.fr/online/dtlug_C2/dtlugbt0500.htm)

The other options available for conversion are settings which correspond to the environment. These are defined in T ools -> Options -> General -> Compatibility ->[External Formats](http://catiadoc.free.fr/online/bascugen_C2/bascucompatibility0700.htm) (In particular, the use of cgr or CATPart can be customized in these options) or [STEP Settings](http://catiadoc.free.fr/online/bascuitf_C2/bascuitf0100.htm).
## [How to run the batch](http://catiadoc.free.fr/online/dtlug_C2/dtlugbt0500.htm)

In a command prompt window, the conversion batch is launched by entering the following command:
On WINDOWS> "C:\<install_dir>\intel_a\code\bin\[\CATStart.exe -env CATIA.V5R10.B10 -direnv C:\Documents and Settings\user\Application Data\DassaultSystemes\CATEnv -run "](http://catiadoc.free.fr/online/dtlug_C2/dtlugbt0500.htm)CATDMUUtility.exe -f inputfile -cgr outputfile1"
On UNIX<install_dir>/<os>_a/code/command/catstart -env CATIA.V5R10.B10 -direnv /CATEnv -run "CATDMUUtility -f /tmp/model_file.mf1 -product /tmp/prod1.CATProduct"
Where 
-env ... is the default environment

-direnv ... is the directory path containing this environment.

CATIA.V5R10.B10 is an example of environment name, it will vary with the level of CATIA installed.
![Image 4](http://catiadoc.free.fr/online/icons_C2/common/ainfo.gif)Please note that this conversion will take into account the settings in Tools -> Options -> General -> Compatibility ->[External Formats](http://catiadoc.free.fr/online/bascugen_C2/bascucompatibility0700.htm)and [STEP Settings](http://catiadoc.free.fr/online/bascuitf_C2/bascuitf0100.htm).
