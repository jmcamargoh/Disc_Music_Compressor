# Libraries to import
import multiprocessing
from multiprocessing import Process
from pydub import AudioSegment
from functools import partial
import time
import os

def convert_file(audio, input_file, output_folder, output_format):
    # Split the name of the file    
    file_name = os.path.splitext(os.path.basename(input_file))[0]

    # Create the file with the format name
    output_path = os.path.join(output_folder, f"{file_name}.{output_format}")

    # Export the new file
    audio.export(output_path, format=output_format)
    print(f"Converted {output_path} - Size: {os.path.getsize(output_path)/1024} KB")
    return 0

# ------------------------------------------------------------------------------------------------------
# Single File Conversion
def single_file(input_file, available_formats, pool_size):
    # Load the file form the path
    audio = AudioSegment.from_file(address, format="aiff")

    output_folder = "Converted Files"  # Create output folder

    # Verify if folder exists
    if not os.path.exists(output_folder):
        os.makedirs(output_folder)

    pool = multiprocessing.Pool(pool_size)
    convert_partial = partial(convert_file, audio, input_file, output_folder)
    pool.map(convert_partial, available_formats)
    pool.close()
    pool.join()

    return 0

# ------------------------------------------------------------------------------------------------------
# Small Test of Multiprocessing
def imprimir(file):
    print(file)
    return 0

# ------------------------------------------------------------------------------------------------------
# Folder Conversion
def folder_processing(address, format, pool_size):
    aif_files = [file for file in os.listdir(address) if file.endswith(".aif")]

    if not aif_files:
        print("Error: No AIF files were found on the folder!")
        return 0

    pool = multiprocessing.Pool(pool_size)
    pool.map(print, aif_files)
    # Close the pool and wait for all the tasks to complete
    pool.close()
    pool.join()

    return 0

# ------------------------------------------------------------------------------------------------------
# Main Execution
if __name__ == "__main__":
    print("Program Started! Welcome to Disc Music Compressor!")
    print("For a Single File: dmc -f FILE_PATH")
    print("For a Folder of Files: dmc -e=[FORMAT] -f FOLDER_PATH")
    selected_command = input("Enter the command for file conversion: ")
    command = selected_command.split()
    available_format = ["mp3", "wav", "ogg", "flac"]

    pool_size = multiprocessing.cpu_count()     # Cores available in pc, to use the pool

    # For a Single File
    if len(command) >= 3 and command[0]=='dmc' and command[1]=='-f':
        address = command[2]
        if os.path.exists(address):
            print(f"The path '{address}' is valid!")
            # Go to single conversion
            begin = time.perf_counter()
            single_file(address, available_format, pool_size)
            end = time.perf_counter()
            execution = end-begin
            print(f"Execution time: {execution} seconds")
        else:
            print("The path is incorrect!")

    # For a whole Folder 
    elif len(command) >= 4 and command[0]=='dmc' and '-e=' in command[1] and command[2]=='-f':
        output_format = command[1][3:]
        address = command[3]
        if output_format in available_format:
            if os.path.exists(address):
                print(f"The path '{address}' is valid!")
                # Go to folder conversion
                begin = time.perf_counter()
                folder_processing(address, output_format, pool_size)
                end = time.perf_counter()
                execution = end-begin
                print(f"Execution time: {execution} seconds")
            else:
                print("The path is incorrect!")
        else:
            print("The format isn't valid!")

    # Wrong written command
    else:
        print("Invalid command format. Please follow the provided examples for a successful conversion")