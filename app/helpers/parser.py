import requests
from bs4 import BeautifulSoup
from datetime import date, timedelta
import pandas as pd

def parse_data():
# Calculate the date range
    today = date.today()
    week_later = today + timedelta(days=7)

    # Create a list of all dates from today to a week later
    dates = [today + timedelta(days=i) for i in range(7)]

    # Initialize an empty list to store all games
    all_games = []

    # Loop through each date
    for single_date in dates:
        # Format the date as YYYY-MM-DD
        formatted_date = single_date.strftime('%Y-%m-%d')
        
        # Construct the URL with the current date
        url = f"https://www.nba.com/games?date={formatted_date}"
        
        # Send a GET request to the NBA website
        response = requests.get(url)
        if response.status_code != 200:
            print(f"Failed to fetch data for {formatted_date}")
            continue
        
        # Parse the HTML content
        soup = BeautifulSoup(response.content, "html.parser")
        
        # Find all matchups on the page
        matchups = soup.find_all("span", class_="MatchupCardTeamName_teamName__9YaBA")
        
        # Extract teams and pair them
        teams = [team.text.strip() for team in matchups]
        games = [{"Date": formatted_date, "Home Team": teams[i], "Away Team": teams[i + 1]} for i in range(0, len(teams), 2)]
        
        # Add the games to the master list
        all_games.extend(games)

    # Convert all games into a DataFrame for readability
    games_df = pd.DataFrame(all_games)

    # Print the collated DataFrame
    file_path = r"C:\Users\tanyu\projects\nba\nba_streamlit\app\data\nba_upcoming_games_week.csv"
    games_df.to_csv(file_path, index=False)
    return games_df


