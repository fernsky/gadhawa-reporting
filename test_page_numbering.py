"""
Test the page numbering system for PDF generation
"""
import os
import sys
import django

# Add the project root to the Python path
project_root = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
sys.path.insert(0, project_root)

# Setup Django
os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'gadhawa_report.settings.development')
django.setup()

from apps.reports.models import ReportCategory, ReportSection, ReportFigure, ReportTable
from apps.reports.utils.page_calculator import calculate_pdf_page_numbers, format_nepali_page_number


def test_page_numbering():
    """Test the page numbering system"""
    print("=== Testing Page Numbering System ===")
    
    # Get sample data
    categories = ReportCategory.objects.filter(is_active=True)[:3]  # First 3 categories
    figures = ReportFigure.objects.all()[:10]  # First 10 figures
    tables = ReportTable.objects.all()[:5]  # First 5 tables
    
    print(f"Categories: {categories.count()}")
    print(f"Figures: {len(figures)}")
    print(f"Tables: {len(tables)}")
    
    # Calculate page numbers
    page_numbers = calculate_pdf_page_numbers(categories, figures, tables)
    
    print("\n=== Front Matter Pages ===")
    if 'front_matter' in page_numbers:
        for section, info in page_numbers['front_matter'].items():
            print(f"{section}: pages {info['start']}-{info['end']} ({info['pages']} pages)")
    
    print("\n=== Category Pages ===")
    for category in categories:
        page_num = page_numbers['categories'].get(category.id, 'N/A')
        nepali_page = format_nepali_page_number(page_num) if page_num != 'N/A' else 'N/A'
        print(f"{category.name}: Page {page_num} (Nepali: {nepali_page})")
    
    print("\n=== Section Pages ===")
    for category in categories:
        sections = category.sections.filter(is_published=True)[:3]  # First 3 sections
        for section in sections:
            page_num = page_numbers['sections'].get(section.id, 'N/A')
            nepali_page = format_nepali_page_number(page_num) if page_num != 'N/A' else 'N/A'
            print(f"  {section.title}: Page {page_num} (Nepali: {nepali_page})")
    
    print("\n=== Test Complete ===")
    return page_numbers


if __name__ == "__main__":
    test_page_numbering()
