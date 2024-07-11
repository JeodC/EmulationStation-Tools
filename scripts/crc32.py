import zlib
import os

def calculate_crc(filename):
    with open(filename, 'rb') as file:
        content = file.read()
        crc = zlib.crc32(content) & 0xFFFFFFFF  # Ensure it's an unsigned integer
    return crc

def add_crc_to_list(filename):
    crc = calculate_crc(filename)
    crc_str = f'{crc:08X}'  # Format the CRC32 as an 8-character hexadecimal string
    return f'{os.path.basename(filename)}: {crc_str}'

def process_files_in_directory(directory, exceptions):
    output_file = f'{os.path.basename(directory)}_crc32.txt'
    files_found = False

    with open(output_file, 'w') as outfile:
        for filename in os.listdir(directory):
            # Exclude the output file itself, any directories, and files with specified extensions
            if (filename != output_file and os.path.isfile(os.path.join(directory, filename)) and 
                not any(filename.endswith(ext) for ext in exceptions)):
                files_found = True
                file_path = os.path.join(directory, filename)
                crc_entry = add_crc_to_list(file_path)
                outfile.write(crc_entry + '\n')
                print(f'Processed: {filename}')

    if not files_found:
        os.remove(output_file)
        print(f"No files found in {directory}!")
        main()  # Restart the script

def main():
    # Define exceptions
    exceptions = ['.xml', '.old', '.dat', '.sav', '.srm']

    # Prompt user for directory
    directory = input('Enter the directory to scan: ')

    # Ensure the directory exists
    if not os.path.exists(directory):
        print(f"Error: Directory '{directory}' does not exist.")
        return

    # Ensure the directory is a valid directory
    if not os.path.isdir(directory):
        print(f"Error: '{directory}' is not a valid directory.")
        return

    # Process files in the specified directory
    process_files_in_directory(directory, exceptions)

if __name__ == "__main__":
    main()
