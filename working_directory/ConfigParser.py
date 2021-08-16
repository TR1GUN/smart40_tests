import configparser
import os
# ----------------------------------------------------------------------------
# path ='/'.join((os.path.abspath(__file__).replace('\\', '/')).split('/')[:-1])
path ='/'.join((os.path.abspath(__file__).replace('\\', '/')).split('/')[:-1])
settings = '../settings.ini'
# настройки берем из конфига
parser = configparser.ConfigParser()
parser.read(os.path.join(path,settings))


dbpath = parser['test']['dbpath']
targetimage = (parser['test']['apiaddr'], int(parser['test']['apiport']))

#-----------------------------------------------------------------------------

machine_name = parser['test']['machine_name']
user_login = parser['test']['user_login']
user_password = parser['test']['user_password']
addres_ssh = parser['test']['addres_ssh']
domain = parser['test']['domain']

# ----------------------------------------------------------------------------