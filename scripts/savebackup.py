import os
import shutil

def copy_dreamcast_saves(directory, save_directory):
    for root, dirs, files in os.walk(directory):
        if os.path.normcase(root).endswith(os.path.join('roms', 'bios', 'dc')):
            dreamcast_files = [f for f in files if f.lower().endswith(".bin") and "save" in f.lower()]

            if dreamcast_files:
                save_subdirectory = os.path.join(save_directory, "bios", "dc")
                os.makedirs(save_subdirectory, exist_ok=True)

                for file in dreamcast_files:
                    file_path = os.path.join(root, file)
                    save_path = os.path.join(save_subdirectory, file)
                    shutil.copy(file_path, save_path)
                    print(f"Copied {file} to {save_path}")

                # Stop scanning after processing bios/dc
                break

def copy_other_saves(directory, save_directory, file_extensions):
    ports_directory = os.path.join(directory, 'ports')

    for entry in os.scandir(directory):
        if entry.is_dir():
            current_directory = entry.path

            # Exclude 'roms/ports' and 'roms/bios/dc' from the search
            if os.path.normcase(current_directory) == os.path.normcase(ports_directory) or \
               os.path.normcase(current_directory).endswith(os.path.join('roms', 'bios', 'dc')):
                continue

            matching_files = [f for f in os.listdir(current_directory) if any(f.lower().endswith(ext) for ext in file_extensions)]

            if matching_files:
                for file in matching_files:
                    file_path = os.path.join(current_directory, file)
                    save_subdirectory = os.path.join(save_directory, os.path.basename(current_directory))
                    os.makedirs(save_subdirectory, exist_ok=True)
                    save_path = os.path.join(save_subdirectory, file)
                    shutil.copy(file_path, save_path)
                    print(f"Copied {file} to {save_path}")

def main():
    # Prompt user for the directory path
    roms_directory = input("Enter the path to your ROMs folder: ")

    # Check if the directory exists
    if not os.path.exists(roms_directory):
        print(f"The directory '{roms_directory}' does not exist.")
        return

    # Create a "saves" directory next to the script
    script_directory = os.path.dirname(os.path.abspath(__file__))
    saves_directory = os.path.join(script_directory, "saves")

    # Caopy Dreamcast saves
    copy_dreamcast_saves(roms_directory, saves_directory)
    
    # Copy other saves -- more file extensions can be added if necessary
    copy_other_saves(roms_directory, saves_directory, [".srm", ".sav"])

if __name__ == "__main__":
    main()