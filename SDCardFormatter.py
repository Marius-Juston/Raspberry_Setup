import os
import time
from pathlib import Path

import Constants
import Helper


def enable_ssh(sd_card_location):
    Helper.create_open_file(sd_card_location + b'ssh', 'w+').close()


def enable_camera(sd_card_location):
    # TODO make it so that it replace adn finds the config.txt file

    file_directory = sd_card_location + b'config.txt'

    if not Path(file_directory.decode("utf-8")).exists():
        file = Helper.create_open_file(file_directory, "wr+")

    else:
        file = Helper.create_open_file(file_directory, "a+")

    lines = file.readlines()

    changed = False

    if len(lines) != 0:
        for l in lines:
            if Constants.camera_enable_config_line in l:
                l.replace(Constants.camera_enable_config_line + "0", Constants.camera_enable_config_line + "1")
                changed = True

    elif len(lines) == 0 or not changed:
        lines.append(Constants.camera_enable_config_line + "1")
        changed = True

    if changed:
        file.writelines(lines)

    file.close()

def setup_sd_card():
    sd_card_location = get_SD_card_location()

    etcher_location = download_etcher()
    Helper.add_to_environmental_variable(Constants.path_variable_name, etcher_location)
    image_location = download_raspberry_iso()
    #
    run_etcher(sd_card_location, image_location)

    enable_ssh(sd_card_location)
    enable_camera(sd_card_location)


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


def get_SD_card_location(already=False):
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

    if len(devices) < 2:
        if not already:
            print("There are no available SD card (check that SD card is " + str(
                Constants.sd_card_min_size / 1000000000) + " GB of higher) this will keep looking for one every 0.5 seconds")
        time.sleep(.5)
        return get_SD_card_location(True)


    elif len(devices) >= 2:
        print("SD card found")

        if len(devices) > 2:
            print("There are more than 1 SD card that meet the requirements. Picking the first one....")

        return devices[1] + b"/"
