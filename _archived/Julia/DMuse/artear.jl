using PyCall
@pyimport dawdreamer as daw
@pyimport pygame
@pyimport mido
Message = mido.Message

paths = Dict(
    :Sylenth1 => "C:/VstPlugins/64bit/Sylenth1.dll"
)

engine = daw.RenderEngine(44100, 256)
instr = engine.make_plugin_processor("instr_1", paths[:Sylenth1])


function play_note(note, length, track, base_num=0, delay=0, velocity=1.0, channel=0, bpm=120)
     meta_time = 60 * 60 * 10 / bpm
     major_notes = [0, 2, 2, 1, 2, 2, 2, 1]
     base_note = 60
     kw = (:note=>base_note + base_num*12 + sum(major_notes[1:note]), :velocity=>Int64(round(64*velocity)), :time=>round(meta_time*length), :channel=>channel)
     println(kw)
     push!(track, Message("note_on"; kw...), Message("note_off"; kw...))
end


function play_midi(file)
     freq = 44100
     bitsize = -16
     channels = 2
     buffer = 1024
     pygame.mixer.init(freq, bitsize, channels, buffer)
     pygame.mixer.music.set_volume(1)
     clock = pygame.time.Clock()

     pygame.mixer.music.load(file)
     pygame.mixer.music.play()

     while pygame.mixer.music.get_busy()
         clock.tick(30)
     end
end


"""mid = mido.MidiFile()
track = mido.MidiTrack()
push!(track, Message("program_change", channel=0, program=2, time=0),
 Message("note_on", note=44, velocity=64, time=1000, channel=0), 
 Message("note_off", note=44, velocity=64, time=1000, channel=0))

play_note(1, 0.5, track)
println(mid)
# push!(mid.tracks, track)"""

py"""
import mido
mid = mido.MidiFile()
track = mido.MidiTrack()


play_note(1, 0.5, track)

mid.tracks.append(track)
"""

println(mid)
mid.save("temp.mid")

play_midi("temp.mid")

# instr.load_midi("20210127_02.mid")
