
# function returning a single (scalar) value:
sec = RPR_parse_timestr("1:12")

# function returning information in the first parameter (function returns void):
(str) = RPR_GetProjectPath("", 512)

# lower volume of track 4 by half (RPR_GetTrackUIVolPan returns Bool):
tr = RPR_GetTrack(0, 3)
(ok, tr, vol, pan) = RPR_GetTrackUIVolPan(tr, 0, 3)
# this also works, if you only care about one of the returned values:
vol = RPR_GetTrackUIVolPan(tr, 0, 3)[2]
RPR_SetMediaTrackInfo_Value(tr, "D_VOL", vol*2)

