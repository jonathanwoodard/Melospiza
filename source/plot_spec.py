# code for generating different variations of spectrograms
import numpy as np
import matplotlib.pyplot as plt
import stft
from scipy.io.wavfile import read
from sklearn.preprocessing import normalize
from sklearn.decomposition import PCA


def plot_spec(f):
    a = read(f)
    spec = stft.spectrogram(a[1])
    auto = np.abs(spec * np.conj(spec))
    norm = normalize(auto, norm="l2")
    img = plt.imshow(norm, origin='lower', cmap='jet', interpolation='nearest', aspect='auto')
    plt.show()


def plot_pca_spec(f):
    pca = PCA(n_components=200, copy=False, whiten=False)
    a = read(f)
    spec = stft.spectrogram(a[1])
    auto = np.abs(spec * np.conj(spec))
    norm = normalize(auto, norm="l2")
    w = 20 * np.log10(pca.fit_transform(norm))
    clipped = np.clip(w, -40, 200)
    img = plt.imshow(clipped, origin='lower', cmap='jet', interpolation='nearest', aspect='auto')
    plt.show()


def plot_pca_spec2(f):
    pca = PCA(n_components=40, copy=False, whiten=True)
    a = read(f)
    spec = stft.spectrogram(a[1])
    v = spec.real.astype(float)
    auto = np.abs(v * np.conj(v))
    norm = normalize(auto, norm="l2")
    w = (pca.fit_transform(norm))
    # clipped = np.clip(w, -40, 200)
    img = plt.imshow(norm, origin='lower', cmap='jet', interpolation='nearest', aspect='auto')
    plt.show()
