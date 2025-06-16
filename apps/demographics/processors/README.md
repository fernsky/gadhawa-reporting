# Demographics Processing System

This system provides a unified, extensible pipeline for processing all demographic data categories in the Lungri Rural Municipality Digital Profile.

## Architecture

### 1. Base Classes (`processors/base.py`)
- **BaseDemographicsProcessor**: Abstract base class for all demographic processors
- **BaseChartGenerator**: Common SVG chart generation functionality
- **BaseReportFormatter**: Common report formatting utilities
- **DEMOGRAPHIC_COLORS**: Color palettes for different categories

### 2. Specific Processors
- **ReligionProcessor** (`processors/religion.py`): Handles religion demographics
- **LanguageProcessor** (`processors/language.py`): Handles mother tongue demographics  
- **CasteProcessor** (`processors/caste.py`): Handles caste demographics

### 3. Manager (`processors/manager.py`)
- **DemographicsManager**: Coordinates all processors and provides unified interface

### 4. Templates
- **`demographics/partials/demographics_section.html`**: Generic section template
- **`demographics/partials/all_demographics.html`**: Combined demographics template

## Usage

### Basic Usage
```python
from apps.demographics.processors.manager import get_demographics_manager

# Get manager instance
manager = get_demographics_manager()

# Process all categories for PDF
all_data = manager.process_all_for_pdf()

# Process specific category
religion_data = manager.process_category_for_pdf('religion')
```

### PDF Generation
The system is integrated into the PDF generation pipeline. All demographics data is available in templates via `all_demographics_data` context variable.

### Adding New Processors

1. **Create processor file** (`processors/your_category.py`):
```python
from .base import BaseDemographicsProcessor, BaseChartGenerator, BaseReportFormatter

class YourCategoryProcessor(BaseDemographicsProcessor):
    def get_section_title(self):
        return "Your Section Title"
    
    def get_section_number(self):
        return "3.X"
    
    def get_data(self):
        # Return processed data
        pass
    
    def generate_report_content(self, data):
        # Return formatted report content
        pass
    
    def generate_chart_svg(self, data, chart_type="pie"):
        # Return SVG chart
        pass
```

2. **Register in manager** (`processors/manager.py`):
```python
from .your_category import YourCategoryProcessor

class DemographicsManager:
    def __init__(self):
        self.processors = {
            'religion': ReligionProcessor(),
            'language': LanguageProcessor(),  
            'caste': CasteProcessor(),
            'your_category': YourCategoryProcessor(),  # Add here
        }
```

3. **Update templates** to include your category in `all_demographics.html`

## Benefits

1. **Consistency**: All demographic categories follow the same processing pattern
2. **Extensibility**: Easy to add new demographic categories
3. **Maintainability**: Common functionality is centralized
4. **Flexibility**: Each category can be customized while sharing base functionality
5. **PDF Focus**: Optimized for PDF generation with minimal code

## Migration from Old System

The new system maintains backward compatibility:
- Religion data is still available via `religion_data` context variable
- Chart data is available via `pdf_charts` context variable
- Report content is available via `coherent_analysis` context variable

New functionality is available via `all_demographics_data` which contains all processed categories.
