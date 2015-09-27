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
# audio_path = "data/target_species/"
species_list = ["Poecile_atricapillus",
                "Poecile_rufescens",
                "Regulus_calendula",
                "Regulus_satrapa"]


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


def file_list(path, species):
    '''
    Create a list of files for further processing
    '''
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
        # arr = np.array(a[1], dtype=float)  already np array - don't need to convert
        spec = stft.spectrogram(a[1])
        spectrograms[f] = spec
    return spectrograms


def norm_spec(spectrograms):
    '''
    INPUT:
        dict of file name: spectrogram
    OUTPUT:
        dict of file name: l2 normalized spectrogram
    '''
    norm = {}
    for k in spectrograms.keys():
        norm[k] = normalize(spectrograms[k], norm="l2")
    return norm


def whiten(normalized):
    '''
    INPUT:
        dict of file name: spectrogram
    OUTPUT:
        dict of file name: pca whitened spectrogram
    '''
    whitened = {}
    pca = PCA(n_components=40, copy=False, whiten=True)
    for k in normalized.keys():
        whitened[k] = pca.fit_transform(normalized[k])


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
