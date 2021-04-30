a = 'C:/Users/n.buslin/Downloads/test_cmd_getshprm'


f = open(a, 'r')
a = f.read()
a = a.encode()
print((a))



lol = 112
#
# lol = hex(lol)
# print(lol, type(lol))
# lol = lol.strip('0x')
# print(lol, type(lol))
# #
# lol = bytes().fromhex(lol)
# #
# print(lol, type(lol))


# from ctypes import *

# lol = c_uint8(lol)
# lol = create_string_buffer(lol, 2)
# lol = lol.to_bytes(2, byteorder='little')
# print(repr(lol), type(lol))
# lol = 112
# import struct
#
# lol = struct.pack("h",lol)
# # lol = bytes.fromhex(lol)
# print(repr(lol), type(lol))
#
# import binascii
# lol = binascii.hexlify(lol)
#
# print(lol, type(lol))
# # # b'x70'
# # # lol = b'\x00'
# # #
# # # lol.
#
#
# # x = 112
# # x = x.to_bytes(2, byteorder='little')
# # print(x)
# #
# # print(memoryview(x).)