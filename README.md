## Melospiza is a birdsong classifier capable of identifying North American bird species from user recorded audio files.

(https://github.com/jonathanwoodard/Melospiza/blob/master/flask_app/static/img/Screenshot.png)

I am currently in the process of refactoring the code for this project, using the
recently released TensorFlow (http://tensorflow.org) project, and a recurrent
neural network for audio feature extraction.  Please check back soon!

The project consists of a web application, www.melospiza.net, where users can
upload audio files of unknown bird vocalizations.  The application uses a Short
Time Fourier Transform to reduce the raw audio files to a list of features which
can be classified using a Random Forest model.

The purpose of this project is to enable accurate avian species identification from
recorded audio.  Automatic identification of species and individuals from large data
sets, including remote sensing data, has important applications, particularly in
monitoring the health of ecological systems and species of concern.  A practical
tool to simplify the identification of commonly observed bird species should also
be useful for public education, and increasing the enjoyment of recreational
bird watching.

Audio files used for this project were obtained from Xeno-Canto (http://www.xeno-canto.org),
the Avian Vocalization Center (http://avocet.zoology.msu.edu) at Michigan State University,
and the Macaulay Library at the Cornell Lab of Ornithology (http://macaulaylibrary.org).
For the initial implementation, the following four species were used:

+   Black-capped Chickadee      *Poecile atricapillus*
+   Chestnut-backed Chickadee   *Poecile rufescens*
+   Golden-crowned Kinglet      *Regulus calendula*
+   Ruby-crowned Kinglet        *Regulus satrapa*

These species were chosen due to the relatively large number of available audio recordings,
and the fact that they are regularly observed during monthly surveys at Seward Park, in
Seattle, Washington.
Observational data for North America, from the Cornell Lab of Ornithology eBird data set,
was obtained from the Global Biodiversity Information Facility (http://www.gbif.org).

##Technical Details:
Melospiza starts with an audio file in .mp3 or .wav format.  A Short Time Fourier
Transform algorithm is used to generate a spectrogram, which is then transformed
into a set of features using a Long Short Term Memory Recurrent Neural Network.
![spectrogram from Black-capped Chickadee] (https://github.com/jonathanwoodard/Melospiza/blob/master/flask_app/static/img/bcch_2_spec.png)
          *spectrogram from Black-capped Chickadee*
