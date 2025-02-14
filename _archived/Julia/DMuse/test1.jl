using PyCall

"""
from pydub import AudioSegment
song = AudioSegment.from_mp3('C:\\CloudMusic\\千坂 - At The Edge.mp3')
song.export('C:\\CloudMusic\\expm\\千坂 - At The Edge.wav', format='wav')"""


@pyimport librosa
@pyimport numpy as np

function audio_to_midi(data, sample_rate, note_min="A1", note_max="G6", pitch_acc = 0.99, spread = 0.6, hop_length=512, frame_length=2048, window_length=1024)
    fmin = librosa.note_to_hz(note_min)
    fmax = librosa.note_to_hz(note_max)
    midi_min = librosa.note_to_midi(note_min)
    midi_max = librosa.note_to_midi(note_max)
    n_notes = midi_max - midi_min + 1
    
    f0, voiced_flag, voiced_prob = librosa.pyin(data, fmin * 0.9, fmax * 1.1, sample_rate, frame_length, window_length, hop_length)
    tuning = librosa.pitch_tuning(f0)
    f0_ = Vector{Int}(round.(librosa.hz_to_midi(f0 .- tuning)))
    onsets = librosa.onset.onset_detect(data, sr=sample_rate, hop_length=hop_length, backtrack=True, units="time")
    println([(librosa.core.midi_to_note(a), round(b; digits=3)) for (a, b) in zip(f0_, onsets)])
end


"""def audio_to_midi(data, sample_rate, note_min='A1', note_max='G6', pitch_acc = 0.99, spread = 0.6, hop_length=512, frame_length=2048, window_length=1024):
fmin = librosa.note_to_hz(note_min)
fmax = librosa.note_to_hz(note_max)
midi_min = librosa.note_to_midi(note_min)
midi_max = librosa.note_to_midi(note_max)
n_notes = midi_max - midi_min + 1

f0, voiced_flag, voiced_prob = librosa.pyin(data, fmin * 0.9, fmax * 1.1, sample_rate, frame_length, window_length, hop_length)
tuning = librosa.pitch_tuning(f0)
f0_ = np.round(librosa.hz_to_midi(f0 - tuning)).astype(int)
onsets = librosa.onset.onset_detect(data, sr=sample_rate, hop_length=hop_length, backtrack=True, units='time')
print([(librosa.core.midi_to_note(int(a)), round(b, 3)) for a, b in zip(f0_, onsets)])
"""

data, sample_rate = librosa.load("C:\\CloudMusic\\expm\\千坂 - At The Edge.wav")
audio_to_midi(data, sample_rate)
