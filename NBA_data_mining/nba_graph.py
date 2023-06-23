import streamlit as st
from nba_api.stats.static import players
from nba_api.stats.endpoints import playercareerstats
from nba_api.stats.endpoints import shotchartdetail
import matplotlib.pyplot as plt
from matplotlib.patches import Circle, Rectangle, Arc

# Define the web app title
st.title("NBA Shooting Hot Zones")

# Fetch the list of NBA players
nba_players = players.get_active_players()

# Create a selectbox to choose a player from the list
player_name = st.selectbox("Select a player:", [player['full_name'] for player in nba_players])

# Get the player's ID
player_id = [player['id'] for player in nba_players if player['full_name'] == player_name][0]

# Get the player's career stats
career = playercareerstats.PlayerCareerStats(player_id=player_id)
career_stats = career.get_data_frames()[0]
team_id = career_stats.tail(1)['TEAM_ID'].item()

season_id = st.selectbox("Select season:", [season for season in career_stats['SEASON_ID']])


# Get the player's physical profile
# player_index = playerindex.PlayerIndex(league_id='00', season='2022-23', is_only_current_season=1) 
# player_profile = player_index.get_data_frames()[0]

# Fetch the player's basic info
player_info = players.find_player_by_id(player_id)

# Display the player's basic info
st.header("Player Information")
st.subheader("Name: " + player_info['full_name'])
st.subheader("Team: " + career_stats.tail(1)['TEAM_ABBREVIATION'].item())
# st.subheader("Height: " + str(player_profile.tail(1)['']) + " ft " + str(player_info['height_inches']) + " in")
# st.subheader("Weight: " + str(player_info['weight_pounds']) + " lbs")

# Fetch the player's shot chart data
shot_chart = shotchartdetail.ShotChartDetail(player_id=player_id, team_id=0, context_measure_simple='FGA')

# Execute the API request
shot_chart_data = shot_chart.get_data_frames()[0]

# 調整底圖大小
plt.rcParams['figure.figsize'] = (12, 11)
# Create a figure and axis for the shot chart
fig, ax = plt.subplots()
# 底圖顏色
ax.set_facecolor("black")

# Customize the plot
ax.set_xlim(-250, 250)
ax.set_ylim(500, -47.5)

# 繪製球場的基礎元素
lw = 2
color = 'orange'

##################################
# 繪製球場
##################################

# Create the basketball hoop
hoop = Circle((0, 0), radius=7.5, linewidth=lw, color=color, fill=False)

# Create center line
c_line = Rectangle((-250, 422.5), 672.5, 0, linewidth=lw, color=color, fill=False)

# Create backboard
backboard = Rectangle((-30, -12.5), 60, 0, linewidth=lw, color=color)

# The paint
# Create the outer box 0f the paint, width=16ft, height=19ft
outer_box = Rectangle((-80, -47.5), 160, 190, linewidth=lw, color=color, 
                        fill=False)
# Create the inner box of the paint, widt=12ft, height=19ft
inner_box = Rectangle((-60, -47.5), 120, 190, linewidth=lw, color=color,
                        fill=False)

# Create free throw top arc
top_free_throw = Arc((0, 142.5), 120, 120, theta1=0, theta2=180,
                        linewidth=lw, color=color, fill=False)
# Create free throw bottom arc
bottom_free_throw = Arc((0, 142.5), 120, 120, theta1=180, theta2=0,
                        linewidth=lw, color=color, linestyle='dashed')
# Restricted Zone, it is an arc with 4ft radius from center of the hoop
restricted = Arc((0, 0), 80, 80, theta1=0, theta2=180, linewidth=lw,
                    color=color)

# Three point line
# Create the right side 3pt lines, it's 14ft long before it arcs
corner_three_a = Rectangle((-220, -47.5), 0, 140, linewidth=lw,
                            color=color)
# Create the right side 3pt lines, it's 14ft long before it arcs
corner_three_b = Rectangle((220, -47.5), 0, 140, linewidth=lw, color=color)
# 3pt arc - center of arc will be the hoop, arc is 23'9" away from hoop
three_arc = Arc((0, 0), 475, 475, theta1=22, theta2=158, linewidth=lw,
                color=color)

# Center Court
center_outer_arc = Arc((0, 422.5), 120, 120, theta1=180, theta2=-180,
                        linewidth=lw, color=color)
center_inner_arc = Arc((0, 422.5), 40, 40, theta1=180, theta2=-180,
                        linewidth=lw, color=color)

# List of the court elements to be plotted onto the axes
court_elements = [c_line, hoop, backboard, outer_box, inner_box, top_free_throw,
                    bottom_free_throw, restricted, corner_three_a,
                    corner_three_b, three_arc, center_outer_arc,
                    center_inner_arc]

# Add the court elements onto the axes
for element in court_elements:
    ax.add_patch(element)


shotchartlist = shotchartdetail.ShotChartDetail(team_id=int(team_id), 
                                                player_id=player_id, 
                                                season_type_all_star='Regular Season', 
                                                season_nullable=season_id,
                                                context_measure_simple="FGA").get_data_frames()

data = shotchartlist[0]

x_missed = data[data['EVENT_TYPE'] == 'Missed Shot']['LOC_X']
y_missed = data[data['EVENT_TYPE'] == 'Missed Shot']['LOC_Y']

x_made = data[data['EVENT_TYPE'] == 'Made Shot']['LOC_X']
y_made = data[data['EVENT_TYPE'] == 'Made Shot']['LOC_Y']


ax.scatter(x_missed, y_missed, c='r', marker="x", s=300, linewidths=3)
ax.scatter(x_made, y_made, facecolors='none', edgecolors='g', marker="o", s=100, linewidths=3)


# Set the plot title and axis labels
ax.set_title("Shooting Hot Zones")
ax.set_xlabel("X (feet)")
ax.set_ylabel("Y (feet)")

# Display the plot in the Streamlit web app
st.pyplot(fig)