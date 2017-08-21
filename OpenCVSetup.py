import os
import socket
from pathlib import Path
import Helper

import Constants


def setup_openCV(ip_address):
    plink_location = download_plink()
    # Helper.add_to_environmental_variable("PATH", plink_location)

    plink_terminal_process = initialize_plink_interface(ip_address)

def raspberry_pi_ip_address():
    try:
        return socket.gethostbyname(Constants.raspberry_pi_network_name)
    except socket.gaierror:
        return None


def download_plink():
    location = Constants.download_directory + Constants.plink_save_download_directory

    if Path(location).exists() and {'etcher.exe', 'node_modules'}.issubset(os.listdir(location)):
        print("Files seem to have already been downloaded delete the files  in", location,
              " and rerun the program if you wish to restart download")
    else:
        Helper.download_file(Constants.plink_url, location, Constants.plink_name)

    return str(Path(location).absolute())

import subprocess

def initialize_plink_interface(ip_address):
    ff = subprocess.Popen("plink -s " + Constants.raspberry_pi_user + "@" + ip_address + " -pw " + Constants.raspibery_pi_password, shell=Fasle, stdin=subprocess.PIPE)
    return ff

def run_command(plink_terminal, command):
    plink_terminal.communicate(command)

def run_command_from_file(terminal):
    if not Path.exists(Constants.opencv_instruction_file):
        print("The file that has the commands to download opencv on the rasp")
