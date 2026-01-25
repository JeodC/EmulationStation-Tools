import xml.etree.ElementTree as ET
from pathlib import Path

def indent(elem, level=0):
    """Recursively add indentation to XML for pretty printing."""
    i = "\n" + level*"    "
    if len(elem):
        if not elem.text or not elem.text.strip():
            elem.text = i + "    "
        for child in elem:
            indent(child, level+1)
        if not elem.tail or not elem.tail.strip():
            elem.tail = i
    else:
        if not elem.tail or not elem.tail.strip():
            elem.tail = i

# Path to your gamelist.xml
gamelist_path = "gamelist.xml"

# Parse XML
tree = ET.parse(gamelist_path)
root = tree.getroot()

for game in root.findall('game'):
    image_tag = game.find('image')
    if image_tag is not None:
        image_path = Path(image_tag.text)
        port_name = image_path.parent.name
        # Check if thumbnail already exists
        if game.find('thumbnail') is None:
            thumbnail_tag = ET.Element('thumbnail')
            thumbnail_tag.text = f"./{port_name}/thumb.png"
            # Insert thumbnail right after image
            image_index = list(game).index(image_tag)
            game.insert(image_index + 1, thumbnail_tag)

# Pretty print
indent(root)

# Save back to file
tree.write(gamelist_path, encoding='utf-8', xml_declaration=True)
