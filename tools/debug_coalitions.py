import pandas as pd

# Load data
votes = pd.read_csv('votes_marche_2025_all_provinces.csv')
votes = votes.rename(columns=lambda x: x.strip())

# Ensure votes column is numeric
if votes["votes"].dtype == 'object':
    votes["votes"] = votes["votes"].astype(str).str.replace(',', '').astype(float)

# Calculate coalition totals
coal_votes = votes.groupby('coalition')['votes'].sum().sort_values(ascending=False)
total_votes = coal_votes.sum()

print("=== COALITION VOTE ANALYSIS ===")
print(f"Total votes: {total_votes}")
print("\nCoalition totals:")
for coalition, votes_count in coal_votes.items():
    pct = 100 * votes_count / total_votes
    print(f"  {coalition}: {votes_count} votes ({pct:.2f}%)")

# Calculate max list per coalition
print("\n=== MAX LIST PER COALITION ===")
list_totals = votes.groupby(['coalition', 'list'])['votes'].sum().reset_index()
for coalition in coal_votes.index:
    coalition_lists = list_totals[list_totals['coalition'] == coalition]
    if not coalition_lists.empty:
        max_list = coalition_lists.loc[coalition_lists['votes'].idxmax()]
        max_pct = 100 * max_list['votes'] / total_votes
        print(f"  {coalition}: max list '{max_list['list']}' with {max_list['votes']} votes ({max_pct:.2f}%)")

# Apply thresholds
print("\n=== THRESHOLD ANALYSIS ===")
for coalition, votes_count in coal_votes.items():
    coal_pct = 100 * votes_count / total_votes
    coalition_lists = list_totals[list_totals['coalition'] == coalition]
    max_list_votes = coalition_lists['votes'].max() if not coalition_lists.empty else 0
    max_list_pct = 100 * max_list_votes / total_votes
    
    # Apply thresholds: 5% coalition OR 3% single list
    coal_threshold = coal_pct >= 5.0
    list_threshold = max_list_pct >= 3.0
    admitted = coal_threshold or list_threshold
    
    print(f"  {coalition}:")
    print(f"    Coalition {coal_pct:.2f}% >= 5.0%? {coal_threshold}")
    print(f"    Max list {max_list_pct:.2f}% >= 3.0%? {list_threshold}")
    print(f"    ADMITTED: {admitted}")
