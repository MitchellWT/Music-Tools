import os
from os.path import isfile, join
import argparse
import music_tag
import musicbrainzngs

def arg_setup():
    parser = argparse.ArgumentParser(description='Added metadata to audio files using data from MusicBrainz')
    parser.add_argument('--album-directory', '-d', type=str)
    parser.add_argument('--mb-disc-id', '-m', type=str)
    parser.add_argument('--album-rip', '-r')

    runtime_args = parser.parse_args()
    runtime_info = {
        'album_directory': runtime_args.album_directory,
        'mb_disc_id' :     runtime_args.mb_disc_id,
        'album_rip':       runtime_args.album_rip
    }

    return runtime_info

def load_files(album_directory):
    album_files = {}
    directory_files = [file for file in os.listdir(album_directory) if isfile(join(album_directory, file))]

    for file in directory_files:
        album_files[file] = music_tag.load_file(join(album_directory, file))

    return album_files

def get_metadata(mb_disc_id):
    musicbrainzngs.set_useragent("Mitchell's Music Tagger", "0.0.1")
    metadata_json = musicbrainzngs.get_releases_by_discid(mb_disc_id, includes=["artists", "recordings"])
    
    return metadata_json['disc']['release-list']

def set_metadata(album_directory, album_files, release_list):
    album_title = release_list['title']
    artist = release_list['artist-credit'][0]['artist']['name']
    year = release_list['date'][0:4]
    disc_count = release_list['medium-count']
    disc_counter = 0
    track_count = 0
    track_counter = 0

    # Gets total amount of album tracks
    for medium_list in release_list['medium-list']:
        track_count += medium_list['track-count']

    for medium_list in release_list['medium-list']:
        disc_counter += 1
        for track in medium_list['track-list']:
            key = "Track_{}.flac".format(track_counter + 1)
            
            album_files[key]['album'] = album_title
            album_files[key]['album-artist'] = artist
            album_files[key]['artist'] = artist
            album_files[key]['disc-number'] = disc_counter
            album_files[key]['total-discs'] = disc_count
            album_files[key]['total-tracks'] = track_count
            album_files[key]['track-number'] = (track_counter + 1)
            album_files[key]['track-title'] = track['recording']['title']
            album_files[key]['year'] = year
            album_files[key].save()

            track_counter += 1

            os.rename(
                album_directory + key, 
                album_directory + "{:02d} - {}.flac".format(
                    track_counter, 
                    track['recording']['title']
                )
            )

if __name__ == '__main__':
    runtime_info = arg_setup()
    album_files = load_files(runtime_info['album_directory'])
    release_list = get_metadata(runtime_info['mb_disc_id'])
    release_list = release_list[0]
    set_metadata(runtime_info['album_directory'], album_files, release_list)
