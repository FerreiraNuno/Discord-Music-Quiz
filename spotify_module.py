import sys
import spotipy
import spotipy.util as util
import re


scope = 'user-library-read'

if len(sys.argv) > 1:
    username = sys.argv[1]
else:
    print("Usage: %s username" % (sys.argv[0],))

token = util.prompt_for_user_token("1176209110", scope)

# playlists:
# Gambi: spotify:playlist:4QL4O51hvS4GpdDQdliDne
# 90's: spotify:playlist:37i9dQZF1DXbTxeAdrVG2l
# 00's: spotify:playlist:37i9dQZF1DX4o1oenSJRJd
# 10's: spotify:playlist:37i9dQZF1DX5Ejj0EkURtP


def song_list(input, type):
    if type == "word":
        sp = spotipy.Spotify(auth=token)
        available_playlists = {"90s": "spotify:playlist:37i9dQZF1DXbTxeAdrVG2l",
                               "00s": "spotify:playlist:37i9dQZF1DX4o1oenSJRJd",
                               "10s": "spotify:playlist:37i9dQZF1DX5Ejj0EkURtP"}
        if isinstance(input, str):
            playlists = [sp.playlist_tracks(available_playlists.get(input))]
        elif isinstance(input, list):
            inputs = []
            for item in input:
                inputs.append(sp.playlist_tracks(available_playlists.get(item)))
            playlists = inputs

    if type == "link":
        sp = spotipy.Spotify(auth=token)
        if isinstance(input, str):
            playlists = [sp.playlist_tracks(input)]
        elif isinstance(input, list):
            inputs = []
            for item in input:
                inputs.append(sp.playlist_tracks(item))
            playlists = inputs

    songs = []
    for playlist in playlists:
        for item in playlist['items']:
            track = item['track']
            a = (track['name'] + ' - ' + track['artists'][0]['name'])
            b = re.sub(r'\([^)]*\)', '', a).replace('- Radio Edit ', '').replace('[Short Radio Edit] ', '')\
                .replace('Club Mix ', '').replace('', '')\
                .replace('feat. ', '').replace('Extended ', '').replace('- Instrumental Version ', '')\
                .replace('Radio Mix ', '').replace('Short Edit ', '').replace('Gabry Ponte Ice Pop Radio - ', '')\
                .replace('Ryan Riback Remix - ', '').replace('Spider-Man: Into the Spider-Verse - ', '')\
                .replace('[Lana Del Rey vs. Cedric Gervais] - Cedric Gervais Remix ', '')\
                .replace('Radio Mix ', '')
            if b.count("' - '") > 1:
                b = b.replace(' - ', '')
            songs.append(b)
    return songs

