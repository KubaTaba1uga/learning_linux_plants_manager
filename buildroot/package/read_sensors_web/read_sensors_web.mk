READ_SENSORS_WEB_VERSION = 1.0
READ_SENSORS_WEB_SOURCE = read_sensors_web.py
READ_SENSORS_WEB_SITE_METHOD = local
READ_SENSORS_WEB_SITE = ../read_sensors_web/
READ_SENSORS_WEB_INSTALL_TARGET = usr/bin
READ_SENSORS_WEB_DEPENDENCIES += python3 python-fastapi python-uvicorn


define READ_SENSORS_WEB_INSTALL_TARGET_CMDS
    $(INSTALL) -D -m 0755 $(@D)/read_sensors_web.py $(TARGET_DIR)/$(READ_SENSORS_WEB_INSTALL_TARGET)/read_sensors_web.py
endef

$(eval $(generic-package))
