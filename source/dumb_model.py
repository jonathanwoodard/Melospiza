import pandas as pd
import numpy as np
import json
import string
from sklearn.ensemble import RandomForestClassifier
import stft
import make_features
from sklearn.cross_validation import train_test_split
from sklearn.ensemble import RandomForestClassifier


# spectrograms = make_spec(test_subset)
# normalized = norm_spec(spectrograms)
# whitened = whiten(normalized)

df = pd.DataFrame(whitened.items(), columns=['Filename', 'Spec_features'])
spec = df['Filename'].values
splits = [string.split(spec[i], sep="/") for i in xrange(len(spec))]
df['species'] = [splits[i][0][:-4] for i in xrange(len(splits))]
df['file_id'] = [splits[i][1][:-4] for i in xrange(len(splits))]
df.set_index('file_id', inplace=True)
del df['Filename']

y = df.pop('species')
X = df
X_train, X_test, y_train, y_test = train_test_split(X, y, test_size=0.2)
rf = RandomForestClassifier(n_estimators=200, criterion='entropy', oob_score=True)


keys = whitened.keys()
splits = [string.split(keys[i], sep="/") for i in xrange(len(keys))]
df = pd.DataFrame()
for i in xrange(len(keys)):
    name = "df" + str(i)
    name = pd.DataFrame()
    for j in xrange(len(whitened[keys[i]].T)):
        name[j] = [whitened[keys[i]].T[j]]
        name[j] = name[j].astype(np.dtype)
    name['species'] = splits[i][0][:-4]
    name['file_id'] = splits[i][1][:-4]
    df = df.append(name)
df = df.set_index('file_id')


# can't fit on array? use mean/var, max, or downsample to 10 points
# mean and variance

keys = whitened.keys()
splits = [string.split(keys[i], sep="/") for i in xrange(len(keys))]
df_mv = pd.DataFrame()
for i in xrange(len(keys)):
    temp = pd.DataFrame()
    for j in xrange(len(whitened[keys[i]].T)):
        autopower = np.abs(whitened[keys[i]] * np.conj(whitened[keys[i]]))
        result = np.log10(autopower)
        mean = "mean" + str(j)
        var = "var" + str(j)
        temp[mean] = result.mean(axis=0)
        temp[var] = result.var(axis=0)
    temp['species'] = splits[i][0][:-4]
    temp['file_id'] = splits[i][1][:-4]
    df_mv = df_mv.append(temp)
df_mv = df_mv.set_index('file_id')

# max

keys = whitened.keys()
splits = [string.split(keys[i], sep="/") for i in xrange(len(keys))]
df_max = pd.DataFrame()
for i in xrange(len(keys)):
    temp = pd.DataFrame()
    for j in xrange(len(whitened[keys[i]].T)):
        autopower = np.abs(whitened[keys[i]] * np.conj(whitened[keys[i]]))
        result = np.log10(autopower)
        max = "max" + str(j)
        temp[max] = result.max(axis=0)
    temp['species'] = splits[i][0][:-4]
    temp['file_id'] = splits[i][1][:-4]
    df_max = df_max.append(temp)
df_max = df_max.set_index('file_id')
