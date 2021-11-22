import os
from os.path import isfile, join
import argparse
import music_tag

def arg_setup():
    parser = argparse.ArgumentParser(description='Added metadata to audio files using data from MusicBrainz')
    parser.add_argument('--album-directory', '-d', type=str)

    runtime_args = parser.parse_args()
    runtime_info = {
        'album_directory': runtime_args.album_directory
    }

    return runtime_info

def load_files(album_directory):
    album_files = []
    directory_files = [file for file in os.listdir(album_directory) if isfile(join(album_directory, file))]

    for file in directory_files:
        print(file)
        print(join(album_directory, file))
        album_files.append(music_tag.load_file(join(album_directory, file)))

    return album_files

def main():
    runtime_info = arg_setup()
    album_files = load_files(runtime_info['album_directory'])

    for file in album_files:
        print(file)        

main()
