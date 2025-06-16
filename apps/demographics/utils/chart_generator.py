"""
Religion Chart Generator Utility

This module provides comprehensive chart generation for religion demographics
with support for multiple chart types and formats (web and PDF).
"""

import io
import base64
import matplotlib
matplotlib.use('Agg')  # Use non-interactive backend
import matplotlib.pyplot as plt
import matplotlib.patches as patches
from matplotlib import font_manager
import seaborn as sns
import pandas as pd
import numpy as np
from django.conf import settings
import os
import warnings

# Suppress all matplotlib font warnings
warnings.filterwarnings("ignore", category=UserWarning)
warnings.filterwarnings("ignore", message=".*Glyph.*missing from font.*")
warnings.filterwarnings("ignore", message=".*does not support.*")
warnings.filterwarnings("ignore", message=".*Font.*not found.*")

# Try to find and set up Nepali/Devanagari font
def setup_nepali_font():
    """Setup Nepali/Devanagari font for matplotlib with robust fallback"""
    try:
        # Get available system fonts
        available_fonts = [f.name for f in font_manager.fontManager.ttflist]
        
        # Common Nepali fonts to try (in order of preference)
        nepali_fonts = [
            'Noto Sans Devanagari',
            'Mangal',
            'Sanskrit 2003',
            'Kruti Dev 010',  
            'DevLys 010',
            'Preeti',
            'Kalimati',
            'Mukti'
        ]
        
        # Find the first available Nepali font
        for font in nepali_fonts:
            if font in available_fonts:
                plt.rcParams['font.family'] = [font, 'sans-serif']
                return font
                
        # Try Unicode-capable fonts that might handle some Devanagari
        unicode_fonts = ['DejaVu Sans', 'Arial Unicode MS', 'Lucida Sans Unicode']
        for font in unicode_fonts:
            if font in available_fonts:
                plt.rcParams['font.family'] = [font, 'sans-serif']
                return font
                
        # Final fallback to system default
        plt.rcParams['font.family'] = ['sans-serif']
        return 'sans-serif'
        
    except Exception:
        # Ultimate fallback
        plt.rcParams['font.family'] = ['sans-serif']
        return 'sans-serif'

# Setup font with error handling
try:
    CURRENT_FONT = setup_nepali_font()
    plt.rcParams['axes.unicode_minus'] = False
except Exception:
    CURRENT_FONT = 'sans-serif'
    plt.rcParams['font.family'] = ['sans-serif']
    plt.rcParams['axes.unicode_minus'] = False

# Custom color palette for religions
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

# Transliterated labels for fallback when Devanagari doesn't work
RELIGION_LABELS_ENGLISH = {
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


class ReligionChartGenerator:
    """Generates various charts for religion demographics"""
    
    def __init__(self):
        self.fig_size = (12, 8)
        self.dpi = 300
        self.font_size_title = 16
        self.font_size_labels = 12
        self.font_size_legend = 10
        self.use_english_fallback = CURRENT_FONT in ['sans-serif', 'Arial']
        
    def _setup_matplotlib_style(self):
        """Setup matplotlib style for better looking charts"""
        try:
            plt.style.use('seaborn-v0_8-whitegrid')
        except:
            try:
                plt.style.use('seaborn-whitegrid')
            except:
                plt.style.use('default')
        
        # Setup color palette
        sns.set_palette("husl")
        
    def _get_display_label(self, religion_code, nepali_label):
        """Get appropriate display label based on font capability"""
        if self.use_english_fallback:
            return RELIGION_LABELS_ENGLISH.get(religion_code, religion_code.title())
        else:
            return nepali_label
        
    def _safe_title(self, nepali_title, english_title):
        """Get safe title based on font capability"""
        if self.use_english_fallback:
            return english_title
        else:
            return nepali_title
        
    def _save_chart_to_base64(self, fig):
        """Convert matplotlib figure to base64 string for web display"""
        buffer = io.BytesIO()
        fig.savefig(buffer, format='png', dpi=self.dpi, bbox_inches='tight', 
                   facecolor='white', edgecolor='none')
        buffer.seek(0)
        image_png = buffer.getvalue()
        buffer.close()
        
        graphic = base64.b64encode(image_png)
        graphic = graphic.decode('utf-8')
        
        plt.close(fig)
        return f"data:image/png;base64,{graphic}"
    
    def _save_chart_for_pdf(self, fig, filename):
        """Save chart as file for PDF inclusion"""
        charts_dir = os.path.join(settings.MEDIA_ROOT, 'charts', 'religion')
        os.makedirs(charts_dir, exist_ok=True)
        
        filepath = os.path.join(charts_dir, filename)
        fig.savefig(filepath, format='png', dpi=self.dpi, bbox_inches='tight',
                   facecolor='white', edgecolor='none')
        plt.close(fig)
        
        return filepath
    
    def generate_overall_pie_chart(self, religion_data):
        """Generate overall religion distribution pie chart"""
        self._setup_matplotlib_style()
        
        # Filter out religions with zero population
        filtered_data = {k: v for k, v in religion_data.items() if v['population'] > 0}
        
        if not filtered_data:
            return None
        
        # Prepare data with safe labels
        labels = []
        sizes = []
        colors = []
        
        for religion_type, data in filtered_data.items():
            # Convert lazy translation objects to strings
            nepali_name = str(data['name_nepali']) if data['name_nepali'] else religion_type
            labels.append(self._get_display_label(religion_type, nepali_name))
            sizes.append(data['population'])
            colors.append(RELIGION_COLORS.get(religion_type, '#7f7f7f'))
        
        # Create figure
        fig, ax = plt.subplots(figsize=self.fig_size)
        
        try:
            # Create pie chart
            wedges, texts, autotexts = ax.pie(
                sizes, labels=labels, colors=colors, autopct='%1.1f%%',
                startangle=90, textprops={'fontsize': self.font_size_labels}
            )
            
            # Customize appearance
            for autotext in autotexts:
                autotext.set_color('white')
                autotext.set_fontweight('bold')
            
            # Set title with fallback
            title = self._safe_title('धर्म अनुसार जनसंख्या वितरण', 'Population Distribution by Religion')
            ax.set_title(title, fontsize=self.font_size_title, fontweight='bold', pad=20)
            
            # Add legend with population numbers
            legend_labels = [f"{label} ({size:,})" for label, size in zip(labels, sizes)]
            legend_title = self._safe_title("धर्म (जनसंख्या)", "Religion (Population)")
            
            ax.legend(wedges, legend_labels, title=legend_title, 
                     loc="center left", bbox_to_anchor=(1, 0, 0.5, 1),
                     fontsize=self.font_size_legend)
            
            plt.tight_layout()
            return self._save_chart_to_base64(fig)
            
        except Exception as e:
            print(f"Error creating pie chart: {e}")
            import traceback
            traceback.print_exc()
            plt.close(fig)
            return None
    
    def generate_ward_comparison_bar(self, ward_data):
        """Generate ward-wise religion comparison bar chart"""
        self._setup_matplotlib_style()
        
        if not ward_data:
            return None
        
        try:
            # Prepare data for stacked bar chart
            wards = sorted(ward_data.keys())
            ward_labels = [f"Ward {w}" if self.use_english_fallback else f"वडा {w}" for w in wards]
            
            # Get all religions present in the data
            all_religions = set()
            for ward_info in ward_data.values():
                all_religions.update(ward_info['religions'].keys())
            
            # Filter out religions with no data across all wards
            active_religions = []
            for religion in sorted(all_religions):
                total_pop = sum(
                    ward_data[ward]['religions'].get(religion, {}).get('population', 0) 
                    for ward in wards
                )
                if total_pop > 0:
                    active_religions.append(religion)
            
            if not active_religions:
                print("No active religions found")
                return None
                
            # Create data matrix for active religions only
            data_matrix = []
            religion_labels = []
            
            for religion in active_religions:
                religion_data_row = []
                for ward in wards:
                    ward_info = ward_data[ward]
                    population = ward_info['religions'].get(religion, {}).get('population', 0)
                    religion_data_row.append(population)
                data_matrix.append(religion_data_row)
                
                # Get religion display name with proper string conversion
                try:
                    from ..models import ReligionTypeChoice
                    religion_nepali = next(
                        (str(choice[1]) for choice in ReligionTypeChoice.choices 
                         if choice[0] == religion), religion
                    )
                    religion_labels.append(self._get_display_label(religion, religion_nepali))
                except Exception:
                    # Fallback if model import fails
                    religion_labels.append(RELIGION_LABELS_ENGLISH.get(religion, religion.title()))
            
            # Create figure
            fig, ax = plt.subplots(figsize=(14, 8))
            
            # Create stacked bar chart
            bottoms = np.zeros(len(wards))
            bar_width = 0.6
            x_positions = np.arange(len(wards))
            
            for religion, data_row, label in zip(active_religions, data_matrix, religion_labels):
                color = RELIGION_COLORS.get(religion, '#7f7f7f')
                ax.bar(x_positions, data_row, bar_width,
                      bottom=bottoms, label=str(label), color=color)
                bottoms += np.array(data_row)
            
            # Set x-axis labels and positions
            ax.set_xticks(x_positions)
            ax.set_xticklabels(ward_labels, rotation=45, ha='right')
            
            # Customize appearance
            title = self._safe_title('वडागत धार्मिक जनसंख्या वितरण', 'Ward-wise Religious Population Distribution')
            ax.set_title(title, fontsize=self.font_size_title, fontweight='bold')
            
            xlabel = self._safe_title('वडा नं.', 'Ward No.')
            ylabel = self._safe_title('जनसंख्या', 'Population')
            ax.set_xlabel(xlabel, fontsize=self.font_size_labels)
            ax.set_ylabel(ylabel, fontsize=self.font_size_labels)
            
            # Format y-axis with comma separator
            ax.yaxis.set_major_formatter(plt.FuncFormatter(lambda x, p: f'{int(x):,}'))
            
            # Add legend
            ax.legend(loc='upper left', bbox_to_anchor=(1, 1), 
                     fontsize=self.font_size_legend)
            
            plt.tight_layout()
            
            return self._save_chart_to_base64(fig)
            
        except Exception as e:
            print(f"Error creating ward comparison chart: {e}")
            import traceback
            traceback.print_exc()
            return None
    
    def generate_religion_trend_chart(self, religion_data):
        """Generate horizontal bar chart showing religion populations"""
        self._setup_matplotlib_style()
        
        # Filter and sort data
        filtered_data = {k: v for k, v in religion_data.items() if v['population'] > 0}
        sorted_data = sorted(filtered_data.items(), key=lambda x: x[1]['population'], reverse=True)
        
        if not sorted_data:
            return None
        
        try:
            # Prepare data with safe labels
            religions = []
            populations = []
            colors = []
            
            for religion_type, data in sorted_data:
                # Convert lazy translation objects to strings
                nepali_name = str(data['name_nepali']) if data['name_nepali'] else religion_type
                religions.append(self._get_display_label(religion_type, nepali_name))
                populations.append(data['population'])
                colors.append(RELIGION_COLORS.get(religion_type, '#7f7f7f'))
            
            # Create figure
            fig, ax = plt.subplots(figsize=(12, 8))
            
            # Create horizontal bar chart
            bars = ax.barh(religions, populations, color=colors)
            
            # Add value labels on bars
            for i, (bar, pop) in enumerate(zip(bars, populations)):
                width = bar.get_width()
                percentage = sorted_data[i][1]["percentage"]
                ax.text(width + max(populations) * 0.01, bar.get_y() + bar.get_height()/2,
                       f'{pop:,} ({percentage:.1f}%)',
                       ha='left', va='center', fontsize=self.font_size_labels)
            
            # Customize appearance
            title = self._safe_title('धर्म अनुसार जनसंख्या (जनसंख्या र प्रतिशत)', 
                                   'Population by Religion (Number and Percentage)')
            ax.set_title(title, fontsize=self.font_size_title, fontweight='bold')
            
            xlabel = self._safe_title('जनसंख्या', 'Population')
            ax.set_xlabel(xlabel, fontsize=self.font_size_labels)
            
            # Format x-axis with comma separator
            ax.xaxis.set_major_formatter(plt.FuncFormatter(lambda x, p: f'{int(x):,}'))
            
            plt.tight_layout()
            return self._save_chart_to_base64(fig)
            
        except Exception as e:
            print(f"Error creating religion trend chart: {e}")
            import traceback
            traceback.print_exc()
            return None
    
    def generate_diversity_comparison_chart(self, ward_data):
        """Generate ward diversity comparison chart"""
        self._setup_matplotlib_style()
        
        if not ward_data:
            return None
        
        try:
            # Prepare data
            wards = sorted(ward_data.keys())
            diversity_indices = [ward_data[ward]['religious_diversity_index'] for ward in wards]
            
            # Create ward labels based on language preference
            ward_labels = [f"Ward {w}" if self.use_english_fallback else f"वडा {w}" for w in wards]
            
            # Create figure
            fig, ax = plt.subplots(figsize=(12, 6))
            
            # Create bar chart
            bars = ax.bar(ward_labels, diversity_indices, 
                         color='skyblue', edgecolor='navy', linewidth=1)
            
            # Add value labels on bars
            for bar, diversity in zip(bars, diversity_indices):
                height = bar.get_height()
                ax.text(bar.get_x() + bar.get_width()/2., height + 0.001,
                       f'{diversity:.3f}', ha='center', va='bottom', 
                       fontsize=self.font_size_labels)
            
            # Customize appearance with language fallback
            title = self._safe_title('वडागत धार्मिक विविधता सूचकांक', 'Ward-wise Religious Diversity Index')
            xlabel = self._safe_title('वडा नं.', 'Ward No.')
            ylabel = self._safe_title('विविधता सूचकांक', 'Diversity Index')
            
            ax.set_title(title, fontsize=self.font_size_title, fontweight='bold')
            ax.set_xlabel(xlabel, fontsize=self.font_size_labels)
            ax.set_ylabel(ylabel, fontsize=self.font_size_labels)
            
            # Rotate x-axis labels if needed
            plt.xticks(rotation=45, ha='right')
            plt.tight_layout()
            
            return self._save_chart_to_base64(fig)
            
        except Exception as e:
            print(f"Error creating diversity comparison chart: {e}")
            import traceback
            traceback.print_exc()
            return None
    
    def generate_pdf_chart(self, data, chart_type='pie'):
        """Generate chart specifically for PDF inclusion"""
        if chart_type == 'pie':
            return self.generate_overall_pie_chart(data)
        elif chart_type == 'bar':
            return self.generate_ward_comparison_bar(data)
        elif chart_type == 'diversity':
            return self.generate_diversity_comparison_chart(data)
        else:
            return None
    
    def generate_all_charts(self, religion_data, ward_data):
        """Generate all charts at once"""
        return {
            'overall_pie': self.generate_overall_pie_chart(religion_data),
            'ward_comparison': self.generate_ward_comparison_bar(ward_data),
            'religion_trend': self.generate_religion_trend_chart(religion_data),
            'diversity_comparison': self.generate_diversity_comparison_chart(ward_data),
        }
