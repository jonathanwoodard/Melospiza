import pandas as pd
import numpy as np
import json
import os
from pydub import AudioSegment
from scipy.io.wavfile import read


audio_path = '/media/jon/external_data/audio/'


def make_dirs(audio_path):
    '''
    Read species names from json and create wav file directory for each species
    '''
    f = []
    for (_, _, filename) in os.walk(audio_path + "json_files"):
        f.extend(filename)
        for name in f:
            os.makedirs(audio_path + name + '_wav')


def dir_list(audio_path):
    '''
    generate a list of all directories in the audio path
    '''
    d_list = []
    for (_, _, filename) in os.walk(audio_path + "json_files"):
        for name in filename:
            d_list.append(audio_path + name + "/")
    return d_list


def file_list(dir_list):
    '''
    generate a list of files in each directory
    '''
    f_list = []
    for (_, _, filename) in os.walk(dir_list):
        for f_id in filename:
            f_list.append(mp3_directory + "/" + f_id)
    return f_list

    wav_directory = mp3_directory + "_wav"
    csv_directory = mp3_directory + "_csv"
    wav_name = wav_directory + "/" + mp3_id[:-3] + "wav"
    sound = AudioSegment.from_mp3(mp3_name)
    sound.export(wav_name)
    a = read(wav_name)
    nparray = np.array(a[1], dtype=float)
    f = np.fft.fft(nparray)
    np.savetxt(csv_directory + "/" + name + ".csv", f, delimiter=",")
