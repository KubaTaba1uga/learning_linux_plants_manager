READ_SENSORS_JOB_VERSION = 1.0
READ_SENSORS_JOB_SOURCE = read_sensors_job.py
READ_SENSORS_JOB_SITE_METHOD = local
READ_SENSORS_JOB_SITE = ../read_sensors_job
READ_SENSORS_JOB_DEPENDENCIES = python3

CRON_DIR = $(TARGET_DIR)/etc/cron/crontabs
CRON_FILE = $(CRON_DIR)/root
CRON_LINE = 0 * * * * python3 /opt/read_sensors_job.py

define READ_SENSORS_JOB_INSTALL_TARGET_CMDS
	chmod 0755 $(@D)/read_sensors_job.py
	cp $(@D)/read_sensors_job.py $(TARGET_DIR)/opt

	# Ensure the cron directory exists
	if [ ! -d "$(CRON_DIR)" ]; then \
	  mkdir -p "$(CRON_DIR)"; \
	fi

	# Ensure the cron file exists
	if [ ! -f "$(CRON_FILE)" ]; then \
	  touch "$(CRON_FILE)"; \
	fi

	# Append the job line if missing
	grep -qxF "$(CRON_LINE)" "$(CRON_FILE)" || echo "$(CRON_LINE)" >> "$(CRON_FILE)"
endef

$(eval $(generic-package))
