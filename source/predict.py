# predict from wav file

import numpy as np
import pandas as pd
from sklearn.ensemble import RandomForestClassifier
from pydub import AudioSegment
from scipy.io.wavfile import read
from sklearn.preprocessing import normalize
from sklearn.decomposition import PCA
import stft
import OSKmeans


def make_mono(input_file):
    '''
    overwrite wav files as mono - other functions will have errors with stereo files
    '''
    if input_file[-3:] == "mp3":
        sound = AudioSegment.from_mp3(input_file)
        sound = sound.set_channels(1)
        sound.export(input_file, format="wav")
    elif input_file[-3:] == "wav":
        sound = AudioSegment.from_wav(input_file)
        sound = sound.set_channels(1)
        sound.export(input_file, format="wav")
    else:
        print "Unrecognized file type. \n"
        print "Files must be .mp3 or .wav format"


# put ransformed audio file into a DataFrame
def wav_to_df(input_file):
    whitened = {}
    df = pd.DataFrame()
    pca = PCA(n_components=40, copy=False, whiten=True)
    a = read(input_file)
    spec = stft.spectrogram(a[1])
    autopower = np.abs(spec * np.conj(spec))
    v = autopower.real.astype(float)
    norm = normalize(v, norm="l2")
    whitened[input_file] = 20 * np.log10(pca.fit_transform(norm))
    temp = pd.DataFrame(whitened.items(), columns=['Filename', 'Spec_features'])
    df = df.append(temp)
    return df, whitened
