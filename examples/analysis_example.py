#!/usr/bin/env python3
"""
Analysis example for the Marche Regional Election Simulator.

This example demonstrates how to analyze election results:
1. Provincial quota analysis
2. Residual percentage ranking
3. Coalition competitiveness
4. Group cap effects
"""

import pandas as pd
import sys
import os

# Add the parent directory to path for imports
sys.path.append(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

from ERM import (run_allocation, coalitions_stage, group_seats_stage, 
                 provincial_integers, assign_residuals, calculate_provincial_quota)

def analyze_provincial_quotas(votes_df, seats_df):
    """Analyze provincial quota calculations."""
    print("=== PROVINCIAL QUOTA ANALYSIS ===")
    
    # Calculate quotas
    quota_df = calculate_provincial_quota(votes_df, seats_df)
    
    # Get admitted coalitions
    coal_votes, _ = coalitions_stage(votes_df, 30, 0.43, 0.40)
    admitted = coal_votes[coal_votes["admitted"]]["coalition"].tolist()
    
    # Provincial totals with only admitted votes
    admitted_votes = votes_df[votes_df["coalition"].isin(admitted)]
    prov_totals = admitted_votes.groupby('province')['votes'].sum()
    
    print("Province\t\tAdmitted Votes\tSeats\tQuota\t\tEffectiveness")
    print("-" * 80)
    
    for _, row in seats_df.iterrows():
        province = row['province']
        seats = row['seats']
        votes = prov_totals.get(province, 0)
        quota = votes // (seats + 1) if seats > 0 else 0
        effectiveness = votes / seats if seats > 0 else 0
        
        print(f"{province:<20}\t{votes:>8,}\t{seats}\t{quota:>8,}\t{effectiveness:>8,.0f}")
    
    print()

def analyze_residual_ranking(final_df):
    """Analyze regional residual percentage ranking."""
    print("=== REGIONAL RESIDUAL RANKING ANALYSIS ===")
    
    # Get top residuals
    top_residuals = final_df.nlargest(15, 'rest_pct')
    
    print("Rank\tList\t\t\t\tProvince\t\tRest %\t\tGot Seat")
    print("-" * 90)
    
    for _, row in top_residuals.iterrows():
        rank = int(row['regional_rest_rank'])
        list_name = row['list'][:25]  # Truncate for display
        province = row['province'][:15]
        rest_pct = row['rest_pct']
        got_residual = "Yes" if row['final_seats'] > row['int_seats'] else "No"
        
        print(f"{rank:>4}\t{list_name:<25}\t{province:<15}\t{rest_pct:>6.2f}%\t{got_residual:>8}")
    
    print()

def analyze_coalition_competitiveness(votes_df, coal_seats):
    """Analyze coalition vote shares vs seat shares."""
    print("=== COALITION COMPETITIVENESS ANALYSIS ===")
    
    # Calculate coalition vote shares
    coal_votes = votes_df.groupby('coalition')['votes'].sum()
    total_votes = coal_votes.sum()
    
    print("Coalition\t\t\tVotes\t\tVote %\t\tSeats\tSeat %\t\tBonus")
    print("-" * 85)
    
    for _, row in coal_seats.iterrows():
        coalition = row['coalition']
        seats = row['seats']
        votes = coal_votes.get(coalition, 0)
        vote_pct = votes / total_votes * 100 if total_votes > 0 else 0
        seat_pct = seats / 30 * 100
        bonus = seat_pct - vote_pct
        
        print(f"{coalition:<20}\t{votes:>8,}\t{vote_pct:>6.1f}%\t\t{seats:>3}\t{seat_pct:>6.1f}%\t{bonus:>+6.1f}pp")
    
    print()

def analyze_group_caps(grp_seats, final_df):
    """Analyze group cap effects."""
    print("=== GROUP CAP ANALYSIS ===")
    
    # Calculate actual seats per group
    actual_seats = final_df.groupby('list')['final_seats'].sum()
    
    print("List\t\t\t\tCap\tActual\tDifference\tUtilization")
    print("-" * 70)
    
    for _, row in grp_seats.iterrows():
        list_name = row['list'][:25]
        cap = row['group_seats']
        actual = actual_seats.get(row['list'], 0)
        diff = actual - cap
        utilization = actual / cap * 100 if cap > 0 else 0
        
        if actual > 0:  # Only show lists that got seats
            print(f"{list_name:<25}\t{cap:>3}\t{actual:>6}\t{diff:>+9}\t{utilization:>8.1f}%")
    
    print()

def main():
    """Run comprehensive analysis."""
    print("=== Marche Regional Election Simulator - Analysis Example ===\n")
    
    # Load data
    try:
        votes_df = pd.read_csv("../votes_marche_2025_all_provinces.csv")
        seats_df = pd.read_csv("../seats_per_province.csv")
        params = pd.read_csv("../params.csv")
        
        total = int(params.loc[params["key"]=="TOTAL_LIST_SEATS", "value"].iloc[0])
        pct19 = float(params.loc[params["key"]=="BONUS_TARGET_PCT_19", "value"].iloc[0])
        pct18 = float(params.loc[params["key"]=="BONUS_TARGET_PCT_18", "value"].iloc[0])
        
    except FileNotFoundError as e:
        print(f"Error loading data: {e}")
        return
    
    # Run allocation
    print("Running allocation for analysis...\n")
    final, coal_seats, grp_seats, removed = run_allocation(votes_df, seats_df, total, pct19, pct18)
    
    if final.empty:
        print("No results to analyze!")
        return
    
    # Run analyses
    analyze_provincial_quotas(votes_df, seats_df)
    analyze_residual_ranking(final)
    analyze_coalition_competitiveness(votes_df, coal_seats)
    analyze_group_caps(grp_seats, final)
    
    # Summary statistics
    print("=== SUMMARY STATISTICS ===")
    print(f"Total lists participating: {votes_df['list'].nunique()}")
    print(f"Lists receiving seats: {len(final[final['final_seats'] > 0]['list'].unique())}")
    print(f"Average seats per winning list: {final[final['final_seats'] > 0]['final_seats'].mean():.1f}")
    print(f"Most successful province (by competition): {final.groupby('province')['list'].nunique().idxmax()}")
    
    if removed and 'province' in removed:
        print(f"Runner-up seat removed from: {removed.get('list', 'Unknown')} in {removed['province']}")
    
    print("\n=== ANALYSIS COMPLETED ===")

if __name__ == "__main__":
    main()