download_directory = "./Downloads/"

etcher_window64_setup = "https://github.com/resin-io/etcher/releases/download/v1.1.2/Etcher-cli-1.1.2-win32-x64.zip"
etcher_window64_setup_name = "Etcher setup.zip"
etcher_download_directory = "Etcher"

debian_jessie_with_raspberry_desktop = "http://downloads.raspberrypi.org/rpd_x86/images/rpd_x86-2017-06-23/2017-06-22-rpd-x86-jessie.iso"
debian_jessie_with_raspberry_desktop_name = "Raspberry_pi.iso"
debian_jessie_with_raspberry_desktop_download_directory = "Raspberry_ISO/"

raspberry_pi_network_name = "raspiberrypi"
raspberry_pi_user = 'pi'
raspibery_pi_password = "raspberry"

opencv_instruction_file = './commands.txt'

plink_save_download_directory = 'PLink/'
plink_name = 'PLink.exe'
plink_url = 'https://the.earth.li/~sgtatham/putty/latest/w64/plink.exe'

camera_enable_config_line = 'start_x='

sd_card_min_size = 15000000000

path_variable_name = "Path"
delete_files_at_end = True

network_information_extraction_regex = "\s+:\s+([A-Za-z0-9-_ ]+)"

end_line = '\r\n'

state_network_regex = "State" + network_information_extraction_regex + end_line
ssid_name_network_regex = "SSID" + network_information_extraction_regex + end_line
profile_name_network_regex = "Profile" + network_information_extraction_regex + " " + end_line
security_key_network_regex = "Key Content\s+:\s+(.+)" + end_line * 2 + "\w"

raspberry_pi_ip_address = "192.168.1.200"
raspberry_pi_netmask = "255.255.255.0"
raspberry_pi_router_ip_address_regex = "([\d\.]{4,15})\\r\\n\\r\\n"
