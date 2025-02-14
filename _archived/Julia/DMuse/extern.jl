using PyCall

@pyimport musicpy.musicpy as mp

macro hello()
    dir = "B:\\musicproject\\MIDI库\\melody"
    _, a, _ = mp.read(dir * "\\20200820_02.mid")
    println(a)
end

