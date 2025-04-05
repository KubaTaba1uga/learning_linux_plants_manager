READ_SENSORS_JOB_VERSION = 1.0
READ_SENSORS_JOB_SOURCE = read_sensors_job.py
READ_SENSORS_JOB_SITE_METHOD = local
READ_SENSORS_JOB_SITE = ../read_sensors_job
READ_SENSORS_JOB_DEPENDENCIES = python3

READ_SENSORS_JOB_CRON_DIR = $(TARGET_DIR)/etc/cron/crontabs
READ_SENSORS_JOB_CRON_FILE = $(READ_SENSORS_JOB_CRON_DIR)/root
READ_SENSORS_JOB_CRON_LINE = 0 * * * * python3 /opt/read_sensors_job.py

define READ_SENSORS_JOB_INSTALL_TARGET_CMDS
	echo ">>> Installing read_sensors_job <<<"
	chmod 0755 $(@D)/read_sensors_job.py
	cp $(@D)/read_sensors_job.py $(TARGET_DIR)/opt

	mkdir -p $(READ_SENSORS_JOB_CRON_DIR)
	touch $(READ_SENSORS_JOB_CRON_FILE)
	grep -qxF '$(READ_SENSORS_JOB_CRON_LINE)' $(READ_SENSORS_JOB_CRON_FILE) || echo '$(READ_SENSORS_JOB_CRON_LINE)' >> $(READ_SENSORS_JOB_CRON_FILE)
endef

$(eval $(generic-package))
