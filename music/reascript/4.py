import ctypes

b = b'\x02\x02\x02\x0232 HH\x03\x03\x03\x03\x00\x00'
p = ctypes.cast(b, c_char_p)
b2 = bytes(p.value)
RPR_ShowConsoleMsg(str(b2))

