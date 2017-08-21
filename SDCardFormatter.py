import os
from pathlib import Path

import Constants
import Helper


def enable_ssh(sd_card_location):
    Helper.create_open_file(sd_card_location+'ssh').close()

def enable_camera(sd_card_location):
    pass

def setup_sd_card():
    etcher_location = download_etcher()
    Helper.add_to_environmental_variable(Constants.path_variable_name, etcher_location)
    image_location = download_raspberry_iso()

    sd_card_location = get_SD_card_location()

    run_etcher(sd_card_location, image_location)

    boot_location = sd_card_location + '/boot/'

    enable_ssh(boot_location)
    enable_camera(boot_location)

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


def get_SD_card_location():
    # TODO find a way yo figure what devices are connected to the computer and figure out from that if there is a SD card
    pass