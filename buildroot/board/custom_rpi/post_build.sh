#!/bin/sh

set -u
set -e

find $TARGET_DIR/lib/modules/*/updates -type f -name *driver*ko* -exec xz -d {} \;

# If inittab exists, add a sysinit entry to load driver modules
if [ -e "${TARGET_DIR}/etc/inittab" ]; then
    # Add the modload entry if it doesn't already exist
    if ! grep -q "::sysinit:/bin/sh -c 'find /lib/modules" "${TARGET_DIR}/etc/inittab"; then
        echo "::sysinit:/bin/sh -c 'find /lib/modules/*/updates -type f -name \"*driver*ko*\" -exec insmod {} \;'" >> "${TARGET_DIR}/etc/inittab"
    fi  
else
    echo "Error: ${TARGET_DIR}/etc/inittab not found." >&2
    exit 2
fi
