import pandas as pd

df = pd.read_csv('votes_marche_2025_all_provinces.csv')
# Strip column names and handle comma-separated votes
df = df.rename(columns=lambda x: x.strip())
if df["votes"].dtype == 'object':
    df["votes"] = df["votes"].astype(str).str.replace(',', '').astype(float)

print('Coalitions:', df['coalition'].unique())
print('\nTotal votes by coalition:')
coal_votes = df.groupby('coalition')['votes'].sum().sort_values(ascending=False)
total = coal_votes.sum()
for coalition, votes in coal_votes.items():
    pct = 100 * votes / total
    print(f'{coalition}: {votes} votes ({pct:.2f}%)')

print('\nMax list per coalition:')
for coalition in coal_votes.index:
    coal_df = df[df['coalition'] == coalition]
    list_votes = coal_df.groupby('list')['votes'].sum()
    max_list = list_votes.max()
    max_list_name = list_votes.idxmax()
    max_pct = 100 * max_list / total
    print(f'{coalition}: {max_list_name} with {max_list} votes ({max_pct:.2f}%)')

print('\nThreshold check:')
for coalition, votes in coal_votes.items():
    coal_pct = 100 * votes / total
    coal_df = df[df['coalition'] == coalition]
    list_votes = coal_df.groupby('list')['votes'].sum()
    max_list_pct = 100 * list_votes.max() / total
    
    coal_ok = coal_pct >= 5.0
    list_ok = max_list_pct >= 3.0
    admitted = coal_ok or list_ok
    
    print(f'{coalition}: Coal {coal_pct:.2f}% >= 5? {coal_ok}, Max list {max_list_pct:.2f}% >= 3? {list_ok} => {admitted}')
