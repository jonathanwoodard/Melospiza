import pandas as pd
import numpy as np
import json
import os
from pydub import AudioSegment
from scipy.io.wavfile import read
import stft
from sklearn.pipeline import Pipeline
from sklearn.preprocessing import normalize
from sklearn.decomposition import PCA
import random
import signal
import cPickle as pickle
from functools import partial
import multiprocessing as mp
import time
from multiprocessing.pool import Pool


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


def make_wav_list(directory_list):
    '''
    INPUT:
        list of tuples containing wav file directories
    OUTPUT:
        list of tuples containing path and file_id for all wav files
    '''
    wav_list = []
    for directory in directory_list:
        for (_, _, filenames) in os.walk(directory[1]):
            for file_id in filenames:
                wav_file = (directory[1] + "/" + file_id)
                wav_list.append((wav_file, file_id))
    return wav_list

npz_directory = '/media/jon/external_data/audio/pickles'


# def make_fft(wav_list, npz_directory):
#     for item in wav_list:
#         a = read(item[0])
#         nparray = np.array(a[1], dtype=float)
#         f = np.fft.fft(nparray)
#         f.dump(npz_directory + item[1][:-3] + "npz")


def make_fft(wav_list, npz_directory):
    for item in wav_list:
        a = read(item[0])
        nparray = np.array(a[1], dtype=float)
        f = np.fft.fft(nparray)
        f_myfile = open((item[1][:-3] + "npz"), 'wb')
        pickle.dump(f, f_myfile)
        f_myfile.close()
        # f.dump(npz_directory + item[1][:-3] + "npz")


def multi_fft(wav_list, npz_directory=npz_directory):
    for item in wav_list:
        a = read(item[0])
        nparray = np.array(a[1], dtype=float)
        f = np.fft.fft(nparray)
        f_myfile = open((item[1][:-3] + "npz"), 'wb')
        pickle.dump(f, f_myfile)
        f_myfile.close()


# def timeout(seconds=30):
audio_path = "data/target_species/"
species_list = ["Poecile_atricapillus",
                "Poecile_rufescens",
                "Regulus_calendula",
                "Regulus_satrapa"]


def file_list(path, species):
    file_list = []
    for sp in species:
        for (_, _, filenames) in os.walk(path + sp + "_wav/"):
            for f in filenames:
                file_list.append(path + sp + "_wav/" + f)
    return file_list


def make_mono(file_list):
    '''
    overwrite wav files as mono - other functions will have errors with stereo files
    '''
    for f in file_list:
        sound = AudioSegment.from_wav(f)
        sound = sound.set_channels(1)
        sound.export(f, format="wav")


def make_spec(file_list):
    '''
    INPUT:
        list of wav file - files will be converted to mono in function
    OUTPUT:
        dictionary with filename as key, spectrogram as value
    '''
    spectrograms = {}
    for f in file_list:
        sound = AudioSegment.from_wav(f)
        sound = sound.set_channels(1)
        sound.export("temp", format="wav")
        a = read("temp")
        arr = np.array(a[1], dtype=float)
        spec = stft.spectrogram(arr)
        spectrograms[f] = spec
    return spectrograms


def norm_spec(spectrograms):
    '''
    INPUT:
        dict of file name: spectrogram
    OUTPUT:
        dict of file name: l2 normalized spectrogram
    '''
    for k, v in spectrograms:
        spectrograms[k] = normalize(v, norm="l2")
    return spectrograms


def whiten(spectrograms):
    '''
    INPUT:
        dict of file name: spectrogram
    OUTPUT:
        dict of file name: pca whitened spectrogram
    '''
    pca = PCA(n_components=40, copy=False, whiten=True)
    for k, v in spectrograms:
        spectrograms[k] = pca.fit_transform(v)


def test_stft(file_list):
    processed_files = []
    problem_files = []
    for f in file_list:
        a = read(f)
        arr = np.array(a[1], dtype=float)
        try:
            ft = stft.process(arr)
            processed_files.append((ft, f))
        except ValueError:
            problem_files.append(f)
    return processed_files, problem_files


def usable_files(file_list, problem_list):
    usable = []
    usable.extend([f for f in file_list if f not in problem_list])
    return usable


def random_sample(species_files, n=10):
    '''
    INPUT:
        a dict of species, file list pairs
    OUTPUT:
        a randomly selected list of n files from each species
    '''
    subset = []
    for k, v in species_files:
        subset.extend([v[i] for i in random.sample(xrange(len(v)))])
    return subset


# stub - need to flesh this out
# def main():
#     ts = time()
#     mkfft = partial(multi_fft)
#     with Pool(8) as p:
#         p.map(multi_fft, files)
#
#
# if __name__ == "__main__":
#     main()

# pydub proved to be slow and error prone, and crashed frequently
# files were converted using ffmpeg and a bash script
# def make_wav(file_list):
#     '''
#     INPUT:
#         list of tuples containing input, output file names
#     OUTPUT:
#         wav files
#     '''
#     while len(file_list) != 0:
#         f = file_list.pop()
#         sound = AudioSegment.from_mp3(f[0])
#         sound.export(f[1])


# def make_fft(wav_directory, csv_directory):
#     for (_, _, filenames) in os.walk(wav_directory):
#         for file_id in filenames:
#             a = read(file_id)
#             nparray = np.array(a[1], dtype=float)
#             f = np.fft.fft(nparray)
#             np.savetxt(csv_directory + "/" + file_id[:-3] + ".csv", f, delimiter=",")

    # wav_directory = mp3_directory + "_wav"
    # csv_directory = mp3_directory + "_csv"
    # wav_name = wav_directory + "/" + mp3_id[:-3] + "wav"
    # sound = AudioSegment.from_mp3(mp3_name)
    # sound.export(wav_name)
    # a = read(wav_name)
    # nparray = np.array(a[1], dtype=float)
    # f = np.fft.fft(nparray)
    # np.savetxt(csv_directory + "/" + name + ".csv", f, delimiter=",")
