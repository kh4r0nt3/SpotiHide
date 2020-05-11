###############################################################################
## Steganography tool developed for the APT subject at the Carlos III University
## of Madrid that hides messages in public playlists of spotify.
###############################################################################
## Author: Jose Carlos Quiroga Alvarez
## Copyright: Copyright 2020, SpotiHide
## Email: 100423673@alumnos.uc3m.es
## Status: Development
###############################################################################

import time
import random
import spotipy
import secrets
import binascii
import pyfiglet
import colorama
import progressbar
from os import system
import spotipy.util as util
from colorama import Fore, Back, Style #Fore: BLACK, RED, GREEN, YELLOW, BLUE, MAGENTA, CYAN, WHITE, RESET.
                                       #Back: BLACK, RED, GREEN, YELLOW, BLUE, MAGENTA, CYAN, WHITE, RESET.
                                       #Style: DIM, NORMAL, BRIGHT, RESET_ALL


USERNAME = ''
MESSAGE_PLAYLIST = ''
ALPHABET_PLAYLIST = ''
SCOPE = 'playlist-modify-public'
SPOTIPY_CLIENT_ID = ''
SPOTIPY_CLIENT_SECRET = ''
SPOTIPY_REDIRECT_URI = ''

def main():

    try:
        while True:
            system('cls')
            menu()
            spotify = auth()
            alphabet_username = input("[*] Alphabet Username [Default: " + USERNAME + "]: ")
            alphabet_playlist = input("[*] Alphabet Playlist [Default: " + ALPHABET_PLAYLIST + "]: ")
            if(alphabet_username == '' or alphabet_playlist == ''):
                alphabet = generate_alphabet(spotify, USERNAME, ALPHABET_PLAYLIST)
            else:
                alphabet = generate_alphabet(spotify, alphabet_username, alphabet_playlist)
            msg = input("[*] Enter a message: ").encode('ascii', errors="ignore")
            print("\n[" + Fore.GREEN + "*" + Style.RESET_ALL + "] Encoding Cool Stuff \O/ \O/ \O/ \O/ [" + str(len(binascii.hexlify(msg).decode("utf-8"))) + " Bytes]\n")
            encode(spotify, USERNAME, MESSAGE_PLAYLIST, msg, alphabet)
            print("\n[" + Back.GREEN + "Successfully Encoded" + Style.RESET_ALL + "]\n")
            print("[" + Fore.GREEN + "*" + Style.RESET_ALL + "] Decoding Cool Stuff /O\\ /O\ /O\ /O\\ \n")
            msg_decoded = decode(spotify, USERNAME, MESSAGE_PLAYLIST, alphabet)
            print("\n[" + Back.GREEN + "Successfully Decoded" + Style.RESET_ALL + "] [" + Fore.GREEN + msg_decoded + Style.RESET_ALL + "]\n")
            print("\n[" + Back.RED + "CONTINUE? [Y/N]" + Style.RESET_ALL + "]")
            finish = input()
            if finish in ['','n','N']:
                exit()


    except KeyboardInterrupt:
        print("\n")
        print("[" + Back.RED + "HAPPY HUNTING" + Style.RESET_ALL + "]")
    except Exception as ex:
        print("[" + Back.RED + "INVALID USERNAME OR PLAYLIST ID" + Style.RESET_ALL + "]")

def menu():
    """
    Simple menu for the tool that configures the colors and prints the name in ASCII.
    """
    colorama.init()
    ascii_banner = pyfiglet.figlet_format("SpotiHide")
    print(ascii_banner)

def auth():
    """
    Authenticates the user through a token to obtain the spotify object.
    """
    token = util.prompt_for_user_token(USERNAME,
                                       SCOPE,
                                       client_id = SPOTIPY_CLIENT_ID,
                                       client_secret = SPOTIPY_CLIENT_SECRET,
                                       redirect_uri= SPOTIPY_REDIRECT_URI)
    if token:
        spotify = spotipy.Spotify(auth=token)
        return spotify
    else:
        print("\n[" + Back.RED + "CANT GET TOKEN FOR" + Style.RESET_ALL + USERNAME + "]")
        exit()

def create_playlist(spotify, username, playlist_name):
    """
    Creates a playlist.
    """
    spotify.user_playlist_create(username, name=playlist_name)

def add_playlist_tracks(spotify, username, playlist_name, track_list):
    """
    Adds a list of tracks to the playlist.
    """
    playlist_id = get_playlist_id(spotify, username, playlist_name)
    spotify.user_playlist_add_tracks(username, playlist_id, track_list)

def delete_playlist_tracks(spotify, username, playlist_name):
    """
    Deletes all the tracks from a playlist.
    """
    playlist_id = get_playlist_id(spotify, username, playlist_name)
    playlist_track_list = get_playlist_tracks_id(spotify, username, playlist_name)
    request_chunks = [playlist_track_list[i:i + 100] for i in range(0, len(playlist_track_list), 100)] # Blocks of 100 songs
    for track_chunk in request_chunks:
        spotify.user_playlist_remove_all_occurrences_of_tracks(username, playlist_id, track_chunk)

def get_playlist_id(spotify, username, playlist_name):
    """
    Returns the id of a playlist by searching on each result page for its name.
    """
    playlist_id = ''
    playlists = spotify.user_playlists(username)
    for playlist in playlists['items']:
        if playlist['name'] == playlist_name:
            playlist_id = playlist['id']
            return playlist_id
    while playlists['next']: # If there are more playlists
        playlists = spotify.next(playlists)
        for playlist in playlists['items']:
            if playlist['name'] == playlist_name:
                playlist_id = playlist['id']
                return playlist_id
    return playlist_id

def get_playlist_tracks_id(spotify, username, playlist_name):
    """
    Returns a list with all the identifiers of the tracks on a playlist.
    """
    track_list = []
    playlist_id = get_playlist_id(spotify, username, playlist_name)
    tracks = spotify.playlist_tracks(playlist_id)
    for i in range(len(tracks['items'])):
        track_list.append(tracks['items'][i]['track']['id'])
    while tracks['next']: # If there are more tracks
        tracks = spotify.next(tracks)
        for i in range(len(tracks['items'])):
            track_list.append(tracks['items'][i]['track']['id'])
    return track_list

def get_playlist_tracks_artist(spotify, username, playlist_name):
    """
    Returns a list with the first artist of all the tracks on a playlist.
    """
    tracks_artist = []
    playlist_id = get_playlist_id(spotify, username, playlist_name)
    tracks = spotify.playlist_tracks(playlist_id)
    for i in range(len(tracks['items'])):
        tracks_artist.append(tracks['items'][i]['track']['artists'][0]['name']) # Appends the first artist
    while tracks['next']: # If there are more tracks
        tracks = spotify.next(tracks)
        for i in range(len(tracks['items'])):
            tracks_artist.append(tracks['items'][i]['track']['artists'][0]['name'])
    return tracks_artist

def get_playlist_16(spotify, username, playlist_name):
    """
    Returns a list of the first 16 artists on the playlist.
    """
    tracks_artist = []
    playlist_id = get_playlist_id(spotify, username, playlist_name)
    tracks = spotify.playlist_tracks(playlist_id)
    for track in range(16):
        tracks_artist.append(tracks['items'][track]['track']['artists'][0]['name']) # Appends the first artist
    return tracks_artist

def get_artists_tracks(spotify, artists):
    """
    Returns a list with one track id for each artist on the list.
    """
    track_list = []
    for artist in progressbar.progressbar(artists):
        filtered_track_list = []
        tracks = spotify.search(q='artist:' + artist , type='track', limit=50) # Searchs among the first 50 tracks
        for track in tracks['tracks']['items']:
            if track['artists'][0]['name'] == artist: # Filters the track artist
                filtered_track_list.append(track['id'])
        rand = secrets.randbelow(len(filtered_track_list))
        track_list.append(filtered_track_list[rand]) # Appends a random track
    return track_list

def generate_alphabet(spotify, username, playlist_name):
    """
    Returns a dictionary with the alphabet obtained from a playlist composed of the corresponding hexadecimal characters and artists.
    """
    hex_list = ["0", "1", "2", "3", "4", "5", "6", "7", "8", "9", "a", "b", "c", "d", "e", "f"]
    artist_list = get_playlist_16(spotify, username, playlist_name)

    #random.shuffle(hex_list)
    #random.shuffle(artist_list)

    alphabet = {hex:artist for hex,artist in zip(hex_list,artist_list)}

    return alphabet

def encode(spotify, username, playlist_name, msg, alphabet):
    """
    Encodes the message
    """
    delete_playlist_tracks(spotify, username, playlist_name)
    msg_hex = binascii.hexlify(msg).decode("utf-8")
    request_chunks = [msg_hex[i:i+100] for i in range(0, len(msg_hex), 100)] # Blocks of 100 songs
    for request in request_chunks:
        artists_list = []
        track_list = []
        for char in request:
            artists_list.append(alphabet[char])
        track_list = get_artists_tracks(spotify, artists_list)
        add_playlist_tracks(spotify, username, playlist_name, track_list)

def decode(spotify, username, playlist_name, alphabet):
    """
    Decodes the message
    """
    hex_msg = []
    encoded_msg = get_playlist_tracks_artist(spotify, username, playlist_name)
    for artist in progressbar.progressbar(encoded_msg):
        for key,value in alphabet.items():
            if artist == value:
                hex_msg.append(key)
            else:
                continue
    decoded_msg = binascii.unhexlify(''.join(hex_msg)).decode("utf-8", errors="ignore")
    time.sleep(2)
    delete_playlist_tracks(spotify, username, playlist_name)
    return decoded_msg

if __name__ == "__main__":
    main()
