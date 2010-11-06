#
# Regular cron jobs for the tvdownloader package
#
0 4	* * *	root	[ -x /usr/bin/tvdownloader_maintenance ] && /usr/bin/tvdownloader_maintenance
