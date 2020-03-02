# TSP-data-speech-to-text
Extract TSP speech data annotation and model ASR system on it
***
TSP speech data is not ready to use for ASR systems as they do not have annotation attached to it. In order to extract annotation you can use the tool named `AFsp-v10r2`. This tool will extract hidded transcripts from the .wav files header. 
#### What is header in wav files?
Well, it's an information inbulit with the files while speech were recorded. To see any header information of a wav file type >>> `xxd | head CB01_01.wav` where CB01_01.wav is the name of the target wav file, you want to see header of. This will generate following cmd output. 

`(base) niraj@Dell:~/Documents/work_place/TSP_Speech/TSP_48k/CB$` `xxd | head CB01_01.wav`
```
RIFF�7WAVEfmt ��wLISTRINFOINAM%Female (age 10) speaker, CB01_01 48kICRD1997-05-07 11:01:41 UTC
afsp�AFspdatabase:
TSP Speech Files v2ID: TSP CB01_01 48k
speaker: CB Female (age 10)
text: "The birch canoe slid on the smooth planks."
recording_conditions: Anechoic room, Sony ECM-909A microphone,
Sony TCD-D2 DAT recorderdata
```
Here one can see that the annotation and other information are stored in the header which `AFsp-v10r2` will extract and our python script use that to make use of compiled C code to generate a pipe seperated csv file with all these information and many more. 

#### What information `AFsp-v10r2` extract? 

```.txt
 WAVE file: /home/niraj/Documents/work_place/TSP_Speech/TSP_48k/MI/MI54_08.wav
   Description: Male speaker, MI54_08 48k
   Samples / channel : 133258 (2.776 s)  1997-04-15 16:28:06 UTC
   Sampling frequency: 48000 Hz
   Number of channels: 1 (16-bit integer)

--File format--
File name: ./TSP_48k/MI/MI54_08.wav
Header length: 342
Sampling frequency: 48000
No. frames: 133258
No. channels: 1
Data type: integer16
Data byte order: little-endian
Host byte order: little-endian

--Information records--
title: Male speaker, MI54_08 48k
creation_date: 1997-04-15 16:28:06 UTC
database: TSP Speech Files v2
ID: TSP MI54_08 48k
speaker: MI Male
text: "Flood the mails with requests for this book."
recording_conditions:
  Anechoic room, Sony ECM-909A microphone,
  Sony TCD-D2 DAT recorder

--File layout--
 <RIFF> 0 -> 266857
     <WAVE> 8 -> 11
     <fmt > 12 -> 35
       ...
     <LIST> 36 -> 113
          <INFO> 44 -> 47
          <INAM> 48 -> 81
            ...
          <ICRD> 82 -> 113
            ...
     <afsp> 114 -> 333
       ...
     <data> 334 -> 266857
       ...
 <EoF > 266858

```
Now our target is to find relevant information from this text and tranform it to a csv file for further processing.

Here are the steps involved: 

1. Download this repository
2. Unzip `AFsp-v10r2` into the home directory
3. Run >>> `make` (this will make C written InfoAudio and other tool accessible to you via command line)
4. Now run >>> python TSP_Speech.py
*** 
This will extract and use `AFsp-v10r2` tool to provide you a big .csv file with annotation and other speech features. They can be used for ASR or TTS modelling. 

