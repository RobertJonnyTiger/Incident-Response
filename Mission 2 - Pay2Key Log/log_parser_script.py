#!/usr/bin/python3
"""
Description:
Parses log.txt as requested:
## Objectives:
  1. How many users are in the file?
  2. How many of them are active users?
  3. A list of active users with their related groups in the following format:
   > User:\<username\>|Groups:\<all_groups\>
"""
import re
import subprocess
import os
pwd = os.getcwd()

file = open("log.txt", "r")
lines = file.readlines()

# Answer objective 1:
num_users = subprocess.check_output("cat log.txt | grep \"User name\" | wc -l", shell = True).decode()

# Answer objective 2:
num_active_users = subprocess.check_output("cat log.txt | grep \"Account active\" | awk '{print $3}' | grep Yes | wc -l", shell = True).decode()

# Answer objective 3:
output_file = 'parsed_log.txt'
user_format = 'User:'
groups_format = '|Groups:'
groups_prefix_sign = '*'
groups_title = 'Global Group memberships'
username_index = 29
delimeter = "----"

with open(output_file, 'a+') as parsed_file:
	parsed_file.write(f'1. Number of users in the file: {num_users}')
	parsed_file.write(f'2. Number of active users in the file: {num_active_users}')
	parsed_file.write('3. List of active users with their related groups:\n')
	parsed_file.write('============================================================')
	for line in lines:
		if 'User name' in line:
			parsed_file.write(user_format + line[username_index:].strip() + groups_format)
		if groups_prefix_sign in line:
			groups = re.sub(groups_title, '', line)
			line_stripped = groups.replace(' ', '')
			no_newline = line_stripped.strip()
			parsed_file.write(no_newline)
		if delimeter in line:
			parsed_file.write('\n')
	parsed_file.write('\n')  # Makes output more pretty
	
print(f'1. Number of users in the file: {num_users}'
      f'2. Number of active users in the file: {num_active_users}'
      f'3. [+] Saved active usernames and groups at {pwd}/{output_file}.')
