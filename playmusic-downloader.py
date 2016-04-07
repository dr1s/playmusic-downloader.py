#!/usr/bin/env python
# -*- coding: utf-8 -*-

import sys
import os
import getpass
import urllib2
import eyed3
import math
import getopt
from gmusicapi import Mobileclient

eyed3.log.setLevel("ERROR")

output_dir = "music"
replace_files = False


def replace_characters(text):
    result = text.replace(u'/','-')
    return result


def login():
    print("Login to Google Play Music")
    user = raw_input("Username: ")
    password = getpass.getpass(prompt="Password: ")
    print(" ")

    if user:
        if password:
            apiMobileClient = Mobileclient(False)
            apiMobileClient.login(user, password, Mobileclient.FROM_MAC_ADDRESS)

            return apiMobileClient
        else:
            print("Password not set")
    else:
        print()


def set_id3_tag(song, file_name):
    audiofile = eyed3.load(file_name)
    audiofile.initTag()

    audiofile.tag.artist = song['artist']
    audiofile.tag.album = song['album']
    audiofile.tag.title = song['title']
    audiofile.tag.track_num = song['trackNumber']
    audiofile.tag.year = song['year']

    if song['albumArtist']:
        audiofile.tag.album_artist = song['albumArtist']
    else:
        audifile.tag.album_artist = song['artist']

    cover_file = os.path.join(os.path.dirname(file_name), 'cover.jpg')
    if not (os.path.exists(cover_file)):
        download_file(song['albumArtRef'][0]['url'], cover_file)
    if (os.path.exists(cover_file)):
        cover_image = open(cover_file, "rb").read()
        audiofile.tag.images.set(3, cover_image, "image/jpeg")

    audiofile.tag.save()


def download_file(url, file_name):
    res = urllib2.urlopen(url)
    fh = open(file_name , "wb")
    fh.write(res.read())
    fh.close()


def download_mp3(api, song, file_path):
    stream_url = api.get_stream_url(song['id'])
    download_file(stream_url, file_path)
    set_id3_tag(song, file_path)


def setup_directories(output, album_artist, album, year):
    if not os.path.exists(output):
        os.mkdir(output)
    artist_dir = os.path.join(output, album_artist)
    if not os.path.exists(artist_dir):
        os.mkdir(artist_dir)
    album_dir = os.path.join(artist_dir, unicode(year) + " - " + album)
    if not os.path.exists(album_dir):
        os.mkdir(album_dir)

    return album_dir


def download_song(api, song):
    artist = replace_characters(song['artist'])
    album = replace_characters(song['album'])
    title = replace_characters(song['title'])
    year = int(song['year'])
    album_artist = artist

    if song['albumArtist']:
        album_artist = replace_characters(song['albumArtist'])

    if song['id']:
        output_path = setup_directories(output_dir, album_artist, album, song['year'])
        file_name = unicode(song['trackNumber']) + u" - "
        file_name +=  artist + u" - " + title + u".mp3"

        file_path = os.path.join(output_path, file_name)

        if not (os.path.exists(file_path)) or replace_files:
            download_mp3(api, song, file_path)
        else:
            song_estimated_size = int(song['estimatedSize'])
            song_filesize = os.path.getsize(file_path)
            size_diff = math.sqrt(math.pow((song_filesize - song_estimated_size), 2))
            if size_diff > 600000:
                download_mp3(api, song, file_path)


def download_all_songs(api):
    library = api.get_all_songs()
    library_size = len(library)
    i = 0

    for song in library:
        i += 1
        file_name = unicode(song['trackNumber']) + u" - " + song['artist']
        file_name += u" - " + song['title']

        stdout = "\r\033[K[" + unicode(i) + "/" + unicode(library_size) + "]"
        stdout += ": " + file_name

        sys.stdout.write(stdout)
        sys.stdout.flush()

        download_song(api, song)

    print(" ")


def main():

    try:
        opts, args = getopt.getopt(sys.argv[1:], "ho:r", ["help", "output="])
    except getopt.GetoptError as err:
        print str(err)
        usage()
        sys.exit(2)
    for o, a in opts:
        if o in ("-h", "--help"):
            #usage()
            sys.exit()
        elif o in ("-o", "--output"):
            global output_dir
            output_dir = a
            output_dir = os.path.abspath(output_dir)
        elif o in ("-r", "--replace"):
            global replace_files
            replace_files = True
        else:
            assert False, "unhandled option"

    api = login()
    if (api):
        download_all_songs(api)


if __name__ == "__main__":
    main()
