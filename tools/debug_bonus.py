import pandas as pd

# Test the dhondt function directly
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

# Test the minimum seat bonus logic exactly as in ERM.py
votes_df = pd.read_csv('votes_marche_2025_all_provinces.csv')
votes_df = votes_df.rename(columns=lambda x: x.strip())
if votes_df["votes"].dtype == 'object':
    votes_df["votes"] = votes_df["votes"].astype(str).str.replace(',', '').astype(float)

list_reg = votes_df.groupby(["list","coalition"], as_index=False)["votes"].sum()
coal = list_reg.groupby("coalition", as_index=False)["votes"].sum().rename(columns={"votes":"total_coal_votes"})
list_reg["votes"] = pd.to_numeric(list_reg["votes"], errors="coerce").fillna(0)
coal["total_coal_votes"] = pd.to_numeric(coal["total_coal_votes"], errors="coerce").fillna(0)

tot_coal = coal["total_coal_votes"].sum()
coal["coal_share"] = coal["total_coal_votes"] / tot_coal if tot_coal > 0 else 0
tot_list = list_reg["votes"].sum()
list_reg["list_share"] = list_reg["votes"] / tot_list if tot_list > 0 else 0

mx = list_reg.groupby("coalition")["list_share"].max().reset_index().rename(columns={"list_share":"max_list_share"})
coal = coal.merge(mx, on="coalition", how="left")

coal["admitted"] = (coal["coal_share"] >= 0.05) | (coal["max_list_share"] >= 0.03)
coal.loc[coal["total_coal_votes"] <= 0, "admitted"] = False

adm = coal[coal["admitted"]].copy()
print("Admitted coalitions:")
print(adm[["coalition", "total_coal_votes", "coal_share"]])

# D'Hondt allocation
total_list_seats = 30
base = dhondt(dict(zip(adm["coalition"], adm["total_coal_votes"])), total_list_seats)
coal_seats = pd.DataFrame({"coalition": list(base.keys()), "seats": list(base.values())})
print(f"\nInitial D'Hondt allocation:")
print(coal_seats)

# Check minimum seat bonus
pct19 = 0.43
pct18 = 0.40

if not coal_seats.empty:
    leader = adm.sort_values("total_coal_votes", ascending=False)["coalition"].iloc[0]
    lshare = float(adm.loc[adm["coalition"] == leader, "coal_share"].iloc[0])
    need = 19 if lshare >= pct19 else (18 if lshare >= pct18 else 0)
    got = int(coal_seats.loc[coal_seats["coalition"] == leader, "seats"].iloc[0])
    
    print(f"\nMinimum seat bonus check:")
    print(f"Leader: {leader}")
    print(f"Leader share: {lshare:.4f}")
    print(f"Needs minimum: {need} seats")
    print(f"Currently has: {got} seats")
    print(f"Bonus needed: {need > 0 and got < need}")
    
    if need > 0 and got < need:
        remaining = total_list_seats - need
        others = adm[adm["coalition"] != leader]
        
        print(f"\nApplying bonus:")
        print(f"Remaining seats after bonus: {remaining}")
        print(f"Other coalitions to allocate to:")
        print(others[["coalition", "total_coal_votes"]])
        
        other_votes = dict(zip(others["coalition"], others["total_coal_votes"]))
        print(f"Other votes dict: {other_votes}")
        
        other_counts = dhondt(other_votes, remaining)
        print(f"D'Hondt for others: {other_counts}")
        
        coal_seats = pd.concat([
            pd.DataFrame({"coalition": [leader], "seats": [need]}),
            pd.DataFrame({"coalition": list(other_counts.keys()), "seats": list(other_counts.values())})
        ], ignore_index=True)

print(f"\nFinal coalition seats:")
print(coal_seats)
