# Infrastructure Sample Data Creation

This document explains how to use the consolidated infrastructure sample data creation command.

## Command: `create_infrastructure_sample_data`

This command creates sample data for all infrastructure-related categories in a single operation.

### Usage

```bash
# Create all infrastructure sample data
python manage.py create_infrastructure_sample_data

# Clear existing data and create fresh sample data
python manage.py create_infrastructure_sample_data --clear

# See what commands would be run without executing them
python manage.py create_infrastructure_sample_data --dry-run

# Combine flags as needed
python manage.py create_infrastructure_sample_data --clear --dry-run
```

### What it does

This consolidated command runs the following infrastructure sample data creation commands:

1. **Market Center Time Sample Data** (`create_market_center_time_sample_data`)
   - Creates ward-wise market center accessibility data
   - Time duration categories: Under 15 min, 15-30 min, 30-60 min, 1+ hour

2. **Public Transport Sample Data** (`create_public_transport_sample_data`)
   - Creates ward-wise public transport accessibility data
   - Time duration categories: Under 15 min, 15-30 min, 30-60 min, 1+ hour

3. **Road Status Sample Data** (`create_road_status_sample_data`)
   - Creates ward-wise road infrastructure status data
   - Road types: Blacktopped, Graveled, Earthen, No Road

### Options

- `--clear`: Clear existing data before creating new data
- `--dry-run`: Show which commands would be run without executing them
- `--help`: Show help information

### Output

The command provides detailed output including:
- Progress for each infrastructure category
- Creation/update counts for each dataset
- Comprehensive statistics and analysis
- Ward-wise summaries
- Infrastructure accessibility insights

### Examples

```bash
# Standard usage - create all infrastructure data
python manage.py create_infrastructure_sample_data

# Fresh start - clear and recreate all data
python manage.py create_infrastructure_sample_data --clear

# Preview mode - see what would happen
python manage.py create_infrastructure_sample_data --dry-run
```

### Related Individual Commands

You can still run individual infrastructure commands if needed:

```bash
python manage.py create_market_center_time_sample_data
python manage.py create_public_transport_sample_data
python manage.py create_road_status_sample_data
```

### Data Created

After running this command, the following infrastructure data will be available:

- **Market Center Accessibility**: Time required to reach market centers by ward
- **Public Transport Accessibility**: Time required to reach public transport by ward  
- **Road Infrastructure**: Road status and accessibility by ward

This data is used for generating infrastructure reports and analysis in the municipality profile system.
