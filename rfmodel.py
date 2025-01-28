from typing import Dict, Text
import pandas as pd
from sklearn.model_selection import train_test_split
from sklearn.linear_model import LogisticRegression
from sklearn.ensemble import RandomForestClassifier
from sklearn.metrics import accuracy_score, top_k_accuracy_score


mastery_train = pd.read_csv(
    "data.csv",
    names = ["user_id", "champion_id", "mastery_points"])

df = pd.DataFrame(mastery_train)
df["Rank"] = df.groupby("user_id").cumcount() + 1

reshaped_df = df.pivot(index="user_id", columns="Rank", values="champion_id").reset_index()

# Rename columns for clarity
reshaped_df.columns = ["PlayerID", "Champion1", "Champion2", "Champion3", "Champion4", "Champion5"]
reshaped_df = reshaped_df.dropna()
print(reshaped_df)


X = reshaped_df[["Champion1", "Champion2", "Champion3", "Champion4"]]
y = reshaped_df["Champion5"]

# Split into Train/Test
X_train, X_test, y_train, y_test = train_test_split(X, y, test_size=0.25, random_state=42)

model = RandomForestClassifier(n_estimators=100, random_state=42)
model.fit(X_train, y_train)

y_pred = model.predict(X_test)


accuracy = accuracy_score(y_test, y_pred)
print(f"Accuracy: {accuracy:.2f}")

top_k_accuracy = top_k_accuracy_score(y_test, model.predict_proba(X_test), k=5)
print(f"Top-5 Accuracy: {top_k_accuracy:.2f}")