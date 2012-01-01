#
# Regular cron jobs for the msdl package
#
0 4	* * *	root	[ -x /usr/bin/msdl_maintenance ] && /usr/bin/msdl_maintenance
