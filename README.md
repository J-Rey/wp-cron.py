# wp-cron.py
A Python wrapper script to run WP-Cron directly through PHP bypassing web server overhead and to run concurrently if multiple sites

WordPress leaves it optional for this to be done upon initial setup although recommends that it should be done to avoid maintenance tasks from being delayed (https://developer.wordpress.org/plugins/cron/hooking-wp-cron-into-the-system-task-scheduler/)

Original blog post explaining more on the reasons why & how to get it setup:
https://pressjitsu.com/blog/wordpress-cron-cli/

Besides standard or multisite WordPress installation(s) on Linux, WP-CLI is also required to be installed:
https://make.wordpress.org/cli/handbook/installing/
