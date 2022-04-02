#!/bin/python3
import subprocess
import argparse
'''
This script is created to automate the process of cracking hashes with johntheripper when you have a list of hash formats.
Use tools like: "hashid -j hash" to identify the possible john's hash format for a hash.
'''


# Some colors I use here (bright) is non-standard, if it doesn't display nicely in your terminal, refer to this link:
# https://en.wikipedia.org/wiki/ANSI_escape_code#SGR_.28Select_Graphic_Rendition.29_parameters
class bcolors:
    HEADER = '\033[95m'  # Bright Magenta
    OKBLUE = '\033[94m'  # Bright Blue
    OKCYAN = '\033[96m'  # Bright Cyan
    OKGREEN = '\033[92m'  # Bright Green
    WARNING = '\033[93m'  # Bright Yellow
    FAIL = '\033[91m'  # Bright Red
    ENDC = '\033[0m'  # Reset or normal
    BOLD = '\033[1m'  # Bold
    UNDERLINE = '\033[4m'  # Underline


def get_arguments():
    parser = argparse.ArgumentParser()
    parser.add_argument("-w", "--wordlist", dest="wordlist", help="The wordlist to be used", required=True)
    parser.add_argument("-p", "--password", dest="password", help="The password/hash to be cracked (file)", required=True)
    parser.add_argument("-f", "--formats", dest="formats", help="The formats for john (stored in a file separated by newline)", required=True)
    options = parser.parse_args()

    return options


options = get_arguments()

wordlist = options.wordlist
hash_file = options.password
formats_file = options.formats

formats = []
# Read and store all formats from the file
with open(formats_file, "r") as file:
    formats_lines = file.readlines()
    for line in formats_lines:
        formats.append(line.strip())

# Start cracking with each format
for format in formats:
    try:
        print(f"{bcolors.HEADER}[+] Cracking with format: {format}{bcolors.ENDC}")
        output = subprocess.check_output(f"john -w={wordlist} --format={format} {hash_file}", shell=True, stderr=subprocess.STDOUT)
        # Password cracked
        if "--show" in output.decode():
            print(f"{bcolors.OKGREEN}[+] Cracked with {format}{bcolors.ENDC}")
            print(output.decode())
            break
        # Password is cracked before this
        if "No password hashes left to crack" in output.decode():
            print(f"{bcolors.WARNING}[-] Password is cracked before with format: {format}{bcolors.ENDC}")
            print(output.decode())
            break
        # Password is not compatible with this format
        if "No password hashes loaded" in output.decode():
            print(f"{bcolors.FAIL}[-] {format} format might not compatible with this hash{bcolors.ENDC}")

        print(output.decode())
    except subprocess.CalledProcessError:
        print(f"{bcolors.FAIL}[-] {format} format might not be supported by john\n{bcolors.ENDC}")
