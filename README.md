# EmulationStation Tools
A collection of python scripts I wrote for various use cases as well as desktop icons for some retro handhelds. Examples come from `Sega Mega Drive & Genesis Classics` collection.

## Parser
A simple python script to parse gamelist.xml files and output what tags are missing from each game found.

Usage: `python parser.py` and type your roms directory e.g. `\\RG351P\roms`. The script will only scan the first subdirectory, not nested subdirectories. Look for output.txt files in a folder created next to wherever you put _parser.py_.

Example output file _genesis_output.txt_:
```
Dynamite Headdy found with missing tags: image
Shinobi III: Return of the Ninja Master found with missing tags: video
Phantasy Star III: Generations of Doom found with missing tags: video
Landstalker found with missing tags: video
```

## Sorter
A simple python script to parse gamelist.xml files and sort them alphabetically by the name tag. Creates backups before parsing.

Usage: `python sorter.py` and type your roms directory e.g. `\\RG351P\roms`. The script will only scan the first subdirectory, not nested subdirectories.

## Sortparse
A combination of the above two scripts.

## Savebackup
A tool that scans immediate directories in the `roms` folder and copies savedata to `saves` next to _savebackup.py_. The script copies Dreamcast memory cards (`bios/dc`) and other emulator savedata `.srm` and `.sav`. 

The file extensions searched can be modified in the script. Because of the complexity of the `roms/ports` folder, it is excluded from the scan.

## CRC32
This script is useful for locating a base rom needed for a romhack or translation patch. Scans a specified directory and outputs the CRC32s to a text file.

Usage: `python crc32.py` and type your directory e.g. `\\RG351P\roms\genesis`. The script will not scan subdirectories.

Example output file _genesis_crc32.txt_:
```
DYNAHEAD_UE.bin: 3DFEEB77
ECCO_TidesofTime.bin: CCB21F98
ECCO_UE.bin: 45547390
```

## muOS-Artscan
This script makes it easy to bring scraper boxart from other CFWs over to muOS. Add all boxart images to their relevant directories, then run the script. It will remove the `-image` suffix from all files it finds that have it, and make the extension `.png`. It will also remove extra files with the following suffixes: `'-titleshot', '-marquee', '-fanart', '-boxback', '-thumb'`.

You can modify the `target_size` variable in script to meet a good size for your device. 400x300 is default.

Drop it in your `muOS/info/catalogue` folder and run it from there.

## Install CIA Files
This `Install CIA Files.sh` file should be placed ideally in your `roms/3ds` folder or `config\modules` for the RockNix Tools menu. It will look in `roms/3ds/cia` for any `.cia` file extensions and install them using the Lime3DS CLI. This is best used for updates and download content.

## EmulationStation Gamelist Rebuilder
If you're importing from ES-DE then you probably have `system.txt` files instead of `gamelist.xml` files, so even if you already have scraped artwork, screenscraper will re-scrape since it assumes artwork is missing. The `rebuild-scraper.py` script remedies that, but only for images. Run the script and provide the path to your roms folder e.g. `\\RG351P\roms` and the script will take care of the rest assuming the artwork in your `images` folder matches the name of the rom in the accompanying system folder.

Suppose you imported scraped artwork for `roms/genesis` and ran `Update Gamelists`, but it didn't get the artwork. Your xml file might look like this.

```xml
<game>
    <path>./DYNAHEAD_UE.bin</path>
    <name>./DYNAHEAD_UE.bin</name>
</game>
```

If you have a file `DYNAHEAD_UE-image.png` in your `images` folder (maybe `roms/genesis/images`) then the script will add `<image>./images/DYNAHEAD_UE-image.png</image>` to this xml block.

```xml
<game>
    <path>./DYNAHEAD_UE.bin</path>
    <name>./DYNAHEAD_UE.bin</name>
    <image>./images/DYNAHEAD_UE-image.png</image>
</game>
```

Bear in mind it is not a replacement for screenscraper, so you may still wish to run screenscraper afterwards to get additional metadata.