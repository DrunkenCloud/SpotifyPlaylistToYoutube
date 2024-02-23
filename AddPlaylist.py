import google_auth_oauthlib.flow
import googleapiclient.discovery
from youtube_search import YoutubeSearch


scopes = ["https://www.googleapis.com/auth/youtube.force-ssl"]
api_service_name = "youtube"
api_version = "v3"

flow = google_auth_oauthlib.flow.InstalledAppFlow.from_client_secrets_file(
    "client_secret3.json", scopes,
    redirect_uri='urn:ietf:wg:oauth:2.0:oob'
)
credentials = flow.run_local_server(port=8080)

youtube = googleapiclient.discovery.build(api_service_name, api_version, credentials=credentials)

playlist_id = '<Playlist_id>'

def search_youtube(query, num_results=1):
    results = YoutubeSearch(query, max_results=num_results).to_dict()

    if not results:
        print("No results found.")
        return 'none'

    top_result = results[0]
    id = top_result['id']
    return id

i = 0
invalid = []
file = open('done.txt','r')
content = file.readlines()
file.close()
file = open('done.txt','a')
with open('songs.txt','r') as f:
    for line in f:
        if(line in content):
            print("Already Done\n")
            continue
        else:
            content.append(line)
            print(line.rstrip().lstrip())
            songid = search_youtube(line.rstrip().lstrip())
            if(songid == 'none'):
                invalid.append(line)
                continue
            try:
                request = youtube.playlistItems().insert(
                    part="snippet",
                    body={
                        "snippet": {
                            "playlistId": playlist_id,
                            "resourceId": {"kind": "youtube#video", "videoId": songid},
                        },
                    },
                )
                response = request.execute()
                print("Video added to the playlist successfully!")
                file.write(line)
            except googleapiclient.errors.HttpError as e:
                print(f"An error occurred: {e}")
                break

for i in invalid:
    print(i)