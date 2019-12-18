#!/usr/bin/python
# Runs WP-Cron (wp-cron.php) locally & consecutively for all WordPress installs listed on the server or found in a multisite network
# Version 1.0 from https://github.com/pressjitsu/wp-cron.py
# Version 1.1+ from https://github.com/J-Rey/wp-cron.py

# Configuration
# If multisite then sites in the network will automatically be found so only need to list the main directory per multisite network
# and for each single install. If only one then like this is fine: WP_DIRS = {'/home/username/public_html'}
WP_DIRS = {'/home/username0/public_html', '/home/username1/public_html', '/home/username2/public_html'}
# Path to the WP-CLI binary + any optional parameters
WP_CLI_PATH = '/usr/local/bin/wp'
# Path to the standard PHP binary + any optional parameters (like -ddisplay_errors=E_ERROR to filter out warnings till fixed)
PHP_PATH = '/usr/bin/php'

import json
import subprocess
import sys, fcntl
import os, pwd
from urllib.parse import urlparse

# Don't run more than once simultaneously.
fp = open('/tmp/wp-cron.pid', 'w')
try:
	fcntl.lockf(fp, fcntl.LOCK_EX | fcntl.LOCK_NB)
except IOError:
	print ('Another instance of wp-cron.py is already running')
	exit()

# Don't run as root.
username = pwd.getpwuid(os.getuid()).pw_name
if username == 'root':
	print ('Do not run as root')
	exit()

# Things that could be used in wp-config.php
env = {
	'HTTP_HOST': '',
	'REQUEST_URI': '',
}

# Loop through the install directories
for WP_DIR in WP_DIRS:

	# Get a list of available sites on the account/in the network
	s = subprocess.check_output([WP_CLI_PATH, '--path=%s' % WP_DIR, '--skip-themes', '--skip-plugins', 'eval', '''
		$urls = array();

		if ( ! is_multisite() ) {
			$urls[] = home_url();
		} else {
			foreach ( wp_get_sites() as $blog ) {
				$urls[] = get_home_url( $blog['blog_id'] );
			}
		}

		echo json_encode( $urls );
		exit;
	'''], env=env)

	urls = json.loads(s)
	for url in urls:
		url = urlparse(url)
		if url.scheme not in ['http', 'https']:
			continue

		# Set up env variables for PHP CLI.
		env = {
			'QUERY_STRING': '',
			'REQUEST_METHOD': 'POST',
			'CONTENT_TYPE': '',
			'CONTENT_LENGTH': '',
			'REQUEST_URI': '/wp-cron.php',
			'REQUEST_SCHEME': 'http',
			'REMOTE_ADDR': '127.0.0.1',
			'SERVER_NAME': url.hostname,
			'HTTP_HOST': url.hostname,
			'HTTP_USER_AGENT': 'wp-cron.py',
			'SERVER_PROTOCOL': 'HTTP/1.1',
		}

		if url.scheme == 'https':
			env['REQUEST_SCHEME'] = 'https'
			env['HTTPS'] = 'on'
			env['SERVER_PORT'] = '443'

		try:
			# Run wp-cron.php via PHP CLI.
			s = subprocess.check_output([PHP_PATH, '%s/wp-cron.php' % WP_DIR], env=env)
			print ('Succeeded running wp-cron.php for %s' % url.hostname)
		except subprocess.CalledProcessError:
			print ('Error running wp-cron.php for %s' % url.hostname)
			continue
