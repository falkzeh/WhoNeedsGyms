from functions import functions as func

import random
import streamlit as st
from streamlit_player import st_player

# Get latest video data from DB
df = func.df_from_postgres(
    "select * from workout.view_yt_workout_finder where rownum <= 10 order by rownum desc, snippet desc, order_category, duration limit 3000;"
)


# Streamlit Setup
st.set_page_config(
    page_title="WhoNeedsGyms?",
    page_icon="🏅",
    layout="centered",
    initial_sidebar_state="expanded",
)

# Sidebar Filters
st.sidebar.title("WhoNeedsGyms?")
st.sidebar.write(
    """
This is a little hobby project by [me](https://github.com/falkzeh). It was built using the YouTube API and Streamlit framework.
The data is being updated daily - so you'll see new videos every day!\n
Have fun and push your limits! 💪"""
)

dur_choice = df["duration"].values[0]
foc_choice = df["snippet"].values[0]
ord_choice = df["order_category"].values[0]

foc = (
    df["snippet"]
    .loc[df["duration"] == dur_choice]
    .loc[df["order_category"] == ord_choice]
    .drop_duplicates()
    .reset_index(drop=True)
)

st.sidebar.write("## How would you like to workout today?")
foc_choice = st.sidebar.selectbox("Focus:", foc)

dur = (
    df["duration"]
    .loc[df["order_category"] == ord_choice]
    .loc[df["snippet"] == foc_choice]
    .drop_duplicates()
    .reset_index(drop=True)
)
dur_choice = st.sidebar.radio("Duration:", dur)

ord = (
    df["order_category"]
    .loc[df["duration"] == dur_choice]
    .loc[df["snippet"] == foc_choice]
    .drop_duplicates()
    .reset_index(drop=True)
)
ord_choice = st.sidebar.radio("Order:", ord)

# Select Video
df = (
    df.loc[df["duration"] == dur_choice]
    .loc[df["snippet"] == foc_choice]
    .loc[df["order_category"] == ord_choice]
    .reset_index(drop=True)
)

# Button for skipping
line = 0
if st.button("Shuffle!"):
    line = random.randint(0, len(df) - 1)

url = df["video_id"].values[line]
title = df["video_title"].values[line]
channel = df["channel_title"].values[line]

# Embed a youtube video
st.video(f"https://youtu.be/{url}")
st.write(f"## {title}")
st.write(f"by {channel}")
