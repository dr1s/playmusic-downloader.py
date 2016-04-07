# playmusicdownloader.py
Download your library from Google Play Musci using the unoffical gmusicapi.
The files will be tagged using eyed3.

## Getting started
* `cd playmusic-downloader.py`
* `python2 setup.py install`
* `playmusicdl`
* Login to Google Play Music
* All files will be stored in the subdirectory `music`

## Usage
`playmusicdl -o download_dir -r`
Will download all music to a directory called `download_dir`.
If there are any preexisting songs they will be replaced.

    usage: playmusicdl [arguments]
      -r | --replace: replace already downloaded songs
      -o | --output output_dir : directory where files will be stored in
      -h | --help : shows this message
## Dependencies
* gmusicapi
* eyed3

## Uninstall
`pip uninstall playmusic-downloader.py`
