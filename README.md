# Parser
A simple python script to parse gamelist.xml files and output what tags are missing from each game found.

Usage: ```python parser.py``` and type your roms directory e.g. ```\\RG351P\roms```. The script will only scan the first subdirectory, not nested subdirectories. Look for output.txt files in a folder created next to wherever you put _parser.py_.

Example output file _genesis_output.txt_:
```
Dynamite Headdy found with missing tags: image
Shinobi III: Return of the Ninja Master found with missing tags: video
Phantasy Star III: Generations of Doom found with missing tags: video
Landstalker found with missing tags: video
```

# Sorter
A simple python script to parse gamelist.xml files and sort them alphabetically by the <name> tag. Creates backups before parsing.

Usage: ```python sorter.py``` and type your roms directory e.g. ```\\RG351P\roms```. The script will only scan the first subdirectory, not nested subdirectories.

# Cleaner
A simple python script to find and remove gamelist.xml.\* files (excluding gamelist.xml and gamelist.xml.old)

Usage: ```python parser.py``` and type your roms directory e.g. ```\\RG351P\roms```. The script will only scan the first subdirectory, not nested subdirectories. Look for output.txt files in a folder created next to wherever you put _parser.py_.
