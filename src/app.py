from functions import functions as func

import streamlit as st


df = func.df_from_postgres('select * from workout.dl_yt_workout_finder limit 5;')
print(df)