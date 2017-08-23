import subprocess

import Helper


def run_command(command, encoding="utf-8"):
    s = subprocess.check_output(command)

    if encoding != None:
        return Helper.decode(s, encoding)

    return s
