from nba_api.stats.endpoints import leaguegamefinder
from nba_api.stats.endpoints import leaguegamelog
import streamlit as st
from datetime import date, timedelta,datetime       
import pandas as pd
import numpy as np
from helpers.parser import parse_data

@st.cache_data
def get_upcoming_games():
    # Call parse_data() only once and cache its result
    return parse_data()

upcoming_games_df = get_upcoming_games()

today = date.today()
week_later = today + timedelta(days=7)

# Create a list of all dates from today to a week later
dates = [today + timedelta(days=i) for i in range(7)]
dates.insert(0,"Choose a date below")

st.title('NBA odds predictor')

date_chosen = st.selectbox(
    "Date of upcoming games",
    dates,
)


if date_chosen != "Choose a date below":
    col1 , col2 = st.columns([1,1])

    date_format ='%Y-%m-%d'
    this_date_df = upcoming_games_df[upcoming_games_df["Date"] == datetime.strftime(date_chosen, date_format)]
    game_idx = 0


    rows = len(upcoming_games_df.index)
    with col1:
        st.write(this_date_df)
    with col2:
        game_idx = st.number_input("Enter Game id",0,rows-1)


    st.write("You have selected " + upcoming_games_df.loc[game_idx, "Home Team"] + " vs " + upcoming_games_df.loc[game_idx, 'Away Team'])
    

#todo write rest of dropdown boxes
#use api to get winrate, some random graphs etcetc