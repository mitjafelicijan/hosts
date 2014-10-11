#!/usr/bin/python

"""
The MIT License (MIT)

Copyright (c) 2014 Mitja Felicijan <mitja.felicijan@gmail.com>

Permission is hereby granted, free of charge, to any person obtaining a copy
of this software and associated documentation files (the "Software"), to deal
in the Software without restriction, including without limitation the rights
to use, copy, modify, merge, publish, distribute, sublicense, and/or sell
copies of the Software, and to permit persons to whom the Software is
furnished to do so, subject to the following conditions:

The above copyright notice and this permission notice shall be included in
all copies or substantial portions of the Software.

THE SOFTWARE IS PROVIDED "AS IS", WITHOUT WARRANTY OF ANY KIND, EXPRESS OR
IMPLIED, INCLUDING BUT NOT LIMITED TO THE WARRANTIES OF MERCHANTABILITY,
FITNESS FOR A PARTICULAR PURPOSE AND NONINFRINGEMENT. IN NO EVENT SHALL THE
AUTHORS OR COPYRIGHT HOLDERS BE LIABLE FOR ANY CLAIM, DAMAGES OR OTHER
LIABILITY, WHETHER IN AN ACTION OF CONTRACT, TORT OR OTHERWISE, ARISING FROM,
OUT OF OR IN CONNECTION WITH THE SOFTWARE OR THE USE OR OTHER DEALINGS IN
THE SOFTWARE.
"""

import sys
import os.path
import socket

class config:
	version = '0.0.1'
	appname = 'Hosts file toggler'
	hosts = '/etc/hosts'
	edited = False
	apphelp = '''\

Because we are attempting to modify system files we need to execute 
script with root privileges. So use it with sudo.

sudo ./hosts.py --version
sudo ./hosts.py --help
sudo ./hosts.py path-to-your-hosts-file
(by default /etc/hosts will be used)
'''

class screen:
	header = '\033[95m'
	blue = '\033[94m'
	gray = '\033[2m'
	green = '\033[92m'
	yellow = '\033[33m'
	red = '\033[91m'
	bold = '\033[1m'
	clear = '\033[2J\033[H'
	endc = '\033[0m'
	title = '\033[45m\033[1m'
	space = ' '
	dblspace = '  '
	newline = '\n'
	dblnewline = '\n\n'

def valid_ip(address):
	parts = address.split('.')
	if len(parts) != 4:
		return False
	for item in parts:
		if not 0 <= int(item) <= 255:
			return False
	return True

def parse_arguments():
	if len(sys.argv) > 1:
		if sys.argv[1] == '--version':
			print config.appname + ', version : ' + config.version
			sys.exit(0)
		elif sys.argv[1] == '--help':
			print config.appname + ', version : ' + config.version
			print config.apphelp
			sys.exit(0)
		else:
			config.hosts = sys.argv[1]

def get_entries(hosts_file):
	host_entries = []
	if not os.path.isfile(hosts_file):
		print 'Hosts file does not exist'
		sys.exit(0)
	else:
		hosts = open(hosts_file, 'r')
		for line in hosts:
			entry = line.split()
			host_entries.append(entry)
		return host_entries

def draw_list(entries):
	print screen.dblspace + screen.title + screen.dblspace + config.appname  + screen.dblspace + screen.endc + screen.newline
	i = 1
	for entry in entries:
		if entry:
			if (valid_ip(entry[0])):
				print screen.green + '  [' + str(i) + '] ' + screen.endc + screen.green + ' '.join(entry) + screen.endc
			elif entry[0] == '#' and valid_ip(entry[1]):
				print screen.gray + '  [' + str(i) + '] ' + screen.endc + screen.gray + ' '.join(entry).replace('# ', '') + screen.endc
		i += 1

def update_host(line_number):
	hosts_file = open(config.hosts)
	lines = hosts_file.readlines()
	lines[line_number-1] = str(lines[line_number-1].strip())

	if lines[line_number-1][:1] == '#':
		lines[line_number-1] = lines[line_number-1].replace('# ', '', 1) + '\n'
	else:
		lines[line_number-1] = '# ' + lines[line_number-1] + '\n'
	
	updated = ''
	for line in lines:
		updated += line
	try:
		hosts_file = open(config.hosts, 'w')
		hosts_file.write(updated)
		hosts_file.close()
	except:
		print screen.newline + screen.dblspace + screen.red + screen.bold + 'Permission denied: /etc/hosts'
		print screen.dblspace + 'Use script with root privileges or with sudo' + screen.endc +screen.dblnewline
		sys.exit(0)
	

parse_arguments()

while 1:
	print screen.clear
	entries = get_entries(config.hosts)
	draw_list(entries)

	if config.edited:
		print screen.newline + screen.dblspace + screen.bold + screen.red + 'Host with id=' + str(config.edited) + ' edited ...' + screen.endc 
		config.edited = False
	
	choice = raw_input(screen.newline + screen.dblspace + screen.yellow + 'Toggle host entry: ')

	if choice in ['Q','q']: break
	elif choice in ['R','r']: pass
	elif choice.isdigit():
		config.edited = choice
		update_host(int(choice))
