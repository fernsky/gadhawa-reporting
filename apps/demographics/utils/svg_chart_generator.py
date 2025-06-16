"""
Simple SVG Chart Generator

This module generates basic SVG charts for embedding in PDFs.
Can be used for any demographic data including religion, language, caste, etc.
"""

import xml.etree.ElementTree as ET
import math
import os
import subprocess
from pathlib import Path

# Default color palette - can be overridden
DEFAULT_COLORS = {
    'DEFAULT_1': '#1f77b4',   # Blue
    'DEFAULT_2': '#ff7f0e',   # Orange
    'DEFAULT_3': '#2ca02c',   # Green
    'DEFAULT_4': '#d62728',   # Red
    'DEFAULT_5': '#9467bd',   # Purple
    'DEFAULT_6': '#8c564b',   # Brown
    'DEFAULT_7': '#e377c2',   # Pink
    'DEFAULT_8': '#7f7f7f',   # Gray
    'DEFAULT_9': '#bcbd22',   # Olive
    'DEFAULT_10': '#17becf',  # Cyan
    'DEFAULT_11': '#ff9896',  # Light Red
    'DEFAULT_12': '#98df8a',  # Light Green
    'DEFAULT_13': '#aec7e8',  # Light Blue
    'DEFAULT_14': '#ffbb78',  # Light Orange
    'DEFAULT_15': '#c5b0d5',  # Light Purple
    'DEFAULT_16': '#c49c94',  # Light Brown
    'DEFAULT_17': '#f7b6d3',  # Light Pink
    'DEFAULT_18': '#c7c7c7',  # Light Gray
    'DEFAULT_19': '#dbdb8d',  # Light Olive
    'DEFAULT_20': '#9edae5',  # Light Cyan
}

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

# Color palette for languages
LANGUAGE_COLORS = {
    'NEPALI': '#1f77b4',
    'LIMBU': '#ff7f0e',
    'RAI': '#2ca02c',
    'HINDI': '#d62728',
    'NEWARI': '#9467bd',
    'SHERPA': '#8c564b',
    'TAMANG': '#e377c2',
    'MAITHILI': '#7f7f7f',
    'BHOJPURI': '#bcbd22',
    'THARU': '#17becf',
    'BAJJIKA': '#ff9896',
    'MAGAR': '#98df8a',
    'DOTELI': '#aec7e8',
    'URDU': '#ffbb78',
    'AWADI': '#c5b0d5',
    'GURUNG': '#c49c94',
    'ENGLISH': '#f7b6d3',
    'OTHER': '#c7c7c7'
}

# Color palette for castes
CASTE_COLORS = {
    'BRAHMIN': '#1f77b4',
    'CHHETRI': '#ff7f0e',
    'MAGAR': '#2ca02c',
    'TAMANG': '#d62728',
    'NEWAR': '#9467bd',
    'THARU': '#8c564b',
    'GURUNG': '#e377c2',
    'RAI': '#7f7f7f',
    'LIMBU': '#bcbd22',
    'SHERPA': '#17becf',
    'DALIT': '#ff9896',
    'MADHESI': '#98df8a',
    'MUSLIM': '#aec7e8',
    'OTHER': '#c7c7c7'
}


class SVGChartGenerator:
    """Generates simple SVG charts for any demographic data"""
    
    def __init__(self, colors=None):
        self.font_family = "Arial, sans-serif"
        self.font_size_title = 18
        self.font_size_labels = 14
        self.font_size_legend = 12
        self.use_english_fallback = False  # Default to showing Nepali text
        self.colors = colors or DEFAULT_COLORS  # Allow custom color palette
    
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
    
    def _get_display_label(self, data_type, nepali_name):
        """Get display label - Nepali name or fallback to data type"""
        if self.use_english_fallback:
            return str(data_type)
        else:
            return str(nepali_name) if nepali_name else str(data_type)
    
    def _safe_title(self, nepali_title, english_title):
        """Return appropriate title based on language preference"""
        if self.use_english_fallback:
            return str(english_title)
        else:
            return str(nepali_title)
    
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
    
    def _get_color_for_item(self, item_key, index=0):
        """Get color for a data item"""
        if item_key in self.colors:
            return self.colors[item_key]
        else:
            # Use default colors cycling through the palette
            color_keys = list(DEFAULT_COLORS.keys())
            return DEFAULT_COLORS[color_keys[index % len(color_keys)]]
    
    def generate_pie_chart_svg(self, demographic_data, include_title=False, title_nepali="", title_english=""):
        """Generate pie chart as SVG with proper font embedding"""
        try:
            # Filter out entries with zero population
            filtered_data = {}
            for k, v in demographic_data.items():
                if isinstance(v, dict) and v.get('population', 0) > 0:
                    filtered_data[k] = v
                elif isinstance(v, (int, float)) and v > 0:
                    # Handle case where demographic_data contains direct values
                    filtered_data[k] = {'population': v, 'name_nepali': str(k)}
            
            if not filtered_data:
                return None
            
            # Prepare data
            labels = []
            values = []
            colors = []
            
            for i, (data_type, data) in enumerate(filtered_data.items()):
                nepali_name = str(data.get('name_nepali', data_type)) if data.get('name_nepali') else data_type
                labels.append(self._get_display_label(data_type, nepali_name))
                values.append(data['population'])
                colors.append(self._get_color_for_item(data_type, i))
            
            # Calculate percentages and angles
            total = sum(values)
            percentages = [v / total * 100 for v in values]
            angles = [p / 100 * 360 for p in percentages]
            
            # SVG dimensions - compact size without excessive padding
            width, height = 600, 300
            center_x, center_y = width // 2, height // 2 - 10
            radius = 120
            
            # Create SVG
            svg = self._create_svg_with_embedded_font(width, height)
            
            # Add title only if requested
            title_offset = 0
            if include_title and (title_nepali or title_english):
                title = self._safe_title(title_nepali, title_english)
                title_elem = ET.SubElement(svg, 'text', {
                    'x': str(center_x),
                    'y': '25',
                    'text-anchor': 'middle',
                    'font-family': self.font_family,
                    'font-size': str(self.font_size_title),
                    'font-weight': 'bold',
                    'fill': 'black'
                })
                title_elem.text = str(title)
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
                text_elem.text = str(percentage_text)
                
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
                text_elem.text = str(legend_text)
            
            # Convert to string
            return ET.tostring(svg, encoding='unicode')
            
        except Exception as e:
            print(f"Error creating SVG pie chart: {e}")
            import traceback
            traceback.print_exc()
            return None
    
    def generate_bar_chart_svg(self, ward_data, include_title=False, title_nepali="", title_english=""):
        """Generate bar chart as SVG for ward-wise demographic data"""
        try:
            if not ward_data:
                return None
            
            # Prepare data - convert ward numbers to strings for consistent sorting
            wards = []
            for ward_key in ward_data.keys():
                if isinstance(ward_key, (int, float)):
                    wards.append(str(int(ward_key)))
                else:
                    wards.append(str(ward_key))
            wards = sorted(wards, key=lambda x: int(x) if x.isdigit() else float('inf'))
            
            # Get all demographic categories present in the data
            all_categories = set()
            for ward_key, ward_info in ward_data.items():
                if isinstance(ward_info, dict) and 'demographics' in ward_info:
                    all_categories.update(ward_info['demographics'].keys())
                elif isinstance(ward_info, dict):
                    # Filter out non-demographic keys
                    for key in ward_info.keys():
                        if key not in ['ward_name', 'total_population']:
                            all_categories.add(key)
            
            # Convert all categories to strings for consistent sorting
            all_categories = [str(cat) for cat in all_categories]
            
            # Filter out categories with no data
            active_categories = []
            for category in sorted(all_categories):
                total_pop = 0
                for ward_key in ward_data.keys():
                    ward_key_str = str(ward_key)
                    try:
                        ward_info = ward_data[ward_key]
                        if isinstance(ward_info, dict):
                            if 'demographics' in ward_info:
                                demographics = ward_info['demographics']
                                if category in demographics:
                                    demo_data = demographics[category]
                                    if isinstance(demo_data, dict) and 'population' in demo_data:
                                        total_pop += demo_data['population']
                                    elif isinstance(demo_data, (int, float)):
                                        total_pop += demo_data
                            else:
                                # Direct demographic data
                                if category in ward_info:
                                    demo_data = ward_info[category]
                                    if isinstance(demo_data, dict) and 'population' in demo_data:
                                        total_pop += demo_data['population']
                                    elif isinstance(demo_data, (int, float)):
                                        total_pop += demo_data
                    except (TypeError, AttributeError, KeyError):
                        continue
                        
                if total_pop > 0:
                    active_categories.append(category)
            
            if not active_categories:
                return None
            
            # SVG dimensions - improved layout with more space for legend
            width, height = 800, 520
            margin = {'top': 30 if include_title else 20, 'right': 20, 'bottom': 100, 'left': 70}
            chart_width = width - margin['left'] - margin['right']
            chart_height = height - margin['top'] - margin['bottom']
            
            # Create SVG
            svg = self._create_svg_with_embedded_font(width, height)
            
            # Add title only if requested
            if include_title and (title_nepali or title_english):
                title = self._safe_title(title_nepali, title_english)
                title_elem = ET.SubElement(svg, 'text', {
                    'x': str(width // 2),
                    'y': '25',
                    'text-anchor': 'middle',
                    'font-family': self.font_family,
                    'font-size': str(self.font_size_title),
                    'font-weight': 'bold',
                    'fill': 'black'
                })
                title_elem.text = str(title)
            
            # Calculate bar positions and max population
            bar_width = chart_width / len(wards)
            max_population = 0
            
            # Get maximum population for scaling
            for ward_str in wards:
                # Find the actual ward key in ward_data
                ward_key = None
                for k in ward_data.keys():
                    if str(k) == ward_str:
                        ward_key = k
                        break
                
                if ward_key is None:
                    continue
                    
                ward_total = 0
                ward_info = ward_data[ward_key]
                
                for category in active_categories:
                    pop = 0
                    if isinstance(ward_info, dict):
                        if 'demographics' in ward_info:
                            demo_data = ward_info['demographics'].get(category, {})
                            if isinstance(demo_data, dict):
                                pop = demo_data.get('population', 0)
                            elif isinstance(demo_data, (int, float)):
                                pop = demo_data
                        else:
                            demo_data = ward_info.get(category, {})
                            if isinstance(demo_data, dict):
                                pop = demo_data.get('population', 0)
                            elif isinstance(demo_data, (int, float)):
                                pop = demo_data
                    ward_total += pop
                    
                max_population = max(max_population, ward_total)
            
            if max_population == 0:
                return None
            
            # Draw Y-axis and grid lines with elevated baseline
            y_axis_x = margin['left']
            chart_top = margin['top']
            chart_bottom = margin['top'] + chart_height
            baseline_offset = 15  # Elevate the baseline so bars appear elevated
            effective_chart_height = chart_height - baseline_offset
            effective_chart_bottom = chart_bottom - baseline_offset
            
            # Y-axis line (with elevated baseline)
            ET.SubElement(svg, 'line', {
                'x1': str(y_axis_x),
                'y1': str(chart_top),
                'x2': str(y_axis_x),
                'y2': str(effective_chart_bottom),
                'stroke': 'black',
                'stroke-width': '2'
            })
            
            # Y-axis scale and grid lines
            scale_steps = 5
            step_value = max_population / scale_steps
            
            for i in range(scale_steps + 1):
                value = i * step_value
                y_pos = effective_chart_bottom - (i * effective_chart_height / scale_steps)
                
                # Horizontal grid line
                ET.SubElement(svg, 'line', {
                    'x1': str(y_axis_x),
                    'y1': str(y_pos),
                    'x2': str(y_axis_x + chart_width),
                    'y2': str(y_pos),
                    'stroke': '#e0e0e0' if i > 0 else 'black',
                    'stroke-width': '1' if i > 0 else '2',
                    'stroke-dasharray': '2,2' if i > 0 else 'none'
                })
                
                # Y-axis tick mark
                ET.SubElement(svg, 'line', {
                    'x1': str(y_axis_x - 5),
                    'y1': str(y_pos),
                    'x2': str(y_axis_x),
                    'y2': str(y_pos),
                    'stroke': 'black',
                    'stroke-width': '1'
                })
                
                # Y-axis label
                if i == 0:
                    scale_text = "०"
                else:
                    scale_text = self._convert_number_to_nepali(int(value))
                    
                ET.SubElement(svg, 'text', {
                    'x': str(y_axis_x - 8),
                    'y': str(y_pos),
                    'text-anchor': 'end',
                    'dominant-baseline': 'middle',
                    'font-family': self.font_family,
                    'font-size': str(self.font_size_labels - 3),
                    'fill': 'black'
                }).text = str(scale_text)
            
            # Draw bars for each ward
            for i, ward_str in enumerate(wards):
                # Find the actual ward key in ward_data
                ward_key = None
                for k in ward_data.keys():
                    if str(k) == ward_str:
                        ward_key = k
                        break
                
                if ward_key is None:
                    continue
                
                x = margin['left'] + i * bar_width
                bottom = effective_chart_bottom  # Use elevated baseline
                ward_info = ward_data[ward_key]
                
                # Stack categories for this ward
                current_y = bottom
                ward_total = 0
                
                for j, category in enumerate(active_categories):
                    pop = 0
                    if isinstance(ward_info, dict):
                        if 'demographics' in ward_info:
                            demo_data = ward_info['demographics'].get(category, {})
                            if isinstance(demo_data, dict):
                                pop = demo_data.get('population', 0)
                            elif isinstance(demo_data, (int, float)):
                                pop = demo_data
                        else:
                            demo_data = ward_info.get(category, {})
                            if isinstance(demo_data, dict):
                                pop = demo_data.get('population', 0)
                            elif isinstance(demo_data, (int, float)):
                                pop = demo_data
                    
                    if pop > 0:
                        bar_height = (pop / max_population) * effective_chart_height  # Use effective height
                        color = self._get_color_for_item(category, j)
                        
                        # Draw bar segment
                        ET.SubElement(svg, 'rect', {
                            'x': str(x + bar_width * 0.15),
                            'y': str(current_y - bar_height),
                            'width': str(bar_width * 0.7),
                            'height': str(bar_height),
                            'fill': color,
                            'stroke': 'white',
                            'stroke-width': '1'
                        })
                        
                        # Add value label on bar if significant height
                        if bar_height > 20:
                            value_text = self._convert_number_to_nepali(pop)
                            ET.SubElement(svg, 'text', {
                                'x': str(x + bar_width / 2),
                                'y': str(current_y - bar_height / 2),
                                'text-anchor': 'middle',
                                'dominant-baseline': 'middle',
                                'font-family': self.font_family,
                                'font-size': str(self.font_size_labels - 2),
                                'font-weight': 'bold',
                                'fill': 'white'
                            }).text = str(value_text)
                        
                        current_y -= bar_height
                        ward_total += pop
                
                # Ward label (positioned below the elevated baseline with more spacing)
                ward_label = f"वडा {self._convert_number_to_nepali(ward_str)}" if not self.use_english_fallback else f"Ward {ward_str}"
                ET.SubElement(svg, 'text', {
                    'x': str(x + bar_width / 2),
                    'y': str(chart_bottom + 25),  # More space from the chart bottom
                    'text-anchor': 'middle',
                    'font-family': self.font_family,
                    'font-size': str(self.font_size_labels - 2),
                    'fill': 'black'
                }).text = str(ward_label)
                
                # Total value label above bar
                if ward_total > 0:
                    total_text = self._convert_number_to_nepali(ward_total)
                    ET.SubElement(svg, 'text', {
                        'x': str(x + bar_width / 2),
                        'y': str(current_y - 5),
                        'text-anchor': 'middle',
                        'font-family': self.font_family,
                        'font-size': str(self.font_size_labels - 3),
                        'fill': 'black'
                    }).text = str(total_text)
            
            # Add horizontal legend at bottom with more spacing
            legend_y = height - margin['bottom'] + 45  # More space between chart and legend
            total_legend_width = 0
            legend_items = []
            
            # Calculate total width needed for legend
            for i, category in enumerate(active_categories):
                category_data = None
                for ward_key in ward_data.keys():
                    ward_info = ward_data[ward_key]
                    if isinstance(ward_info, dict):
                        if 'demographics' in ward_info and category in ward_info['demographics']:
                            category_data = ward_info['demographics'][category]
                            break
                        elif category in ward_info:
                            category_data = ward_info[category]
                            break
                
                if category_data and isinstance(category_data, dict) and 'name_nepali' in category_data:
                    label = self._get_display_label(category, category_data['name_nepali'])
                else:
                    label = str(category)
                
                # Estimate text width (rough approximation)
                text_width = len(label) * 6  # Approximate character width
                item_width = 12 + 4 + text_width + 15  # colorbox + spacing + text + margin
                legend_items.append((category, label, item_width))
                total_legend_width += item_width
            
            # Center the legend
            legend_start_x = (width - total_legend_width) / 2
            current_x = legend_start_x
            
            # Draw legend items grouped together
            for i, (category, label, item_width) in enumerate(legend_items):
                color = self._get_color_for_item(category, i)
                
                # Legend color box
                ET.SubElement(svg, 'rect', {
                    'x': str(current_x),
                    'y': str(legend_y - 6),
                    'width': '12',
                    'height': '12',
                    'fill': color,
                    'stroke': 'black',
                    'stroke-width': '1'
                })
                
                # Legend text
                ET.SubElement(svg, 'text', {
                    'x': str(current_x + 16),
                    'y': str(legend_y),
                    'dominant-baseline': 'middle',
                    'font-family': self.font_family,
                    'font-size': str(self.font_size_legend - 1),
                    'fill': 'black'
                }).text = str(label)
                
                # Move to next position
                current_x += item_width
            
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
    
    def generate_chart_image(self, demographic_data, output_name, static_dir="static/images", 
                           chart_type="pie", include_title=False, title_nepali="", title_english=""):
        """
        Generate chart image using Inkscape conversion
        
        Args:
            demographic_data: Data for the chart (any demographic data)
            output_name: Base name for the output files (without extension)
            static_dir: Directory to save images
            chart_type: Type of chart ('pie' or 'bar')
            include_title: Whether to include title in the chart
            title_nepali: Nepali title for the chart
            title_english: English title for the chart
            
        Returns:
            tuple: (success, png_path, svg_path)
        """
        try:
            # Ensure static directory exists
            static_path = Path(static_dir)
            static_path.mkdir(parents=True, exist_ok=True)
            
            # Generate SVG
            if chart_type == "pie":
                svg_content = self.generate_pie_chart_svg(
                    demographic_data, 
                    include_title=include_title,
                    title_nepali=title_nepali,
                    title_english=title_english
                )
            elif chart_type == "bar":
                svg_content = self.generate_bar_chart_svg(
                    demographic_data, 
                    include_title=include_title,
                    title_nepali=title_nepali,
                    title_english=title_english
                )
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
