from functions.secrets import secrets as sec

import requests
import json
import sys
import psycopg2
import logging
import pandas as pd

logging.basicConfig(level=logging.DEBUG, format='%(asctime)s - %(message)s', datefmt='%d-%b-%y %H:%M:%S')

def query_postgres(query=None):
    """Query the configured Postgres database. Connection Credentials set in secrets/secrets.py.

    Args:
        query (str): Query that will be executed on Postgres
    """

    try:
        con = psycopg2.connect(database=sec.db_name, user=sec.db_user, password=sec.db_password, host=sec.db_host, port=sec.db_port)
        cur = con.cursor()
        cur.execute(f'''{query}''')
        con.commit()
    
    except Exception as e:
        logging.error(f'{e}')

    finally:
        con.close()

def df_from_postgres(query=None):
    """Query the configured Postgres database and return a Pandas DataFrame.

    Args:
        query (str): Query that will be executed on Postgres
    
    Returns:
        df (DataFrame): Query Result in Pandas DataFrame
    """

    try:
        engine = psycopg2.connect(database=sec.db_name, user=sec.db_user, password=sec.db_password, host=sec.db_host, port=sec.db_port)
        df = pd.read_sql_query(query, con=engine)
        return df
    
    except Exception as e:
        logging.error(f'{e}')

    finally:
        engine.close()

def yt_finder(snippet=None, duration='any', order='relevance'):
    """Executes YouTube search for specific text snippet and returns results.
       https://developers.google.com/youtube/v3/docs/search/list

    Args:
        snippet (str): Text snippet to look for on YouTube
        duration (str): Duration of the video [any/long/medium/short]
        order (str): Search result order [rating/date/relevance/title/videoCount/viewCount]

    Returns:
        results (list): Video id, video title, channel id and channel title of results
    """

    req = requests.get(f'''https://www.googleapis.com/youtube/v3/search?part=snippet&q={snippet.replace(' ', '%20')}&key={sec.yt_api_key}&maxResults=5&type=video&videoDuration={duration}&order={order}''')
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
