#!/bin/bash

# Batch install any .cia files in /roms/3ds/cia using a discovered emulator

set -euo pipefail

# Source profile for environment variables
. /etc/profile

# Initialize control settings
control-gen_init.sh
source /storage/.config/gptokeyb/control.ini
get_controls

# Logging
CIADIR=~/roms/3ds/cia
CIALOG=~/roms/3ds/cia_install_log.txt
> "$CIALOG"

# Detect emulator based on available binaries
if [[ -x /usr/bin/lime3ds ]]; then
    EMULATOR="lime3ds"
    EMULATOR_CMD="/usr/bin/lime3ds"
    GPTOKEYB_CMD="$GPTOKEYB lime3ds -c /storage/.config/lime3ds/lime3ds.gptk"
    PROC_NAME="lime3ds"
elif [[ -x /usr/bin/azahar ]]; then
    EMULATOR="azahar"
    EMULATOR_CMD="/usr/bin/azahar"
    GPTOKEYB_CMD="$GPTOKEYB azahar -c /storage/.config/azahar/azahar.gptk"
    PROC_NAME="azahar"
elif [[ -x /usr/bin/citra ]]; then
    EMULATOR="citra"
    EMULATOR_CMD="/usr/bin/citra"
    GPTOKEYB_CMD="$GPTOKEYB citra -c /storage/.config/citra/citra.gptk"
    PROC_NAME="citra"
else
    echo "No supported 3DS emulator binary found!" | tee -a "$CIALOG"
    exit 1
fi

# Emulator-specific config setup
if [ ! -d "/storage/.config/$EMULATOR" ]; then
    cp -r "/usr/config/$EMULATOR" "/storage/.config/"
fi

# Create ROM directories and safe symlinks
for dir in sdmc nand; do
    ROM_DIR="/storage/roms/3ds/$EMULATOR/$dir"
    CONFIG_DIR="/storage/.config/$EMULATOR/$dir"

    mkdir -p "$ROM_DIR"

    if [ ! -L "$CONFIG_DIR" ] || [ ! -e "$CONFIG_DIR" ]; then
        ln -sf "$ROM_DIR" "$CONFIG_DIR"
    fi
done

# Set up safe share directory symlink
SHARE_DIR="/storage/.local/share/$EMULATOR"
if [ ! -L "$SHARE_DIR" ] || [ ! -e "$SHARE_DIR" ]; then
    mkdir -p "$(dirname "$SHARE_DIR")"
    ln -sf "/storage/.config/$EMULATOR" "$SHARE_DIR"
fi

# Install CIA files in parallel with concurrency control
install_cia() {
    $GPTOKEYB_CMD &  # Start controller handling once
    pids=()

    for cia in "${cia_files[@]}"; do
        (
            echo "Installing ${cia}..." | tee -a "$CIALOG"

            # Run emulator for this CIA
            $EMULATOR_CMD -i "${cia}" 2>&1

            # Log success/failure per CIA
            if [ "${PIPESTATUS[0]}" -eq 0 ]; then
                echo -e "\nSuccessfully installed $(basename "$cia")." | tee -a "$CIALOG"
            else
                echo -e "\nFailed to install $(basename "$cia"). Check log for details." | tee -a "$CIALOG"
            fi
        ) &
        pids+=($!)

        # Limit number of concurrent installs for stability
        while [ "${#pids[@]}" -ge 6 ]; do
            for i in "${!pids[@]}"; do
                if ! kill -0 "${pids[i]}" 2>/dev/null; then
                    unset 'pids[i]'
                fi
            done
            sleep 1
        done
    done

    # Wait for all remaining jobs
    for pid in "${pids[@]}"; do
        wait "$pid"
    done

    pkill -9 "$PROC_NAME"
}

# Discover CIA files
cia_files=()
if [ -d "$CIADIR" ]; then
    readarray -t cia_files < <(find "$CIADIR" -type f -name "*.cia")
fi

if [ "${#cia_files[@]}" -eq 0 ]; then
    echo "No CIA files found in ${CIADIR} or directory ${CIADIR} does not exist!" | tee -a "$CIALOG"
    sleep 5
    exit 1
else
    echo "Found 3DS emulator ${EMULATOR}"
    echo "Found ${#cia_files[@]} CIA file(s) in ${CIADIR}" | tee -a "$CIALOG"
    install_cia
fi
