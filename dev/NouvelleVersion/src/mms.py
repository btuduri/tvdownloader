
#http://code.google.com/p/pydowntv/source/browse/trunk/trunk/Servers/pylibmms/libmms.py?spec=svn84&r=84


import ctypes

libmms = ctypes.cdll.LoadLibrary("libmms.so.0")

url = "mms://webcast1.fiberpipe.tv/idl_vod/designlab101806.wsx"
mmscon = libmms.mmsx_connect(None, None, url, int(5000))

print libmms.mmsx_get_length(mmscon)

buffer = ctypes.create_string_buffer(10)
count = libmms.mmsx_read(0, mmscon, buffer, 10)

print "lut:",buffer.value

libmms.mmsx_close(mmscon)

