import os

def rename_and_delete_files():
    # List of suffixes to delete
    delete_suffixes = ['-titleshot', '-marquee', '-fanart', '-boxback', '-thumb']

    # Walk through all directories and subdirectories
    for root, dirs, files in os.walk('.'):
        print(f'Scanning directory: {root}')
        # Loop through each file in the directory
        for file_name in files:
            # Check if the file name ends with '-image.png' or '-image.jpg'
            if file_name.endswith('-image.png') or file_name.endswith('-image.jpg'):
                # Generate the new file name by removing the '-image' suffix and changing extension to .png
                new_name = file_name.replace('-image.png', '.png').replace('-image.jpg', '.png')
                # Create the full old and new file paths
                old_path = os.path.join(root, file_name)
                new_path = os.path.join(root, new_name)
                # Check if the new file name already exists
                if not os.path.exists(new_path):
                    # Rename the file
                    os.rename(old_path, new_path)
                    print(f'Renamed: {old_path} -> {new_path}')
                else:
                    print(f'Skipped (already exists): {new_path}')
            else:
                # Check if the file name ends with any of the delete suffixes
                for suffix in delete_suffixes:
                    if file_name.endswith(suffix) or any(file_name.endswith(suffix + ext) for ext in ['.png', '.jpg', '.jpeg', '.gif']):
                        # Create the full file path
                        file_path = os.path.join(root, file_name)
                        # Delete the file
                        os.remove(file_path)
                        print(f'Deleted: {file_path}')
                        break  # No need to check other suffixes once matched

if __name__ == "__main__":
    rename_and_delete_files()
