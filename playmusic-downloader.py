#!/usr/bin/env python

import sys
import os
import getpass
import urllib
import eyed3
from gmusicapi import Mobileclient


eyed3.log.setLevel("ERROR")

output_dir = "music"

def login():
    print("Login to Google Play Music")
    user = raw_input("Username: ")
    password = getpass.getpass(prompt="Password: ")
    print(" ")

    if (user and password):
        apiMobileClient = Mobileclient(False)
        apiMobileClient.login(user, password, Mobileclient.FROM_MAC_ADDRESS)

        return apiMobileClient

def set_id3_tag(song, file_name):
    audiofile = eyed3.load(file_name)
    audiofile.initTag()

    audiofile.tag.artist = song['artist']
    audiofile.tag.album = song['album']
    audiofile.tag.title = song['title']
    audiofile.tag.track_num = song['trackNumber']

    if song['albumArtist']:
        audiofile.tag.album_artist = song['albumArtist']
    else:
        audifile.tag.album_artist = song['artist']

    cover_file = os.path.dirname(file_name) + "/cover.jpg"
    download_album_cover(song['albumArtRef'][0]['url'], cover_file)
    if (os.path.exists(cover_file)):
        cover_image = open(cover_file, "rb").read()
        audiofile.tag.images.set(3, cover_image, "image/jpeg")

    audiofile.tag.save()


def download_album_cover(url, file_name):
    if not (os.path.exists(file_name)):
        urllib.request.urlretrieve(url, file_name)


def download_song(stream_url, song):
    artist = song['artist']
    album = song['album']
    album_artist = artist

    if song['albumArtist']:
        album_artist = song['albumArtist']

    if not os.path.exists(output_dir + "/" + album_artist):
        os.mkdir(output_dir + "/" + album_artist)
    if not os.path.exists(output_dir + "/" + album_artist + "/" + album):
        os.mkdir(output_dir + "/" + album_artist + "/" + album)

    if song['id']:
        output_path = output_dir + "/" + album_artist + "/" + album
        file_name = str(song['trackNumber']) + " - "
        file_name +=  song['artist'] + " - " + song['title'] + ".mp3"

        urllib.request.urlretrieve(stream_url, output_path+ '/' + file_name)
        set_id3_tag(song, output_path + '/' + file_name)


def download_all_songs(api):
    library = api.get_all_songs()
    library_size = len(library)
    i = 0

    if not os.path.exists(output_dir):
        os.mkdir(output_dir)

    for song in library:
        i += 1

        file_name = str(song['trackNumber']) + " - " + song['artist']
        file_name += " - " + song['title']

        stdout = "\r[" + str(i) + "/" + str(library_size)
        stdout += "]: " + file_name + "                                        "

        sys.stdout.write(stdout)
        sys.stdout.flush()

        stream_url = api.get_stream_url(song['id'])
        download_song(stream_url, song)


def main():
    api = login()
    if (api):
        download_all_songs(api)

if __name__ == "__main__":
    main()
