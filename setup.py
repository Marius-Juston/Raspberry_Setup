from cx_Freeze import setup, Executable

# TODO save all the files to a exe using cx_freeze. in command prompt write python setup.py build

setup(name="raspiSetup",
      version='0.1',
      description='setsup the raspberry pi',
      executables=[Executable("RaspberryPiSetup.py")], requires=['cx_Freeze'])
