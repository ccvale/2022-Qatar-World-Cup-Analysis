import streamlit as st
import pandas as pd
import numpy as np
import matplotlib.pyplot as plt
import seaborn as sns
import plotly.express as px

st.title('World Cup Matches')

@st.cache_data
def load_data(df_path: str):
    data = pd.read_csv(df_path)
    return data

def get_opponents(teamA):
    # create a list of all the teams that have played against the home team
    opponents = matches[(matches['team1'] == teamA) | (matches['team2'] == teamA)]
    opponents = opponents[(opponents['team1'] != teamA) | (opponents['team2'] != teamA)]
    opponents = opponents['team1'].append(opponents['team2'])
    opponents = opponents.unique()
    return opponents

data_load_state = st.text('Loading data...')
countries = load_data('gui/final_countries.csv')
matches = load_data('gui/final_matches.csv')
data_load_state.text('Data loaded!')

if st.checkbox('Show Groups'):
    groupID = st.select_slider('Select a Group', options=['A', 'B', 'C', 'D', 'E', 'F', 'G', 'H'])
    filtered_countries = countries[countries['GroupID'] == groupID][['Nation', 'Rank']]
    st.subheader(f'Countries in Group {groupID}')
    st.write(filtered_countries)

st.write('---')

st.write('## Generate Match Statistics')
# create a dropdown menu of all the countries
teamA = st.selectbox('Select country', countries['Nation'].unique())
# create a dropdown menu of all the countries that have played against the home team

teamB = st.selectbox('Select opponent they\'ve played against', get_opponents(teamA)[1:])

match = matches[((matches['team1'] == teamA) & (matches['team2'] == teamB)) | ((matches['team1'] == teamB) & (matches['team2'] == teamA))]
st.write(match)
stat = st.selectbox('Select statistic to visualize', options=['Possession', 'Goals', 'Assists', 'Shots', 'Total Passes'])
st.subheader(f'Visualizing {stat} - {teamA} vs {teamB} ({match["category"].values[0]})')
if stat == 'Possession':
    fig = px.pie(match, values=[match['possession team1'].values[0], match['possession team2'].values[0]], names=[match['team1'].values[0], match['team2'].values[0]])
    st.plotly_chart(fig, use_container_width=True)
elif stat == 'Goals':
    # plotly express chart of goals scored by each team
    fig = px.bar(match, x=[match['team1'].values[0], match['team2'].values[0]], y=[match['number of goals team1'].values[0], match['number of goals team2'].values[0]], color=[match['team1'].values[0], match['team2'].values[0]])
    st.plotly_chart(fig, use_container_width=True)
elif stat == 'Assists':
    st.write('adsfasd')
elif stat == 'Shots':
    st.write('adsfasd')
elif stat == 'Total Passes':
    st.write('adsfasd')
