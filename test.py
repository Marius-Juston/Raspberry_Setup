# import pywinusb



# nbtstat -a ip adress

import socket
# IP1 = socket.gethostbyname(socket.gethostname()) # local IP adress of your computer
# IP2 = socket.gethostbyname('name_of_your_computer') # IP adress of remote computer

def collect_device_information():
    import re
    import subprocess
    device_re = re.compile(r"Bus\s+(?P<bus>\d+)\s+Device\s+(?P<device>\d+).+ID\s(?P<id>\w+:\w+)\s(?P<tag>.+)$", re.I)
    df = subprocess.check_output("lsusb")
    devices = []
    for i in df.split(b"\n"):
        if i:
            info = device_re.match(i)
            if info:
                dinfo = info.groupdict()
                dinfo['device'] = '/dev/bus/usb/%s/%s' % (dinfo.pop('bus'), dinfo.pop('device'))
                devices.append(dinfo)
    print(devices)


collect_device_information()