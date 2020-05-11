# SpotiHide

##### Steganography tool to hide messages in public playlists of Spotify

## Installation

```bash
pip install spotipy pyfiglet colorama progressbar2
```
## Quick Start

To get started, install SpotiHide and create an app on https://developers.spotify.com/. Configure your new USERNAME, SPOTIPY_CLIENT_ID, SPOTIPY_CLIENT_SECRET and SPOTIPY_REDIRECT_URI. Set up the MESSAGE_PLAYLIST where the message will be encoded and decoded and the alphabet in the ALPHABET_PLAYLIST, composed of at least 16 songs with the first 16 different artists:

```bash
USERNAME = USERNAME
MESSAGE_PLAYLIST = MESSAGE_PLAYLIST
ALPHABET_PLAYLIST = ALPHABET_PLAYLIST
SCOPE = 'playlist-modify-public'
SPOTIPY_CLIENT_ID = SPOTIPY_CLIENT_ID
SPOTIPY_CLIENT_SECRET = SPOTIPY_CLIENT_SECRET
SPOTIPY_REDIRECT_URI = SPOTIPY_REDIRECT_URI
```
## Usage

```bash
python3 SpotiHide.py
[*] Alphabet Username [Default: USERNAME]:
[*] Alphabet Playlist [Default: APT_ALPHABET]:
[*] Enter a message:
[*] Encoding Cool Stuff \O/ \O/ \O/ \O/ [? Bytes]
[Successfully Encoded]
[*] Decoding Cool Stuff /O\ /O\ /O\ /O\
[Successfully Decoded] [MESSAGE]
```
