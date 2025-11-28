import pandas as pd

# Load data
votes_df = pd.read_csv("votes_marche_2025_all_provinces.csv")
seats_per_province_df = pd.read_csv("seats_per_province.csv") 
results_df = pd.read_csv("provincial_results.csv")
group_seats_df = pd.read_csv("group_seats.csv")

# Clean data
votes_df = votes_df.rename(columns=lambda x: x.strip())
if votes_df["votes"].dtype == 'object':
    votes_df["votes"] = votes_df["votes"].astype(str).str.replace(',', '').astype(float)

# Focus on Fermo
fermo_votes = votes_df[votes_df["province"] == "Fermo"]
fermo_results = results_df[results_df["province"] == "Fermo"]
fermo_seats = seats_per_province_df[seats_per_province_df["province"] == "Fermo"]["seats"].iloc[0]

print("=== FERMO ANALYSIS ===")
print(f"Fermo should have {fermo_seats} seats")

# Calculate the quota
total_fermo_votes = fermo_votes["votes"].sum()
quota = total_fermo_votes // (fermo_seats + 1)
print(f"Total Fermo votes: {total_fermo_votes}")
print(f"Quota: {quota} = {total_fermo_votes} / ({fermo_seats} + 1)")

# Check integer seats calculation
print("\n=== INTEGER SEATS ===")
admitted_coalitions = ["Centrodestra", "Centrosinistra"]
fermo_admitted = fermo_votes[fermo_votes["coalition"].isin(admitted_coalitions)]

for coalition in admitted_coalitions:
    coalition_votes = fermo_admitted[fermo_admitted["coalition"] == coalition]
    for _, row in coalition_votes.iterrows():
        int_seats = row["votes"] // quota
        rest = row["votes"] - int_seats * quota
        rest_pct = (rest / quota) * 100 if quota > 0 else 0
        print(f"{row['list']}: {row['votes']} votes, {int_seats} int_seats, rest {rest} ({rest_pct:.2f}%)")

print(f"\nInteger seats total: {(fermo_admitted['votes'] // quota).sum()}")

# Check what the results show
print("\n=== ACTUAL RESULTS ===")
for _, row in fermo_results.iterrows():
    print(f"{row['list']}: {row['votes']} votes, {row['int_seats']} int → {row['final_seats']} final, rest_pct {row['rest_pct']:.2f}%, rank {row['regional_rest_rank']}")

print(f"\nTotal final seats: {fermo_results['final_seats'].sum()}")

# Check group caps
print("\n=== GROUP CAPS ===")
for _, row in group_seats_df.iterrows():
    if row["list"] in fermo_results["list"].values:
        fermo_final = fermo_results[fermo_results["list"] == row["list"]]["final_seats"].iloc[0]
        print(f"{row['list']}: regional cap = {row['group_seats']}, Fermo allocation = {fermo_final}")
