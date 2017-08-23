# IP1 = socket.gethostbyname(socket.gethostname()) # local IP adress of your computer
# IP2 = socket.gethostbyname('name_of_your_computer') # IP adress of remote computer


# print(SDCardFormatter.setup_wifi(b"E:/Game Design/Raspiberry Setup/"))
import Network
import SDCardFormatter

SDCardFormatter.set_static_ip("E:/Game Design/Raspiberry Setup/", Network.get_current_network())
