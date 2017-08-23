import io
import os
import shutil
import urllib.request
import zipfile
from pathlib import Path

import requests
import win32com.shell.shell as shell


def create_open_file(file, mode):
    return open(file, mode)


def decode(byte_object, encoding="utf-8"):
    return byte_object.decode(encoding)

def download_file(url, directory, file_name):
    os.makedirs(directory, exist_ok=True)

    with urllib.request.urlopen(url) as response, open(directory + file_name, 'wb') as out_file:
        shutil.copyfileobj(response, out_file)


def run_program(program_command):
    return os.system(program_command)


def run_program_as_admin(program, program_parameters):
    return shell.ShellExecuteEx(lpVerb='runas', lpFile=program, lpParameters=program_parameters)
    # pass


def remove_file(file):
    os.remove(file)



def extract_zip(zip_file_url, extract_folder):
    if not Path(extract_folder).exists():
        os.makedirs(extract_folder)

    r = requests.get(zip_file_url)
    z = zipfile.ZipFile(io.BytesIO(r.content))
    z.extractall(extract_folder)


def add_to_environmental_variable(variable, location):
    if location not in os.environ[variable]:
        os.environ[variable] += location + ";"
