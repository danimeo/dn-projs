using PyCall
using WAV

pushfirst!(PyVector(pyimport("sys")."path"), "")
aepy = pyimport("artear_py")

#aepy.note_to_wav([(1, 1.0), (3, 1.0), (5, 1.0)], "temp.mid")
#aepy.play_midi("temp.mid")

y, fs = wavread("temp.wav")
println(y)
