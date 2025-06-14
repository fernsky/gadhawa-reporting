"""
Advanced page number calculation utilities for robust PDF generation
"""
import math
from typing import Dict, Any, List, Optional

class RobustPageCalculator:
    """
    Advanced page number calculator that provides accurate page tracking
    for all elements in the PDF report
    """
    
    def __init__(self):
        self.reset()
    
    def reset(self):
        """Reset all counters and tracking data"""
        self.front_matter_pages = {}
        self.content_pages = {}
        self.current_page = 1
        self.page_mappings = {
            'categories': {},
            'sections': {},
            'figures': {},
            'tables': {}
        }
    
    def estimate_content_length(self, content: str) -> int:
        """Estimate number of lines content will take"""
        if not content:
            return 0
        
        # Rough estimation: 80 characters per line, 45 lines per page
        chars_per_line = 80
        lines_per_page = 45
        
        # Remove HTML tags for better estimation
        import re
        clean_content = re.sub(r'<[^>]+>', '', content or '')
        
        # Estimate lines needed
        lines = max(1, len(clean_content) // chars_per_line + 1)
        return lines
    
    def calculate_front_matter_pages(self, categories, figures=None, tables=None):
        """Calculate pages needed for front matter sections"""
        pages = {}
        current_page = 1  # Start with Roman numeral i
        
        # Table of Contents
        toc_items = 0
        for category in categories:
            toc_items += 1  # Category itself
            toc_items += len(category.sections.all())  # All sections
        
        # Estimate TOC pages (roughly 30 items per page)
        toc_pages = max(1, math.ceil(toc_items / 30))
        pages['toc'] = {
            'start': current_page,
            'pages': toc_pages,
            'end': current_page + toc_pages - 1
        }
        current_page += toc_pages
        
        # List of Figures
        if figures and len(figures) > 0:
            fig_pages = max(1, math.ceil(len(figures) / 35))  # 35 items per page
            pages['figures'] = {
                'start': current_page,
                'pages': fig_pages,
                'end': current_page + fig_pages - 1
            }
            current_page += fig_pages
        
        # List of Tables
        if tables and len(tables) > 0:
            table_pages = max(1, math.ceil(len(tables) / 35))  # 35 items per page
            pages['tables'] = {
                'start': current_page,
                'pages': table_pages,
                'end': current_page + table_pages - 1
            }
            current_page += table_pages
        
        self.front_matter_pages = pages
        return pages
    
    def calculate_content_pages(self, categories):
        """Calculate pages for main content with detailed tracking"""
        current_page = 1  # Start main content at page 1
        
        for category in categories:
            category_start = current_page
            
            # Category title takes some space
            current_page += 0.1  # Small increment for title
            
            # Track category
            self.page_mappings['categories'][category.id] = int(math.ceil(current_page))
            
            for section in category.sections.all():
                section_start = current_page
                
                # Section header
                current_page += 0.1
                
                # Section content
                if hasattr(section, 'content_nepali') and section.content_nepali:
                    content_lines = self.estimate_content_length(section.content_nepali)
                elif hasattr(section, 'content') and section.content:
                    content_lines = self.estimate_content_length(section.content)
                else:
                    content_lines = 5  # Default placeholder content
                
                # Convert lines to pages (45 lines per page)
                content_pages = content_lines / 45
                current_page += content_pages
                
                # Section figures
                section_figures = getattr(section, 'figures', None)
                if section_figures:
                    for figure in section_figures.all():
                        # Each figure takes about 0.3 pages (including caption)
                        figure_page = math.ceil(current_page + 0.15)
                        self.page_mappings['figures'][figure.id] = figure_page
                        current_page += 0.3
                
                # Section tables
                section_tables = getattr(section, 'tables', None)
                if section_tables:
                    for table in section_tables.all():
                        # Each table takes about 0.4 pages (including data)
                        table_page = math.ceil(current_page + 0.2)
                        self.page_mappings['tables'][table.id] = table_page
                        current_page += 0.4
                
                # Track section
                self.page_mappings['sections'][section.id] = int(math.ceil(section_start))
            
            # Ensure each category starts on a new page
            current_page = math.ceil(current_page)
        
        return self.page_mappings
    
    def calculate_all_pages(self, categories, figures=None, tables=None):
        """Calculate all page numbers for the entire document"""
        # Calculate front matter
        front_matter = self.calculate_front_matter_pages(categories, figures, tables)
        
        # Calculate main content
        content_mapping = self.calculate_content_pages(categories)
        
        return {
            'front_matter': front_matter,
            'categories': content_mapping['categories'],
            'sections': content_mapping['sections'],
            'figures': content_mapping['figures'],
            'tables': content_mapping['tables']
        }


def format_nepali_page_number(page_num, use_roman=False):
    """Format page number in Nepali digits"""
    if use_roman:
        # Convert to Roman numerals first, then to Nepali
        roman_numerals = {
            1: 'i', 2: 'ii', 3: 'iii', 4: 'iv', 5: 'v',
            6: 'vi', 7: 'vii', 8: 'viii', 9: 'ix', 10: 'x',
            11: 'xi', 12: 'xii', 13: 'xiii', 14: 'xiv', 15: 'xv',
            20: 'xx', 25: 'xxv', 30: 'xxx', 40: 'xl', 50: 'l'
        }
        
        if page_num in roman_numerals:
            return roman_numerals[page_num]
        else:
            # For larger numbers, construct Roman numeral
            return str(page_num)  # Fallback to regular number
    
    # Convert Arabic numerals to Nepali
    nepali_digits = {
        '0': '०', '1': '१', '2': '२', '3': '३', '4': '४',
        '5': '५', '6': '६', '7': '७', '8': '८', '9': '९'
    }
    
    nepali_num = ''
    for digit in str(page_num):
        nepali_num += nepali_digits.get(digit, digit)
    
    return nepali_num


def calculate_pdf_page_numbers(categories, figures=None, tables=None):
    """Main function to calculate all page numbers for PDF generation"""
    calculator = RobustPageCalculator()
    return calculator.calculate_all_pages(categories, figures, tables)
