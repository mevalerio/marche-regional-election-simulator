import pandas as pd
import numpy as np
from math import floor

votes_df = pd.read_csv('votes_marche_2025_all_provinces.csv')
votes_df = votes_df.rename(columns=lambda x: x.strip())

print("Total votes in dataset:", votes_df['votes'].sum())
print("\nCoalition totals:")
coal_totals = votes_df.groupby('coalition')['votes'].sum().sort_values(ascending=False)
total_votes = coal_totals.sum()
for coalition, votes in coal_totals.items():
    pct = 100 * votes / total_votes
    print(f"  {coalition}: {votes:,} votes ({pct:.2f}%)")

print("\nLargest lists per coalition:")
list_totals = votes_df.groupby(['coalition', 'list'])['votes'].sum().reset_index()
list_totals['list_pct'] = 100 * list_totals['votes'] / total_votes
for coalition in coal_totals.index:
    coalition_lists = list_totals[list_totals['coalition'] == coalition].sort_values('votes', ascending=False)
    max_list = coalition_lists.iloc[0] if not coalition_lists.empty else None
    if max_list is not None:
        print(f"  {coalition}: {max_list['list']} = {max_list.votes:,} votes ({max_list.list_pct:.2f}%)")

print("\nThreshold analysis:")
for coalition, votes in coal_totals.items():
    coal_pct = 100 * votes / total_votes
    coalition_lists = list_totals[list_totals['coalition'] == coalition]
    max_list_pct = coalition_lists['list_pct'].max() if not coalition_lists.empty else 0
    admitted = (coal_pct >= 5.0) or (max_list_pct >= 3.0)
    print(f"  {coalition}: Coalition {coal_pct:.2f}% >= 5.0? {coal_pct >= 5.0}, Max list {max_list_pct:.2f}% >= 3.0? {max_list_pct >= 3.0} => Admitted: {admitted}")
