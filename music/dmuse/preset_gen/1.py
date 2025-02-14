import os
import shutil

dst_dir = 'C:/dev_spa/artear_1/mid'

wav_dir = 'C:/dev_spa/artear_1/wav_gen'
wav_dst_dir = 'C:/dev_spa/artear_1/wav'


def get_files(directory, ext):
    path_list = []
    for paths in [[os.path.join(dirpath, name).replace('\\', '/') for name in filenames if name.endswith('.' + ext)] for
                  dirpath, dirnames, filenames in os.walk(directory)]:
        path_list.extend(paths)
    return path_list


mid_files = get_files('G:/编曲资源', 'mid')
wav_files = get_files(wav_dir, 'wav')

for mid in mid_files:
    wav = os.path.join(wav_dir, os.path.splitext( os.path.basename(mid))[0]) + '.wav'
    if os.path.exists(wav):
        shutil.copy(mid, dst_dir)
        shutil.copy(wav, wav_dst_dir)
