from functions import functions as func


def get_results(snippet, duration, order):
    results = func.yt_finder(snippet, duration=duration, order=order)
    
    try:
        for item in results:
            func.query_postgres(f'''insert into workout.dl_yt_workout_finder
                                    (video_id, video_title, channel_id, channel_title, duration, order_category, snippet)
                                    values
                                    ('{item['video_id']}', '{item['video_title']}', '{item['channel_id']}', '{item['channel_title']}', '{duration}', '{order}', '{snippet}');''')
    except Exception as e:
        print(e)
        pass


if __name__ == '__main__':
    get_results('Home Workout', duration='any', order='relevance')
