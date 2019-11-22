# wp-cron.py
A Python wrapper script to run WP-Cron directly through PHP bypassing web server overhead and to run consecutively if multiple sites

WordPress leaves it optional for this to be done upon initial setup although recommends that it should be done to avoid maintenance tasks from being delayed (https://developer.wordpress.org/plugins/cron/hooking-wp-cron-into-the-system-task-scheduler/)

Original blog announcement explaining much more on the reasons why & how to get it setup:
https://pressjitsu.com/blog/wordpress-cron-cli/

Both links above explain how to schedule it with cron daemon but could also use systemd user timer with lingering for the user.

Besides what would be already needed for a standard or multisite WordPress installation on Linux, WP-CLI is also required to be installed:
https://make.wordpress.org/cli/handbook/installing/

Further work needs done to port the code so works with both Python 2 & 3 but one can use the Python 3 script available at https://github.com/J-Rey/wp-cron.py/tree/Py3 in the meantime.
