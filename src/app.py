from functions import functions as func

import random
import streamlit as st
from streamlit_player import st_player

# Get latest video data from DB
df = func.df_from_postgres('select * from workout.dl_yt_workout_finder;')

# Streamlit Setup
st.title('WhoNeedsGyms?')

# Button for skipping
line = 0
if st.button('Next!'):
    line = random.randint(1,10)

# Sidebar Filters
dur_choice = df['duration'].values[0]
foc_choice = df['snippet'].values[0]
ord_choice = df['order_category'].values[0]

dur = df['duration'].loc[df['order_category'] == ord_choice].loc[df['snippet'] == foc_choice].drop_duplicates().reset_index(drop=True)
dur_choice = st.sidebar.selectbox('Duration:', dur)

foc = df['snippet'].loc[df['duration'] == dur_choice].loc[df['order_category'] == ord_choice].drop_duplicates().reset_index(drop=True)
foc_choice = st.sidebar.selectbox('Focus:', foc)

ord = df['order_category'].loc[df['duration'] == dur_choice].loc[df['snippet'] == foc_choice].drop_duplicates().reset_index(drop=True)
ord_choice = st.sidebar.selectbox('Order:', ord) 

# Select Video
df = df.loc[df['duration'] == dur_choice].loc[df['snippet'] == foc_choice].loc[df['order_category'] == ord_choice].reset_index(drop=True)

url = df['video_id'].values[line]
title = df['video_title'].values[line]
channel = df['channel_title'].values[line]

# Embed a youtube video
st.video(f'https://youtu.be/{url}')
st.write(f'## {title}')
st.write(f'by {channel}')


