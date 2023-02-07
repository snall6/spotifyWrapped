import spotipy
from spotipy.oauth2 import SpotifyOAuth
import pandas as pd
import gspread
#give client access to personal spotify account
CID = 'CID'
SECRET = 'SECRET'
SCOPE = "user-top-read"
URI='http://127.0.0.1:9090'

#give google sheets + gspread access to program --> service account
gc = gspread.service_account(filename='/Users/sailajanallacheruvu/Desktop/spotifyMoodRing/spotify-wrapped-372500-7b30c15ddb3e.json')
#use spotipy to access information from local account
sp = spotipy.Spotify(auth_manager=SpotifyOAuth(client_id=CID, client_secret=SECRET, redirect_uri=URI, scope=SCOPE))
songs = sp.current_user_top_tracks(50, 0, "long_term")
#get song ids and relevant features for 50 of user's topmost tracks
#id, name, album, artist
def get_track_ids(time_frame):
    track_ids = []
    for song in time_frame['items']:
        track_ids.append(song['id'])
    return track_ids
def get_track_features(id):
    meta = sp.track(id)
    name = meta['name']
    album = meta['album']['name']
    artist = meta['album']['artists'][0]['name']
    #spotify_url = meta['external_urls']['spotify']
    #album_cover = meta['album']['images'][0]['url']
    track_info = [name, album, artist]#, spotify_url, album_cover]
    return track_info

ids = get_track_ids(songs)

#sheet = gc.create("spotifywrapped")
#sheet.share('sailaseshu27@gmail.com', perm_type='user', role='writer')

def insert_to_gsheet(track_ids):
#create 2d array containing important info of features of
#user's 50 topmost tracks
    result = []
    for id in ids:
        all_features = get_track_features(id)
        all_features.append(id)
        result.append(all_features)
    #print(result)
    #create a pandas dataframe representing information accumulated above
    df_songs_info = pd.DataFrame(result, columns=['name', 'album', 'artist', 'id'])
    #print(df_songs_info)

    #open sheet we are using to save information to
    sheet = gc.create("spotifywrapped")
    #save to relevant worksheet
    worksheet = sheet.worksheet(f'{time}')
    worksheet.update([df_songs_info.columns.values.tolist()] + df_songs_info.values.tolist())
    print('Updated')


#save top tracks info to sheet representing each user
time_ranges = ['short_term', 'medium_term', 'long_term']
for time in time_ranges:
    top_tracks = sp.current_user_top_tracks(50, 0, time)
    track_ids = get_track_ids(top_tracks)
    insert_to_gsheet(track_ids)
