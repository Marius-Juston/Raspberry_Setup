import re

import Constants
import Terminal


# TODO make it so that it returns a dictionary will all network settings

def get_router_ip_address():
    ip_config_output = Terminal.run_command("ipconfig")

    regex_search = re.search(Constants.raspberry_pi_router_ip_address_regex, ip_config_output).group(1)

    return regex_search


def get_current_network():
    profile_info = Terminal.run_command("netsh wlan show interfaces")

    regex_search = re.search(Constants.state_network_regex, profile_info).group(1)

    if regex_search == "connected":
        ssid = re.search(Constants.ssid_name_network_regex, profile_info).group(1)

        profile_name = re.search(Constants.profile_name_network_regex, profile_info).group(1)

        profile_password = get_network_profile_info(profile_name)

        router_ip_adress = get_router_ip_address()

        return ssid, profile_password, router_ip_adress

    return None


def get_network_profile_info(profile_name):
    profile_info = Terminal.run_command("netsh wlan show profiles name=" + profile_name + " key=clear")

    regex_search = re.search(Constants.security_key_network_regex, profile_info).group(1)

    return regex_search