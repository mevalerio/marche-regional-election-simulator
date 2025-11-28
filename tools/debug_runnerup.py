import pandas as pd
from ERM import run_allocation

# Load data
votes_df = pd.read_csv("votes_marche_2025_all_provinces.csv")
seats_per_province_df = pd.read_csv("seats_per_province.csv")
params = pd.read_csv("params.csv")

total = int(params.loc[params["key"]=="TOTAL_LIST_SEATS","value"].iloc[0])
p19 = float(params.loc[params["key"]=="BONUS_TARGET_PCT_19","value"].iloc[0])
p18 = float(params.loc[params["key"]=="BONUS_TARGET_PCT_18","value"].iloc[0])

print("=== DEBUG: Runner-up seat removal ===")

final, coal_seats, grp_seats, removed = run_allocation(votes_df, seats_per_province_df, total, p19, p18)

print("Coalition seats:")
print(coal_seats)

print("\nRunner-up seat removed info:")
print(removed)

if removed:
    print(f"\nSeat removed from: Province={removed.get('province')}, List={removed.get('list')}")
    
    # Check allocation before and after removal for that province
    province = removed.get('province')
    if province:
        prov_seats = final[final['province'] == province]['final_seats'].sum()
        required_seats = seats_per_province_df[seats_per_province_df['province'] == province]['seats'].iloc[0]
        print(f"{province} after removal: {prov_seats}/{required_seats} seats")

print("\nFinal seat totals per province:")
for province in seats_per_province_df['province']:
    actual = final[final['province'] == province]['final_seats'].sum()
    required = seats_per_province_df[seats_per_province_df['province'] == province]['seats'].iloc[0]
    print(f"{province}: {actual}/{required}")

print(f"\nTotal seats allocated: {final['final_seats'].sum()}")
