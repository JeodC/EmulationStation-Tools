# EmulationStation Tools
Just a repository of python scripts I wrote for various use cases.

## Parser
A simple python script to parse gamelist.xml files and output what tags are missing from each game found.

Usage: ```python parser.py``` and type your roms directory e.g. ```\\RG351P\roms```. The script will only scan the first subdirectory, not nested subdirectories. Look for output.txt files in a folder created next to wherever you put _parser.py_.

Example output file _genesis_output.txt_:
```
Dynamite Headdy found with missing tags: image
Shinobi III: Return of the Ninja Master found with missing tags: video
Phantasy Star III: Generations of Doom found with missing tags: video
Landstalker found with missing tags: video
```

## Sorter
A simple python script to parse gamelist.xml files and sort them alphabetically by the name tag. Creates backups before parsing.

Usage: ```python sorter.py``` and type your roms directory e.g. ```\\RG351P\roms```. The script will only scan the first subdirectory, not nested subdirectories.

## Savebackup
A tool that scans immediate directories in the `roms` folder and copies savedata to `saves` next to _savebackup.py_. The script copies Dreamcast memory cards (`bios/dc`) and other emulator savedata `.srm` and `.sav`. 
The file extensions searched can be modified in the script. Because of the complexity of the `roms/ports` folder, it is excluded from the scan.

## CRC32
Scans a specified directory for files of a specified file extension. Appends the CRC32 in hexadecimal format to the end of the filename as `Filename (CRC32).ext`
