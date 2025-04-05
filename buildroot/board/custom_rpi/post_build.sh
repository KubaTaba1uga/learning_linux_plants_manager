#!/bin/sh

set -u
set -e

# Reusable function that appends a line to a file only if that line is not already present.
add_line_if_not_present() {
    local file="$1"
    local line="$2"
    if ! grep -qF "$line" "$file"; then
        echo "$line" >> "$file"
    fi
}

# Decompress driver modules
find $TARGET_DIR/lib/modules/*/updates -type f -name *driver*ko* -exec xz -d {} \;

# If inittab exists, add a sysinit entry to load driver modules
if [ -e "${TARGET_DIR}/etc/inittab" ]; then
    add_line_if_not_present \
        "${TARGET_DIR}/etc/inittab" \
        "::sysinit:/bin/sh -c 'find /lib/modules/*/updates -type f -name *2303*driver*ko* -exec insmod {} \;'"
    
    add_line_if_not_present \
        "${TARGET_DIR}/etc/inittab" \
        "::sysinit:/bin/sh -c 'find /lib/modules/*/updates -type f -name *7830*driver*ko* -exec insmod {} mp_min_voltage_output=10 mp_max_voltage_output=23 \;'"

    add_line_if_not_present \
        "${TARGET_DIR}/etc/inittab" \
        "::sysinit:/bin/sh -c 'find /lib/modules/*/updates -type f -name *irrigation*driver*ko* -exec insmod {} \;'"
    
else
    echo "Error: ${TARGET_DIR}/etc/inittab not found." >&2
    exit 2
fi
