import pandas as pd
from ERM import provincial_integers, assign_residuals, group_seats_stage, coalitions_stage

# Load data
votes_df = pd.read_csv("votes_marche_2025_all_provinces.csv")
votes_df = votes_df.rename(columns=lambda x: x.strip())
if "votes" in votes_df.columns and votes_df["votes"].dtype == 'object':
    votes_df["votes"] = votes_df["votes"].astype(str).str.replace(',', '').astype(float)
for col in ["votes"]:
    if col in votes_df.columns:
        votes_df[col] = pd.to_numeric(votes_df[col], errors="coerce").fillna(0)

seats_per_province_df = pd.read_csv("seats_per_province.csv")
params = pd.read_csv("params.csv")

total = int(params.loc[params["key"]=="TOTAL_LIST_SEATS","value"].iloc[0])
p19 = float(params.loc[params["key"]=="BONUS_TARGET_PCT_19","value"].iloc[0])
p18 = float(params.loc[params["key"]=="BONUS_TARGET_PCT_18","value"].iloc[0])

# Get coalition and group seats
coal_votes, coal_seats = coalitions_stage(votes_df, total, p19, p18)
admitted = coal_votes[coal_votes["admitted"]]["coalition"].tolist()
print("Admitted coalitions:", admitted)

grp_seats = group_seats_stage(votes_df[votes_df["coalition"].isin(admitted)], coal_seats)
print("\nGroup seats:")
print(grp_seats)

# Get provincial integers
stepC, prov_meta = provincial_integers(votes_df[votes_df["coalition"].isin(admitted)], seats_per_province_df, admitted)
print("\nProvincial integers (stepC):")
print(stepC[['province', 'list', 'votes', 'int_seats', 'rest_pct']].head(20))

print("\nProvince metadata:")
print(prov_meta)

# Check total integer seats assigned
total_int_seats = stepC['int_seats'].sum()
print(f"\nTotal integer seats assigned: {total_int_seats}")
print(f"Should be less than or equal to: {total}")

# Check seats assigned per province after integers
int_seats_per_prov = stepC.groupby('province')['int_seats'].sum()
print("\nInteger seats per province:")
for province, seats in int_seats_per_prov.items():
    required = seats_per_province_df[seats_per_province_df['province'] == province]['seats'].iloc[0]
    print(f"{province}: {seats}/{required}")

# Now run assign_residuals
alloc, order = assign_residuals(stepC, prov_meta, grp_seats)
print("\nAfter residual assignment:")
final_seats_per_prov = alloc.groupby('province')['final_seats'].sum()
for province, seats in final_seats_per_prov.items():
    required = seats_per_province_df[seats_per_province_df['province'] == province]['seats'].iloc[0]
    print(f"{province}: {seats}/{required}")

print(f"\nTotal final seats: {alloc['final_seats'].sum()}")
print(f"Residual order length: {len(order)}")

# Check remaining capacity
remaining_seats = 30 - alloc['final_seats'].sum()
print(f"Remaining seats to allocate: {remaining_seats}")
