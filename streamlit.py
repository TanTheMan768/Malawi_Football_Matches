# Imports
import streamlit as st
import pandas as pd
import plotly.express as px

# Streamlit config
st.set_page_config(page_title="Malawi National Football Team")

# Data Manipulation
df = pd.read_csv("Dataset_malawi_national_football_team_matches.csv")

""" Clean date column """
df['Date'] = pd.to_datetime(df['Date'], format='mixed')
df['Year'] = df['Date'].dt.year

""" Get basic Win/Loss data"""
total_matches = len(df)
wins = len(df[df['Result'] == 'Win'])
losses = len(df[df['Result'] == 'Loss'])
draws = len(df[df['Result'] == 'Draw'])
total_win_rate = wins / total_matches * 100
home_win_rate = len(df[(df['Result'] == 'Win') & (df['Venue'] == 'Home')]) / len(df[df['Venue'] == 'Home']) * 100
away_win_rate = len(df[(df['Result'] == 'Win') & (df['Venue'] == 'Away')]) / len(df[df['Venue'] == 'Away']) * 100

""" Get point delta statistics """
df['ScoreDelta'] = df['Team Score'] - df['Opponent Score']
score_delta_avg = df['ScoreDelta'].mean()

""" Count the number of each result type per year """
result_counts = df[(df['Year'] > 2005) & (df['Result'] != 'TBD')].groupby(['Year', 'Result']).size().reset_index(name='WLcount')

fig = px.bar(
    result_counts,
    x='Year',
    y='WLcount',
    color='Result',
    title="Malawi National Football Team Win Rate Over Time",
    subtitle="Filtered to show only matches after 2005 and excludes matches with a result of 'TBD'",
    labels={'WLcount': 'Number of Matches', 'Year': 'Year'},
    barmode='group'
)

# Display
st.header("Malawi National Football Team")
st.write(df)

st.subheader("Dataset Overview")
st.write(f"Total Matches: {total_matches}")
st.write(f"Number of Wins: {wins}")
st.write(f"Number of Losses: {losses}")
st.write(f"Number of Draws: {draws}")
st.write(f"Total Win Rate: {total_win_rate:.2f}%")
st.write(f"Home Win Rate: {home_win_rate:.2f}%")
st.write(f"Away Win Rate: {away_win_rate:.2f}%")
st.write(f"Average Score Delta: {score_delta_avg:.2f}")

st.subheader("Win Rate Over Time")
st.write(fig)