#! /bin/bash

# Rename files to remove white spaces
for file in "$1"*; do
    no_space_file=${file/ /_}
    if [[ $file != $no_space_file ]]; then
        mv "$file" "$no_space_file"
    fi
done

# Converts WAV to 176Hz 32-bit FLAC
for i in "$1"*; do
    flac_out=${i/wav/flac}
    flac_out=${flac_out/$1/}
    ffmpeg -i "$i" -af aformat=s32:176000 "$2""$flac_out"
done
