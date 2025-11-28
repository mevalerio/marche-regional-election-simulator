#!/usr/bin/env python3
"""
Basic usage example for the Marche Regional Election Simulator.

This example demonstrates the basic workflow:
1. Load input data
2. Run the allocation
3. Analyze results
4. Generate reports
"""

import pandas as pd
import sys
import os

# Add the parent directory to path for imports
sys.path.append(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

from ERM import run_allocation

def main():
    """Run a basic election simulation."""
    
    print("=== Marche Regional Election Simulator - Basic Example ===\n")
    
    # Load input data
    try:
        votes_df = pd.read_csv("../votes_marche_2025_all_provinces.csv")
        seats_df = pd.read_csv("../seats_per_province.csv") 
        params = pd.read_csv("../params.csv")
        
        # Get parameters
        total = int(params.loc[params["key"]=="TOTAL_LIST_SEATS", "value"].iloc[0])
        pct19 = float(params.loc[params["key"]=="BONUS_TARGET_PCT_19", "value"].iloc[0])
        pct18 = float(params.loc[params["key"]=="BONUS_TARGET_PCT_18", "value"].iloc[0])
        
        print(f"Loaded data for {len(votes_df)} vote records across {votes_df['province'].nunique()} provinces")
        print(f"Parameters: {total} total seats, {pct19:.0%} threshold for 19 seats, {pct18:.0%} for 18 seats\n")
        
    except FileNotFoundError as e:
        print(f"Error loading data: {e}")
        print("Make sure you're running from the examples/ directory and input files exist.")
        return
    
    # Run the allocation
    print("Running seat allocation...")
    final, coal_seats, grp_seats, removed = run_allocation(votes_df, seats_df, total, pct19, pct18)
    
    if final.empty:
        print("No allocation results generated!")
        return
        
    print("✓ Allocation completed successfully\n")
    
    # Analyze results
    print("=== COALITION RESULTS ===")
    if not coal_seats.empty:
        for _, row in coal_seats.iterrows():
            print(f"{row['coalition']}: {row['seats']} seats")
    print()
    
    print("=== PROVINCIAL DISTRIBUTION ===")
    provincial_totals = final.groupby('province')['final_seats'].sum()
    required_seats = seats_df.set_index('province')['seats']
    
    total_allocated = 0
    for province in required_seats.index:
        allocated = provincial_totals.get(province, 0)
        required = required_seats[province]
        status = "✓" if allocated == required else "✗"
        print(f"{province}: {allocated}/{required} seats {status}")
        total_allocated += allocated
    
    print(f"\nTotal: {total_allocated}/{total} seats {'✓' if total_allocated == total else '✗'}")
    
    # Top lists by seats
    print("\n=== TOP LISTS BY SEATS ===")
    list_totals = final.groupby('list')['final_seats'].sum().sort_values(ascending=False).head(10)
    for list_name, seats in list_totals.items():
        if seats > 0:
            print(f"{list_name}: {seats} seats")
    
    # Runner-up information
    if removed:
        print(f"\n=== RUNNER-UP SEAT ===")
        if 'province' in removed and 'list' in removed:
            print(f"Seat removed from {removed['list']} in {removed['province']}")
        else:
            print(f"Runner-up already represented: {removed}")
    
    print("\n=== EXAMPLE COMPLETED ===")
    print("Check the generated CSV files for detailed results:")
    print("- provincial_results.csv: Complete allocation by province and list")
    print("- coalition_seats.csv: Seats per coalition") 
    print("- group_seats.csv: Maximum seats per list")
    print("- runnerup_reserved.csv: Runner-up seat information")

if __name__ == "__main__":
    main()