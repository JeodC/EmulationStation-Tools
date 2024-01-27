import zlib
import os

def calculate_crc(filename):
    with open(filename, 'rb') as file:
        content = file.read()
        crc = zlib.crc32(content) & 0xFFFFFFFF  # Ensure it's an unsigned integer
    return crc

def add_crc_to_filename(file_path):
    crc = calculate_crc(file_path)
    crc_str = f'{crc:08X}'  # Format the CRC32 as an 8-character hexadecimal string
    base_name, extension = os.path.splitext(file_path)
    new_filename = f'{base_name} ({crc_str}){extension}'
    return new_filename

def process_files_in_directory(directory, file_extension):
    for filename in os.listdir(directory):
        if filename.endswith(file_extension):
            file_path = os.path.join(directory, filename)
            new_filename = add_crc_to_filename(file_path)
            
            # Rename the file
            os.rename(file_path, new_filename)
            
            print(f'Renamed: {filename} -> {new_filename}')

def main():
    # Prompt user for directory and file extension
    directory = input('Enter the directory to scan: ')
    file_extension = input('Enter the file extension (e.g., .gb): ')

    # Ensure the directory exists
    if not os.path.exists(directory):
        print(f"Error: Directory '{directory}' does not exist.")
        return

    # Ensure the directory is a valid directory
    if not os.path.isdir(directory):
        print(f"Error: '{directory}' is not a valid directory.")
        return

    # Process files in the specified directory with the given file extension
    process_files_in_directory(directory, file_extension)

if __name__ == "__main__":
    main()