# Social Sample Data Creation

This document explains how to use the consolidated social sample data creation command.

## Command: `create_social_sample_data`

This command creates sample data for all social-related categories in a single operation.

### Usage

```bash
# Create all social sample data
python manage.py create_social_sample_data

# Clear existing data and create fresh sample data (where supported)
python manage.py create_social_sample_data --clear

# See what commands would be run without executing them
python manage.py create_social_sample_data --dry-run

# Combine flags as needed
python manage.py create_social_sample_data --clear --dry-run
```

### What it does

This consolidated command runs the following social sample data creation commands:

1. **Literacy Status Sample Data** (`create_literacy_status_sample_data`)
   - Creates ward-wise literacy status data (reading/writing capabilities)
   - Supports `--reset` flag for clearing data

2. **Major Subject Sample Data** (`create_major_subject_sample_data`)
   - Creates ward-wise educational major subject data
   - No clear flag support

3. **Old Age and Single Women Sample Data** (`create_old_age_single_women_sample_data`)
   - Creates ward-wise elderly population and single women data
   - No clear flag support

4. **School Dropout Sample Data** (`create_school_dropout_sample_data`)
   - Creates ward-wise school dropout data with causes
   - Supports `--clear` flag

5. **Solid Waste Management Sample Data** (`create_solid_waste_management_sample_data`)
   - Creates ward-wise solid waste management method data
   - Supports `--clear` flag

6. **Toilet Type Sample Data** (`create_toilet_type_sample_data`)
   - Creates ward-wise toilet type and sanitation data
   - Supports `--clear` flag

### Options

- `--clear`: Clear existing data before creating new data (passed to sub-commands that support it)
- `--dry-run`: Show which commands would be run without executing them
- `--help`: Show help information

### Clear Flag Support

The command intelligently handles different clear argument patterns:

| Command | Clear Support | Clear Argument |
|---------|---------------|----------------|
| Literacy Status | ✓ | `--reset` |
| Major Subject | ✗ | None |
| Old Age & Single Women | ✗ | None |
| School Dropout | ✓ | `--clear` |
| Solid Waste Management | ✓ | `--clear` |
| Toilet Type | ✓ | `--clear` |

### Output

The command provides detailed output including:
- Progress for each social category
- Creation/update counts for each dataset
- Comprehensive statistics and analysis
- Ward-wise summaries and breakdowns
- Educational and social insights

### Examples

```bash
# Standard usage - create all social data
python manage.py create_social_sample_data

# Fresh start - clear and recreate all data (where supported)
python manage.py create_social_sample_data --clear

# Preview mode - see what would happen
python manage.py create_social_sample_data --dry-run
```

### Related Individual Commands

You can still run individual social commands if needed:

```bash
python manage.py create_literacy_status_sample_data --reset
python manage.py create_major_subject_sample_data
python manage.py create_old_age_single_women_sample_data
python manage.py create_school_dropout_sample_data --clear
python manage.py create_solid_waste_management_sample_data --clear
python manage.py create_toilet_type_sample_data --clear
```

### Data Created

After running this command, the following social data will be available:

- **Literacy Status**: Reading and writing capabilities by ward
- **Educational Subjects**: Major subject specializations by ward
- **Demographics**: Elderly population and single women statistics
- **Education Issues**: School dropout causes and patterns
- **Sanitation**: Solid waste management methods by ward
- **Infrastructure**: Toilet types and sanitation facilities by ward

This data is used for generating social reports and analysis in the municipality profile system.

### Notes

- Some commands may not support the `--clear` flag, which is normal
- The consolidated command will continue executing even if individual commands fail
- Detailed statistics and analysis are provided for each category
- All data includes ward-wise breakdowns for comprehensive reporting
