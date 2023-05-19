import streamlit as st
from nba_api.stats.static import players
from nba_api.stats.endpoints import shotchartdetail
from nba_api.stats.static import teams
import matplotlib.pyplot as plt

# Define the web app title
st.title("NBA Shooting Hot Zones")

# Fetch the list of NBA players
nba_players = players.get_players()

# Create a selectbox to choose a player from the list
player_name = st.selectbox("Select a player:", [player['full_name'] for player in nba_players])

# Get the player's ID
player_id = [player['id'] for player in nba_players if player['full_name'] == player_name][0]

# Fetch the player's basic info
player_info = players.find_player_by_id(player_id)
print(player_info)
# Display the player's basic info
st.header("Player Information")
st.subheader("Name: " + player_info['full_name'])
st.subheader("Team: " + player_info['Team'])
st.subheader("Height: " + str(player_info['height_feet']) + " ft " + str(player_info['height_inches']) + " in")
st.subheader("Weight: " + str(player_info['weight_pounds']) + " lbs")

# Fetch the player's shot chart data
shot_chart = shotchartdetail.ShotChartDetail(player_id=player_id, team_id=0, context_measure_simple='FGA')

# Execute the API request
shot_chart_data = shot_chart.get_data_frames()[0]

# Create a figure and axis for the shot chart
fig, ax = plt.subplots()

# Plot the shot chart data
ax.scatter(shot_chart_data['LOC_X'], shot_chart_data['LOC_Y'], color='blue', alpha=0.6)

# Customize the plot
ax.set_xlim(-250, 250)
ax.set_ylim(0, 500)

# Set the aspect ratio to 1:1
ax.set_aspect(1)

# Set the plot title and axis labels
ax.set_title("Shooting Hot Zones")
ax.set_xlabel("X (feet)")
ax.set_ylabel("Y (feet)")

# Display the plot in the Streamlit web app
st.pyplot(fig)