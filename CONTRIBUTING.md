# Contributing to Marche Regional Election Simulator

Thank you for your interest in contributing to this project! This simulator implements the Marche regional electoral law, so accuracy and legal compliance are paramount.

## 🎯 How to Contribute

### Reporting Issues
- **Bug reports**: Include the specific input data and expected vs actual output
- **Legal compliance**: Reference specific articles from L.R. 27/2004 if you find discrepancies
- **Performance issues**: Provide details about execution time and data size

### Code Contributions
1. **Fork** the repository
2. **Create a branch** for your feature/fix
3. **Test thoroughly** with various scenarios
4. **Document** any changes to the electoral logic
5. **Submit a pull request**

## 📋 Development Guidelines

### Legal Compliance
- All changes must comply with **L.R. 27/2004, Articles 18-19**
- Reference specific legal provisions in comments
- Maintain exact mathematical formulations from the law

### Testing Requirements
- Test with multiple electoral scenarios
- Verify provincial seat totals remain correct (30 total)
- Validate against expected results when available
- Run all debug scripts to ensure consistency

### Code Standards
- Follow existing naming conventions
- Add docstrings for new functions
- Include legal article references in comments
- Maintain backward compatibility with input data formats

## 🔍 Key Areas for Contribution

### Algorithm Improvements
- Optimization of D'Hondt calculations
- Enhanced residual allocation logic
- Improved group caps handling

### Documentation
- Additional examples and use cases
- Legal interpretation clarifications
- Performance benchmarking

### Testing
- Edge case scenarios
- Historical election validation
- Stress testing with large datasets

### Reporting
- Enhanced PDF formatting
- Additional analysis metrics
- Visualization improvements

## 📚 Understanding the Electoral System

Before contributing, familiarize yourself with:

1. **Coalition Thresholds** (Art. 18): 5% for coalitions, 3% for individual lists
2. **D'Hondt Method**: Proportional allocation with divisor series
3. **Minimum Bonus**: Leading coalition guaranteed minimum seats based on vote percentage
4. **Provincial Quotas**: `total_votes ÷ (seats + 1)` for each province
5. **Residual Ranking**: Regional ranking of remainder percentages
6. **Group Caps**: Maximum seats per list enforcement
7. **Runner-up Reserve**: Ensuring second coalition representation

## 🧪 Testing Your Changes

### Required Tests
```bash
# Run the main simulator
python ERM.py

# Verify allocation totals
python debug_allocation.py

# Check provincial quotas
python check_quota.py

# Validate specific provinces
python debug_fermo.py
```

### Expected Results
- Total seats: exactly 30
- Provincial distribution: as specified in seats_per_province.csv
- All admitted coalitions have representation
- Group caps are respected
- Regional rest ranking is correct

## 📄 Pull Request Process

1. **Description**: Clearly explain what your changes do
2. **Legal justification**: Reference relevant law articles
3. **Testing**: Include test results and validation steps
4. **Breaking changes**: Note any changes to input/output formats
5. **Documentation**: Update README.md if needed

## ❓ Questions?

- Check existing issues for similar questions
- Review the legal documents in the repository
- Examine debug scripts for implementation details
- Reference the comprehensive README.md

## 🎓 Educational Context

This project is developed for academic research on Italian regional electoral systems. Contributions should maintain:
- **Academic rigor** in legal interpretation
- **Transparency** in algorithmic implementation  
- **Reproducibility** of results
- **Educational value** for understanding electoral systems