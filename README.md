## Melospiza is a birdsong classifier capable of identifying North American bird species from user recorded audio files.

Currently, this project supports four species common in the Pacific Northwest.  More species coming soon!

The project consists of a web application, www.melospiza.net, where users can
upload audio files of unknown bird vocalizations.  The application uses a Short
Time Fourier Transform to reduce the raw audio files to a list of features which
can be classified using a Random Forest model.
