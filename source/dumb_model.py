import pandas as pd
import numpy as np
import json
import string
from sklearn.ensemble import RandomForestClassifier
import stft
import make_features
from sklearn.cross_validation import train_test_split
from sklearn.ensemble import RandomForestClassifier


spectrograms = make_spec(test_subset)
normalized = norm_spec(spectrograms)
whitened = whiten(normalized)

df = pd.DataFrame(whitened.items(), columns=['Filename', 'Spec_features'])
spec = df['Filename']
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

# feature hasher

# keys = whitened.keys()
# splits = [string.split(keys[i], sep="/") for i in xrange(len(keys))]
# hasher = FeatureHasher(n_features=40, input_type="string")
# df_hash = pd.DataFrame()
# for i in xrange(len(keys)):
#     temp = pd.DataFrame()
#     for j in xrange(len(whitened[keys[i]].T)):
#         autopower = np.abs(whitened[keys[i]] * np.conj(whitened[keys[i]]))
#         result = np.log10(autopower)
#         h = "hash" + str(j)
#         string = ["%.4f" % n for n in result.flatten()]
#         temp[h] = result.max(axis=0)
#     temp['species'] = splits[i][0][:-4]
#     temp['file_id'] = splits[i][1][:-4]
#     df_hash = df_hash.append(temp)
# df_hash = df_max.set_index('file_id')

# random files
target = ['data/target_species/Regulus_satrapa_wav/254952.wav',
          'data/target_species/Poecile_atricapillus_wav/206087.wav',
          'data/target_species/Regulus_satrapa_wav/210900.wav',
          'data/target_species/Regulus_calendula_wav/185177.wav',
          'data/target_species/Regulus_satrapa_wav/52465.wav',
          'data/target_species/Poecile_rufescens_wav/269229.wav',
          'data/target_species/Regulus_calendula_wav/13587.wav',
          'data/target_species/Poecile_atricapillus_wav/174869.wav',
          'data/target_species/Regulus_calendula_wav/160018.wav',
          'data/target_species/Regulus_calendula_wav/131365.wav',
          'data/target_species/Regulus_calendula_wav/229050.wav',
          'data/target_species/Poecile_atricapillus_wav/267505.wav',
          'data/target_species/Poecile_atricapillus_wav/161652.wav',
          'data/target_species/Poecile_rufescens_wav/28255.wav',
          'data/target_species/Poecile_atricapillus_wav/160353.wav',
          'data/target_species/Poecile_rufescens_wav/157659.wav',
          'data/target_species/Regulus_satrapa_wav/159218.wav',
          'data/target_species/Poecile_atricapillus_wav/233942.wav',
          'data/target_species/Regulus_satrapa_wav/161134.wav',
          'data/target_species/Regulus_calendula_wav/125256.wav',
          'data/target_species/Regulus_calendula_wav/160014.wav',
          'data/target_species/Regulus_calendula_wav/173895.wav',
          'data/target_species/Regulus_satrapa_wav/14481.wav',
          'data/target_species/Regulus_calendula_wav/54373.wav',
          'data/target_species/Regulus_calendula_wav/160378.wav',
          'data/target_species/Poecile_atricapillus_wav/188372.wav',
          'data/target_species/Poecile_atricapillus_wav/139827.wav',
          'data/target_species/Regulus_satrapa_wav/215704.wav',
          'data/target_species/Regulus_calendula_wav/229937.wav',
          'data/target_species/Regulus_calendula_wav/135077.wav',
          'data/target_species/Regulus_satrapa_wav/92098.wav',
          'data/target_species/Regulus_calendula_wav/17045.wav',
          'data/target_species/Regulus_satrapa_wav/179789.wav',
          'data/target_species/Regulus_calendula_wav/229944.wav',
          'data/target_species/Regulus_satrapa_wav/160226.wav',
          'data/target_species/Poecile_atricapillus_wav/144664.wav',
          'data/target_species/Regulus_calendula_wav/193121.wav',
          'data/target_species/Poecile_atricapillus_wav/277126.wav',
          'data/target_species/Regulus_satrapa_wav/6274.wav',
          'data/target_species/Regulus_satrapa_wav/37394.wav',
          'data/target_species/Regulus_satrapa_wav/168195.wav',
          'data/target_species/Regulus_satrapa_wav/93427.wav',
          'data/target_species/Regulus_calendula_wav/180327.wav',
          'data/target_species/Regulus_satrapa_wav/159896.wav',
          'data/target_species/Regulus_calendula_wav/195546.wav',
          'data/target_species/Poecile_rufescens_wav/160252.wav',
          'data/target_species/Regulus_calendula_wav/153884.wav',
          'data/target_species/Poecile_rufescens_wav/36609.wav',
          'data/target_species/Regulus_calendula_wav/176980.wav',
          'data/target_species/Regulus_calendula_wav/162427.wav',
          'data/target_species/Poecile_atricapillus_wav/265075.wav',
          'data/target_species/Regulus_calendula_wav/160386.wav',
          'data/target_species/Regulus_satrapa_wav/161132.wav',
          'data/target_species/Regulus_satrapa_wav/154306.wav',
          'data/target_species/Regulus_satrapa_wav/87183.wav',
          'data/target_species/Regulus_calendula_wav/185181.wav',
          'data/target_species/Regulus_calendula_wav/236498.wav',
          'data/target_species/Regulus_calendula_wav/182934.wav',
          'data/target_species/Poecile_atricapillus_wav/253535.wav',
          'data/target_species/Poecile_rufescens_wav/178009.wav',
          'data/target_species/Poecile_rufescens_wav/159871.wav',
          'data/target_species/Regulus_satrapa_wav/159718.wav',
          'data/target_species/Regulus_satrapa_wav/253562.wav',
          'data/target_species/Regulus_calendula_wav/195035.wav',
          'data/target_species/Regulus_calendula_wav/255394.wav',
          'data/target_species/Poecile_rufescens_wav/159429.wav',
          'data/target_species/Regulus_calendula_wav/252010.wav',
          'data/target_species/Poecile_atricapillus_wav/216847.wav',
          'data/target_species/Regulus_satrapa_wav/146197.wav',
          'data/target_species/Poecile_atricapillus_wav/132861.wav',
          'data/target_species/Regulus_calendula_wav/48220.wav',
          'data/target_species/Regulus_satrapa_wav/168196.wav',
          'data/target_species/Poecile_atricapillus_wav/199358.wav',
          'data/target_species/Poecile_rufescens_wav/105731.wav',
          'data/target_species/Regulus_calendula_wav/197072.wav',
          'data/target_species/Poecile_rufescens_wav/163642.wav',
          'data/target_species/Regulus_satrapa_wav/210901.wav',
          'data/target_species/Regulus_calendula_wav/159571.wav',
          'data/target_species/Regulus_calendula_wav/76888.wav',
          'data/target_species/Regulus_calendula_wav/185186.wav',
          'data/target_species/Regulus_calendula_wav/159644.wav',
          'data/target_species/Poecile_rufescens_wav/89915.wav',
          'data/target_species/Poecile_atricapillus_wav/216533.wav',
          'data/target_species/Poecile_atricapillus_wav/178778.wav',
          'data/target_species/Poecile_atricapillus_wav/168971.wav',
          'data/target_species/Regulus_satrapa_wav/161135.wav',
          'data/target_species/Poecile_atricapillus_wav/278350.wav',
          'data/target_species/Poecile_rufescens_wav/159862.wav',
          'data/target_species/Regulus_satrapa_wav/1216.wav',
          'data/target_species/Regulus_calendula_wav/185185.wav',
          'data/target_species/Poecile_atricapillus_wav/156746.wav',
          'data/target_species/Regulus_calendula_wav/255646.wav',
          'data/target_species/Poecile_atricapillus_wav/149941.wav',
          'data/target_species/Regulus_satrapa_wav/161120.wav',
          'data/target_species/Regulus_satrapa_wav/104683.wav',
          'data/target_species/Regulus_satrapa_wav/103079.wav',
          'data/target_species/Regulus_satrapa_wav/159574.wav',
          'data/target_species/Poecile_rufescens_wav/160116.wav',
          'data/target_species/Regulus_calendula_wav/191466.wav',
          'data/target_species/Regulus_calendula_wav/187471.wav']
