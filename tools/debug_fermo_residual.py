import pandas as pd
from math import floor

# Load current results
final_results = pd.read_csv('provincial_results.csv')
group_caps = pd.read_csv('group_seats.csv')
seats_per_province = pd.read_csv('seats_per_province.csv')

print("=== FERMO RESIDUAL ALLOCATION DEBUG ===")

# Focus on Fermo
fermo_results = final_results[final_results['province'] == 'Fermo'].copy()
fermo_seats = seats_per_province[seats_per_province['province'] == 'Fermo']['seats'].values[0]

print(f"Fermo should have {fermo_seats} seats")
print(f"Fermo currently has {fermo_results['final_seats'].sum()} seats allocated")

# Check capacity constraints
print("\n=== CAPACITY CONSTRAINTS ===")

# Provincial capacity
prov_left = fermo_seats - fermo_results['final_seats'].sum()
print(f"Provincial capacity remaining: {prov_left}")

# List capacity
caps = dict(zip(group_caps["list"], group_caps["group_seats"]))
current_allocations = final_results.groupby("list")["final_seats"].sum().to_dict()

print("\nList capacity analysis:")
for _, row in fermo_results.iterrows():
    list_name = row['list']
    current_total = current_allocations.get(list_name, 0)
    cap = caps.get(list_name, 0)
    remaining = cap - current_total
    print(f"  {list_name}: {current_total}/{cap} allocated, {remaining} remaining")

# Check residual candidates by rest_pct
print(f"\n=== RESIDUAL CANDIDATES (sorted by rest_pct) ===")
fermo_sorted = fermo_results.sort_values('rest_pct', ascending=False)
for _, row in fermo_sorted.iterrows():
    list_name = row['list']
    current_total = current_allocations.get(list_name, 0)
    cap = caps.get(list_name, 0)
    remaining = cap - current_total
    eligible = remaining > 0 and prov_left > 0
    print(f"  {list_name}: {row['rest_pct']:.2f}% rest, capacity {remaining}, eligible: {eligible}")
