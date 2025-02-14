from threading import Thread

try:
    import ctypes
    import binascii
    import time
            
    lib = ctypes.cdll.LoadLibrary('C:\\REAPER\\Scripts\\2.dll')
                
    send_tagname = 'rpr_c2r'
    recv_tagname = 'rpr_r2c'
    lib.start_listening(ctypes.c_char_p(send_tagname), ctypes.c_char_p(recv_tagname))
    
    RPR_Main_OnCommand(40001, 0)
    
    def loop(lib):
        i = 0
        while True:
            s = ''
            p = ctypes.c_char_p(s)
            lib.get_message(p)
            #RPR_ShowConsoleMsg(binascii.b2a_hex(bytes(p.value)) + '\n')
            
            #track = RPR_GetLastTouchedTrack()
            #RPR_ShowMessageBox(binascii.b2a_hex(bytes(p.value)) + '\n', 'Info', 0)
            #RPR_GetSetMediaTrackInfo_String(track, 'P_NAME', binascii.b2a_hex(bytes(p.value)), True)
            
            i += 1
            b2 = b'\x02\x02\x02\x02' + bytes(str(i)) + 'Success!\x03\x03\x03\x03\x00\x00'
            p2 = ctypes.cast(b2, c_char_p)
            
            lib.push_message(p2, len(b2))
            
            time.sleep(0.5)
    
    thr = Thread(target=loop, args=(lib, ))
    thr.setDaemon(False)
    thr.start()
except Exception as e:
    RPR_ShowMessageBox(str(e), 'Error', 0)

