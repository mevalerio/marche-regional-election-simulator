from ERM import coalitions_stage, dhondt
import pandas as pd

# Load the exact same data as ERM.py main
votes_df = pd.read_csv("votes_marche_2025_all_provinces.csv")
votes_df.columns = votes_df.columns.str.strip()

# Handle comma-separated numbers in votes column BEFORE numeric conversion
if "votes" in votes_df.columns and votes_df["votes"].dtype == 'object':
    votes_df["votes"] = votes_df["votes"].astype(str).str.replace(',', '').astype(float)

# Ensure votes column is numeric
if "votes" in votes_df.columns:
    votes_df["votes"] = pd.to_numeric(votes_df["votes"], errors="coerce").fillna(0)

# Add debug prints to coalitions_stage by copying the function manually
def debug_coalitions_stage(votes_df, total_list_seats, pct19, pct18):
    print("=== COALITIONS_STAGE DEBUG ===")
    
    # Fix: strip whitespace from column names
    votes_df = votes_df.rename(columns=lambda x: x.strip())
    if "votes" not in votes_df.columns:
        raise ValueError("Column 'votes' not found in votes_df. Available columns: %s" % votes_df.columns.tolist())
    
    # Handle comma-separated numbers in votes column
    if votes_df["votes"].dtype == 'object':
        votes_df["votes"] = votes_df["votes"].astype(str).str.replace(',', '').astype(float)
    
    list_reg = votes_df.groupby(["list","coalition"], as_index=False)["votes"].sum()
    print(f"List regional shape: {list_reg.shape}")
    
    # voti coalizione = somma voti delle liste (escludi pres_votes)
    coal = list_reg.groupby("coalition", as_index=False)["votes"].sum().rename(columns={"votes":"total_coal_votes"})
    print(f"Coal shape: {coal.shape}")
    
    # Ensure all vote columns are numeric
    list_reg["votes"] = pd.to_numeric(list_reg["votes"], errors="coerce").fillna(0)
    coal["total_coal_votes"] = pd.to_numeric(coal["total_coal_votes"], errors="coerce").fillna(0)
    tot_coal = coal["total_coal_votes"].sum()
    coal["coal_share"] = coal["total_coal_votes"] / tot_coal if tot_coal > 0 else 0
    tot_list = list_reg["votes"].sum()
    # Fix: calculate max list share per coalition correctly
    list_reg["list_share"] = list_reg["votes"] / tot_list if tot_list > 0 else 0
    mx = list_reg.groupby("coalition")["list_share"].max().reset_index().rename(columns={"list_share":"max_list_share"})
    coal = coal.merge(mx, on="coalition", how="left")
    # Apply admission thresholds: 5% coalition OR 3% single list
    coal["admitted"] = (coal["coal_share"] >= 0.05) | (coal["max_list_share"] >= 0.03)
    coal.loc[coal["total_coal_votes"] <= 0, "admitted"] = False
    adm = coal[coal["admitted"]].copy()
    
    print(f"Admitted coalitions:")
    print(adm[["coalition", "total_coal_votes", "coal_share"]])
    
    # D'Hondt allocation
    base = dhondt(dict(zip(adm["coalition"], adm["total_coal_votes"])), total_list_seats)
    coal_seats = pd.DataFrame({"coalition": list(base.keys()), "seats": list(base.values())})
    print(f"Initial D'Hondt allocation:")
    print(coal_seats)
    
    # premio minimo 19/18
    if not coal_seats.empty:
        leader = adm.sort_values("total_coal_votes", ascending=False)["coalition"].iloc[0]
        lshare = float(adm.loc[adm["coalition"] == leader, "coal_share"].iloc[0])
        need = 19 if lshare >= pct19 else (18 if lshare >= pct18 else 0)
        got = int(coal_seats.loc[coal_seats["coalition"] == leader, "seats"].iloc[0])
        print(f"Leader: {leader}, share: {lshare:.4f}, need: {need}, got: {got}")
        
        if need > 0 and got < need:
            print("Applying minimum seat bonus...")
            remaining = total_list_seats - need
            others = adm[adm["coalition"] != leader]
            print(f"Remaining seats: {remaining}")
            print(f"Others:")
            print(others[["coalition", "total_coal_votes"]])
            
            other_counts = dhondt(dict(zip(others["coalition"], others["total_coal_votes"])), remaining)
            print(f"Other D'Hondt result: {other_counts}")
            
            df1 = pd.DataFrame({"coalition": [leader], "seats": [need]})
            df2 = pd.DataFrame({"coalition": list(other_counts.keys()), "seats": list(other_counts.values())})
            print(f"DF1: {df1}")
            print(f"DF2: {df2}")
            
            coal_seats = pd.concat([
                df1,
                df2
            ], ignore_index=True)
            
    print(f"Final coalition seats:")
    print(coal_seats)
    return coal, coal_seats

# Test with debug
coal, seats = debug_coalitions_stage(votes_df, 30, 0.43, 0.40)
print("\n=== FINAL RESULT ===")
print("Coalitions admitted:")
print(coal[coal["admitted"]][["coalition", "coal_share", "max_list_share"]])
print("Seats allocated:")
print(seats)
