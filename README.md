A simple python script to parse gamelist.xml files and output what tags are missing from each game found.

Usage: ```python parser.py``` and type your roms directory e.g. ```\\RG351P\roms```. The script will only scan the first subdirectory, not nested subdirectories. Look for output.txt files in a folder created next to wherever you put _parser.py_.

Example output file _genesis_output.txt_:
```
Ecco The Tides of Time found in \\rg351p\roms\genesis\gamelist.xml but is missing desc, image, video, developer, publisher, genre.
Sonic the Hedgehog 3 found in \\rg351p\roms\genesis\gamelist.xml but is missing desc, image, video, releasedate, developer, publisher, genre.
Dynamite Headdy found in \\rg351p\roms\genesis\gamelist.xml but is missing image.
Shinobi III: Return of the Ninja Master found in \\rg351p\roms\genesis\gamelist.xml but is missing video.
Phantasy Star III: Generations of Doom found in \\rg351p\roms\genesis\gamelist.xml but is missing video.
Landstalker found in \\rg351p\roms\genesis\gamelist.xml but is missing video.
```
