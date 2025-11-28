# Marche Regional Election Seat Allocation Simulator

A Python implementation of the seat allocation algorithm for Marche Regional Council elections, following the electoral law **L.R. 27/2004 (Articles 18-19) as amended and applied in the 2025 regional election**.

## 📋 Overview

This project simulates the complex seat distribution process for the Marche Regional Council, implementing the most current version of the electoral law with all amendments as applied in the 2025 election cycle. The complete legal text is included in this repository as `LR_27_2004_Marche_Electoral_Law.pdf`.

### Key Legal Framework

- **Base Law**: L.R. 27/2004, Articles 18-19 (Marche Regional Electoral Law)
- **Version**: As amended and applied for the 2025 regional election
- **Full Text**: Available in `LR_27_2004_Marche_Electoral_Law.pdf`
- **Implementation**: Strict compliance with legal provisions as written

### Electoral Mechanisms Implemented

- **Coalition admission thresholds** (Art. 18, comma 5-6)
- **D'Hondt proportional allocation** with minimum bonus system (Art. 19, comma 1-2)
- **Provincial seat distribution** with quotas and residual allocation (Art. 19, comma 4-6)
- **Group caps enforcement** (Art. 19, comma 5)
- **Runner-up reserved seat** mechanism (Art. 19, comma 7)

## 🎯 Key Features

- **Legal Compliance**: Strict implementation of L.R. 27/2004 as amended for 2025
- **Provincial Analysis**: Detailed seat allocation by province with quota calculations
- **Regional Rest Ranking**: Complete residual percentage ranking across all provinces
- **Multiple Output Formats**: CSV data, Markdown reports, and PDF documentation
- **Comprehensive Validation**: Debug tools and verification scripts
- **Academic Rigor**: Full legal documentation and mathematical formulations

## 📊 Input Data

The simulator requires several CSV files:

### Required Files
- `votes_marche_2025_all_provinces.csv` - Sample election data by province, list, and coalition
- `seats_per_province.csv` - Seat allocation per province (must total 30)
- `params.csv` - Electoral parameters (thresholds, bonuses)

### Input Data Format

**votes_marche_2025_all_provinces.csv:**
```csv
province,list,coalition,president,votes
Ancona,Partito Democratico,Centrosinistra,Matteo Ricci,49000
Ancona,Fratelli d'Italia,Centrodestra,Francesco Acquaroli,48000
...
```

**seats_per_province.csv:**
```csv
province,seats
Ancona,9
Ascoli Piceno,4
Fermo,4
Macerata,6
Pesaro e Urbino,7
```

**params.csv:**
```csv
key,value
TOTAL_LIST_SEATS,30
BONUS_TARGET_PCT_19,0.43
BONUS_TARGET_PCT_18,0.40
```

## 🚀 Usage

### Basic Execution
```bash
python ERM.py
```

### Output Files Generated
The simulator generates the following output files:
- `provincial_results.csv` - Detailed allocation by province and list
- `coalition_seats.csv` - Seats per coalition
- `group_seats.csv` - Seats per list/group
- `runnerup_reserved.csv` - Runner-up seat information
- `province_seat_report.md` - Detailed Markdown report
- `ripartizioneSeggi_finale.pdf` - Official-style PDF report

## 📈 Electoral Process Flow

### 1. Coalition Admission (Art. 18)
- **5% threshold** for coalitions OR
- **3% threshold** for individual lists
- Filters out non-qualifying coalitions/lists

### 2. D'Hondt Allocation with Bonus (Art. 19)
- Proportional seat distribution among admitted coalitions
- **Minimum bonus system**: Leading coalition gets at least 19 seats if ≥43% votes, 18 seats if ≥40%

### 3. Group Seat Distribution (Art. 19)
- Coalition seats distributed to individual lists using D'Hondt
- Each list gets seats proportional to their votes within the coalition

### 4. Provincial Integer Allocation (Art. 19)
- **Provincial quota**: `total_votes ÷ (seats + 1)` per province
- **Integer seats**: `list_votes ÷ provincial_quota` (integer part)
- **Residual calculation**: Remaining vote percentage after integer allocation

### 5. Residual Seat Assignment (Art. 19)
- **Regional ranking**: All residuals ranked by percentage across provinces
- **Group caps**: Enforce maximum seats per list
- **Sequential allocation**: Highest residuals get remaining seats

### 6. Runner-up Reserve (Art. 19)
- Ensures second-place presidential coalition has representation
- Only removes seats if runner-up has no representation

## 🔍 Key Functions

### Core Algorithm Functions
- `coalitions_stage()` - Coalition admission and D'Hondt allocation
- `group_seats_stage()` - Distribute coalition seats to lists
- `provincial_integers()` - Calculate provincial quotas and integer seats
- `assign_residuals()` - Regional residual ranking and allocation
- `reserve_runner_up()` - Handle runner-up seat reservation

### Utility Functions
- `dhondt()` - D'Hondt proportional allocation method
- `calculate_provincial_quota()` - Provincial quota calculations
- `generate_province_seat_markdown()` - Markdown report generation
- `generate_province_seat_pdf()` - PDF report generation

## 📝 Legal References

Based on **Legge Regionale 27/2004** of Regione Marche (as amended for 2025):

- **Art. 18, comma 5-6**: Coalition and list admission thresholds
- **Art. 19, comma 1-2**: D'Hondt method and minimum bonus system
- **Art. 19, comma 3**: Distribution of coalition seats to lists
- **Art. 19, comma 4**: Provincial seat allocation using quotas
- **Art. 19, comma 5-6**: Group caps and residual seat ranking
- **Art. 19, comma 7**: Reserved seat for runner-up presidential candidate

**Complete Legal Text**: `LR_27_2004_Marche_Electoral_Law.pdf`

## 🛠️ Development Tools

The `tools/` directory contains validation and debugging utilities:

### Essential Validation Tools
- `debug_allocation.py` - Overall allocation verification
- `check_quota.py` - Provincial quota validation
- `test_step_by_step.py` - Function-by-function testing

### Specific Analysis Tools
- `debug_coalitions.py` - Coalition admission analysis
- `debug_bonus.py` - Minimum bonus system verification
- `debug_residuals.py` - Residual allocation tracing
- `debug_fermo.py` - Province-specific allocation debugging
- `debug_runnerup.py` - Runner-up seat analysis

## 📋 Requirements

- **Python 3.7+**
- **pandas** - Data manipulation
- **reportlab** - PDF generation

Install dependencies:
```bash
pip install -r requirements.txt
```

## 🎯 Example Results

For the 2025 simulation data:
- **Total Seats**: 30 (as required by law)
- **Ancona**: 9 seats ✓
- **Ascoli Piceno**: 4 seats ✓  
- **Fermo**: 4 seats ✓
- **Macerata**: 6 seats ✓
- **Pesaro e Urbino**: 7 seats ✓

## 📊 Project Structure

```
marche-regional-election-simulator/
├── README.md                          # Project documentation
├── LICENSE                            # MIT License
├── requirements.txt                   # Python dependencies
├── CHANGELOG.md                       # Version history
├── CONTRIBUTING.md                    # Contribution guidelines
├── ERM.py                            # Main simulator script
├── LR_27_2004_Marche_Electoral_Law.pdf # Complete legal text
├── params.csv                        # Electoral parameters
├── seats_per_province.csv            # Provincial seat allocation
├── votes_marche_2025_all_provinces.csv # Sample election data
├── docs/                             # Additional documentation
│   ├── API_REFERENCE.md              # Function documentation
│   └── LEGAL_IMPLEMENTATION.md       # Legal compliance details
├── examples/                         # Usage examples
│   ├── basic_usage.py               # Simple usage demonstration
│   └── analysis_example.py          # Advanced analysis tools
└── tools/                           # Validation and debugging
    ├── debug_allocation.py          # Overall verification
    ├── check_quota.py               # Quota validation
    └── [other debug tools]          # Specific analysis utilities
```

## 🤝 Contributing

This implementation follows the legal text precisely as amended for 2025. For improvements or bug reports:

1. Verify against L.R. 27/2004 provisions (see included PDF)
2. Test with various electoral scenarios
3. Ensure provincial seat totals remain correct
4. Validate against official results when available

## 📄 License

This project is for educational and research purposes, implementing public electoral law. See LICENSE for details.

## ✨ Acknowledgments

Developed by **Valerio Ficcadenti** at London South Bank University for academic research on Italian regional electoral systems, specifically analyzing the Marche regional council seat allocation mechanism as applied in the 2025 election.

## 📞 Contact

- **Author**: Valerio Ficcadenti
- **Institution**: London South Bank University  
- **Email**: ficcadv2@lsbu.ac.uk
- **Research Focus**: Italian electoral systems and regional governance

## 🔗 Legal Documentation

The complete legal framework including all amendments applied in 2025 is available in:
- `LR_27_2004_Marche_Electoral_Law.pdf`

This ensures full transparency and academic rigor in the implementation of the electoral algorithm.