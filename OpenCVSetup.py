import socket
import subprocess
from pathlib import Path

import Constants
import Helper
import Network


def get_commands(command_file):
    file = Helper.create_open_file(command_file, "r")

    commands = []

    current_batch = ""

    for line in file.readlines():
        if not line.startswith("\n") and not line.startswith("#"):
            current_batch += line

            if "sudo reboot" in line:
                commands.append(current_batch)
                current_batch = ""

            elif "sudo halt" in line:
                commands.append(current_batch)
                break

    if current_batch is not commands[len(commands) - 1] or current_batch is not "":
        commands.append(current_batch)

    return commands


def setup_openCV(ip_address):
    print("downloading plink")
    download_plink()

    print("Getting commands from the " + Constants.opencv_instruction_file + " file")
    commands = get_commands(Constants.opencv_instruction_file)

    for command in commands:
        if Network.ping(ip_address):
            initialize_plink_interface(ip_address, command)
        else:
            print("could not find " + ip_address + " waiting for ping")
            Network.wait_for_ping(ip_address)


def raspberry_pi_ip_address():
    try:
        return socket.gethostbyname(Constants.raspberry_pi_network_name)
    except socket.gaierror:
        return None


def download_plink():
    location = Constants.download_directory + Constants.plink_save_download_directory

    if Path(location).exists():
        print("Files seem to have already been downloaded delete the files  in", location,
              " and rerun the program if you wish to restart download")
    else:
        Helper.download_file(Constants.plink_url, location, Constants.plink_name)

    return str(Path(location).absolute())


def initialize_plink_interface(ip_address, commands):
    ff = subprocess.Popen(
        "plink -ssh " + Constants.raspberry_pi_user + "@" + ip_address + " -pw " + Constants.raspberry_pi_password + " " + commands,
        shell=False, stdin=subprocess.PIPE, stdout=subprocess.PIPE, stderr=subprocess.PIPE, universal_newlines=True)
    return ff


def run_command(plink_terminal, command):
    plink_terminal.communicate(command)
