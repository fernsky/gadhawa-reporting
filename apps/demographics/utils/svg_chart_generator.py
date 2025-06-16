"""
Simple SVG Chart Generator

This module generates basic SVG charts for embedding in PDFs.
"""

import xml.etree.ElementTree as ET
import math
import os
import subprocess
from pathlib import Path

# Color palette for religions
RELIGION_COLORS = {
    'HINDU': '#FF6B35',      # Orange
    'BUDDHIST': '#F7931E',   # Golden
    'KIRANT': '#1f77b4',     # Blue  
    'CHRISTIAN': '#2ca02c',  # Green
    'ISLAM': '#17becf',      # Cyan
    'NATURE': '#8c564b',     # Brown
    'BON': '#e377c2',        # Pink
    'JAIN': '#bcbd22',       # Olive
    'BAHAI': '#9467bd',      # Purple
    'SIKH': '#ff7f0e',       # Orange variant
    'OTHER': '#7f7f7f'       # Gray
}

# English labels for religions
RELIGION_LABELS = {
    'HINDU': 'Hindu',
    'BUDDHIST': 'Buddhist', 
    'KIRANT': 'Kirant',
    'CHRISTIAN': 'Christian',
    'ISLAM': 'Islam',
    'NATURE': 'Nature',
    'BON': 'Bon',
    'JAIN': 'Jain',
    'BAHAI': 'Bahai',
    'SIKH': 'Sikh',
    'OTHER': 'Other'
}


class SVGChartGenerator:
    """Generates simple SVG charts"""
    
    def __init__(self):
        self.font_family = "Arial, sans-serif"
        self.font_size_title = 18
        self.font_size_labels = 14
        self.font_size_legend = 12
        self.use_english_fallback = False  # Default to showing Nepali text
    
    def _create_svg(self, width, height):
        """Create basic SVG element"""
        return ET.Element('svg', {
            'width': str(width),
            'height': str(height),
            'xmlns': 'http://www.w3.org/2000/svg'
        })
    
    def _create_svg_with_embedded_font(self, width, height):
        """Create SVG element with embedded font support"""
        return self._create_svg(width, height)
    
    def _get_display_label(self, religion_type, nepali_name):
        """Get display label for religion - Nepali name or English fallback"""
        if self.use_english_fallback:
            return RELIGION_LABELS.get(religion_type, religion_type)
        else:
            return nepali_name if nepali_name else RELIGION_LABELS.get(religion_type, religion_type)
    
    def _safe_title(self, nepali_title, english_title):
        """Return appropriate title based on language preference"""
        if self.use_english_fallback:
            return english_title
        else:
            return nepali_title
    
    def _convert_number_to_nepali(self, number):
        """Convert English numbers to Nepali numerals"""
        if self.use_english_fallback:
            return str(number)
        
        # Nepali digit mapping
        nepali_digits = {
            '0': '०', '1': '१', '2': '२', '3': '३', '4': '४',
            '5': '५', '6': '६', '7': '७', '8': '८', '9': '९'
        }
        
        result = str(number)
        for eng, nep in nepali_digits.items():
            result = result.replace(eng, nep)
        
        return result
    
    def generate_pie_chart_svg(self, religion_data, include_title=False):
        """Generate pie chart as SVG with proper font embedding"""
        try:
            # Filter out religions with zero population
            filtered_data = {k: v for k, v in religion_data.items() if v['population'] > 0}
            
            if not filtered_data:
                return None
            
            # Prepare data
            labels = []
            values = []
            colors = []
            
            for religion_type, data in filtered_data.items():
                nepali_name = str(data['name_nepali']) if data['name_nepali'] else religion_type
                labels.append(self._get_display_label(religion_type, nepali_name))
                values.append(data['population'])
                colors.append(RELIGION_COLORS.get(religion_type, '#7f7f7f'))
            
            # Calculate percentages and angles
            total = sum(values)
            percentages = [v / total * 100 for v in values]
            angles = [p / 100 * 360 for p in percentages]
            
            # SVG dimensions - compact size without excessive padding
            width, height = 600, 450
            center_x, center_y = width // 2, height // 2 - 10
            radius = 120
            
            # Create SVG
            svg = self._create_svg_with_embedded_font(width, height)
            
            # Add title only if requested
            title_offset = 0
            if include_title:
                title = self._safe_title('धर्म अनुसार जनसंख्या वितरण', 'Population Distribution by Religion')
                title_elem = ET.SubElement(svg, 'text', {
                    'x': str(center_x),
                    'y': '25',
                    'text-anchor': 'middle',
                    'font-family': self.font_family,
                    'font-size': str(self.font_size_title),
                    'font-weight': 'bold',
                    'fill': 'black'
                })
                title_elem.text = title
                title_offset = 30
            
            # Draw pie slices
            start_angle = -90  # Start from top
            for i, (label, value, color, angle) in enumerate(zip(labels, values, colors, angles)):
                end_angle = start_angle + angle
                
                # Calculate slice path
                start_x = center_x + radius * math.cos(math.radians(start_angle))
                start_y = center_y + radius * math.sin(math.radians(start_angle))
                end_x = center_x + radius * math.cos(math.radians(end_angle))
                end_y = center_y + radius * math.sin(math.radians(end_angle))
                
                large_arc = "1" if angle > 180 else "0"
                
                path_data = f"M {center_x} {center_y} L {start_x} {start_y} A {radius} {radius} 0 {large_arc} 1 {end_x} {end_y} Z"
                
                # Create slice
                slice_elem = ET.SubElement(svg, 'path', {
                    'd': path_data,
                    'fill': color,
                    'stroke': 'white',
                    'stroke-width': '2'
                })
                
                # Add percentage text on slice
                mid_angle = start_angle + angle / 2
                text_x = center_x + (radius * 0.7) * math.cos(math.radians(mid_angle))
                text_y = center_y + (radius * 0.7) * math.sin(math.radians(mid_angle))
                
                percentage_text = f"{percentages[i]:.1f}%"
                if not self.use_english_fallback:
                    percentage_text = self._convert_number_to_nepali(f"{percentages[i]:.1f}") + "%"
                
                text_elem = ET.SubElement(svg, 'text', {
                    'x': str(text_x),
                    'y': str(text_y),
                    'text-anchor': 'middle',
                    'dominant-baseline': 'middle',
                    'font-family': self.font_family,
                    'font-size': str(self.font_size_labels - 2),
                    'font-weight': 'bold',
                    'fill': 'white'
                })
                text_elem.text = percentage_text
                
                start_angle = end_angle
            
            # Add legend - positioned more compactly
            legend_x = center_x + radius + 30
            legend_y = center_y - (len(labels) * 20) // 2
            
            # Skip legend title to save space
            for i, (label, value, color) in enumerate(zip(labels, values, colors)):
                y_pos = legend_y + i * 20
                
                # Legend color box
                ET.SubElement(svg, 'rect', {
                    'x': str(legend_x),
                    'y': str(y_pos - 6),
                    'width': '12',
                    'height': '12',
                    'fill': color,
                    'stroke': 'black',
                    'stroke-width': '1'
                })
                
                # Legend text - more compact
                nepali_count = self._convert_number_to_nepali(value)
                legend_text = f"{label} ({nepali_count})" if not self.use_english_fallback else f"{label} ({value})"
                
                text_elem = ET.SubElement(svg, 'text', {
                    'x': str(legend_x + 16),
                    'y': str(y_pos),
                    'dominant-baseline': 'middle',
                    'font-family': self.font_family,
                    'font-size': str(self.font_size_legend - 1),
                    'fill': 'black'
                })
                text_elem.text = legend_text
            
            # Convert to string
            return ET.tostring(svg, encoding='unicode')
            
        except Exception as e:
            print(f"Error creating SVG pie chart: {e}")
            import traceback
            traceback.print_exc()
            return None
    
    def generate_bar_chart_svg(self, ward_data, include_title=False):
        """Generate bar chart as SVG"""
        try:
            if not ward_data:
                return None
            
            # Prepare data
            wards = sorted(ward_data.keys())
            
            # Get all religions present in the data
            all_religions = set()
            for ward_info in ward_data.values():
                all_religions.update(ward_info['religions'].keys())
            
            # Filter out religions with no data
            active_religions = []
            for religion in sorted(all_religions):
                total_pop = sum(
                    ward_data[ward]['religions'].get(religion, {}).get('population', 0) 
                    for ward in wards
                )
                if total_pop > 0:
                    active_religions.append(religion)
            
            if not active_religions:
                return None
            
            # SVG dimensions - more compact
            width, height = 800, 450
            margin = {'top': 30 if include_title else 20, 'right': 150, 'bottom': 60, 'left': 60}
            chart_width = width - margin['left'] - margin['right']
            chart_height = height - margin['top'] - margin['bottom']
            
            # Create SVG
            svg = self._create_svg_with_embedded_font(width, height)
            
            # Add title only if requested
            if include_title:
                title = self._safe_title('वडा अनुसार धार्मिक जनसंख्या वितरण', 'Religious Population by Ward')
                title_elem = ET.SubElement(svg, 'text', {
                    'x': str(width // 2),
                    'y': '25',
                    'text-anchor': 'middle',
                    'font-family': self.font_family,
                    'font-size': str(self.font_size_title),
                    'font-weight': 'bold',
                    'fill': 'black'
                })
                title_elem.text = title
            
            # Calculate bar positions
            bar_width = chart_width / len(wards)
            max_population = max(
                sum(ward_data[ward]['religions'].get(religion, {}).get('population', 0) 
                    for religion in active_religions)
                for ward in wards
            )
            
            # Draw bars for each ward
            for i, ward in enumerate(wards):
                x = margin['left'] + i * bar_width
                bottom = margin['top'] + chart_height
                
                # Stack religions for this ward
                current_y = bottom
                for religion in active_religions:
                    pop = ward_data[ward]['religions'].get(religion, {}).get('population', 0)
                    if pop > 0:
                        bar_height = (pop / max_population) * chart_height
                        color = RELIGION_COLORS.get(religion, '#7f7f7f')
                        
                        # Draw bar segment
                        ET.SubElement(svg, 'rect', {
                            'x': str(x + bar_width * 0.1),
                            'y': str(current_y - bar_height),
                            'width': str(bar_width * 0.8),
                            'height': str(bar_height),
                            'fill': color,
                            'stroke': 'white',
                            'stroke-width': '1'
                        })
                        
                        current_y -= bar_height
                
                # Ward label
                ward_label = f"वडा {self._convert_number_to_nepali(ward)}" if not self.use_english_fallback else f"Ward {ward}"
                text_elem = ET.SubElement(svg, 'text', {
                    'x': str(x + bar_width / 2),
                    'y': str(bottom + 20),
                    'text-anchor': 'middle',
                    'font-family': self.font_family,
                    'font-size': str(self.font_size_labels),
                    'fill': 'black'
                })
                text_elem.text = ward_label
            
            # Add legend - more compact
            legend_x = width - margin['right'] + 10
            legend_y = margin['top'] + 10
            
            # Skip legend title to save space
            for i, religion in enumerate(active_religions):
                y_pos = legend_y + i * 20
                color = RELIGION_COLORS.get(religion, '#7f7f7f')
                
                # Legend color box
                ET.SubElement(svg, 'rect', {
                    'x': str(legend_x),
                    'y': str(y_pos - 6),
                    'width': '12',
                    'height': '12',
                    'fill': color,
                    'stroke': 'black',
                    'stroke-width': '1'
                })
                
                # Legend text
                religion_data = None
                for ward in wards:
                    if religion in ward_data[ward]['religions']:
                        religion_data = ward_data[ward]['religions'][religion]
                        break
                
                if religion_data:
                    nepali_name = str(religion_data.get('name_nepali', religion))
                    label = self._get_display_label(religion, nepali_name)
                else:
                    label = RELIGION_LABELS.get(religion, religion)
                
                text_elem = ET.SubElement(svg, 'text', {
                    'x': str(legend_x + 16),
                    'y': str(y_pos),
                    'dominant-baseline': 'middle',
                    'font-family': self.font_family,
                    'font-size': str(self.font_size_legend - 1),
                    'fill': 'black'
                })
                text_elem.text = label
            
            # Convert to string
            return ET.tostring(svg, encoding='unicode')
            
        except Exception as e:
            print(f"Error creating SVG bar chart: {e}")
            import traceback
            traceback.print_exc()
            return None
    
    def save_svg_to_file(self, svg_content, filename):
        """Save SVG content to file"""
        try:
            with open(filename, 'w', encoding='utf-8') as f:
                f.write(svg_content)
            return True
        except Exception as e:
            print(f"Error saving SVG: {e}")
            return False
    
    def generate_chart_image(self, religion_data, output_name, static_dir="static/images", 
                           chart_type="pie", include_title=False):
        """
        Generate chart image using Inkscape conversion
        
        Args:
            religion_data: Data for the chart
            output_name: Base name for the output files (without extension)
            static_dir: Directory to save images
            chart_type: Type of chart ('pie' or 'bar')
            include_title: Whether to include title in the chart
            
        Returns:
            tuple: (success, png_path, svg_path)
        """
        try:
            # Ensure static directory exists
            static_path = Path(static_dir)
            static_path.mkdir(parents=True, exist_ok=True)
            
            # Generate SVG
            if chart_type == "pie":
                svg_content = self.generate_pie_chart_svg(religion_data, include_title=include_title)
            elif chart_type == "bar":
                svg_content = self.generate_bar_chart_svg(religion_data, include_title=include_title)
            else:
                raise ValueError(f"Unsupported chart type: {chart_type}")
            
            if not svg_content:
                return False, None, None
            
            # Define file paths
            svg_path = static_path / f"{output_name}.svg"
            png_path = static_path / f"{output_name}.png"
            
            # Save SVG file
            if not self.save_svg_to_file(svg_content, str(svg_path)):
                return False, None, None
            
            # Convert to PNG using Inkscape
            try:
                # Try to run Inkscape command
                cmd = [
                    "inkscape",
                    str(svg_path),
                    "--export-type=png",
                    f"--export-filename={png_path}",
                    "--export-dpi=150"  # High quality for PDF
                ]
                
                result = subprocess.run(cmd, capture_output=True, text=True, timeout=30)
                
                if result.returncode == 0:
                    print(f"✓ Chart generated: {png_path}")
                    return True, str(png_path), str(svg_path)
                else:
                    print(f"Inkscape error: {result.stderr}")
                    return False, None, str(svg_path)
                    
            except subprocess.TimeoutExpired:
                print("Inkscape conversion timed out")
                return False, None, str(svg_path)
            except FileNotFoundError:
                print("Inkscape not found. Please install Inkscape and add it to PATH")
                return False, None, str(svg_path)
            except Exception as e:
                print(f"Error running Inkscape: {e}")
                return False, None, str(svg_path)
                
        except Exception as e:
            print(f"Error generating chart image: {e}")
            import traceback
            traceback.print_exc()
            return False, None, None
    
    @staticmethod
    def generate_religion_charts(religion_data, municipality_name=""):
        """
        Generate all religion-related charts for a municipality
        
        Args:
            religion_data: Dictionary of religion data
            municipality_name: Name of municipality for unique filenames
            
        Returns:
            dict: Dictionary with chart information
        """
        generator = SVGChartGenerator()
        charts_info = {}
        
        # Generate pie chart
        output_name = f"religion_pie_chart_{municipality_name}".replace(" ", "_").lower()
        success, png_path, svg_path = generator.generate_chart_image(
            religion_data=religion_data,
            output_name=output_name,
            static_dir="static/images",
            chart_type="pie",
            include_title=False
        )
        
        if success:
            charts_info['pie_chart'] = {
                'png_path': png_path,
                'svg_path': svg_path,
                'success': True
            }
        else:
            charts_info['pie_chart'] = {
                'png_path': None,
                'svg_path': svg_path,
                'success': False
            }
        
        return charts_info
