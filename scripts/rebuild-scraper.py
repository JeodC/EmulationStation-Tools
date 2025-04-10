import os
import sys
import subprocess
import importlib.util
import xml.etree.ElementTree as ET
from xml.dom import minidom

def check_and_install_dependencies():
    """Check if required modules are installed and attempt to install them if missing."""
    required_modules = ['xml.dom.minidom']
    missing = False

    for module in required_modules:
        if importlib.util.find_spec(module) is None:
            print(f"Missing required module: {module}")
            missing = True

    if missing:
        print("Attempting to install missing dependencies using pip...")
        try:
            subprocess.check_call([sys.executable, '-m', 'pip', 'install', 'lxml'])
            print("Dependencies installed successfully.")
        except subprocess.CalledProcessError as e:
            print(f"ERROR: Failed to install dependencies: {e}")
            print("Please install the required modules manually using 'pip install lxml'.")
            sys.exit(1)
    else:
        print("All required dependencies are already installed.")

def prettify_xml(elem):
    """Convert an ElementTree element to a pretty-printed XML string with minimal extra newlines."""
    rough_string = ET.tostring(elem, 'utf-8')
    reparsed = minidom.parseString(rough_string)
    pretty_xml = reparsed.toprettyxml(indent="    ")
    lines = [line for line in pretty_xml.split('\n') if line.strip()]
    return '\n'.join(lines)

def process_gamelist(xml_file):
    try:
        print(f"Parsing XML file: {xml_file}")
        tree = ET.parse(xml_file)
        root = tree.getroot()
    except ET.ParseError as e:
        print(f"ERROR: Failed to parse XML in {xml_file}: {e}")
        return

    xml_dir = os.path.dirname(xml_file)
    images_dir = os.path.join(xml_dir, "images")
    print(f"Checking for images directory: {images_dir}")
    
    modified = False
    total_games = len(root.findall('game'))
    print(f"Found {total_games} game entries to process")
    
    for i, game in enumerate(root.findall('game'), 1):
        image_tag = game.find('image')
        path_tag = game.find('path')
        
        print(f"Processing game {i}/{total_games}")
        if image_tag is not None:
            print(f"  - Already has image tag: {image_tag.text}")
            continue
            
        if path_tag is None:
            print(f"  - Skipping: No path tag found")
            continue
            
        rom_path = path_tag.text
        if rom_path.startswith('./'):
            rom_path = rom_path[2:]
        rom_filename = os.path.splitext(rom_path)[0]
        print(f"  - ROM filename: {rom_filename}")
        
        image_path = os.path.join(images_dir, f"{rom_filename}-image.png")
        relative_image_path = f"./images/{rom_filename}-image.png"
        
        print(f"  - Looking for image at: {image_path}")
        if os.path.exists(image_path):
            print(f"  - Image found! Adding tag: {relative_image_path}")
            new_image = ET.Element('image')
            new_image.text = relative_image_path
            desc_tag = game.find('desc')
            if desc_tag is not None:
                game.insert(list(game).index(desc_tag) + 1, new_image)
            else:
                game.insert(1, new_image)  # After path if no desc
            modified = True
        else:
            print(f"  - WARNING: No matching image found")

    if modified:
        old_file_path = f"{xml_file}.old"
        print(f"Changes detected, creating backup: {old_file_path}")
        
        if os.path.exists(old_file_path):
            print(f"Removing existing backup file")
            os.remove(old_file_path)
            
        print(f"Backing up original file")
        os.rename(xml_file, old_file_path)
        
        print(f"Writing updated XML to {xml_file}")
        pretty_xml = prettify_xml(root)
        with open(xml_file, 'w', encoding='utf-8') as f:
            f.write(pretty_xml)
        print(f"Successfully updated {xml_file} with new image tags")
    else:
        print(f"No changes needed for {xml_file}")

def scan_and_process_directory(directory):
    print(f"Starting scan of immediate subdirectories in: {directory}")
    subdirs = [d for d in os.listdir(directory) 
              if os.path.isdir(os.path.join(directory, d)) and d.lower() != 'ports']
    
    if not subdirs:
        print("No immediate subdirectories found (excluding 'ports').")
        return

    for subdir in subdirs:
        subdir_path = os.path.join(directory, subdir)
        print(f"Scanning subdirectory: {subdir}")
        
        for filename in os.listdir(subdir_path):
            if filename.lower() == 'gamelist.xml':
                xml_file_path = os.path.join(subdir_path, filename)
                print(f"\nFound gamelist.xml at: {xml_file_path}")
                process_gamelist(xml_file_path)
                print("-" * 50)

def main():
    print("""
EmulationStation Gamelist Rebuilder
=============================
This script scans immediate subdirectories of your ROMs folder (e.g., roms/gba, roms/gbc)
for 'gamelist.xml' files, excluding the 'ports' directory. For each game entry without
an <image> tag, it checks for a matching image file in the subdirectory's 'images' folder
(named '[rom_filename]-image.png') and adds the appropriate <image> tag if found.
Backups of modified files are created with a '.old' extension.
""")
    
    print("Checking for required dependencies...")
    check_and_install_dependencies()
    
    directory = input("Enter the path to your ROMs folder: ")
    
    if not os.path.exists(directory):
        print(f"ERROR: The directory '{directory}' does not exist.")
        return
    
    print(f"\nStarting processing for ROMs folder: {directory}")
    print("=" * 50)
    scan_and_process_directory(directory)
    print("=" * 50)
    print("Processing completed successfully.")

if __name__ == "__main__":
    main()