# Religion Demographics System

## Overview

This is a comprehensive religion demographics analysis system for the Lungri Rural Municipality Digital Profile project. The system provides dynami### Sample Output

### Statistical Overview
> गाउँपालिकामा रहेका कुल २७,४९५ जनसंख्या मध्ये २६,२३१ अर्थात ९५.४० प्रतिशत जनसंख्याले हिन्दु धर्म मान्दछन् भने दोस्रोमा बौद्ध धर्म मान्नेको संख्या ७७ अर्थात ०.२८ प्रतिशत रहेका छन् । त्यसैगरी १२१ अर्थात ०.४४ प्रतिशत क्रिश्चियन रहेका छन् भने प्रकृति धर्म मान्ने ६६ अर्थात ०.२४ प्रतिशत रहेका छन् ।

### Ward Analysis
> वडा नं. ३ मा सबैभन्दा बढी धार्मिक विविधता रहेको छ भने वडा नं. २ र ५ मा एकल धर्म (हिन्दू) को प्रधानता रहेको छ । वडा नं. १, ३, ६, र ७ मा धार्मिक विविधता देखिन्छ ।visualization, formal report generation, and PDF integration for religious population analysis.

## Features

### 🎯 Core Functionality
- **Dynamic Data Management**: Ward-wise religion population tracking
- **Advanced Visualizations**: Interactive charts and graphs
- **Formal Report Generation**: Official Nepali government report style
- **PDF Integration**: Seamless inclusion in full municipality reports
- **Multilingual Support**: Nepali and English language support

### 📊 Visualization Types
1. **Overall Religion Distribution (Pie Chart)**
   - Shows percentage breakdown of all religions
   - Color-coded for easy identification
   - Population counts and percentages

2. **Ward-wise Comparison (Stacked Bar Chart)**
   - Compares religious distribution across all wards
   - Stacked representation for detailed analysis
   - Interactive tooltips with detailed information

3. **Religion Trend Analysis (Horizontal Bar Chart)**
   - Ranks religions by population size
   - Shows both absolute numbers and percentages
   - Identifies major and minor religious communities

4. **Religious Diversity Index**
   - Calculates diversity metrics for each ward
   - Identifies most and least diverse areas
   - Supports policy and planning decisions

### 📋 Report Sections
1. **Constitutional Context**: Legal framework for religious freedom
2. **Statistical Overview**: Key demographic statistics
3. **Ward-wise Analysis**: Detailed breakdown by administrative units
4. **Diversity Analysis**: Religious plurality metrics
5. **Cultural Practices**: Traditional festivals and celebrations
6. **Recommendations**: Policy suggestions for religious harmony
7. **Conclusions**: Summary and future outlook

## Installation

### Prerequisites
```bash
# Install required Python packages
pip install matplotlib==3.9.0
pip install seaborn==0.13.2
pip install numpy==2.1.0
```

### Django Setup
1. Add the demographics app to your `INSTALLED_APPS`:
```python
INSTALLED_APPS = [
    # ... other apps
    'apps.demographics',
]
```

2. Run migrations:
```bash
python manage.py makemigrations demographics
python manage.py migrate
```

3. Create actual data:
```bash
python manage.py create_religion_sample_data
```

This will load the actual ward-wise religion population data covering:
- **Ward 1**: 5,603 people (Hindu majority with Christian and Nature minorities)
- **Ward 2**: 4,265 people (Hindu only)  
- **Ward 3**: 3,038 people (Hindu majority with Buddhist and Christian minorities)
- **Ward 4**: 4,059 people (Hindu majority with Nature minority)
- **Ward 5**: 3,406 people (Hindu only)
- **Ward 6**: 4,511 people (Hindu majority with Buddhist minority)
- **Ward 7**: 2,613 people (Hindu majority with Buddhist, Christian, and Nature minorities)

**Total Population**: 27,495 people across 7 wards

## Usage

### 1. Web Interface
Access the religion demographics analysis at:
```
/demographics/religion/
```

### 2. API Endpoints
- **Overall Data**: `/demographics/religion/data/?type=overall`
- **Ward Data**: `/demographics/religion/data/?type=ward_wise`

### 3. PDF Generation
The religion section is automatically included in the full municipality report:
```
/reports/pdf/full/
```

### 4. Standalone Report Partial
For custom PDF generation:
```
/demographics/religion/report-partial/
```

## Data Model

### WardWiseReligionPopulation
```python
class WardWiseReligionPopulation(BaseModel):
    ward_number = models.PositiveIntegerField(validators=[MinValueValidator(1), MaxValueValidator(9)])
    religion_type = models.CharField(max_length=20, choices=ReligionTypeChoice.choices)
    population = models.PositiveIntegerField(default=0)
    
    class Meta:
        unique_together = ["ward_number", "religion_type"]
```

### Supported Religions
- **हिन्दू** (Hindu)
- **बौद्ध** (Buddhist)  
- **किरात** (Kirant)
- **क्रिश्चियन** (Christian)
- **इस्लाम** (Islam)
- **प्रकृति** (Nature)
- **बोन** (Bon)
- **जैन** (Jain)
- **बहाई** (Bahai)
- **सिख** (Sikh)
- **अन्य** (Other)

## Architecture

### 1. Models (`apps/demographics/models.py`)
- Data structure definitions
- Religion type choices
- Ward-wise population tracking

### 2. Views (`apps/demographics/views/religion.py`)
- `ReligionDemographicsView`: Main analysis view
- `ReligionDataAPIView`: JSON API endpoint
- `ReligionReportPartialView`: PDF report generation

### 3. Utilities
- **Chart Generator** (`utils/chart_generator.py`): Matplotlib-based visualization
- **Report Formatter** (`utils/report_formatter.py`): Formal report content generation

### 4. Templates
- `religion_analysis.html`: Web interface
- `religion_report_partial.html`: PDF report section

### 5. Management Commands
- `create_religion_sample_data`: Generate test data

## Customization

### Adding New Religion Types
1. Update `ReligionTypeChoice` in `models.py`
2. Add color mapping in `RELIGION_COLORS` (chart_generator.py)
3. Run migrations and update data

### Modifying Report Content
Edit the `ReligionReportFormatter` class methods:
- `_generate_introduction()`: Introduction text
- `_generate_recommendations()`: Policy recommendations
- `_generate_conclusion()`: Summary content

### Chart Styling
Modify the `ReligionChartGenerator` class:
- Colors: Update `RELIGION_COLORS` dictionary
- Layout: Adjust `fig_size`, `font_size_*` parameters
- Style: Change matplotlib style settings

## Testing

Run the comprehensive test suite:
```bash
python test_religion_system.py
```

The test covers:
- ✅ Model functionality
- ✅ View data processing
- ✅ Chart generation
- ✅ Report formatting
- ✅ PDF integration

## Sample Output

### Statistical Overview
> गाउँपालिकामा रहेका कुल ५,८५१ जनसंख्या मध्ये ४,२४७ अर्थात ७२.५९ प्रतिशत जनसंख्याले हिन्दु धर्म मान्दछन् भने दोस्रोमा बौद्ध धर्म मान्नेको संख्या १,४१९ अर्थात २४.२५ प्रतिशत रहेका छन् ।

### Ward Analysis
> वडा नं. ३ मा सबैभन्दा बढी धार्मिक विविधता (विविधता सूचकांक: ०.३४५) रहेको छ भने वडा नं. १ मा सबैभन्दा कम धार्मिक विविधता (विविधता सूचकांक: ०.१२३) रहेको छ ।

## Contributing

1. **Fork the repository**
2. **Create feature branch**: `git checkout -b feature/religion-enhancement`
3. **Make changes** following the existing code style
4. **Add tests** for new functionality
5. **Submit pull request** with detailed description

## License

This project is part of the Lungri Rural Municipality Digital Profile system.

## Support

For questions or issues:
1. Check the test suite output
2. Review the model relationships
3. Verify data integrity with management commands
4. Test individual components separately

---

**Note**: This system is designed to be easily extensible to other demographic categories (caste, language, occupation, etc.) following the same architectural pattern.
