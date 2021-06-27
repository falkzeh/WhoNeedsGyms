from secrets import secrets as sec

import requests
import json


test_snippet = 'ALL Jail Themes - Persona 5 Scramble / Strikers OST'

def yt_finder(snippet=None):
    """Executes YouTube search for specific text snippet and returns results.

    Args:
        snippet (str): Text snippet to look for on YouTube

    Returns:
        results (list): Video id, video title, channel id and channel title of results
    """

    req = requests.get(f'https://www.googleapis.com/youtube/v3/search?part=snippet&q={snippet.replace(' ', '%20')}&key={sec.yt_api_key}')
    json = req.json()

    results = []

    for video in json['items']:
        if video['id']['kind'] == 'youtube#video':
            video_id = video['id']['videoId']
            video_title = video['snippet']['title']
            channel_id = video['snippet']['channelId']
            channel_title = video['snippet']['channelTitle']

            data = {"video_id": video_id, "video_title": video_title, "channel_id": channel_id, "channel_title": channel_title}
            results.append(data)
        
        else:
            pass
    
    return results
