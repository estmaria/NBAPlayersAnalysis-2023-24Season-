import pandas as pd
import seaborn as sns
import matplotlib.pyplot as plt
import plotly.express as px
import plotly.io as pio

pio.renderers.default = 'browser'

df = pd.read_csv("NBA_2024_per_game(03-01-2024).csv")
df = df[df["G"] >= 10]
df = df.rename(columns={
    "Tm": "Team",
    "TRB": "REB"
})

df["TotalPoints"] = df["PTS"] * df["G"]
df["Efficiency"] = (df["PTS"] + df["REB"] + df["AST"] - df["TOV"]) / df["G"]
df["AST/TOV"] = df["AST"]/df["TOV"]

top_10_scorers = df.sort_values("TotalPoints", ascending=False).head(10)
print("Top10 Scorers")
print()
print(top_10_scorers[["Player", "Team", "G", "PTS", "TotalPoints"]])
print()

efficient_players = df.sort_values("Efficiency", ascending=False).head(10)
print("Top10 Most Efficient Players")
print()
print(efficient_players[["Player", "Team", "PTS", "AST", "REB", "TOV", "Efficiency"]])
print()

summary_by_position = df.groupby("Pos")[["PTS", "AST", "REB", "TOV", "Efficiency"]].mean().round(1)
print ("Stats by Position")
print()
print(summary_by_position)

top_scorers = df.sort_values("PTS", ascending=False).head(10)
sns.barplot(x="PTS", y="Player", data=top_scorers)
plt.title("Top 10 Scorers (Points per Game)")
plt.show()

position_scoring = df.groupby("Pos")["PTS"].mean().sort_values(ascending=False)
sns.barplot(x=position_scoring.index, y=position_scoring.values)
plt.title("Average Points Per Game by Position")
plt.xlabel("Position")
plt.ylabel("Points Per Game")
plt.show()


fig = px.scatter(df, x="MP", y="PTS", size="REB", color="Team",
                 hover_name="Player", title="Minutes vs Points with Rebounds")
fig.show()



