import pandas as pd
import numpy as np
import os
import json
from scipy.io.wavfile import read
from sklearn.preprocessing import normalize
from sklearn.decomposition import PCA
import matplotlib.pyplot as plt
import stft


'''
Read wav files and transform to numpy arrays
try to perform stft.process - if there is a problem with the
wavfile, add filename to a list of problem files.
Otherwise, add stft and filename to a list of results

Need to incorporate a timeout function so that the function
will move to the next file if processing takes too long.
'''

audio_path = '~/data/target_species/'
species_list = ['Poecile_atricapillus',
                'Poecile_rufescens',
                'Regulus_calendula',
                'Regulus_satrapa']

# some manually curated files - try training with these and see what accuracy
# looks like

# call type 1
BCCH_1 = ['31109', '31291', '31292', '37387', '17094', '70185', '76198',
          '76199', '76507', '76508', '83509']

# call type 2
BCCH_2 = ['51771', '16887', '16904', '37387', '51770', '91543', '114073',
          '114086', '121068', '132414', '134017']

# call type 1
RCKI_1 = ['211133', '131366', '175094', '210994', '159644', '173895', '173893'
          '203760', '159694', '65724', '233730', '2014', '229934']

# call type 2
RCKI_2 = ['195035', '188240', '182072', '195036', '104778', '193768', '160175',
          '277696', '229938', '187471', '131643', '54373', '53774', '185177']

BCCH = ['31109', '31291', '31292', '37387', '17094', '70185', '76198',
        '76199', '76507', '76508', '83509', '51771', '16887', '16904',
        '51770', '91543', '114073', '114086', '121068', '132414', '134017']

CBCH = ['35305', '36609', '199587', '164260', '163642', '163621', '161411',
        '160116', '159981', '159980', '159455', '28256', '28258', '109655',
        '143244', '143245', '159030', '159160', '159325', '159423', '159740']

RCKI = ['211133', '131366', '175094', '210994', '159644', '173895', '173893',
        '203760', '159694', '65724', '233730', '201424', '229934', '195035',
        '188240', '182072', '195036', '104778', '193768', '160175', '277696',
        '229938', '187471', '131643', '54373', '53774', '185177']

GCKI = ['6274', '11485', '13863', '13864', '14480', '14962', '41584', '87183',
        '89172', '93427', '99383', '106952', '111113']

files = []

for item in BCCH:
    files.append(audio_path + species_list[0] + "_wav/" + item + ".wav")

for item in CBCH:
    files.append(audio_path + species_list[1] + "_wav/" + item + ".wav")

for item in RCKI:
    files.append(audio_path + species_list[2] + "_wav/" + item + ".wav")

for item in GCKI:
    files.append(audio_path + species_list[3] + "_wav/" + item + ".wav")


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


def file_list(path, species):
    file_list = []
    for sp in species:
        for (_, _, filenames) in os.walk(path + sp + "_wav/"):
            for f in filenames:
                file_list.append(path + sp + "_wav/" + f)
    return file_list


# dump transformed audio to json
def wav_to_json(wav_list, json_list):
    pca = PCA(n_components=40, copy=False, whiten=True)
    for f in file_list:
        a = read(f)
        spec = stft.spectrogram(a[1])
        v = spec.real.astype(float)
        norm = normalize(v, norm="l2")
        whitened = pca.fit_transform(norm)
        temp = pd.DataFrame(whitened)
        with open(json_list[0], 'w') as myfile:
            json.dumps(temp.to_json(path_or_buf=json_list[0]), myfile)


# put ransformed audio files in a DataFrame
def wav_to_df(wav_list):
    whitened = {}
    df = pd.DataFrame()
    pca = PCA(n_components=40, copy=False, whiten=True)
    for f in wav_list:
        a = read(f)
        spec = stft.spectrogram(a[1])
        autopower = np.abs(spec * np.conj(spec))
        v = autopower.real.astype(float)
        norm = normalize(v, norm="l2")
        whitened[f] = 20 * np.log10(pca.fit_transform(norm))
        temp = pd.DataFrame(whitened.items(), columns=['Filename', 'Spec_features'])
        df = df.append(temp)
    return df, whitened
