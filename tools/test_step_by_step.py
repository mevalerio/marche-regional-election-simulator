import pandas as pd
import sys
import os

try:
    # Add current directory to path
    sys.path.insert(0, os.getcwd())
    
    from ERM import run_allocation, coalitions_stage, group_seats_stage, provincial_integers, assign_residuals, reserve_runner_up
    
    print("Imports successful")
    
    # Load data
    votes_df = pd.read_csv("votes_marche_2025_all_provinces.csv")
    votes_df = votes_df.rename(columns=lambda x: x.strip())
    
    if "votes" in votes_df.columns and votes_df["votes"].dtype == 'object':
        votes_df["votes"] = votes_df["votes"].astype(str).str.replace(',', '').astype(float)
    
    for col in ["votes"]:
        if col in votes_df.columns:
            votes_df[col] = pd.to_numeric(votes_df[col], errors="coerce").fillna(0)
    
    seats_per_province_df = pd.read_csv("seats_per_province.csv")
    params = pd.read_csv("params.csv")
    
    total = 30
    p19 = 0.43
    p18 = 0.40
    
    print("Data loaded successfully")
    
    # Test step by step
    print("Testing coalitions_stage...")
    coal_votes, coal_seats = coalitions_stage(votes_df, total, p19, p18)
    print(f"Coalition seats: {coal_seats}")
    
    admitted = coal_votes[coal_votes["admitted"]]["coalition"].tolist()
    print(f"Admitted coalitions: {admitted}")
    
    print("Testing group_seats_stage...")
    grp_seats = group_seats_stage(votes_df[votes_df["coalition"].isin(admitted)], coal_seats)
    print(f"Group seats shape: {grp_seats.shape}")
    
    print("Testing provincial_integers...")
    stepC, prov_meta = provincial_integers(votes_df[votes_df["coalition"].isin(admitted)], seats_per_province_df, admitted)
    print(f"Provincial integers shape: {stepC.shape}")
    print(f"Columns: {stepC.columns.tolist()}")
    
    print("Testing assign_residuals...")
    alloc, order = assign_residuals(stepC, prov_meta, grp_seats)
    print(f"After residuals shape: {alloc.shape}")
    print(f"Columns: {alloc.columns.tolist()}")
    
    print("Testing reserve_runner_up...")
    final, removed = reserve_runner_up(alloc, order, votes_df, coal_votes, coal_seats)
    print(f"Final shape: {final.shape}")
    print(f"Final columns: {final.columns.tolist()}")
    print(f"Removed: {removed}")
    
    print("SUCCESS: All functions work individually")
    
except Exception as e:
    print(f"ERROR: {e}")
    import traceback
    traceback.print_exc()
