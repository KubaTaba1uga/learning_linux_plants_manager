################################################################################
#
# am_2303_driver - out-of-tree Linux kernel module
#
################################################################################

AM_2303_DRIVER_VERSION = 1.0
AM_2303_DRIVER_SITE = https://github.com/KubaTaba1uga/kernel_am2303_driver

# If you are developing locally, you can override the source:
AM_2303_DRIVER_OVERRIDE_SRCDIR = ../am2303_driver

# Use the kernel module package infrastructure.
$(eval $(kernel-module))
$(eval $(generic-package))
