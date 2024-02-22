# Libraries to import
import multiprocessing
from pydub import AudioSegment
from functools import partial
import subprocess
import time
import os
import sys

# ------------------------------------------------------------------------------------------------------
# Error handler for incomplete processes
def error_handler():
    print("Process Final Status 1")
    return 0

# ------------------------------------------------------------------------------------------------------
# Convert File Function
def convert_file(input_file, output_folder, output_format):
    # Load the file form the path
    audio = AudioSegment.from_file(input_file, format="aiff")

    # Split the name of the file    
    file_name = os.path.splitext(os.path.basename(input_file))[0]

    # Create the file with the format name
    output_path = os.path.join(output_folder, f"{file_name}.{output_format}")

    # Export the new file
    audio.export(output_path, format=output_format)
    print(f"Converted: {output_path} - Size: {os.path.getsize(output_path)/1024} KB")
    return 0

# ------------------------------------------------------------------------------------------------------
# Estimated File Size
def estimated_size(file_w_formats):
    input_file, format = file_w_formats
    converted_file = f"{input_file[:-4]}.{format}"
    
    # Calculate the size of the converted file
    try:
        # Redirect ffmpeg output to a tempfile (this is just to avoid all the prompt info os ffmpeg)
        with open(os.devnull, 'w') as null_file:
            subprocess.run(["ffmpeg", "-i", input_file, "-f", format, converted_file], stdout=null_file, stderr=null_file)
        # Find the estimated size
        size = os.path.getsize(converted_file) // 1024  # Conversion to KB
        return size
    except Exception as e:
        print(f"Error when estimating size: {e}")
        return -1
    finally:
        # Delete tempfile
        if os.path.exists(converted_file):
            os.remove(converted_file)

# ------------------------------------------------------------------------------------------------------
# Single File Conversion
def single_file(input_file, available_formats, pool_size):
    file_w_formats = [(input_file, format) for format in available_formats]

    start_estimated = time.perf_counter()    # Time processing start
    # Multiprocessing to calculate faster the estimated size
    with multiprocessing.Pool(pool_size) as pool:
        results = pool.map(estimated_size, file_w_formats)

    estimated_sizes = dict(zip(available_formats, results)) # Zip creates tuples (in this case, the format with it's file size)
    
    print("Each Format Estimated File Sizes:")
    for format, size in estimated_sizes.items():
        print(f"{format}: {size} KB")

    end_estimated = time.perf_counter()      # Time processing end
    execution_estimated = end_estimated-start_estimated
    print(f"Estimated File Process time: {execution_estimated} seconds")
    print("")
    
    decision = input("Select the format to keep the file on disk: ")

    if decision in available_formats:
        output_folder = "Converted Single File"  # Create output folder
        # Verify if folder exists
        if not os.path.exists(output_folder):
            os.makedirs(output_folder)

        start = time.perf_counter()    # Time processing start
        convert_file(input_file, output_folder, decision)   # Convert the single file into selected format
        end = time.perf_counter()      # Time processing end
        execution = end-start
        print(f"Conversion time: {execution} seconds")
        
    else:
        print("The format isn't available")
        error_handler()

    return 0

# ------------------------------------------------------------------------------------------------------
# Folder Conversion
def folder_processing(address, format, pool_size):
    aif_files = []
    for file in os.listdir(address):    # Maybe we can improve this part to be faster!
        complete_path = os.path.join(address, file)
        if complete_path.endswith('.aif'): aif_files.append(complete_path)

    if not aif_files:
        print("Error: No AIF files were found on the folder!")
        error_handler()
        return 0
    
    output_folder = "Converted Folder Files"  # Create output folder

    # Verify if folder exists
    if not os.path.exists(output_folder):
        os.makedirs(output_folder)

    pool = multiprocessing.Pool(pool_size)
    start = time.perf_counter()    # Time processing start
    convert_partial = partial(convert_file, output_folder=output_folder, output_format=format)
    pool.map(convert_partial, aif_files)
    pool.close()
    pool.join()
    end = time.perf_counter()      # Time processing end
    execution = end-start
    print(f"Conversion time: {execution} seconds")

    return 0

# ------------------------------------------------------------------------------------------------------
# Main Execution
if __name__ == "__main__":
    available_format = ["mp3", "wav", "ogg", "flac"]

    pool_size = multiprocessing.cpu_count()     # Cores available in pc, to use the pool

    # For a Single File
    if sys.argv[1] == '-f':
        address = "".join(sys.argv[2])
        if os.path.exists(address):
            print(f"The path '{address}' is valid!")
            # Go to single conversion
            single_file(address, available_format, pool_size)
            print("Process Final Status: 0")
        else:
            print("The path is incorrect or doesn't exists!")
            error_handler()

    # For Folder Conversion 
    elif '-e=' in sys.argv[1] and sys.argv[2] == '-f':
        output_format = sys.argv[1][3:]
        address = "".join(sys.argv[3])
        if output_format in available_format:
            if os.path.exists(address):
                print(f"The format '{output_format}' is valid!")
                print(f"The path '{address}' is valid!")
                # Go to folder conversion
                folder_processing(address, output_format, pool_size)
                print("Process Final Status: 0")
            else:
                print("The path is incorrect or doesn't exists!")
                error_handler()
        else:
            print("The format isn't valid!")
            error_handler()
    
    # Wrong written command
    else:
        print("Invalid command format. Please follow the provided examples for a successful conversion")
        error_handler()

    """# For a Single File
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
            print("Process Final Status: 0")
        else:
            print("The path is incorrect!")
            error_handler()

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
                print("Process Final Status: 0")
            else:
                print("The path is incorrect!")
                error_handler()
        else:
            print("The format isn't valid!")
            error_handler()

    # Wrong written command
    else:
        print("Invalid command format. Please follow the provided examples for a successful conversion")
        error_handler()"""
        
        
        
# ------------------------------------------------------------------------------------------------------
""""
import multiprocessing

def main():
    pool_size = multiprocessing.cpu_count()     # Cores available in pc, to use the pool
    print(pool_size)
    return 0

main()
"""