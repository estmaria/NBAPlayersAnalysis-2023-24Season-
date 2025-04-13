import pandas as pd
from sklearn.linear_model import LinearRegression
from sklearn.model_selection import train_test_split
from sklearn.metrics import mean_squared_error

df_2024 = df = pd.read_csv("nba_2024_per_game(03-01-2024).csv")
df_2023 = pd.read_csv("nba_2022_2023.csv")

df_2023["Season"] = "2022-23"
df_2024["Season"] = "2023-24"

df_2023.columns = df_2023.columns.str.strip()
df_2024.columns = df_2024.columns.str.strip()

df_2023 = df_2023[["Player", "PTS", "AST", "TRB", "MP", "G", "FGA", "FG%", "3P%", "FT%"]].copy()
df_2023.rename(columns={"PTS": "Prev_PPG"}, inplace=True)

df_2024 = df_2024[["Player", "PTS", "AST", "TRB", "MP", "G", "FGA", "FG%", "3P%", "FT%"]].copy()
df_2024.loc[:, "Next_PPG"] = df_2024["PTS"]

# Merge the data
merged_df = pd.merge(df_2023, df_2024[["Player", "Next_PPG"]], on="Player")
merged_df.dropna(inplace=True)

# Define features for training
train_features = ["Prev_PPG", "AST", "TRB", "MP", "G", "FGA", "FG%", "3P%", "FT%"]
X = merged_df[train_features]
y = merged_df["Next_PPG"]

# Train/test split
X_train, X_test, y_train, y_test = train_test_split(X, y, test_size=0.2, random_state=42)

# Train model
model = LinearRegression()
model.fit(X_train, y_train)

# Evaluate
y_pred = model.predict(X_test)
mse = mean_squared_error(y_test, y_pred)
print("Mean Squared Error:", round(mse, 2))

df_2024_for_pred = df_2024.rename(columns={"PTS": "Prev_PPG"}).copy()

# Ensure columns match the trained features
# Drop rows with missing values in the prediction features
X_future = df_2024_for_pred[train_features].dropna()

# Also update df_2024 to match rows that survived (optional but useful)
df_2024_clean = df_2024.loc[X_future.index]

# Predict
df_2024_clean["Predicted_PPG_2025"] = model.predict(X_future)

# Show top predictions
print(df_2024_clean[["Player", "PTS", "Predicted_PPG_2025"]].sort_values(by="Predicted_PPG_2025", ascending=False).head(10))
