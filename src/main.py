from functions import functions as func
import prefect
from prefect import task, Flow


def get_results(snippet, duration, order):
    results = func.yt_finder(snippet, duration=duration, order=order)

    try:
        for item in results:
            func.query_postgres(
                f"""insert into workout.dl_yt_workout_finder
                                    (video_id, video_title, channel_id, channel_title, duration, order_category, snippet)
                                    values
                                    ('{item['video_id']}', '{item['video_title']}', '{item['channel_id']}', '{item['channel_title']}', '{duration}', '{order}', '{snippet}');"""
            )
    except Exception as e:
        print(e)
        pass


@task
def get_new_videos():
    for snippet in [
        "Home Workout",
        "home workout for women",
        "home workout for men",
        "beginner workout at home",
        "home workout with dumbbells",
        "workout at home no jumping",
        "workout at home belly fat",
        "home workout chest",
        "home workout abs",
        "home workout arms",
        "home workout back",
        "home workout cardio",
    ]:
        for duration in ["long", "medium", "short"]:
            for order in ["relevance", "rating", "date"]:
                get_results(snippet, duration=duration, order=order)

    func.query_postgres("refresh materialized view workout.view_yt_workout_finder;")


flow = Flow("get_new_videos_flow", tasks=[get_new_videos])

flow.register(project_name="WhoNeedsGyms")
