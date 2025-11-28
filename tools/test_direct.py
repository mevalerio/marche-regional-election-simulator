from ERM import coalitions_stage
import pandas as pd

# Test exactly what happens in ERM.py main execution
votes_df = pd.read_csv("votes_marche_2025_all_provinces.csv")
votes_df.columns = votes_df.columns.str.strip()

# Handle comma-separated numbers in votes column BEFORE numeric conversion
if "votes" in votes_df.columns and votes_df["votes"].dtype == 'object':
    votes_df["votes"] = votes_df["votes"].astype(str).str.replace(',', '').astype(float)

# Ensure votes column is numeric
if "votes" in votes_df.columns:
    votes_df["votes"] = pd.to_numeric(votes_df["votes"], errors="coerce").fillna(0)

print("Testing coalitions_stage directly...")

coal, seats = coalitions_stage(votes_df, 30, 0.43, 0.40)

print("Coalitions:")
print(coal[["coalition", "admitted", "coal_share", "max_list_share"]])

print("\nCoalition seats:")
print(seats)
