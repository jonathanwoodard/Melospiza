import numpy as np
import os
from pydub import AudioSegment
from scipy.io.wavfile import read
# import stft
from sklearn.preprocessing import normalize
from sklearn.decomposition import PCA
# from sklearn.feature_extraction import FeatureHasher
from multiprocessing.pool import Pool


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


def single_spec(f):
    spectrograms = {}
    sound = AudioSegment.from_wav(f)
    sound = sound.set_channels(1)
    sound.export('temp', format='wav')
    a = read('temp')
    arr = np.array(a[1], dtype=float)
    spec = stft.spectrogram(arr)
    spectrograms[f] = spec
    return spectrograms


def multi_spec(file_list):
    pool = Pool(processes=8)
    results = pool.map(single_spec, file_list, chunksize=1)
    return results


def norm_spec(spectrograms):
    '''
    INPUT:
        dict of file name: spectrogram
    OUTPUT:
        dict of file name: l2 normalized spectrogram
    '''
    normalized = {}
    keys = spectrograms.keys()
    for k in keys:
        v = spectrograms[k].real.astype(float)
        normalized[k] = normalize(v, norm="l2")
    return normalized


def whiten(spectrograms):
    '''
    INPUT:
        dict of file name: spectrogram
    OUTPUT:
        dict of file name: pca whitened spectrogram
    '''
    pca = PCA(n_components=40, copy=False, whiten=True)
    whitened = {}
    keys = spectrograms.keys()
    for k in keys:
        whitened[k] = pca.fit_transform(spectrograms[k])
    return whitened


# data = a numpy array containing the signal to be processed
# fs = a scalar which is the sampling frequency of the data
# data = whitened[keys[i]]  # for i in whitened.keys()
# fs = 1024
# fft_size = 1024
# overlap_fac = 0.5
# hop_size = np.int32(np.floor(fft_size * (1 - overlap_fac)))
# pad_end_size = fft_size          # the last segment can overlap the end of the data array by no more than one window size
# total_segments = np.int32(np.ceil(len(data) / np.float32(hop_size)))
# t_max = len(data) / np.float32(fs)
#
# window = np.hanning(fft_size)  # our half cosine window
# inner_pad = np.zeros(fft_size)  # the zeros which will be used to double each segment size
#
# proc = np.concatenate((data, np.zeros(pad_end_size)))              # the data to process
# result = np.empty((total_segments, fft_size), dtype=np.float32)    # space to hold the result
#
# for i in xrange(total_segments):                      # for each segment
#     current_hop = hop_size * i                        # figure out the current segment offset
#     segment = proc[current_hop:current_hop + fft_size]  # get the current segment
#     windowed = segment * window                       # multiply by the half cosine function
#     padded = np.append(windowed, inner_pad)           # add 0s to double the length of the data
#     spectrum = np.fft.fft(padded) / fft_size          # take the Fourier Transform and scale by the number of samples
#     autopower = np.abs(spectrum * np.conj(spectrum))  # find the autopower spectrum
#     result[i, :] = autopower[:fft_size]               # append to the results array
#
# result = 20 * np.log10(result)          # scale to db
# result = np.clip(result, -40, 200)    # clip values
