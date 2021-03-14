#!/usr/bin/python3
import sys, re

commands = [
    "cat",
    "crontab",
    "hostname",
    "ifconfig",
    "ip",
    "iptables",
    "ls",
    "netstat",
    "pwd",
    "route",
    "uname",
    "whoami"
]
log_file_arg = sys.argv[1]
with open(log_file_arg, "r") as log_file:
    audit_full_msg = log_file.readlines()
    for msg in audit_full_msg:
        for command in commands:
            if command in msg:
                pat = re.findall(r"[(0-9.0-9:0-9)]", msg)
                nums = "".join(pat)
                num_audit_msg = nums[:19]
                print(f"Audit No.: {num_audit_msg}    Command={command}")

