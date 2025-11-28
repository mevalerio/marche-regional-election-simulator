import pandas as pd
from ERM import run_allocation

# Load data
votes_df = pd.read_csv("votes_marche_2025_all_provinces.csv")
seats_per_province_df = pd.read_csv("seats_per_province.csv")
params = pd.read_csv("params.csv")

# Get parameters
total = int(params.loc[params["key"]=="TOTAL_LIST_SEATS","value"].iloc[0])
p19 = float(params.loc[params["key"]=="BONUS_TARGET_PCT_19","value"].iloc[0])
p18 = float(params.loc[params["key"]=="BONUS_TARGET_PCT_18","value"].iloc[0])

print("=== DEBUG: Allocation Analysis ===")
print(f"Total list seats: {total}")
print(f"Bonus target pct 19: {p19}")
print(f"Bonus target pct 18: {p18}")

# Run allocation
final, coal_seats, grp_seats, removed = run_allocation(votes_df, seats_per_province_df, total, p19, p18)

print("\n=== REQUIRED vs ACTUAL SEATS ===")
required = seats_per_province_df.set_index('province')['seats'].to_dict()
actual = final.groupby('province')['final_seats'].sum().to_dict()

for province in required:
    req = required[province]
    act = actual.get(province, 0)
    status = "✓" if req == act else "✗"
    print(f"{province}: Required={req}, Actual={act} {status}")

print(f"\nTotal required: {sum(required.values())}")
print(f"Total actual: {sum(actual.values())}")

# Focus on Fermo
print("\n=== FERMO DETAILED ANALYSIS ===")
fermo_data = final[final['province'] == 'Fermo'].copy()
if not fermo_data.empty:
    print("Fermo allocation:")
    for _, row in fermo_data.iterrows():
        print(f"  {row['list']}: {row['final_seats']} seats")
    print(f"Total Fermo seats: {fermo_data['final_seats'].sum()}")
else:
    print("No Fermo data found!")

# Check if all provinces have the right total
print("\n=== ALLOCATION VERIFICATION ===")
all_correct = True
for province in required:
    if actual.get(province, 0) != required[province]:
        all_correct = False
        print(f"ERROR: {province} has {actual.get(province, 0)} seats but should have {required[province]}")

if all_correct:
    print("✓ All provinces have correct seat allocation!")
else:
    print("✗ Some provinces have incorrect seat allocation!")
