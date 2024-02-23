import spotipy
from spotipy.oauth2 import SpotifyClientCredentials

client_id = '<client_id here>'
client_secret = '<client_secret here>'

client_credentials_manager = SpotifyClientCredentials(client_id=client_id, client_secret=client_secret)
sp = spotipy.Spotify(client_credentials_manager=client_credentials_manager)

playlist_id = '<enter playlist id>'

file = open('songs.txt', 'w')

j = 0
while(True):
    try:
        results = sp.playlist_tracks(playlist_id, offset=100*j)

        if results and 'items' in results:
            for i, track in enumerate(results['items']):
                try:
                    track_name = track['track']['name']
                    artists = [artist['name'] for artist in track['track']['artists']]
                    track_link = track['track']['external_urls']['spotify']
                except:
                    continue

                print(f"{i+(j*100)}. Track: {track_name} - Artists: {', '.join(artists)} - Link: {track_link}")
                final = ''
                for artist in artists:
                    final += artist
                    final += ' '
                file.write(f'{track_name} {final}\n')
            if(i!=99):
                break

        else:
            print("No tracks found in the playlist.")
    except Exception as e:
        print(f"Error: {e}")
    j+=1
