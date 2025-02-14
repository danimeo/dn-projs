tr = RPR_GetTrack(0, 0)
#RPR_TrackFX_SetParamNormalized(tr, 0, 1, 0.95)
#RPR_TrackFX_AddByName(tr, 'VST:Sylenth1', False, -1)
retval, track, fx, presetname, presetname_sz = RPR_TrackFX_GetPreset(tr, 0, '', 64)
RPR_ShowConsoleMsg(str(retval) + ' ' + presetname + '\n')
ss = RPR_TrackFX_SetPreset(tr, 0, 
RPR_ShowConsoleMsg(ss + '\n')


