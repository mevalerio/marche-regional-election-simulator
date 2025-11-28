# Electoral Law Implementation Guide

## L.R. 27/2004 Articles 18-19 Implementation

This document provides detailed information on how the Marche regional electoral law is implemented in the simulator.

### Article 18: Coalition and List Admission

#### Legal Text Implementation
- **Comma 5**: Coalition threshold of 5% of valid votes
- **Comma 6**: Individual list threshold of 3% of valid votes

#### Code Implementation
```python
def coalitions_stage(votes_df, total_list_seats, pct19, pct18):
    # Calculate coalition and list shares
    coal["coal_share"] = coal["total_coal_votes"] / tot_coal if tot_coal > 0 else 0
    list_reg.assign(list_share=list_reg["votes"] / tot_list if tot_list > 0 else 0)
    
    # Apply admission thresholds
    coal["admitted"] = (coal["coal_share"] >= 0.05) | (coal["max_list_share"] > 0.03)
```

### Article 19: Seat Allocation

#### Comma 1-2: D'Hondt Method with Minimum Bonus

**Legal provision**: Leading coalition gets minimum 19 seats if ≥43% votes, 18 seats if ≥40% votes.

**Implementation**:
```python
# D'Hondt base allocation
base = dhondt(dict(zip(adm["coalition"], adm["total_coal_votes"])), total_list_seats)

# Apply minimum bonus
if not coal_seats.empty:
    leader = adm.loc[adm["coal_share"].idxmax(), "coalition"]
    lshare = float(adm.loc[adm["coalition"]==leader, "coal_share"])
    got = int(coal_seats.loc[coal_seats["coalition"]==leader, "seats"])
    
    if lshare >= pct19 and got < 19:  # 43% threshold
        coal_seats.loc[coal_seats["coalition"]==leader, "seats"] = 19
    elif lshare >= pct18 and got < 18:  # 40% threshold  
        coal_seats.loc[coal_seats["coalition"]==leader, "seats"] = 18
```

#### Comma 3: Group Seat Distribution

Coalition seats are distributed to lists using D'Hondt within each coalition.

#### Comma 4: Provincial Allocation

**Provincial quota formula**: `Q = V / (S + 1)`
- V = total admitted votes in province
- S = seats allocated to province

**Integer seats**: `floor(list_votes / Q)`

#### Comma 5-6: Group Caps and Residual Allocation

1. Enforce maximum seats per list
2. Create regional ranking of residual percentages
3. Allocate remaining seats in order of highest residuals

#### Comma 7: Runner-up Reserved Seat

Ensure second-place presidential coalition has at least one seat by removing from last allocated residual seat.

## Mathematical Formulas

### Provincial Quota
```
Q_province = total_admitted_votes_province ÷ (seats_province + 1)
```

### Integer Seats
```
integer_seats_list = floor(votes_list ÷ Q_province)
```

### Residual Percentage
```
rest_pct = (votes_list - integer_seats_list × Q_province) ÷ total_province_votes × 100
```

### D'Hondt Quotients
```
quotient = votes ÷ (seats_already_won + 1)
```

## Key Data Structures

### Input DataFrames

**votes_df**: Election results
```
province | list | coalition | president | votes
```

**seats_per_province_df**: Provincial seat allocation
```
province | seats
```

### Output DataFrames

**provincial_results.csv**: Final allocation
```
province | list | coalition | votes | int_seats | rest | rest_pct | regional_rest_rank | final_seats
```

## Validation Rules

1. **Total seats**: Must equal 30
2. **Provincial totals**: Must match seats_per_province.csv
3. **Group caps**: No list exceeds assigned group_seats
4. **Non-negative**: All seat counts ≥ 0
5. **Admitted only**: Only admitted coalitions get seats