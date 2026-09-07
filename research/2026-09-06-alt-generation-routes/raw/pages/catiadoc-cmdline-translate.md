Title: Translating Files from the Command Line

URL Source: http://catiadoc.free.fr/online/dglug_C2/dglugbt0500.htm

Markdown Content:
![Image 1](http://catiadoc.free.fr/online/icons_C2/common/atarget.gif)This procedure describes how to run the  CATDMUUtility Batch.
[](http://catiadoc.free.fr/online/dglug_C2/dglugbt0500.htm)The CATDMUUtility is a batch process enabling the generation of .CATPart, .cgr formats from IGES.
![Image 2](http://catiadoc.free.fr/online/icons_C2/common/ainfo.gif)*   Some IGES entities are not converted to V5. Click [here](http://catiadoc.free.fr/online/dglug_C2/dglugbt0200.htm#ix-IGES%20entities%20that%20are%20not%20converted) for more information.
*   The following examples show typical arguments and command switches passed to the [CATDMUUtility](http://catiadoc.free.fr/online/dglug_C2/dglugbt0500.htm) batch:
Converting a IGES part to a V5 cgr file[CATStart.exe -env CATIA.V5R10.B10 -direnv C:\Documents and Settings\user\Application Data\DassaultSystemes\CATEnv -run "](http://catiadoc.free.fr/online/dglug_C2/dglugbt0500.htm)CATDMUUtility -f InputPartFile -cgr OutputCgrFile"
Converting a IGES part to a V5 CATPart file[CATStart.exe -env CATIA.V5R10.B10 -direnv C:\Documents and Settings\user\Application Data\DassaultSystemes\CATEnv -run "](http://catiadoc.free.fr/online/dglug_C2/dglugbt0500.htm)CATDMUUtility -f InputPartFile -part OutputPartFile.CATPart"
## [](http://catiadoc.free.fr/online/dglug_C2/dglugbt0500.htm)Options
Input and output options that can be used with CATDMUUtility are described below.
### [Input Options](http://catiadoc.free.fr/online/dglug_C2/dglugbt0500.htm)
-f Input file with appropriate extension. A path must follow the option.

 For IGES part, the extension file should be .igs,
### [Output Options](http://catiadoc.free.fr/online/dglug_C2/dglugbt0500.htm)
-cgr Output file for cgr corresponding to a part input file.
-part Output file for CATPart corresponding to the part input file.
### [Other options](http://catiadoc.free.fr/online/dglug_C2/dglugbt0500.htm)

The other options available for conversion are the settings corresponding to the environment.

 They are defined in Tools -> Options -> General -> Compatibility -> External Formats and IGES.

In particular, the use of cgr or CATPart can be customized in these options.

 For more information see [Customizing External Formats](http://catiadoc.free.fr/online/bascugen_C2/bascucompatibility0700.htm)in _CATIA Infrastructure User's Guide_ and [IGES Settings](http://catiadoc.free.fr/online/bascuitf_C2/bascuitf0400.htm).
## [How to run the Batch](http://catiadoc.free.fr/online/dglug_C2/dglugbt0500.htm)
Run the following shell to start the batch process :
1.   Write a shell script containing the following lines:

2.   Run the shell.

Where 

-env ... is the default environment 

-direnv ... is the directory path containing this environment.

CATIA.V5R10.B10 is an example of environment name, it will vary with the level of CATIA installed.
