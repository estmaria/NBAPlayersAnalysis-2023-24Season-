import streamlit as st
import pandas as pd
import plotly.express as px

df = pd.read_csv("nba_2024_per_game(03-01-2024).csv")
st.title("🏀 NBA Player Performance Dashboard (2023-24 season)")
st.markdown("Explore player stats by team — compare points, assists, and more!")

selected_team = st.selectbox("Choose a Team", sorted(df["Tm"].unique()))

# Filter data
filtered = df[df["Tm"] == selected_team]

# Show top players
st.subheader(f"Top 5 Scorers - {selected_team}")
top_players = filtered.sort_values("PTS", ascending=False).head(5)
st.dataframe(top_players[["Player", "PTS", "AST", "TRB", "FG%", "3P%", "STL","BLK","TOV" ,"MP"]])

# Plot - Points vs Minutes
st.subheader("Points vs Minutes Played")
fig = px.scatter(
    filtered,
    x="MP",
    y="PTS",
    color="Player",
    size="AST",
    hover_name="Player",
    title=f"{selected_team} Players: Minutes vs Points",
    height=500
)
st.plotly_chart(fig, use_container_width=True)