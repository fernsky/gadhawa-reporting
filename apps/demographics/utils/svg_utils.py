"""
SVG Utilities

Provides common functionality for handling SVG charts and files.
"""

import xml.etree.ElementTree as ET
from pathlib import Path

class SVGUtils:
    """Utility class for SVG operations"""

    @staticmethod
    def create_svg(width, height):
        """Create basic SVG element"""
        return ET.Element('svg', {
            'width': str(width),
            'height': str(height),
            'xmlns': 'http://www.w3.org/2000/svg'
        })

    @staticmethod
    def save_svg_to_file(svg_content, filename):
        """Save SVG content to file"""
        try:
            Path(filename).write_text(svg_content, encoding='utf-8')
            return True
        except Exception as e:
            print(f"Error saving SVG to file: {e}")
            return False

    @staticmethod
    def convert_number_to_nepali(number):
        """Convert English numbers to Nepali numerals"""
        nepali_digits = {
            '0': '०', '1': '१', '2': '२', '3': '३', '4': '४',
            '5': '५', '6': '६', '7': '७', '8': '८', '9': '९'
        }
        result = str(number)
        for eng, nep in nepali_digits.items():
            result = result.replace(eng, nep)
        return result
