import streamlit as st
import pandas as pd
import numpy as np
import plotly.express as px

st.title('World Cup Matches')

@st.cache_data # cache data so it doesn't have to be reloaded every time
def load_data(df_path: str):
    data = pd.read_csv(df_path)
    return data

def get_opponents(teamA):
    # get all opponents that teamA has played against, so we have access to only real matches that were played
    opponents = matches[(matches['team1'] == teamA) | (matches['team2'] == teamA)]
    opponents = opponents[(opponents['team1'] != teamA) | (opponents['team2'] != teamA)]
    opponents = opponents['team1'].append(opponents['team2'])
    opponents = opponents.unique()
    opponents = np.delete(opponents, np.where(opponents == teamA))
    return opponents

data_load_state = st.text('Loading data...')
countries = load_data('gui/final_countries.csv')
matches = load_data('gui/final_matches.csv')
data_load_state.text('') # data is loaded and cached

if st.checkbox('Show Groups'):
    groupID = st.select_slider('Select a Group', options=['A', 'B', 'C', 'D', 'E', 'F', 'G', 'H'])
    filtered_countries = countries[countries['GroupID'] == groupID][['Nation', 'Rank']]
    st.subheader(f'Countries in Group {groupID}')
    st.write(filtered_countries)

st.write('---')

st.write('## Generate Match Statistics')

teamA = st.selectbox('Select country', countries['Nation'].unique())
teamB = st.selectbox('Select opponent they\'ve played against', get_opponents(teamA))

match = matches[((matches['team1'] == teamA) & (matches['team2'] == teamB)) | ((matches['team1'] == teamB) & (matches['team2'] == teamA))]
st.write(match) # will be removed later; just for testing

stat = st.selectbox('Select statistic to visualize', options=['Possession', 'Goals', 'Assists', 'Shots Attempted', 'Total Passes', 'Fouls Committed', 'Forced Turnovers', 'Goal Preventions'])
st.subheader(f'Visualizing {stat} - {teamA} vs {teamB} ({match["category"].values[0]})')

# different graphs; different stats? more customization?
if stat == 'Possession':
    fig = px.pie(match, values=[match['possession team1'].values[0], match['possession team2'].values[0]], names=[match['team1'].values[0], match['team2'].values[0]])
    st.plotly_chart(fig, use_container_width=True)
elif stat == 'Goals':
    fig = px.bar(match, x=[match['team1'].values[0], match['team2'].values[0]], y=[match['number of goals team1'].values[0], match['number of goals team2'].values[0]], color=[match['team1'].values[0], match['team2'].values[0]])
    fig.update_layout(xaxis_title='Team', yaxis_title='Goals Scored')
    st.plotly_chart(fig, use_container_width=True)
elif stat == 'Assists':
    fig = px.bar(match, x=[match['team1'].values[0], match['team2'].values[0]], y=[match['assists team1'].values[0], match['assists team2'].values[0]], color=[match['team1'].values[0], match['team2'].values[0]])
    fig.update_layout(xaxis_title='Team', yaxis_title='Goals Assisted')
    st.plotly_chart(fig, use_container_width=True)
elif stat == 'Shots Attempted':
    fig = px.bar(match, x=[match['team1'].values[0], match['team2'].values[0]], y=[match['total attempts team1'].values[0], match['total attempts team2'].values[0]], color=[match['team1'].values[0], match['team2'].values[0]])
    fig.update_layout(xaxis_title='Team', yaxis_title='Shots Attempted')
    st.plotly_chart(fig, use_container_width=True)
elif stat == 'Total Passes':
    fig = px.bar(match, x=[match['team1'].values[0], match['team2'].values[0]], y=[match['passes completed team1'].values[0], match['passes completed team2'].values[0]], color=[match['team1'].values[0], match['team2'].values[0]])
    fig.update_layout(xaxis_title='Team', yaxis_title='Total Passes')
    st.plotly_chart(fig, use_container_width=True)
elif stat == 'Fouls Committed':
    fig = px.bar(match, x=[match['team1'].values[0], match['team2'].values[0]], y=[match['fouls against team1'].values[0], match['fouls against team2'].values[0]], color=[match['team1'].values[0], match['team2'].values[0]])
    fig.update_layout(xaxis_title='Team', yaxis_title='Fouls Committed')  
    st.plotly_chart(fig, use_container_width=True)
elif stat == 'Forced Turnovers':
    fig = px.bar(match, x=[match['team1'].values[0], match['team2'].values[0]], y=[match['forced turnovers team1'].values[0], match['forced turnovers team2'].values[0]], color=[match['team1'].values[0], match['team2'].values[0]])
    fig.update_layout(xaxis_title='Team', yaxis_title='Forced Turnovers')
    st.plotly_chart(fig, use_container_width=True)
elif stat == 'Goal Preventions':
    fig = px.bar(match, x=[match['team1'].values[0], match['team2'].values[0]], y=[match['goal preventions team1'].values[0], match['goal preventions team2'].values[0]], color=[match['team1'].values[0], match['team2'].values[0]])
    fig.update_layout(xaxis_title='Team', yaxis_title='Goal Preventions')
    st.plotly_chart(fig, use_container_width=True)