#!/bin/bash

# SPDX-License-Identifier: GPL-2.0-or-later
# Copyright (C) 2024-present ROCKNIX (https://github.com/ROCKNIX)

. /etc/profile
set_kill set "-9 lime3ds"

control-gen_init.sh
source /storage/.config/gptokeyb/control.ini
get_controls

[ ! -d /storage/.config/lime3ds ] && cp -r /usr/config/lime3ds /storage/.config

[ ! -d /storage/roms/3ds/lime3ds/sdmc ] && mkdir -p /storage/roms/3ds/lime3ds/sdmc
rm -rf /storage/.config/lime3ds/sdmc
ln -sf /storage/roms/3ds/lime3ds/sdmc /storage/.config/lime3ds/sdmc

[ ! -d /storage/roms/3ds/lime3ds/nand ] && mkdir -p /storage/roms/3ds/lime3ds/nand
rm -rf /storage/.config/lime3ds/nand
ln -sf /storage/roms/3ds/lime3ds/nand /storage/.config/lime3ds/nand

rm -rf /storage/.local/share/lime3ds
ln -sf /storage/.config/lime3ds /storage/.local/share/lime3ds

install_cia() {
    $GPTOKEYB lime3ds -c /storage/.config/lime3ds/lime3ds.gptk &
    for cia in "${cia_files[@]}"; do
        echo "Installing ${cia}..." | tee -a "$CIALOG"
        /usr/bin/lime3ds -i "${cia}" 2>&1 | while read -r line; do
            if [[ "$line" =~ lime_sdl/lime_sdl\.cpp:operator\(\):249 ]]; then
                # Extract and refresh the percentage line, but don't log it to the file
                echo -ne "\r${line##*lime_sdl/lime_sdl.cpp:operator():249: }"
            # Filter for lines that are relevant and remove fluff
            elif [[ "$line" =~ "Installed" ]]; then
                # Clean up 'Installed' lines
                echo && echo "$line" | sed -E 's/.*Installed\s+(.+)\.cia\s+successfully\./Successfully installed \1./' | tee -a "$CIALOG" && echo
            elif [[ "$line" =~ "Error" ]]; then
                # Clean up error lines
                echo "$line" | sed -E 's/.*<Error>.*:\s*(.*)/Error: \1/' | tee -a "$CIALOG"
            elif [[ "$line" =~ "invalid" ]]; then
                # Log lines containing "invalid"
                echo "$line" | tee -a "$CIALOG"
            fi
        done
    done
    pkill -9 gptokeyb
}

# Logging
CIADIR=~/roms/3ds/cia
CIALOG=~/roms/3ds/cia_install_log.txt
> $CIALOG

# Check for .cia files
cia_files=()
if [ -d "$CIADIR" ]; then
  for file in "$CIADIR"/*.cia; do
    [ -e "$file" ] && cia_files+=("$file")
  done
fi

if [ "${#cia_files[@]}" -eq 0 ]; then
  echo "No CIA files found in ${CIADIR} or directory ${CIADIR} does not exist!" | tee -a "$CIALOG"
  sleep 5
  exit 1
else
  echo "Found ${#cia_files[@]} CIA file(s) in ${CIADIR}" | tee -a "$CIALOG"
  install_cia
fi

