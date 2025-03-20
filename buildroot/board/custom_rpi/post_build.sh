#!/bin/sh

set -u
set -e

find /lib/modules/*/updates -type f -name *driver*ko* -exec xz -d {} \;

