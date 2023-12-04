import os

def delete_non_backup_gamelists(directory):
    # Iterate through the directory and its immediate subdirectories
    for root, dirs, files in os.walk(directory):
        # Print the base directory and immediate subdirectories
        if root == directory or root.startswith(os.path.join(directory, os.path.sep)):
            # Filter subdirectories to only include immediate subdirectories
            dirs[:] = [d for d in dirs if os.path.join(root, d) == os.path.join(directory, d)]
            for subdir in dirs:
                subdir_path = os.path.join(root, subdir)
                # Check for 'gamelist.*' files in each immediate subdirectory
                for filename in os.listdir(subdir_path):
                    if filename.lower().startswith('gamelist.') and filename.lower() not in ['gamelist.xml', 'gamelist.xml.old']:
                        gamelist_path = os.path.join(subdir_path, filename)
                        # Delete the 'gamelist.*' file
                        os.remove(gamelist_path)
                        print(f"Deleted {filename} in '{subdir_path}'.")

def main():
    # Prompt user for the directory path
    directory = input("Enter the path to your roms folder: ")

    # Check if the directory exists
    if not os.path.exists(directory):
        print(f"The directory '{directory}' does not exist.")
        return

    # Delete non-backup gamelist files in the provided directory and its immediate subdirectories
    delete_non_backup_gamelists(directory)

if __name__ == "__main__":
    main()
