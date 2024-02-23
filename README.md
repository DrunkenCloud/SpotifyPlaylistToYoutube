# A Spotify to Youtube Playlist Converter

Ok so, welcome to this repo. If your here I assume you want to convert your Spotify playlist to a Youtube music one cause honestly, spotify is just not worth it anymore for the price of premium（＞人＜；）


Well I shall now explain and show my code on how I did it. Also before I begin I wish you use do this on a Linux OS or WSL since its better there but it works on windows as well. Just you might want to delete some of the print statements I included in the code to see my progress on the songs.

I made 2 python programs for 2 seperate purposes, one to get all the song names and artists from my spotify playlist and write them together, line by line, onto a songs.txt file. Then I use this list and use my second program to find the videos and add them to my musics playlist on youtube using google's YouTube Data V3 api.

# Gettin Songs from Spotify

First go to your terminal and install the Spotipy module for python, command is:

>  pip install spotipy

Then go to the [Spotify's Developer website](https://developer.spotify.com/dashboard) to get your api. Create a New App after you log in. The name and other parameters dont really matter and you can put whatever you want.

After creating you app, go the settings part of your app and get your **Client ID** and **Client Secret**. These 2 will be used in the GetSongs.py file on lines 4 and 5:

```
client_id = '<client_id here>'
client_secret = '<client_secret here>'
```

Now, to get your spotify playlist id. Go to your playlist, left click, copy link to playlist. It will look like this:

> https://open.spotify.com/playlist/3Fl6uhbGrSkCXik6WKrc2J?si=026a2ec3e5ac4acb

The playlist id for this is `3Fl6uhbGrSkCXik6WKrc2J` which is located on the URL right after playlist/ and before the '?'. This should be updated on the GetSongs.py file at line 10:

`playlist_id = '<enter playlist id>'`

Now onto the main part of the code. First we autheticate and connect to our api

```
client_credentials_manager = SpotifyClientCredentials(client_id=client_id, client_secret=client_secret)
sp = spotipy.Spotify(client_credentials_manager=client_credentials_manager)
```

Also we are rate limited to only 100 songs per request on a regular api. So we have to improvise using the offset parameter for requesting on Spotify's api. 

I included print statements to track the goings but if your on windows I would suggest removing them as windows/vscode doesnt print characters out of UTF-8 unless said explicitely, which is a problem if your song titles has Japanese, Chinese, or any language other than English.

Feel free to look through the rest of the shitty code I made lol. That should be all and you can run it.

# Adding the Songs to the Youtube Playlist

Again, first thing to do is install the required modules.

> pip install google-auth-oauthlib google-auth google-auth-httplib2 google-api-python-client youtube-search

As for why im using youtube-search instead of just using the google api to do the searching, I will explain it later in this section.

Now, you can head over to [Google Cloud](https://console.cloud.google.com/) to get make your youtube API. First connect to your google account, creating a new project is optional or you can use the default project.

Then search for Youtube Data API V3 and enable it. Navigate to the API and you will see something similar to this: 

![image](https://hackmd.io/_uploads/S1gYRzU26.png)


First order of business, to configure the API. Head over to the OAuth Consent Screen and start the process. The first choice for it must be External, next few dont matter, but for the scope, please do select all of them, or else the api wont work. 

As for why all of them, im lazy to find the ones that are actually needed. Also remember to add a google account as a test user, this will be the account you will be Authenticating to the api with.

After which go to the Credentials tab and create a new Credential, make sure its for Desktop and download the client_secret.json it and move it to the same directory as AddPlaylist.py. We will use this file as shown in the file at line 10-13:

```
flow = google_auth_oauthlib.flow.InstalledAppFlow.from_client_secrets_file(
    "client_secrets.json", scopes,
    redirect_uri='urn:ietf:wg:oauth:2.0:oob'
)
```


Now head to your youtube and get or make a playlist in which you want to add your songs. This is a typical playlist link:

> https://www.youtube.com/playlist?list=PL5P5SkYF_H6A2lxhFG_gzGuoCHjy4U-2Q

The playlist id is the last part after '?list=', which is PL5P5SkYF_H6A2lxhFG_gzGuoCHjy4U-2Q in this case. Replace this id with the code on line 18:

```
playlist_id = '<Playlist_id>'
```

Now onto why my code looks so shit here and why we used a txt file to store the songs. The youtube is built such that it takes around 1-3 seconds to look up and add a video to a playlist, while you can get 100s of songs within a few songs on spotify's API. So I used a txt file since I didnt want to refresh the Spotify token every few minutes.

There is also the quota limit on google's youtube api. The documentation says there is 10000 quota per day on the youtube api BUT dont take it literally. There is something called quota cost and differs on which type of request your doing. You can learn more [here](https://developers.google.com/youtube/v3/getting-started), but essentually, different requests cost differently as shown [here](https://developers.google.com/youtube/v3/determine_quota_cost). 

The cost of doing a search is 100 which is wayyy too much and hence I used the youtube-search module to get the links and hence video IDs of youtube videos and feed that into a program that adds the video to the playlist, which costs 50 and hence lets us adds songs to our playlist with a lower cost.

If you read up until now, then it means you understand that the code I made can essentually add 200 songs to your playlist per day as cost of each song is 50 and daily limit is 10000.

I also made a done.txt just so that I can see if I missed any songs which I can add later one. On the same note, if you want to extend the 200 songs per day limit, just make more api's using different google accounts and make sure switch the client_secrets.json file if you do so. (P.S This is what I did)

That is all, you should be able to run the AddPlaylist.py file and if you face any problems please do contact me.