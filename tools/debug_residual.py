#!/usr/bin/env python3
"""
Debug script to trace the residual seat allocation logic step by step.
Focus on why Fermo only gets 3 seats instead of 4.
"""

import pandas as pd
import numpy as np

def dhondt(values, seats):
    if seats <= 0 or sum(values.values()) <= 0:
        return {k:0 for k in values}
    qs=[]
    for k,v in values.items():
        for d in range(1,seats+1):
            qs.append((k, v/d))
    qs.sort(key=lambda x:x[1], reverse=True)
    win=[k[0] for k in qs[:seats]]
    return {k:win.count(k) for k in values}

def coalitions_stage(votes_df, total_list_seats, pct19, pct18):
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
    
    base = dhondt(dict(zip(adm["coalition"], adm["total_coal_votes"])), total_list_seats)
    coal_seats = pd.DataFrame({"coalition": list(base.keys()), "seats": list(base.values())})
    
    first = coal_seats["seats"].max()
    if first < 19:
        idx = coal_seats["seats"].idxmax()
        coal_seats.iloc[idx, 1] = 19
    
    return coal_seats, coal

def group_seats_stage(list_votes_df, coal_seats_df):
    list_by_coal = list_votes_df.groupby("coalition", as_index=False)["votes"].sum()
    out = []
    for _, row in coal_seats_df.iterrows():
        coal = row["coalition"]
        seats = row["seats"]
        lists = list_votes_df[list_votes_df["coalition"] == coal]
        if lists.empty:
            continue
        grp_seats = dhondt(dict(zip(lists["list"], lists["votes"])), seats)
        for lst, s in grp_seats.items():
            out.append({"coalition": coal, "list": lst, "seats": s})
    return pd.DataFrame(out)

def provincial_integers(province_df, quota):
    """Calculate integer seats for each list in a province based on quota."""
    print(f"\n=== Provincial integers calculation ===")
    print(f"Province: {province_df['province'].iloc[0] if not province_df.empty else 'UNKNOWN'}")
    print(f"Quota: {quota}")
    
    result = province_df.copy()
    result["int_seats"] = (result["votes"] // quota).astype(int)
    result["rest"] = result["votes"] - result["int_seats"] * quota
    
    # Calculate rest percentage
    result["rest_pct"] = (result["rest"] / quota * 100) if quota > 0 else 0
    
    for _, row in result.iterrows():
        print(f"  {row['list']}: {row['votes']} votes, {row['int_seats']} int seats, rest {row['rest']:.0f} ({row['rest_pct']:.2f}%)")
    
    return result

def assign_residuals(df, seats_per_province_df, group_seats_df):
    """Assign residual seats based on regional ranking of rest percentages."""
    print(f"\n=== Residual seat assignment ===")
    
    # Initialize final_seats with int_seats
    df["final_seats"] = df["int_seats"]
    
    # Calculate seats still needed per province
    prov_totals = df.groupby("province")["int_seats"].sum()
    prov_left = {}
    for prov in seats_per_province_df["province"]:
        target = seats_per_province_df[seats_per_province_df["province"] == prov]["seats"].iloc[0]
        allocated = prov_totals.get(prov, 0)
        prov_left[prov] = target - allocated
        print(f"Province {prov}: target {target}, allocated {allocated}, need {prov_left[prov]} more")
    
    # Calculate seats still available per list
    lst_totals = df.groupby("list")["int_seats"].sum()
    lst_left = {}
    for lst in group_seats_df["list"]:
        target = group_seats_df[group_seats_df["list"] == lst]["seats"].iloc[0]
        allocated = lst_totals.get(lst, 0)
        lst_left[lst] = target - allocated
        print(f"List {lst}: target {target}, allocated {allocated}, have {lst_left[lst]} more available")
    
    # Sort by rest_pct descending for residual allocation
    order = []
    iteration = 0
    
    while any(left > 0 for left in prov_left.values()):
        iteration += 1
        print(f"\n--- Iteration {iteration} ---")
        allocated_this_round = False
        
        # Get candidates sorted by rest_pct descending
        cand = df[["province", "list", "coalition", "votes", "rest_pct"]].sort_values("rest_pct", ascending=False)
        
        print("Top candidates by rest %:")
        for i, (_, r) in enumerate(cand.head(10).iterrows()):
            print(f"  {i+1}. {r['list']} in {r['province']}: {r['rest_pct']:.2f}% (prov need: {prov_left.get(r['province'], 0)}, list avail: {lst_left.get(r['list'], 0)})")
        
        for _, r in cand.iterrows():
            p, l = r["province"], r["list"]
            if prov_left.get(p, 0) > 0 and lst_left.get(l, 0) > 0:
                print(f"  ALLOCATING: {l} in {p} (rest: {r['rest_pct']:.2f}%)")
                i = df[(df["province"] == p) & (df["list"] == l)].index[0]
                df.at[i, "final_seats"] += 1
                prov_left[p] -= 1
                lst_left[l] -= 1
                order.append((p, l))
                allocated_this_round = True
                break  # Only allocate one seat per iteration
        
        if not allocated_this_round:
            print("  No allocation possible this round - breaking")
            break
    
    print(f"\nFinal province seat counts:")
    final_prov_totals = df.groupby("province")["final_seats"].sum()
    for prov in seats_per_province_df["province"]:
        target = seats_per_province_df[seats_per_province_df["province"] == prov]["seats"].iloc[0]
        actual = final_prov_totals.get(prov, 0)
        print(f"  {prov}: {actual}/{target} ({'OK' if actual == target else 'MISMATCH'})")
    
    return df, order

def main():
    # Load data
    votes_df = pd.read_csv("votes_marche_2025_all_provinces.csv")
    # Fix column names with spaces
    votes_df = votes_df.rename(columns=lambda x: x.strip())
    # Fix comma-separated votes
    if votes_df["votes"].dtype == 'object':
        votes_df["votes"] = votes_df["votes"].astype(str).str.replace(',', '').astype(float)
    seats_per_province_df = pd.read_csv("seats_per_province.csv")
    
    print("=== DEBUGGING RESIDUAL ALLOCATION ===")
    
    # Stage 1: Coalition admission and seat allocation
    coal_seats, coal_votes = coalitions_stage(votes_df, 30, 0.19, 0.18)
    print("\nCoalition seats:", coal_seats)
    
    # Stage 2: Group/list seat allocation
    list_votes = votes_df.groupby(["list", "coalition"], as_index=False)["votes"].sum()
    grp_seats = group_seats_stage(list_votes, coal_seats)
    print("\nGroup seats:")
    print(grp_seats)
    
    # Stage 3: Provincial allocation
    print("\n=== PROVINCIAL ALLOCATION ===")
    
    # Filter for admitted coalitions only
    admitted_coalitions = coal_votes[coal_votes["admitted"]]["coalition"].tolist()
    print(f"Admitted coalitions: {admitted_coalitions}")
    
    province_results = []
    for province in seats_per_province_df["province"]:
        print(f"\n--- Processing {province} ---")
        
        # Get votes for this province (only admitted coalitions)
        prov_votes = votes_df[
            (votes_df["province"] == province) & 
            (votes_df["coalition"].isin(admitted_coalitions))
        ]
        
        if prov_votes.empty:
            print(f"No admitted coalition votes in {province}")
            continue
        
        # Calculate quota for this province
        total_votes = prov_votes["votes"].sum()
        target_seats = seats_per_province_df[seats_per_province_df["province"] == province]["seats"].iloc[0]
        quota = total_votes // (target_seats + 1)
        
        print(f"Total admitted votes: {total_votes}")
        print(f"Target seats: {target_seats}")
        print(f"Quota: {quota}")
        
        # Group by list
        prov_list_votes = prov_votes.groupby(["list", "coalition"], as_index=False)["votes"].sum()
        prov_list_votes["province"] = province
        
        # Calculate integer seats
        prov_results = provincial_integers(prov_list_votes, quota)
        province_results.append(prov_results)
    
    # Combine all provinces
    all_prov = pd.concat(province_results, ignore_index=True)
    
    # Assign residual seats
    final_alloc, order = assign_residuals(all_prov, seats_per_province_df, grp_seats)
    
    print("\n=== FINAL RESULTS ===")
    fermo_results = final_alloc[final_alloc["province"] == "Fermo"]
    print("\nFermo allocation:")
    for _, row in fermo_results.iterrows():
        if row["final_seats"] > 0:
            print(f"  {row['list']}: {row['final_seats']} seats")
    
    total_fermo_seats = fermo_results["final_seats"].sum()
    print(f"\nTotal Fermo seats: {total_fermo_seats} (should be 4)")

if __name__ == "__main__":
    main()
