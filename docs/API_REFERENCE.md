# API Documentation

## Core Functions

### Coalition Stage

#### `coalitions_stage(votes_df, total_list_seats, pct19, pct18)`
Implements Article 18 admission thresholds and Article 19 D'Hondt allocation with minimum bonus.

**Parameters:**
- `votes_df` (DataFrame): Vote data with columns [province, list, coalition, votes]
- `total_list_seats` (int): Total seats to allocate (typically 30)
- `pct19` (float): Threshold for 19-seat bonus (typically 0.43)
- `pct18` (float): Threshold for 18-seat bonus (typically 0.40)

**Returns:**
- `coal_votes` (DataFrame): Coalition vote totals and admission status
- `coal_seats` (DataFrame): Seats allocated to each coalition

### Group Seats Stage

#### `group_seats_stage(votes_df, coal_seats_df)`
Distributes coalition seats to individual lists using D'Hondt method.

**Parameters:**
- `votes_df` (DataFrame): Vote data for admitted coalitions only
- `coal_seats_df` (DataFrame): Coalition seat allocations

**Returns:**
- `group_seats` (DataFrame): Maximum seats per list [list, coalition, group_seats]

### Provincial Allocation

#### `provincial_integers(votes_df, province_seats_df, admitted_coalitions)`
Calculates provincial quotas and integer seat allocation.

**Parameters:**
- `votes_df` (DataFrame): Vote data for admitted coalitions
- `province_seats_df` (DataFrame): Seats per province [province, seats]
- `admitted_coalitions` (list): List of admitted coalition names

**Returns:**
- `allocation_df` (DataFrame): Integer seats and residual percentages
- `province_meta` (DataFrame): Provincial metadata with quotas

### Residual Assignment

#### `assign_residuals(df_step, prov_meta, group_caps)`
Assigns remaining seats based on regional residual ranking while enforcing group caps.

**Parameters:**
- `df_step` (DataFrame): Provincial allocation with integer seats
- `prov_meta` (DataFrame): Province metadata
- `group_caps` (DataFrame): Maximum seats per list

**Returns:**
- `final_allocation` (DataFrame): Complete seat allocation
- `residual_order` (list): Order of residual seat assignments

### Runner-up Reservation

#### `reserve_runner_up(df_alloc, residual_order, votes_df, coal_votes, coal_seats)`
Implements Article 19 comma 7 runner-up seat reservation.

**Parameters:**
- `df_alloc` (DataFrame): Current seat allocation
- `residual_order` (list): Order of residual assignments
- `votes_df` (DataFrame): Original vote data
- `coal_votes` (DataFrame): Coalition vote totals
- `coal_seats` (DataFrame): Coalition seat allocations

**Returns:**
- `final_allocation` (DataFrame): Allocation after runner-up adjustment
- `removed_info` (dict): Information about removed seat

## Utility Functions

### D'Hondt Method

#### `dhondt(values, seats)`
Pure D'Hondt proportional allocation.

**Parameters:**
- `values` (dict): {party_name: vote_count}
- `seats` (int): Total seats to allocate

**Returns:**
- `allocation` (dict): {party_name: seat_count}

### Quota Calculation

#### `calculate_provincial_quota(votes_df, seats_per_province_df)`
Calculates provincial quotas for reporting.

**Parameters:**
- `votes_df` (DataFrame): Vote data
- `seats_per_province_df` (DataFrame): Provincial seat counts

**Returns:**
- `quota_df` (DataFrame): [province, quota]

## Report Generation

### Markdown Reports

#### `generate_province_seat_markdown(votes_df, provincial_results_df, quota_df, seats_per_province_df, output_path)`
Generates comprehensive Markdown report.

### PDF Reports

#### `generate_province_seat_pdf(provincial_results_df, output_path, seats_per_province_df, votes_df)`
Creates PDF report matching official format.

### Heatmap

#### `generate_province_seat_heatmap(provincial_results_df, output_path)`
Creates seat distribution heatmap in Markdown.

## Data Validation

### Input Validation
- Column presence and naming
- Data type verification
- Vote count validation
- Provincial seat total verification

### Output Validation
- Seat count totals
- Non-negative allocations
- Group cap enforcement
- Provincial distribution accuracy

## Error Handling

Common error scenarios:
- Missing required columns
- Invalid vote data
- Seat total mismatches
- No admitted coalitions
- Group cap violations

## Performance Considerations

- Time complexity: O(n log n) for sorting operations
- Memory usage: Linear with input size
- Bottlenecks: Regional residual ranking, D'Hondt calculations

## Example Usage

```python
import pandas as pd
from ERM import run_allocation

# Load input data
votes_df = pd.read_csv("votes_marche_2025_all_provinces.csv")
seats_df = pd.read_csv("seats_per_province.csv")
params = pd.read_csv("params.csv")

# Run allocation
final, coal_seats, grp_seats, removed = run_allocation(
    votes_df, seats_df, total=30, pct19=0.43, pct18=0.40
)

# Analyze results
print(f"Total seats: {final['final_seats'].sum()}")
print(f"Provinces: {final.groupby('province')['final_seats'].sum()}")
```