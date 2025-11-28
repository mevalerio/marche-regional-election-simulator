import pandas as pd
from ERM import run_allocation

# Load data
votes_df = pd.read_csv("votes_marche_2025_all_provinces.csv")
seats_per_province_df = pd.read_csv("seats_per_province.csv")
params = pd.read_csv("params.csv")

total = int(params.loc[params["key"]=="TOTAL_LIST_SEATS","value"].iloc[0])
p19 = float(params.loc[params["key"]=="BONUS_TARGET_PCT_19","value"].iloc[0])
p18 = float(params.loc[params["key"]=="BONUS_TARGET_PCT_18","value"].iloc[0])

final, coal_seats, grp_seats, removed = run_allocation(votes_df, seats_per_province_df, total, p19, p18)

print("Columns in final DataFrame:")
print(final.columns.tolist())
print("\nFirst few rows:")
print(final.head())
print(f"\nDataFrame shape: {final.shape}")
print(f"Total final_seats: {final['final_seats'].sum()}")
