import pandas as pd

# Load and process data exactly like ERM.py
votes_df = pd.read_csv('votes_marche_2025_all_provinces.csv')
votes_df = votes_df.rename(columns=lambda x: x.strip())

# Handle comma-separated numbers in votes column
if votes_df["votes"].dtype == 'object':
    votes_df["votes"] = votes_df["votes"].astype(str).str.replace(',', '').astype(float)

# Debug the coalitions_stage logic step by step
print("=== DEBUGGING COALITIONS_STAGE ===")

list_reg = votes_df.groupby(["list","coalition"], as_index=False)["votes"].sum()
print(f"List regional votes shape: {list_reg.shape}")
print("First few list_reg entries:")
print(list_reg.head())

coal = list_reg.groupby("coalition", as_index=False)["votes"].sum().rename(columns={"votes":"total_coal_votes"})
print(f"\nCoalition votes shape: {coal.shape}")
print("Coalition votes:")
print(coal)

# Ensure all vote columns are numeric
list_reg["votes"] = pd.to_numeric(list_reg["votes"], errors="coerce").fillna(0)
coal["total_coal_votes"] = pd.to_numeric(coal["total_coal_votes"], errors="coerce").fillna(0)

tot_coal = coal["total_coal_votes"].sum()
coal["coal_share"] = coal["total_coal_votes"] / tot_coal if tot_coal > 0 else 0

tot_list = list_reg["votes"].sum()
list_reg["list_share"] = list_reg["votes"] / tot_list if tot_list > 0 else 0

print(f"\nTotal coalition votes: {tot_coal}")
print(f"Total list votes: {tot_list}")

mx = list_reg.groupby("coalition")["list_share"].max().reset_index().rename(columns={"list_share":"max_list_share"})
print(f"\nMax list shares per coalition:")
print(mx)

coal = coal.merge(mx, on="coalition", how="left")
print(f"\nCoalition data with max list shares:")
print(coal)

# Apply admission thresholds
coal["admitted"] = (coal["coal_share"] >= 0.05) | (coal["max_list_share"] >= 0.03)
coal.loc[coal["total_coal_votes"] <= 0, "admitted"] = False

print(f"\nFinal coalition admission status:")
print(coal[["coalition", "coal_share", "max_list_share", "admitted"]])

adm = coal[coal["admitted"]].copy()
print(f"\nAdmitted coalitions:")
print(adm)
