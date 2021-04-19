# Здесь расположим Поиск нашей виртуальной машины -
# Это важно - вынести в отдельный файл - тк необходимо при запуске в многопоточном режиме

import virtualbox
vbox = virtualbox.VirtualBox
vbox = vbox()
from working_directory.ConfigParser import machine_name
# Ищем нашу виртуальную тачку
vm = vbox.find_machine(machine_name)