import pandas as pd

results = pd.read_csv('provincial_results.csv')
fermo = results[results['province'] == 'Fermo']

# Check Fratelli d'Italia which has 1 int_seat
fd = fermo[fermo['list'] == 'Fratelli d\'Italia'].iloc[0]
print('Fratelli d\'Italia:')
print('  votes:', fd['votes'])
print('  int_seats:', fd['int_seats']) 
print('  rest:', fd['rest'])
if fd['int_seats'] > 0:
    implied_quota = (fd['votes'] - fd['rest']) / fd['int_seats']
    print('  Implied quota:', implied_quota)

# Check Partito Democratico
pd_row = fermo[fermo['list'] == 'Partito Democratico'].iloc[0]
print('\nPartito Democratico:')
print('  votes:', pd_row['votes'])
print('  int_seats:', pd_row['int_seats'])
print('  rest:', pd_row['rest'])
if pd_row['int_seats'] > 0:
    implied_quota = (pd_row['votes'] - pd_row['rest']) / pd_row['int_seats']
    print('  Implied quota:', implied_quota)

# Calculate what the quota should be
total_fermo_votes = fermo['votes'].sum()
seats = 4
expected_quota = total_fermo_votes // (seats + 1)
print(f'\nExpected quota: {expected_quota} = {total_fermo_votes} / ({seats} + 1)')
