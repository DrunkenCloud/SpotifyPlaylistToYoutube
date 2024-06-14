import google_auth_oauthlib.flow
import googleapiclient.discovery
from youtube_search import YoutubeSearch


scopes = ["https://www.googleapis.com/auth/youtube.force-ssl"]
api_service_name = "youtube"
api_version = "v3"

flow = google_auth_oauthlib.flow.InstalledAppFlow.from_client_secrets_file(
    "client_secrets.json", scopes,
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

def read_and_delete_lines(file_path, num_lines=200):
    lines = []
    with open(file_path, 'r') as file:
        for i in range(num_lines):
            line = file.readline()
            if not line:
                num_lines = i
                break
            lines.append(line)
    
    with open(file_path, 'r') as file:
        data = file.readlines()
    
    with open(file_path, 'w') as file:
        file.writelines(data[num_lines:])
    
    return lines

if __name__ == "__main__":
    lines = read_and_delete_lines("./songs.txt")
    done = []
    invalid = []
    with open("done.txt", "r") as f:
        done = f.readlines()

    done_file_handler = open("done.txt", "a")

    for line in lines:
        if (line in done):
            print(f"{line} is already done!\n")
            continue
        done.append(line)
        print("Doing: ", line.rstrip().lstrip())
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
            print("Video added to the playlist successfully!\n")
            done_file_handler.write(line)
        except googleapiclient.errors.HttpError as e:
            print(f"An error occurred: {e}\n\n")
            continue
    
    done_file_handler.close()

    for i in invalid:
        print("Could not find video for: ", invalid)
