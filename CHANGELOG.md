# Changelog

All notable changes to the Marche Regional Election Simulator project will be documented in this file.

The format is based on [Keep a Changelog](https://keepachangelog.com/en/1.0.0/),
and this project adheres to [Semantic Versioning](https://semver.org/spec/v2.0.0.html).

## [1.0.0] - 2025-11-28

### Added
- Initial implementation of Marche regional election seat allocation
- Full compliance with L.R. 27/2004 Articles 18-19
- Coalition admission thresholds (5% for coalitions, 3% for lists)
- D'Hondt proportional allocation with minimum bonus system
- Provincial quota calculation and integer seat allocation
- Regional residual percentage ranking system
- Group caps enforcement for maximum seats per list
- Runner-up reserved seat mechanism
- Comprehensive CSV output generation
- Markdown and PDF report generation
- Debug and validation tools
- Complete documentation and examples

### Electoral Features
- **Coalition Stage**: Threshold-based admission and D'Hondt allocation
- **Group Seats**: Coalition-to-list seat distribution
- **Provincial Allocation**: Quota-based integer seats with residuals
- **Residual Assignment**: Regional ranking with group caps
- **Runner-up Reserve**: Second coalition representation guarantee

### Technical Features
- Pandas-based data processing
- ReportLab PDF generation
- Modular function architecture
- Comprehensive error handling
- Input data validation
- Output format standardization

### Documentation
- Complete README with usage instructions
- API reference documentation
- Legal implementation guide
- Contributing guidelines
- Example scripts and analysis tools
- Educational context and references

### Validation Tools
- Provincial allocation verification
- Coalition and group seat debugging
- Residual allocation tracing
- Quota calculation validation
- Step-by-step process verification

## [Planned Features]

### [1.1.0] - Future
- Historical election data validation
- Performance optimization for large datasets
- Additional output format options
- Enhanced visualization tools
- Web interface for interactive analysis

### [1.2.0] - Future
- Support for different electoral scenarios
- Sensitivity analysis tools
- Statistical validation methods
- Integration with official electoral data sources

---

## Development Notes

### Legal Compliance
- All implementations strictly follow L.R. 27/2004 text
- Mathematical formulations match legal requirements
- Provincial seat totals always equal 30
- Group caps and thresholds properly enforced

### Testing Methodology
- Multiple electoral scenarios tested
- Edge cases validated
- Historical data cross-referenced where available
- Debug tools verify each allocation step

### Performance Characteristics
- Time complexity: O(n log n) for sorting operations
- Memory usage: Linear with input data size
- Suitable for real-time election analysis
- Optimized for standard regional council size (30 seats)