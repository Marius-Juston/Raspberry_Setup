from cx_Freeze import setup, Executable

base = None

executables = [Executable("RaspberryPiSetup.py", base=base)]

packages = ["idna"]
options = {
    'build_exe': {

        'packages': packages,
    },
}

setup(
    name="RaspberrySetup",
    options=options,
    version="0.1",
    description='sets up the raspberry pi',
    executables=executables, requires=['cx_Freeze']
)
