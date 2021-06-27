/*
MATERIALIZED VIEW used as source in apps.py
 */

create materialized view workout.view_yt_workout_finder
as

select * from(
select video_id
   	, video_title
	, channel_id
	, channel_title
	, duration
	, case when order_category = 'relevance' then 'Default'
		   when order_category = 'rating' then 'Best Ratings'
		   when order_category = 'date' then 'Newest' end as order_category
	, case when snippet = 'Home Workout' then 'Balanced Body'
		   when snippet = 'home workout for women' then 'For Women'
		   when snippet = 'home workout for men' then 'For Men'
		   when snippet = 'beginner workout at home' then 'For Beginners'
		   when snippet = 'home workout with dumbbells' then 'With Dumbbells'
		   when snippet = 'workout at home no jumping' then 'No Jumping/ Apartment Friendly'
		   when snippet = 'workout at home belly fat' then 'Belly Fat'
		   when snippet = 'home workout chest' then 'Chest'
		   when snippet = 'home workout abs' then 'ABS'
		   when snippet = 'home workout arms' then 'Arms'
		   when snippet = 'home workout back' then 'Back'
		   when snippet = 'home workout cardio' then 'Cardio' end as snippet
	, row_number() over(partition by duration, order_category, snippet order by inserted_at desc) as rownum
from workout.dl_yt_workout_finder) as main
where main.rownum <= 5
order by rownum desc;