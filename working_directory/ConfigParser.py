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


# ----------------------------------------------------------------------------

# # НАдо доделать !!!
# class ConfigParser:
#     """
#     Класс для того чтоб парсить конфиг - Почему бы и нет.
#     """
#
#     __parser = None
#     def __init__(self):
#         __parser = self.__parseconfig()
#
#         self.__dbpath = __parser['test']['dbpath']
#
#         self.__targetimage = (__parser['test']['apiaddr'], int(__parser['test']['apiport']))
#         # Метод для чтения конфига
#     def __parseconfig(self):
#         # настройки берем из конфига:
#         parser = configparser.ConfigParser()
#         parser.read('settings.ini')
#         return parser
#
#     def get_parse_config_dbpath(self):
#         dbpath =  self.__dbpath
#         return dbpath
#
#     def get_parse_config_targetimage(self):
#         return self.__targetimage

# ----------------------------------------------------------------------------