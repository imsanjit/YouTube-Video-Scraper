!pip install google-api-python-client

#Importing required libraries
from apiclient.discovery import build
import pandas as pd
import json
import csv
from google.colab import files

# taking input from user for youtube api key and youtube channel id

api_key = input('Enter your youtube API Key here: \n')  # Add your "youtube api v3"api key here
channel_id = input('\nEnter your youtube chanel ID here: \n')

# Get upload playlist id

yt = build('youtube', 'v3', developerKey= api_key)
req = yt.channels().list(id= channel_id, part= 'contentDetails').execute()

def get_channel_videos(channel_id):
    # get Uploads playlist id
    res = yt.channels().list(id=channel_id, 
                                  part='contentDetails').execute()
    playlist_id = res['items'][0]['contentDetails']['relatedPlaylists']['uploads']
    
    videos = []
    next_page_token = None
    
    while 1:
        res = yt.playlistItems().list(playlistId=playlist_id, 
                                           part='snippet', 
                                           maxResults=50,
                                           pageToken=next_page_token).execute()
        videos += res['items']
        next_page_token = res.get('nextPageToken')
        
        if next_page_token is None:
            break
    
    return videos

# scraping videos from youtube upload playlist

videos = get_channel_videos(channel_id)
print(f'\nTotal number of video are: {len(videos)}')

# get all video from youtube channel in json file

all_Yt_Details = []

for i, video in enumerate(videos):
    ytDetails = {
        "ID" : i+1,
        "Video_ID" : video['snippet']['resourceId']['videoId'],
        "URL" : f"https://www.youtube.com/watch?v={video['snippet']['resourceId']['videoId']}",
        "Title" : video['snippet']['title'],
        "Published Date": video['snippet']['publishedAt'].split("T")[0]

    }
    all_Yt_Details.append(ytDetails)

with open('youtube_data.json', 'w') as f:
    json.dump(all_Yt_Details, f, indent=4)
files.download("youtube_data.json")

## get all video from youtube channel in excel file

data = pd.read_json('/content/youtube_data.json')
data.to_csv('youtube_data.csv', index= False)
files.download("youtube_data.csv")

print('\n\nFile Downloaded')
