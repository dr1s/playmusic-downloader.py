#!/usr/bin/env python
# -*- coding: utf-8 -*-

import sys
import os
import getpass
import urllib
import urllib2
import eyed3
from gmusicapi import Mobileclient

eyed3.log.setLevel("ERROR")

output_dir = "music"
replace_files = False

output_dir = os.path.abspath(output_dir)

def replace_characters(text):
    result = text.replace(u'/','-')
    return result


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

    cover_file = os.path.join(os.path.dirname(file_name), 'cover.jpg')
    download_album_cover(song['albumArtRef'][0]['url'], cover_file)
    if (os.path.exists(cover_file)):
        cover_image = open(cover_file, "rb").read()
        audiofile.tag.images.set(3, cover_image, "image/jpeg")

    audiofile.tag.save()


def download_album_cover(url, file_name):
    if url and not (os.path.exists(file_name)):
        res = urllib2.urlopen(url)
        fh = open(file_name, "wb")
        fh.write(res.read())
        fh.close

        #urllib.request.urlretrieve(url, file_name)


def download_song(api, song):
    artist = song['artist']
    album = song['album']
    title = replace_characters(song['title'])
    album_artist = artist

    if song['albumArtist']:
        album_artist = song['albumArtist']

    if not os.path.exists(output_dir + u"/" + album_artist):
        os.mkdir(output_dir + "/" + album_artist)
    if not os.path.exists(output_dir + u"/" + album_artist + u"/" + album):
        os.mkdir(output_dir + u"/" + album_artist + u"/" + album)

    if song['id']:
        #output_path = output_dir + "/" + album_artist + "/" + album
        output_path = os.path.join(os.path.join(output_dir, album_artist), album)
        file_name = unicode(song['trackNumber']) + u" - "
        file_name +=  artist + u" - " + title + u".mp3"


        #urlib.request.urlretrieve(stream_url, output_path+ '/' + file_name)
        if not (os.path.exists(output_path + '/' + file_name)) or replace_files:
            stream_url = api.get_stream_url(song['id'])
            #print (output_path + u'/' + file_name)

            res = urllib2.urlopen(stream_url)
            fh = open(os.path.join(output_path, file_name) , "wb")
            fh.write(res.read())
            fh.close()
            set_id3_tag(song, os.path.join(output_path, file_name))


def download_all_songs(api):
    library = api.get_all_songs()
    library_size = len(library)
    i = 0

    if not os.path.exists(output_dir):
        os.mkdir(output_dir)

    for song in library:
        i += 1

        file_name = unicode(song['trackNumber']) + u" - " + song['artist']
        file_name += u" - " + song['title']

        stdout = "\r\033[K[" + unicode(i) + "/" + unicode(library_size)
        stdout += "]: " + file_name

        sys.stdout.write(stdout)
        sys.stdout.flush()

        download_song(api, song)


def main():
    api = login()
    if (api):
        download_all_songs(api)

if __name__ == "__main__":
    main()
