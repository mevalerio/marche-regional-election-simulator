def dhondt(votes, seats):
    """D'Hondt divisor method"""
    if not votes or sum(votes.values()) == 0:
        return {k: 0 for k in votes.keys()}
    allocations = {party: 0 for party in votes}
    for i in range(seats):
        quotients = {party: votes[party] / (allocations[party] + 1) for party in votes}
        winner = max(quotients, key=quotients.get)
        allocations[winner] += 1
    return allocations

# Test D'Hondt with single coalition and 11 seats
single_coalition = {'Centrosinistra': 285427.0}
result = dhondt(single_coalition, 11)
print(f"D'Hondt with single coalition: {result}")

# Test D'Hondt with zero seats
result_zero = dhondt(single_coalition, 0)
print(f"D'Hondt with zero seats: {result_zero}")

# Test what happens when remaining = 11
remaining = 30 - 19
print(f"Remaining seats: {remaining}")

# Test creating the DataFrame like in the bonus logic
import pandas as pd

leader = "Centrodestra"
need = 19
other_counts = {'Centrosinistra': 11}

print("Creating DataFrame...")
df1 = pd.DataFrame({"coalition": [leader], "seats": [need]})
print("Leader DataFrame:")
print(df1)

df2 = pd.DataFrame({"coalition": list(other_counts.keys()), "seats": list(other_counts.values())})
print("Others DataFrame:")
print(df2)

final_df = pd.concat([df1, df2], ignore_index=True)
print("Combined DataFrame:")
print(final_df)
