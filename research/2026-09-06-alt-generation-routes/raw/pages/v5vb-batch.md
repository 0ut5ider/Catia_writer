Title: Executing CATIA scripts in batch mode

URL Source: https://v5vb.wordpress.com/2010-09-26/exec-scripts-in-batch-mode/

Published Time: 2010-09-27T01:18:44+00:00

Markdown Content:
68 Votes

I got the idea for this article from a reader of this blog. He sent me an email asking what would be the best way to extract some information from thousands of drawings in an automated way. That information in his scenario is the value of a handful of parameters that are attached to the root drawing node in each drawing. I recommended to execute a script in batch mode that would open each drawing one by one and read those parameter values and write the data to a text file.

In our email exchanges, we both agreed that this seemed like a great topic to share with everyone for a few reasons. First, this is a relatively common scenario so many people could benefit by sharing the code that opens the drawings and writes out the parameter values. Also, I have a feeling that many have never run a script in batch mode so this article might unlock some new capabilities. So in this article, I will discuss the basics of running a batch and share the code we developed and tested.

**What is batch mode?**

When you start up CATIA on a typical day to do your work, you are running in interactive mode. Interactive mode means that you see CATIA and its user interface on the screen. You are able to click commands, select things and interact with it. On the other hand, batch mode is a way to start CATIA without any user interface. Obviously there are limited use cases where this would be a good idea since CATIA is running “behind the scenes” and you can’t see anything on the screen. Typically, the reasons to use batch mode are to run CATIA utilities (See Tools-Utility menu item) or to execute a script.

**Why use batch mode?**

So when should you consider running a script in batch mode? I think it is likely to be a good choice over running the script in interactive mode when:

*   You need to do some operations on a lot of separate CATIA files
*   You need to generate a lot of new data (geometry creation, product structure creation, etc.)
*   You need the best possible performance (speed)
*   No user interaction is required for the script to do its job.

One of the key items above is that CATIA will run considerably faster in batch mode than it does in interactive mode. This is because when it runs in interactive mode, it constantly has to process updates to the interactive graphical display but in batch mode none of those updates are done. At the end of this article, I will share the performance numbers for the drawing example batch.

The last item (no user interaction required) is very important. Your program must be able to make all of its own decisions without any user interactions or else the batch will not be successful. So if you have an existing program that you would like to try as a batch you should check very carefully for this and fix any potential issues. This might mean hard coding values or decision logic into the program or making the program read input information from a text file or possibly even passing arguments into the script when the batch is launched. These scenarios won’t be covered in this article because the example code I will share does not require any user input.

**The example scenario and script**

As mentioned earlier, our scenario is to open thousands of drawings and extract some parameter values and write them to a text file. We want to do this as efficiently as possible since there are thousands of files to process. The parameters we need to access exist on the root parameters collection of each drawing. All of the drawings will be located in a single folder on the local file system. The program should be flexible enough so that we can easily specify a list of parameter names whose values should be retrieved from each drawing without having to modify the code each time the script is used.

I am not going to explain how the script works because the focus of this article is running a batch not this specific script. However, I did add some brief comments throughout the code to aid in understanding what the macro is doing. Take a little time and read through it because there are some interesting things in it.

If you want to try the script yourself either in interactive mode or batch, simply make some drawings that have one or more parameters in their root parameters set. Then just edit the variables at the start of the script to specify the parameter name(s) you want to look for and the folder where the drawing files exist.

Here is the code,

`Option``Explicit`

`Sub``CATMain()`

```Dim``objFolder``As``Object`

```Dim``intIndex``As``Integer`

```Dim``intIndex2``As``Integer`

```Dim``objFile``As``File`

```Dim``objDwgDoc``As``Document`

```Dim``objParams``As``Parameters`

```Dim``strParamName``As``String`

```Dim``varParamNames``As``Variant`

```Dim``strOutputValues``As``String`

```Dim``intArraySize``As``Integer`

```Dim``strOutputFilePath``As``String`

```Dim``objTextStream``As``TextStream`

```Dim``strOutput``As``String`

```Dim``objFileSystem``As``Object`

```Dim``strTimeStamp``As``String`

```Dim``lngNbDwgs``As``Long`

```Const``FOLDER``As``String``=``"C:\Temp\BatchTest"`

```Const``PARAMNAMES``As``String``=``"TestString,TestLength,TestMass"`

```If``CATIA.FileSystem.FolderExists(FOLDER) =``False``Then``Exit``Sub`

```strOutput =``"Folder processed: "``& FOLDER & Chr(13)`

```strOutput = strOutput &``"Parameter names: "``& PARAMNAMES & Chr(13) & Chr(13)`

```strOutput = strOutput &``"File #"``& Chr(9) &``"Drawing name"``& Chr(9) & Replace(PARAMNAMES,``","``, Chr(9)) & Chr(13)`

```If``InStr(1, PARAMNAMES,``","``) > 0``Then`

```varParamNames = Split(PARAMNAMES,``","``)`

```Else`

```ReDim``varParamNames(0)`

```varParamNames(0) = PARAMNAMES`

```End``If`

```intArraySize = UBound(varParamNames)`

```lngNbDwgs = 0`

```Set``objFolder = CATIA.FileSystem.GetFolder(FOLDER)`

```If``objFolder.Files.Count > 0``Then`

```For``intIndex = 1``To``objFolder.Files.Count`

```Set``objFile = objFolder.Files.Item(intIndex)`

```If``UCase(Right(objFile.Name, 11)) =``".CATDRAWING"``Then`

```lngNbDwgs = lngNbDwgs + 1`

```Set``objDwgDoc = CATIA.Documents.Open(objFile.Path)`

```Set``objParams = objDwgDoc.Parameters.RootParameterSet.AllParameters`

```strOutput = strOutput & lngNbDwgs & Chr(9)`

```strOutput = strOutput & objDwgDoc.Name & Chr(9)`

```For``intIndex2 = 0``To``intArraySize`

```strParamName = Trim(varParamNames(intIndex2))`

```strOutput = strOutput & Chr(9) & GetParameterValue(objParams, strParamName)`

```Next`

```strOutput = strOutput & Chr(13)`

```objDwgDoc.Close`

```End``If`

```Next`

```End``If`

```If``lngNbDwgs = 0``Then``strOutput = strOutput &``"No CATDrawings were found!"`

```strTimeStamp = Replace(Now,``"/"``,``"-"``)`

```strTimeStamp = Replace(strTimeStamp,``":"``,``"-"``)`

```strTimeStamp = Replace(strTimeStamp,``" "``,``"_"``)`

```strOutputFilePath = objFolder.Path &``"\" & "``DwgParamBatchResult_``" & strTimeStamp & "``.txt"`

```Set``objFile = CATIA.FileSystem.CreateFile(strOutputFilePath,``True``)`

```Set``objTextStream = objFile.OpenAsTextStream(``"ForWriting"``)`

```objTextStream.Write strOutput`

```objTextStream.Close`

`End``Sub`

`Function``GetParameterValue(``ByRef``iParams``As``Parameters,``ByVal``iParamName``As``String``)``As``String`

```Dim``objParam``As``Parameter`

```On``Error``Resume``Next`

```Set``objParam = iParams.Item(iParamName)`

```If``Err.Number = 0``Then`

```GetParameterValue = objParam.ValueAsString`

```Else`

```GetParameterValue =``"Not Found"`

```End``If`

`End``Function`

**Before running a macro in batch mode**

I want to point out that you should always test your script in interactive mode first before running it in batch mode. As I mentioned earlier, you will not see messages or receive any feedback from the run unless your code outputs any error information to a text file or the command window. So for our scenario, a dozen or so files were placed in a folder and the script was run to make sure it works properly before moving on to the batch.

**How to start the batch**

There are quite a few ways to start CATIA in batch mode. The CATIA help documentation explains five different ways, but I recommend option #4 with the command string in a .bat file. There are several reasons I tend to do this. The main reason is that I don’t care much for typing in a big long string at a command prompt. It is too easy to mistype something especially when the command string gets very long like in this case. I also like to store the exact command line string somewhere for next time and if you are going to do that you might as well just save it in a text file with a .bat extension.Once you have prepared the .bat file, all you have to do is double click the file and Windows will execute the command as if you had typed it at a command line.

Lets look at what goes into this command string for a couple of common scenarios. In each case you need to first specify where the CATIA executable is located (CNext.exe). After that, you specify options by typing dash (-) followed by the name of the option followed by a space then the value for the option.

Example 1: You want to start CATIA with the default environment

**CNextPath –macro –batch ScriptPath**

Example 2: You want to start CATIA with a custom environment (more common)

**CNextPath –direnv EnvFolderPath –env EnvName –batch –macro ScriptPath**

**CNextPath**The full path to the installed location of CNext.exe

**–direnv**(Option) The folder path where your environment files are located

**EnvFolderPath** The value of the folder path where your environment files are located

**–env**(Option) The name of the environment to start

**EnvName**The name of the environment to start

**–batch**(Option) CATIA will be started in batch mode.

**–macro**(Option) CATIA will execute the requested script

**ScriptPath**The full path to the script you want to run

In most cases you will probably want to start CATIA with the custom environment that is used at your company, so you will use the second example above. Below is an example command line string (note that you will have to customize it for your own company specific installation). Save this string in a text file and save it with a .bat extension. To test it, simply double click on this .bat file and CATIA should start with the options specified and run the script.

“C:\Program Files\Dassault Systemes\B18\intel_a\code\bin\cnext.exe” –direnv E:\CATEnv –env CATIA.V5R18.B18 -macro -batch “C:\Temp\BatchTest\DwgParamBatch.CATScript”

* * *

_Edit (05OCT10)_

I am editing this article to add more details related to setting up the batch. I added this section after reading the comments below and because when I wrote the article, I didn’t actually run the batch. I wrote that part based on the help docs and from memory, but it has been a while since i ran a batch so I thought I should go back and confirm everything.

You can launch a CATIA V5 batch by starting CNEXT.exe directly or you can use the CATSTART.exe process. The command line syntax is slightly different for each method so I have listed some examples for each below.

**Using CNEXT.exe**

CD /D D:\Program Files\Dassault Systemes\B18\intel_a\code\bin

 CNEXT.exe –direnv E:\CATEnv –env CATIA.V5R18.B18 -batch -macro C:\Temp\BatchTest\DwgParamBatch.CATScript

*   _On the first line of the batch file, I change directory using the CD command to the bin folder where the CATIA application files are located._
*   _The /D option specifies that you want to change the drive as well as the directory. If your install is not on C:\ you should add this option._
*   _When using the CD command to change directory you do not need quotes if the path contains spaces._

CD C:\Program Files\Dassault Systemes\B18\intel_a\code\bin

 CNEXT.exe –direnv E:\CATEnv –env CATIA.V5R18.B18 -batch -macro “C:\Temp\BatchTest\Dwg Param Batch.CATScript”

*   _In this case, the bin folder is on C:\ so I left out the /D option after the CD command_
*   _In this case, the macro path contains spaces so it must be enclosed in quotes_

**Using CATSTART.exe**

CD C:\Program Files\Dassault Systemes\B18\intel_a\code\bin

 CATSTART.exe –direnv E:\CATEnv –env CATIA.V5R18.B18 -object “-batch -macro C:\Temp\BatchTest\DwgParamBatch.CATScript”

*   _When using the CATSTART.exe process, you should use the -object option then enclose the -batch -macro option s_ _and the macro path all inside quotes_
*   _It is OK if the macro path has spaces in it because it is already enclosed in quotes._

**Other Considerations**

If your CATIA environment is setup to work with ENOVIA and you are prompted to login when CATIA starts in interactive mode then you should setup the batch using one of the options listed below.

Option 1: Start the batch using the CNEXT.exe process (not CATSTART.exe)

Option 2: If you want to use CATSTART.exe then you should open CATIA in interactive mode and go to Tools-Options and turn off the login at startup option. If you do not turn this off, CATIA seems to always start CATIA in interactive mode even when the -batch option is specified.

_End Edit (05OCT10)_

* * *

**Results and performance comparison**

The above script was run on a set of drawings both in batch mode and interactive mode and average time per drawing was calculated for both scenarios. In interactive mode, the script averaged about 2.6 minutes per drawing. Most of this is due to the load time to open the drawing then load it all into memory and update the display with all of that information. The actual task we are automating (reading the parameter values) probably only takes a small fraction of a second but it takes considerable time to load the data in interactive mode.

In batch mode, the average time was reported to be a little over 3 seconds. According to these numbers, batch mode is about a 50X improvement. This is an incredible performance gain! I was very surprised because I have run batches in the past but never went back and ran them again in interactive mode to compare times. I did not do any time trials of the script in this article myself because I don’t have a large sample of real world drawings all having the required parameters. I am just sharing the numbers that were reported back to me.

**Conclusion**

In this article my goal was to expose you to running a script in batch mode. I think the basic information I provided should be enough to setup most batch scenarios. Finally, I hope the real world example and the results it produced were interesting to read about and maybe you can benefit from using a batch in the future.

* If you have some experiences with running scripts in batch mode and maybe even have some performance comparison data you would like to share, please post a comment below. I’d like to hear more real world examples of the actual performance gains you saw when using batch mode.

**Where to get more help**

You can get more information about batch mode in the CATIA help documentation. Just go to the Infrastructure chapter and look for the topic called “Starting a Session on Windows”.

_Please take a moment to rate this article…Just click the stars up near the title._

* * *
