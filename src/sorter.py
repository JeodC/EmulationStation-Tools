import os
import xml.etree.ElementTree as ET

def sort_games_by_name(xml_content):
    root = ET.fromstring(xml_content)
    sorted_games = sorted(root.findall('game'), key=lambda x: x.find('name').text)
    
    for game in sorted_games:
        root.remove(game)
    
    for game in sorted_games:
        root.append(game)

    return ET.tostring(root, encoding='utf-8').decode('utf-8')

def process_gamelist(xml_file):
    try:
        # Attempt to parse the XML file
        tree = ET.parse(xml_file)
        root = tree.getroot()
    except ET.ParseError as e:
        # Print an error message if parsing fails
        print(f"Error parsing XML in {xml_file}: {e}")
        return

    # Construct the backup file path
    old_file_path = f"{xml_file}.old"

    # Check if the old file already exists and delete it
    if os.path.exists(old_file_path):
        os.remove(old_file_path)

    # Rename the old gamelist.xml to the old file
    os.rename(xml_file, old_file_path)

    # Sort the games by name
    sorted_xml_content = sort_games_by_name(ET.tostring(root, encoding='utf-8').decode('utf-8'))

    # Write the sorted content back to the original gamelist.xml file
    with open(xml_file, 'w', encoding='utf-8') as file:
        file.write(sorted_xml_content)

def scan_and_sort_directory(directory):
    # Iterate through the directory and its immediate subdirectories
    for root, dirs, files in os.walk(directory):
        # Print the base directory and immediate subdirectories
        if root == directory or root.startswith(os.path.join(directory, os.path.sep)):
            # Filter subdirectories to only include immediate subdirectories
            dirs[:] = [d for d in dirs if os.path.join(root, d) == os.path.join(directory, d)]
            for subdir in dirs:
                subdir_path = os.path.join(root, subdir)
                # Check for 'gamelist.xml' in each immediate subdirectory
                for filename in os.listdir(subdir_path):
                    if filename.lower() == 'gamelist.xml':
                        xml_file_path = os.path.join(subdir_path, filename)
                        # Sort the 'gamelist.xml' file and write the sorted content back to the original file
                        process_gamelist(xml_file_path)
                        print(f"Processed and sorted gamelist.xml in '{subdir_path}'.")

def main():
    # Prompt user for the directory path
    directory = input("Enter the path to your roms folder: ")

    # Check if the directory exists
    if not os.path.exists(directory):
        print(f"The directory '{directory}' does not exist.")
        return

    # Scan and sort the provided directory and its immediate subdirectories
    scan_and_sort_directory(directory)

if __name__ == "__main__":
    main()
