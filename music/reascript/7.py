try:
    import ctypes
    import re
            
    lib = ctypes.cdll.LoadLibrary('C:\\REAPER\\Scripts\\2.dll')
                
    send_tagname = 'rpr_c2r'
    recv_tagname = 'rpr_r2c'
    lib.start_listening(ctypes.c_char_p(send_tagname), ctypes.c_char_p(recv_tagname), 65536)
    
    def send(msg):
        global lib
        b2 = b'\x02\x02\x02\x02' + bytes(msg) + b'\x03\x03\x03\x03'
        p2 = ctypes.cast(b2, c_char_p)
        lib.push_message(p2, len(b2))
    
    def recv():
        global lib
        s = ''
        p = ctypes.c_char_p(s)
        lib.get_message(p)
        data = bytes(p.value)
        length = len(data)
        if length >= 8:
            a, b = 0, 0
            for i, byte in enumerate(data):
                bts = data[i:i+4]
                if i + 4 >= length or bts == b'\x03\x03\x03\x03':
                    b = i
                    break
                elif bts == b'\x02\x02\x02\x02':
                    a = i + 4
            if a >= 4 and b >= 4 and a <= b:
                return data[a:b].decode(encoding='utf-8')
            else:
                return ''
        else:
            return ''
    
    param_ids = {}
    
    def load_instruments(fxname, n):
        global param_ids
        tr = RPR_GetLastTouchedTrack()
        for i in range(n):
            RPR_TrackFX_AddByName(tr, fxname, False, i)
        id = 0
        param_name = '?'
        ids = {}
        while param_name:
            param_name = RPR_TrackFX_GetParamName(tr, 0, id, '', 64)[4]
            ids[param_name] = id
            id += 1
        param_ids[fxname] = ids
    
    def get_fxname(tr, i):
        s = re.sub('VSTi: ', 'VST:', RPR_TrackFX_GetFXName(tr, i, '', 128)[3])
        return re.sub(' \\(.*\\)', '', s)
    
    def get_param_value(tr, i, param_name):
        global param_ids
        fxname = get_fxname(tr, i)
        return RPR_TrackFX_GetParamNormalized(tr, i, param_ids[fxname][param_name])
    
    def set_param_value(tr, i, param_name, value):
        global param_ids
        fxname = get_fxname(tr, i)
        #RPR_ShowConsoleMsg(str(value) + 'g\n')
        RPR_TrackFX_SetParamNormalized(tr, i, param_ids[fxname][param_name], value)
    
    def set_track_params(tr, params_str):
        fxs = params_str.split(';')
        for i, fx in enumerate(fxs):
            params = fx.split(',')
            fxname = params[0].replace('_', ' ')
            for id, param in enumerate(params[1:]):
                RPR_TrackFX_SetParamNormalized(tr, i, id, float(param))
    
    def get_track_params(tr):
        lst = []
        n_fx = RPR_TrackFX_GetCount(tr)
        for i in range(n_fx):
            id = 0
            param_name = '?'
            params = [get_fxname(tr, i).replace(' ', '_')]
            while param_name:
                param_name = RPR_TrackFX_GetParamName(tr, i, id, '', 64)[4]
                param_value = RPR_TrackFX_GetParamNormalized(tr, i, id)
                params.append(str(param_value))
                id += 1
            #RPR_ShowConsoleMsg(','.join(params))
            lst.append(','.join(params))
        return ';'.join(lst)
    
    def set_track_presets(tr, presets):
        presets_ = presets.split(';')
        for i, preset in enumerate(presets_):
            #RPR_ShowConsoleMsg(preset + '\n')
            RPR_TrackFX_SetPreset(tr, i, preset)
    
    def loop():
        global param_ids
        msg = recv()
        #RPR_ShowConsoleMsg(msg)
        cmds = msg.split('&&')
        
        for cmd_ in cmds:
            cmd = cmd_.strip().split(' ')
            if cmd[0] == 'set':
                #RPR_ShowConsoleMsg('set' + '\n')
                #send('')
                desc = cmd[1].split('@')
                attr = desc[0]
                loc = desc[1].split('/')
                if loc[0].startswith('tr'):
                    if len(loc) == 1:
                        if loc[0][2:] == 'lt':
                            tr = RPR_GetLastTouchedTrack()
                        else:
                            tr = RPR_GetTrack(0, int(loc[0][2:]))
                        if attr == 'name':
                            RPR_GetSetMediaTrackInfo_String(tr, 'P_NAME', cmd[2], True)
                        elif attr == 'vol':
                            RPR_SetMediaTrackInfo_Value(tr, 'D_VOL', float(cmd[2]))
                        elif attr == 'pan':
                            RPR_SetMediaTrackInfo_Value(tr, 'D_PAN', float(cmd[2]))
                        elif attr == 'params':
                            set_track_params(tr, cmd[2])
                        elif attr == 'presets':
                            set_track_presets(tr, cmd[2])
                    elif len(loc) == 2 and loc[1].startswith('fx'):
                        if loc[0][2:] == 'lt':
                            tr = RPR_GetLastTouchedTrack()
                        else:
                            tr = RPR_GetTrack(0, int(loc[0][2:]))
                        if attr == 'param':
                            name, value_str = cmd[2].split('=')
                            set_param_value(tr, int(loc[1][2:]), name.replace('_', ' '), float(value_str))
                        elif attr == 'preset':
                            RPR_TrackFX_SetPreset(tr, int(loc[1][2:]), cmd[2])
                    elif len(loc) == 2 and loc[1].startswith('it'):
                        pass
            elif cmd[0] == 'get':
                #RPR_ShowConsoleMsg('get' + '\n')
                desc = cmd[1].split('@')
                attr = desc[0]
                loc = desc[1].split('/')
                if loc[0].startswith('tr'):
                    if len(loc) == 1:
                        if loc[0][2:] == 'lt':
                            tr = RPR_GetLastTouchedTrack()
                        else:
                            tr = RPR_GetTrack(0, int(loc[0][2:]))
                        if attr == 'name':
                            (retval, tr_, parmname, stringNeedBig, setNewValue) = RPR_GetSetMediaTrackInfo_String(tr, 'P_NAME', '', False)
                            send('data ' + stringNeedBig)
                        elif attr == 'vol':
                            vol = RPR_GetTrackUIVolPan(tr, 0, 0)[2]
                            send('data ' + str(vol))
                        elif attr == 'pan':
                            pan = RPR_GetTrackUIVolPan(tr, 0, 0)[3]
                            send('data ' + str(pan))
                        elif attr == 'params':
                            #RPR_ShowConsoleMsg(get_track_params(tr))
                            send('data ' + get_track_params(tr))
                    elif len(loc) == 2 and loc[1].startswith('fx'):
                        if loc[0][2:] == 'lt':
                            tr = RPR_GetLastTouchedTrack()
                        else:
                            tr = RPR_GetTrack(0, int(loc[0][2:]))
                        if attr == 'param':
                            name = cmd[2]
                            value = get_param_value(tr, int(loc[1][2:]), name.replace('_', ' '))
                            send('data ' + str(value))
                    elif len(loc) == 2 and loc[1].startswith('it'):
                        pass
            
        RPR_defer('loop()')
    
    #RPR_Main_OnCommand(40001, 0)
    load_instruments('VST:Sylenth1', 3)
    loop()
except Exception as e:
    RPR_ShowMessageBox(str(e), 'Error!', 0)

