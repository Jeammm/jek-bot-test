import spotipy
import spotipy.oauth2 as oauth2
from spotipy.oauth2 import SpotifyOAuth
from spotipy.oauth2 import SpotifyClientCredentials

def get_name(link):
    start = link.find("track/") + 6
    finish = start + 22
    name = link[start:finish]

    auth_manager = SpotifyClientCredentials(client_id = '1189102c663748eb82d1dd97e9ceb348',
                                            client_secret = '2988e1513ce34f55a1d18473af6b60f9')

    sp = spotipy.Spotify(auth_manager=auth_manager)
    track_info = f"spotify:track:{name}"

    track = sp.track(track_info)

    return track["album"]["name"]

def get_episode(link):
    start = link.find("episode/") + 8
    finish = start + 22
    name = link[start:finish]
    auth_manager = SpotifyClientCredentials(client_id = '1189102c663748eb82d1dd97e9ceb348',
                                            client_secret = '2988e1513ce34f55a1d18473af6b60f9')

    sp = spotipy.Spotify(auth_manager=auth_manager)
    episode_info = f"spotify:episode:{name}?market=ES"

    episode_name = sp.episode(episode_info)

    return episode_name["name"]

def get_playlist(link):
    start = link.find("playlist/") + 9
    finish = start + 22
    name = link[start:finish]
    auth_manager = SpotifyClientCredentials(client_id = '1189102c663748eb82d1dd97e9ceb348',
                                            client_secret = '2988e1513ce34f55a1d18473af6b60f9')

    sp = spotipy.Spotify(auth_manager=auth_manager)
    playlist_info = f"spotify:playlist:{name}"
    playlist_list = sp.playlist(playlist_info)

    playlist_name = playlist_list["name"]
    tracks = []

    for song in playlist_list["tracks"]["items"]:
        tracks.append(f"{song['track']['name']} {song['track']['artists'][0]['name']}")

    return {"playlist_name" : playlist_name,
            "tracks" : tracks
            }
