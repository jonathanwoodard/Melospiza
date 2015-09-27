# spark analysis

import pandas as pd
import numpy as np
from pydub import AudioSegment
from scipy.io.wavfile import read
from sklearn.preprocessing import normalize
from sklearn.decomposition import PCA


files = [" # list of files to be processed"]

wavs = [read(f)[1] for f in files[:]]  # create a list of np arrays

rdd = sc.parallelize([wavs[i] for i in xrange(len(wavs))])
