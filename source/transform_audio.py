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
    INPUT:
        path to data file directories
    OUTPUT:
        For each directory containing mp3 files, generate a new directory
        to recieve wav files.  Return a list of tuples containing mp3 and wav
        directory paths.
    '''
    directory_list = []
    for (_, _, filename) in os.walk(audio_path + "json_files"):
        for name in filename:
            input_directory = audio_path + name
            output_directory = input_directory + "_wav"
            directory_list.append((input_directory, output_directory))
    return directory_list


def make_file_list(directory_list):
    '''
    INPUT:
        list of tuples containing input, output directories
    OUTPUT:
        list of tuples containing input, output file names
    '''
    file_list = []
    for directory in directory_list:
        for (_, _, filenames) in os.walk(directory[0]):
            for file_id in filenames:
                mp3_file = (directory[0] + "/" + file_id)
                wav_file = (directory[1] + "/" + file_id[:-3] + "wav")
                file_list.append((mp3_file, wav_file))
    return file_list


def make_wav(file_list):
    '''
    INPUT:
        list of tuples containing input, output file names
    OUTPUT:
        wav files
    '''
    while len(file_list) != 0:
        f = file_list.pop()
        sound = AudioSegment.from_mp3(f[0])
        sound.export(f[1])


def make_fft(wav_directory, csv_directory):
    for (_, _, filenames) in os.walk(wav_directory):
        for file_id in filenames:
            a = read(file_id)
            nparray = np.array(a[1], dtype=float)
            f = np.fft.fft(nparray)
            np.savetxt(csv_directory + "/" + file_id[:-3] + ".csv", f, delimiter=",")



    wav_directory = mp3_directory + "_wav"
    csv_directory = mp3_directory + "_csv"
    wav_name = wav_directory + "/" + mp3_id[:-3] + "wav"
    sound = AudioSegment.from_mp3(mp3_name)
    sound.export(wav_name)
    a = read(wav_name)
    nparray = np.array(a[1], dtype=float)
    f = np.fft.fft(nparray)
    np.savetxt(csv_directory + "/" + name + ".csv", f, delimiter=",")
