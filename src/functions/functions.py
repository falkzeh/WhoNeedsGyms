from secrets import secrets as sec

import requests
import json
import sys
import psycopg2
import logging

logging.basicConfig(level=logging.debug, format='%(asctime)s - %(message)s', datefmt='%d-%b-%y %H:%M:%S')

def query_postgres(query):
    """Query the configured Postgres database. Connection Credentials set in secrets/secrets.py.

    Args:
        query (str): Query that will be executed on Postgres
    """

    try:
        con = psycopg2.connect(database=sec.db_database, user=sec.db_user, password=sec.db_password, host=sec.db_host, port=sec.db_port)
        cur = con.cursor()
        cur.execute(f'''{query}''')
        con.commit()
    
    except Exception as e:
        logging.error(f'{e}')
        sys.exit()

    finally:
        con.close()

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
