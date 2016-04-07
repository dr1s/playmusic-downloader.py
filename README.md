# playmusic-downloader.py
Download your library from Google Play Musci using the unoffical gmusicapi.
The files will be tagged using eyed3.

## Getting started
* `cd playmusic-downloader.py`
* `python2 setup.py`
* `python2 playmusic-downloader.py`
* Login to Google Play Music
* All files will be stored in the subdirectory `music`

## Usage
`python2 playmusic-downloader.py -o download_dir -r`
Will download all music to a directory called `download_dir`.
If there are any preexisting songs they will be replaced.

## Dependencies
* gmusicapi
* eyed3
