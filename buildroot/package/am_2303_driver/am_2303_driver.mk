################################################################################
#
# am_2303_driver - out-of-tree Linux kernel module
#
################################################################################

AM_2303_DRIVER_VERSION = 1.0
AM_2303_DRIVER_SITE = http://www.foosoftware.org/download

# If you are developing locally, you can override the source:
AM_2303_DRIVER_OVERRIDE_SRCDIR = ../am2303_driver

# If additional options are needed for building, for example:
AM_2303_DRIVER_MAKE_OPTS = -j$(nproc)   # any additional options

# Declare dependency on the Linux kernel package so that the module is rebuilt if the kernel is changed.
AM_2303_DRIVER_DEPENDENCIES = linux

# Use the kernel module package infrastructure.
# $(eval $(linux-module-package))
$(eval $(kernel-module))
$(eval $(generic-package))
