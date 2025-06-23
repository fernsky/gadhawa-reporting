# Demographics Processing System

This system provides a unified, extensible pipeline for processing all demographic data categories in the Gadhawa Rural Municipality Digital Profile with enhanced image generation capabilities.

## Architecture

### 1. Base Classes (`processors/base.py`)
- **BaseDemographicsProcessor**: Abstract base class for all demographic processors
- **BaseChartGenerator**: Common SVG chart generation functionality with Nepali text support
- **BaseReportFormatter**: Common report formatting utilities

### 2. Specific Processors
- **ReligionProcessor** (`processors/religion.py`): Handles religion demographics
- **LanguageProcessor** (`processors/language.py`): Handles mother tongue demographics  
- **CasteProcessor** (`processors/caste.py`): Handles caste demographics

### 3. Manager (`processors/manager.py`)
- **DemographicsManager**: Coordinates all processors and provides unified interface

### 4. Templates
- **`demographics/religion/religion_report_partial.html`**: Religion section template
- **`demographics/language/language_report_partial.html`**: Language section template
- **`demographics/caste/caste_report_partial.html`**: Caste section template

## Key Features

### Enhanced Chart Generation
- **Customizable Dimensions**: Each processor can specify custom width, height, and radius
- **Nepali Text Support**: All charts display Nepali labels and numbers
- **PNG Generation**: Automatic SVG to PNG conversion using Inkscape
- **Fallback Support**: SVG fallback if PNG conversion fails

### Chart Specifications
- **Religion Charts**: 900x450px with 130px radius
- **Language Charts**: 950x450px with 125px radius  
- **Caste Charts**: 900x450px with 130px radius

### Nepali Localization
- All chart labels use Nepali text (`name_nepali` field)
- Population numbers displayed in Nepali numerals
- Percentages formatted in Nepali
- Chart titles in Nepali

## Usage

### Basic Usage
```python
from apps.demographics.processors.manager import get_demographics_manager

# Get manager instance
manager = get_demographics_manager()

# Process all categories for PDF with PNG charts
all_data = manager.process_all_for_pdf()

# Process specific category
religion_data = manager.process_category_for_pdf('religion')

# Access generated charts
charts = religion_data['charts']
if 'pie_chart_png' in charts:
    png_url = charts['pie_chart_png']  # e.g., 'images/charts/religion_pie_chart.png'
```

### Custom Chart Dimensions
```python
class MyProcessor(BaseDemographicsProcessor):
    def __init__(self):
        super().__init__()
        # Customize chart dimensions
        self.pie_chart_width = 1000
        self.pie_chart_height = 500
        self.chart_radius = 150
```

### Template Usage
In your PDF templates, charts are automatically available:
```html
{% if pdf_charts.religion.pie_chart_png %}
    <img src="{% static pdf_charts.religion.pie_chart_png %}" alt="धर्म अनुसार जनसंख्या वितरण">
{% elif pdf_charts.religion.pie_chart_svg %}
    <img src="{% static pdf_charts.religion.pie_chart_svg %}" alt="धर्म अनुसार जनसंख्या वितरण">
{% endif %}
```

## Chart Generation Process

1. **Data Processing**: Each processor fetches and processes demographic data
2. **SVG Generation**: Charts generated as SVG with Nepali fonts and labels
3. **File Saving**: SVG files saved to `static/images/charts/`
4. **PNG Conversion**: Inkscape converts SVG to high-quality PNG (150 DPI)
5. **URL Generation**: Both PNG and SVG URLs provided for template use

## File Structure
```
static/images/charts/
├── religion_pie_chart.svg
├── religion_pie_chart.png
├── language_pie_chart.svg
├── language_pie_chart.png
├── caste_pie_chart.svg
└── caste_pie_chart.png
```

## Requirements

### System Requirements
- **Inkscape**: Required for PNG conversion
  ```bash
  # Windows (using Chocolatey)
  choco install inkscape
  
  # Ubuntu/Debian
  sudo apt-get install inkscape
  
  # macOS (using Homebrew)
  brew install inkscape
  ```

### Python Requirements
- Django with Nepali number formatting utilities
- Standard libraries: `xml.etree.ElementTree`, `subprocess`, `pathlib`

## Testing

### Test Scripts
- **`test_sample_charts.py`**: Tests chart generation with sample data
- **`test_chart_generation.py`**: Tests with actual database data

```bash
# Test chart generation
python test_sample_charts.py

# Test with real data
python test_chart_generation.py
```

## Adding New Processors

1. **Create processor file** (`processors/your_category.py`):
```python
from .base import BaseDemographicsProcessor, BaseChartGenerator

class YourCategoryProcessor(BaseDemographicsProcessor):
    def __init__(self):
        super().__init__()
        # Customize dimensions
        self.pie_chart_width = 800
        self.pie_chart_height = 400
        self.chart_radius = 120
    
    def get_section_title(self):
        return "Your Section Title"
    
    def get_data(self):
        # Return processed data with 'name_nepali' field
        pass
    
    def generate_chart_svg(self, data, chart_type="pie"):
        generator = self.YourChartGenerator(
            width=self.pie_chart_width,
            height=self.pie_chart_height,
            radius=self.chart_radius
        )
        return generator.generate_pie_chart_svg(data)
    
    class YourChartGenerator(BaseChartGenerator):
        COLORS = {'KEY': '#color'}
        
        def generate_pie_chart_svg(self, data):
            title = "Your Nepali Title"
            return self.generate_simple_pie_chart(data, self.COLORS, title)
```

2. **Register in manager** (`processors/manager.py`)
3. **Create template** following the pattern of existing templates
4. **Test with sample data**

## Troubleshooting

### PNG Conversion Issues
- Ensure Inkscape is installed and in PATH
- Check file permissions in static directory
- SVG fallback will be used automatically

### Font Issues
- Nepali fonts: Noto Sans Devanagari, Mangal, Kalimati
- Fonts embedded in SVG for better rendering
- Install Nepali fonts system-wide for best results

### Chart Not Displaying
- Check static file configuration
- Verify chart generation succeeded
- Ensure template paths are correct

## Benefits

1. **Consistency**: All demographic categories follow the same processing pattern
2. **Localization**: Full Nepali text support in charts and data
3. **Quality**: High-resolution PNG charts for professional PDFs
4. **Extensibility**: Easy to add new demographic categories
5. **Maintainability**: Common functionality centralized
6. **Flexibility**: Customizable dimensions per category
7. **Reliability**: Fallback mechanisms for chart generation
