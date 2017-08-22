import sys

import Constants
import Helper
import OpenCVSetup
import SDCardFormatter


def main():
    SDCardFormatter.setup_sd_card()
    # import RaspberryISO

    print("Please remove the SD card now and plug it in the raspberry py. When finished press enter")
    input()

    print("trying to connect to raspberry pi with network name as:", Constants.raspberry_pi_network_name)

    ip_address = None

    while ip_address is None:
        ip_address = OpenCVSetup.raspberry_pi_ip_address()

    print("The raspberry was found on the network. The ip address is:", ip_address)

    OpenCVSetup.setup_openCV(ip_address)

    if Constants.delete_files_at_end:
        Helper.remove_file(Constants.download_directory)
    return 0


if __name__ == '__main__':
    sys.exit(main())
