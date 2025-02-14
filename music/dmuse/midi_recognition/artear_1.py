import os
import random
import dawdreamer as daw
from scipy.io import wavfile

from musicpy import read
import numpy as np

sample_rate = 44100
buffer_size = 256

to_render = True

plugin_paths = {
    'Sylenth1': 'C:/VstPlugins/64bit/Sylenth1.dll',
    'TruePianos': 'C:/VstPlugins/64bit/Vstplugins/TruePianos x64.dll',
}

preset_dirs = {
    'Sylenth1': 'presets/sylenth1',
}

# preset_gen_model_one_filename = 'models/preset_gen/model_one.h5'
mid_dir = 'G:/编曲资源'
fxp_dir = 'C:/dev_spa/artear_1/res/LEAD'
wav_gen_dir = 'C:/dev_spa/artear_1/wav_gen_15s'


def get_files(directory, ext):
    path_list = []
    for paths in [[os.path.join(dirpath, name).replace('\\', '/') for name in filenames if name.endswith('.' + ext)] for
                  dirpath, dirnames, filenames in os.walk(directory)]:
        path_list.extend(paths)
    return path_list


print('正在获取路径下所有MIDI和预设文件……')
mid_paths = get_files(mid_dir, 'mid')
fxp_paths = get_files(fxp_dir, 'fxp')

engine = daw.RenderEngine(sample_rate, buffer_size)

instr = engine.make_plugin_processor('instr_1', plugin_paths['Sylenth1'])
engine.load_graph([(instr, [])])

print('正在渲染音频……')
c, l = 0, len(mid_paths)
for mid in mid_paths:
    fxp = random.choice(fxp_paths)
    print('[' + str(c + 1) + '/' + str(l) + '] Rendering:', mid, fxp, end='...')
    
    audio_path = os.path.join(wav_gen_dir, os.path.splitext(os.path.basename(mid))[0]) + '.wav'
    if os.path.exists(audio_path):
        name = os.path.splitext(os.path.basename(mid))[0].split('_')
        name, num = '_'.join(name[:-1]), name[-1]
        if num == '':
            num = '1'
        elif num.isdigit():
            num = str(int(num) + 1)
        audio_path_ = os.path.join(wav_gen_dir, name + '_' + num) + '.wav'
    else:
        audio_path_ = audio_path
    
    instr.load_midi(mid)
    instr.load_preset(fxp)
    
    engine.render(15.)
    audio = engine.get_audio()
    wavfile.write(audio_path_, sample_rate, audio.transpose())
    
    if audio_path != audio_path_ and os.path.getsize(audio_path) == os.path.getsize(audio_path_):
        os.remove(audio_path)
    
    print(' Done.')
    c += 1


print('完成。')
