# Master Sample Data Creation

This document explains how to use the master consolidated sample data creation command that creates ALL sample data across all domains.

## Command: `create_all_sample_data`

This is the **master command** that creates sample data for ALL domains (demographics, economics, infrastructure, and social) in a single operation.

### Usage

```bash
# Create ALL sample data across all domains
python manage.py create_all_sample_data

# Clear existing data and create fresh sample data across all domains
python manage.py create_all_sample_data --clear

# See what commands would be run without executing them
python manage.py create_all_sample_data --dry-run

# Continue with other domains even if one fails
python manage.py create_all_sample_data --skip-errors

# Combine flags as needed
python manage.py create_all_sample_data --clear --skip-errors --dry-run
```

### What it does

This master command runs the following consolidated domain commands in sequence:

1. **Demographics Sample Data** (`create_demographics_sample_data`)
   - Religion, Language, Caste, Househead, Occupation, Economically Active
   - 6 sub-commands, supports `--clear` and `--skip-errors`

2. **Economics Sample Data** (`create_economics_sample_data`)
   - Major Skills, Remittance Expenses
   - 2 sub-commands, supports `--clear`

3. **Infrastructure Sample Data** (`create_infrastructure_sample_data`)
   - Market Center Time, Public Transport, Road Status
   - 3 sub-commands, supports `--clear`

4. **Social Sample Data** (`create_social_sample_data`)
   - Literacy Status, Major Subjects, Old Age, School Dropout, Solid Waste, Toilet Type
   - 6 sub-commands, supports mixed clear patterns (`--clear`, `--reset`, or none)

### Options

- `--clear`: Clear existing data before creating new data (passed to all sub-commands)
- `--dry-run`: Show which commands would be run without executing them
- `--skip-errors`: Continue with other domains even if one domain fails
- `--help`: Show help information

### Output Features

The command provides comprehensive output including:
- **Progress Tracking**: Clear visibility of which domain is being processed
- **Execution Time**: Individual and total execution times
- **Success/Failure Tracking**: Detailed results for each domain
- **Data Overview**: Quick statistics showing records created across all domains
- **Performance Metrics**: Average execution time per domain
- **Comprehensive Summary**: Final status with tips and recommendations

### Examples

```bash
# Standard usage - create all sample data
python manage.py create_all_sample_data

# Fresh start - clear and recreate all data
python manage.py create_all_sample_data --clear

# Preview mode - see what would happen
python manage.py create_all_sample_data --dry-run

# Resilient execution - continue even if some domains fail
python manage.py create_all_sample_data --clear --skip-errors
```

### Domain Commands Hierarchy

```
create_all_sample_data (MASTER)
├── create_demographics_sample_data
│   ├── create_religion_sample_data
│   ├── create_language_sample_data
│   ├── create_caste_sample_data
│   ├── create_househead_sample_data
│   ├── create_occupation_sample_data
│   └── create_economically_active_sample_data
├── create_economics_sample_data
│   ├── create_major_skills_sample_data
│   └── create_remittance_expenses_sample_data
├── create_infrastructure_sample_data
│   ├── create_market_center_time_sample_data
│   ├── create_public_transport_sample_data
│   └── create_road_status_sample_data
└── create_social_sample_data
    ├── create_literacy_status_sample_data
    ├── create_major_subject_sample_data
    ├── create_old_age_single_women_sample_data
    ├── create_school_dropout_sample_data
    ├── create_solid_waste_management_sample_data
    └── create_toilet_type_sample_data
```

### Data Created

After running this master command, the following comprehensive sample data will be available:

#### Demographics (12 categories)
- Religion demographics across municipality
- Language/mother tongue demographics
- Caste demographics by population
- Househead gender by ward
- Occupation distribution by ward
- Economically active population by age/gender

#### Economics (2 categories)
- Major skills by ward and skill type
- Remittance expense patterns by ward

#### Infrastructure (3 categories)
- Market center accessibility by time duration
- Public transport accessibility by time duration
- Road status and infrastructure by ward

#### Social (6 categories)
- Literacy status by ward (reading/writing capabilities)
- Educational major subjects by ward
- Elderly population and single women demographics
- School dropout causes and patterns
- Solid waste management methods by ward
- Toilet types and sanitation facilities by ward

### Performance

- **Total Categories**: 23 different data categories
- **Typical Execution Time**: < 1 second
- **Total Records Created**: ~400+ records across all domains
- **Ward Coverage**: All 7 wards for ward-specific data
- **Municipality Coverage**: Municipality-wide data where applicable

### Error Handling

- **Individual Domain Failures**: Use `--skip-errors` to continue with other domains
- **Transaction Safety**: Each domain runs in its own transaction
- **Detailed Error Reporting**: Clear error messages with specific command failures
- **Graceful Degradation**: Partial success is clearly indicated

### Alternative Commands

You can still run individual domain or category commands if needed:

```bash
# Domain level
python manage.py create_demographics_sample_data
python manage.py create_economics_sample_data
python manage.py create_infrastructure_sample_data
python manage.py create_social_sample_data

# Individual category level
python manage.py create_religion_sample_data
python manage.py create_major_skills_sample_data
python manage.py create_market_center_time_sample_data
python manage.py create_literacy_status_sample_data
# ... and 19 more individual commands
```

### Best Practices

1. **Initial Setup**: Use `--clear` for fresh installations
2. **Development**: Use `--dry-run` to preview changes
3. **Production**: Use `--skip-errors` for resilient execution
4. **Testing**: Run individual domain commands for focused testing

### Integration

This master command is ideal for:
- **CI/CD Pipelines**: Automated sample data creation
- **Development Environment Setup**: Quick data initialization
- **Demo Environments**: Comprehensive sample data for presentations
- **Testing**: Full dataset for integration testing

This master command represents the complete sample data ecosystem for the municipality profile system, providing a one-stop solution for all sample data needs across demographics, economics, infrastructure, and social domains.
