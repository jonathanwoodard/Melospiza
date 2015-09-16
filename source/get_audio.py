import requests
import json
import os


def json_download(species_list, tags=None):
    '''
    INPUT:
        species_list: target list of species to download
        destination: destination path for downloaded files
        tags: dict of tag: value pairs to add to query; defaults to None
    OUTPUT: json
    '''
    source_url = "http://www.xeno-canto.org/api/2/recordings?query="
    dest_dir = "/media/jon/external_data/audio/"

    for species in species_list:
        s = species.split()
        q = source_url + s[0] + '%20' + s[1]
        page = requests.get(q, stream=True)
        with open((dest_dir + species.replace(' ', '_')), 'wb') as f:
            f.write(page.content)


url = "http://www.xeno-canto.org/"
audio_path = '/media/jon/external_data/audio/'


def make_dirs(audio_path):
    f = []
    for (_, _, filename) in os.walk(audio_path + "json_files"):
        f.extend(filename)
        for name in f:
            os.makedirs(audio_path + name)


def get_audio(audio_path, url):
    '''
    INPUT:
        audio_path: path to the directory where audio files will be written
        url: base url from which audio files will be downloaded
    '''
    ids = []
    errors = []
    json_path = audio_path + "json_files"
    for (_, _, filename) in os.walk(json_path):
        for name in filename:
            with open(json_path + '/' + name) as j:
                temp = json.load(j)
                for item in temp['recordings']:
                    ids.append((item['id'], name))
    for i in ids:
        output = audio_path + '/' + i[1] + '/' + i[0] + '.mp3'
        target_url = url + i[0] + '.mp3/download'
        with open(output, 'wb') as handle:
            response = requests.get(target_url, stream=True)
            if not response.ok:
                errors.append(output)
            for block in response.iter_content(1024):
                handle.write(block)


def get_audio2(audio_path, url):
    '''
    INPUT:
        audio_path: path to the directory where audio files will be written
        url: base url from which audio files will be downloaded
    '''
    ids = []
    errors = []
    json_path = audio_path + "target"
    for (_, _, filename) in os.walk(json_path):
        for name in filename:
            with open(json_path + '/' + name) as j:
                temp = json.load(j)
                for item in temp['recordings']:
                    ids.append((item['id'], name))
    for i in ids:
        output = audio_path + '/' + i[1] + '/' + i[0] + '.mp3'
        target_url = url + i[0] + '/download'
        with open(output, 'wb') as handle:
            response = requests.get(target_url, stream=True)
            if not response.ok:
                errors.append(output)
            for block in response.iter_content(1024):
                handle.write(block)


def get_audio3(audio_path, url):
    '''
    INPUT:
        audio_path: path to the directory where audio files will be written
        url: base url from which audio files will be downloaded
    '''
    ids = []
    errors = []
    json_path = audio_path + "target"
    for (_, _, filename) in os.walk(json_path):
        for name in filename:
            with open(json_path + '/' + name) as j:
                temp = json.load(j)
                for item in temp['recordings']:
                    ids.append((item['id'], name))
    for i in ids:
        output = audio_path + '/' + i[1] + '/' + i[0] + '.mp3'
        if not os.path.isfile(output):
            target_url = url + i[0] + '/download'
            with open(output, 'wb') as handle:
                response = requests.get(target_url, stream=True)
                if not response.ok:
                    errors.append(output)
                for block in response.iter_content(1024):
                    handle.write(block)
