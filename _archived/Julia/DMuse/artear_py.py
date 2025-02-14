import pygame
import os
import time
from mido import Message, MidiFile, MidiTrack
from midi2audio import FluidSynth


def play_note(note, length, track, base_num=0, delay=0, velocity=1.0, channel=0, bpm=120):
    meta_time = 60 * 60 * 10 / bpm
    major_notes = [0, 2, 2, 1, 2, 2, 2, 1]
    base_note = 60
    track.append(Message('note_on', note=base_note + base_num*12 + sum(major_notes[0:note]), velocity=round(64*velocity), time=round(delay*meta_time), channel=channel))
    track.append(Message('note_off', note=base_note + base_num*12 + sum(major_notes[0:note]), velocity=round(64*velocity), time=round(meta_time*length), channel=channel))


def play_midi(file):
    freq = 44100
    bitsize = -16
    channels = 2
    buffer = 1024
    pygame.mixer.init(freq, bitsize, channels, buffer)
    pygame.mixer.music.set_volume(1)
    clock = pygame.time.Clock()
    try:
        pygame.mixer.music.load(file)
    except:
        import traceback
        print(traceback.format_exc())
    pygame.mixer.music.play()
    while pygame.mixer.music.get_busy():
        clock.tick(30)


def note_to_wav(seqs, filename, base_num=0, delay=0, velocity=1.0, channel=0, bpm=120):
    mid = MidiFile()
    track = MidiTrack()
    for note, length in seqs:
        play_note(note, length, track, base_num=0, delay=0, velocity=1.0, channel=0, bpm=120)       # 时
    mid.tracks.append(track)
    mid.save(filename)
    while not os.path.exists(filename):
        print('Waiting for the .mid file...')
        time.sleep(0.2)
    fs = FluidSynth()
    fs.midi_to_audio(filename, os.path.splitext(filename)[0] + '.wav')


note_to_wav([(1, 1.0), (3, 1.0), (5, 1.0)], "temp.mid")

os.path.exists
