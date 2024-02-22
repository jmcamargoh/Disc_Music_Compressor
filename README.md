# Disc Music Compressor
This project aims to convey the understanding of parallel processing and virtualization of memory and CPU. It consists of a converter of *.aif* files into different formats, using threads to optimize its execution time and understand the operation of the CPU when several processes run at the same time

## Related Information
- The programming language used is *Python 3.11.0*.
- It shows the time of conversion for a folder of *.aif* files, and time to calculate the estimated size for single files.
- In *"Convertir"* folder are some *.aif* files to try the code.
- The code creates 2 folders:
    - To keep the files of Folder Conversion.
    - To keep the files of Single Conversion.

### Libraries
- *multiprocessing*
- *ffmpeg*
- *pydub (AudioSegment)*
- *functools (partial)*
- *subprocess*
- *time*
- *os*
- *sys*

## Commands
**IMPORTANT:** Every path in the commands must be into " ", te be readen by the code.

### For Single File Conversion
- python DMC.py -f *"file_path"*

### For Folder Conversion
- python DMC.py e=**FORMAT** -f *"file_path"*