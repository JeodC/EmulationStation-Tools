import os
from PIL import Image

def rename_and_delete_files():
    # List of suffixes to delete
    delete_suffixes = ['-titleshot', '-marquee', '-fanart', '-boxback', '-thumb']
    # Target size for resizing images
    target_size = (400, 300)

    # Walk through all directories and subdirectories
    for root, dirs, files in os.walk('.'):
        # Loop through each file in the directory
        for file_name in files:
            file_path = os.path.join(root, file_name)
            
            # Check if the file name ends with '-image.png' or '-image.jpg'
            if file_name.endswith('-image.png') or file_name.endswith('-image.jpg'):
                # Generate the new file name by removing the '-image' suffix and changing extension to .png
                new_name = file_name.replace('-image.png', '.png').replace('-image.jpg', '.png')
                new_path = os.path.join(root, new_name)
                
                # Check if the new file name already exists
                if not os.path.exists(new_path):
                    # Rename the file
                    os.rename(file_path, new_path)
                    print(f'Renamed: {file_path} -> {new_path}')
                    file_path = new_path

            # Check if the file name ends with any of the delete suffixes
            delete_file = any(file_name.endswith(suffix) or any(file_name.endswith(suffix + ext) for ext in ['.png', '.jpg', '.jpeg', '.gif']) for suffix in delete_suffixes)
            
            if delete_file:
                os.remove(file_path)
                print(f'Deleted: {file_path}')
            else:
                # Resize the image if necessary
                try:
                    with Image.open(file_path) as img:
                        if img.size != target_size:
                            img = img.resize(target_size, Image.LANCZOS)
                            img.save(file_path)
                            print(f'Resized: {file_path} to {target_size}')
                except Exception as e:
                    print(f'Error processing {file_path}: {e}')

if __name__ == "__main__":
    rename_and_delete_files()
