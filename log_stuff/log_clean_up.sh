#!/bin/bash

backup_audit_log() {
	now=$(date '+%Y-%m-%d')
	cd /var/log/audit/
	echo "creating tarball"
	tar -cvzf audit-log-$now.tar.gz audit.log

	echo "Copyihng tarball to /home/scanuser/..."
	mv ./audit-log-$now.tar.gz /home/scanuser/audit-log-backup/audit-log-$now.tar.gz
}

clear_audit_log() {
	echo "Clearing /var/log/audit/audit.log"
	echo "" > /var/log/audit.log
}

backup_audit_log && clear_audit_log