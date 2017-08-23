import os
import time
from pathlib import Path

import Constants
import Helper
import Network
import Terminal


def enable_ssh(sd_card_location):
    Helper.create_open_file(sd_card_location + b'ssh', 'w+').close()


def enable_camera(sd_card_location):
    file_directory = sd_card_location + b'config.txt'

    lines = []

    if Path(Helper.decode(file_directory)).exists():
        with Helper.create_open_file(file_directory, "r") as file:
            lines = file.readlines()

    file_write = Helper.create_open_file(file_directory, "w+")

    if len(lines) != 0:
        for i in range(len(lines)):
            if Constants.camera_enable_config_line + "0" in lines[i]:
                lines[i] = lines[i].replace(Constants.camera_enable_config_line + "0",
                                            Constants.camera_enable_config_line + "1")

    elif len(lines) == 0:
        lines.append(Constants.camera_enable_config_line + "1")

    file_write.writelines(lines)

    file_write.close()


def setup_wifi(sd_card_location, network_info):
    file_directory = sd_card_location + b'wpa_supplicant.conf'
    file_write = Helper.create_open_file(file_directory, "w+")


    lines = ["network={\n",
             '\tssid="' + network_info[0] + '"\n',
             '\tpsk="' + network_info[1] + '"\n',
             '\tkey_mgmt=WPA-PSK\n',
             "}"
             ]

    file_write.writelines(lines)
    file_write.close()


def eject_SD_card_prompt():
    Terminal.run_command("RunDll32.exe shell32.dll,Control_RunDLL hotplug.dll")


def set_static_ip(sd_card_location, network_info):
    file_directory = sd_card_location + 'cmdline.txt'
    file_write = Helper.create_open_file(file_directory, "a+" if os.path.exists(file_directory) else "w+")

    file_write.write(" ip=" + Constants.raspberry_pi_ip_address +
                     "::" + network_info[2] +
                     ":" + Constants.raspberry_pi_netmask +
                     ":rpi:eth0:off")
    file_write.close()

def setup_sd_card():
    sd_cards = get_SD_card_location()

    print("Locating avaliable SD card in system")
    sd_card_location = look_for_sd_card(sd_cards)

    print("Using the SD card at ", Helper.decode(sd_card_location))

    print("Downloading etcher")
    etcher_location = download_etcher()
    print("Finished downloading etcher at", etcher_location)

    print("Adding etcher to environmental of the program")
    Helper.add_to_environmental_variable(Constants.path_variable_name, etcher_location)

    print("Downloading ISO image file")
    image_location = download_raspberry_iso()
    print("Finished downloading ISO image file at ", image_location)

    print("Running etcher with drive as ", Helper.decode(sd_card_location) + " and using the ISO image file at",
          image_location)
    run_etcher(Helper.decode(sd_card_location), image_location)
    print("Finished running etcher")

    print("Enabling SSH on raspberry pi")
    enable_ssh(sd_card_location)

    print("Enabling camera on raspberry pi")
    enable_camera(sd_card_location)

    network_info = Network.get_current_network()

    print("Setting up wifi on raspberry pi. The raspberry pi will use your network and network password to connect")
    setup_wifi(sd_card_location, network_info)

    print("Setting static ip address of the Raspberry Pi to ", Constants.raspberry_pi_ip_address)
    set_static_ip(sd_card_location, network_info)

    print("Openning prompt to eject SD card")
    eject_SD_card_prompt()

    print("Finished setting up Raspberry Pi SD card")

def download_etcher():
    location = Constants.download_directory + Constants.etcher_download_directory

    if Path(location).exists() and {'etcher.exe', 'node_modules'}.issubset(os.listdir(location)):
        print("Files seem to have already been downloaded delete the files  in", location,
              " and rerun the program if you wish to restart download")
    else:
        Helper.extract_zip(Constants.etcher_window64_setup, location)

    return str(Path(location).absolute())


def remove_useless_files():
    Helper.remove_file(Constants.download_directory + Constants.etcher_window64_setup_name)


def download_raspberry_iso():
    location = Constants.download_directory + Constants.debian_jessie_with_raspberry_desktop_download_directory

    if Path(location).exists() and Constants.debian_jessie_with_raspberry_desktop_name in os.listdir(location):
        print("Files seem to have already been downloaded delete the files  in", location, "and rerun the program "
                                                                                           "if you wish to restart "
                                                                                           "download")
    else:
        Helper.download_file(Constants.debian_jessie_with_raspberry_desktop, location,
                             Constants.debian_jessie_with_raspberry_desktop_name)

    return location + Constants.debian_jessie_with_raspberry_desktop_name


def run_etcher(drive, iso_location):
    Helper.run_program_as_admin("etcher", "-d " + drive + " " + iso_location)


def look_for_sd_card(devices, already=False):
    if len(devices) < 2:
        if not already:
            print("There are no available SD card (check that SD card is " + str(
                Constants.sd_card_min_size / 1000000000) + "GB of higher) this will keep looking for one every 0.5 "
                                                           "seconds")
        time.sleep(.5)
        return look_for_sd_card(get_SD_card_location(), already=True)


    elif len(devices) >= 2:
        print("SD card found")

        if len(devices) > 2:
            print("There are more than 1 SD card that meet the requirements. Picking the first one....")

        return devices[1] + b"/"


def get_SD_card_location():
    import subprocess
    df = subprocess.check_output(
        'wmic logicaldisk '
        'where "'
        'size>=' + str(Constants.sd_card_min_size) + ' and '
                                                     'drivetype=2 and '
                                                     'filesystem=\'FAT32\' and '
                                                     'description=\'Removable Disk\'" '
                                                     'get name')

    devices = df.replace(b"\r\r\n", b"").split()
    return devices
