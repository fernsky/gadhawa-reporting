"""
Death Pyramid Generator

This module generates population pyramid charts for death registration (deceased population) data.
"""

from pathlib import Path
import xml.etree.ElementTree as ET


class DeathPyramidGenerator:
    """Generates population pyramid SVG charts for death registration"""

    def __init__(self):
        self.font_family = "Noto Sans Devanagari, Arial, sans-serif"
        self.font_size_title = 20
        self.font_size_labels = 14
        self.font_size_axis = 12
        self.male_color = "#3498db"  # Blue for males
        self.female_color = "#e74c3c"  # Red for females
        self.grid_color = "#ecf0f1"  # Light gray for grid
        self.text_color = "#2c3e50"  # Dark gray for text
        self.background_color = "#ffffff"  # White background

    def _convert_number_to_nepali(self, number):
        english_to_nepali = {
            "0": "०",
            "1": "१",
            "2": "२",
            "3": "३",
            "4": "४",
            "5": "५",
            "6": "६",
            "7": "७",
            "8": "८",
            "9": "९",
        }
        return "".join(english_to_nepali.get(char, char) for char in str(number))

    def _get_age_group_label(self, age_group_code):
        age_group_labels = {
            "AGE_0_4": "०-४",
            "AGE_5_9": "५-९",
            "AGE_10_14": "१०-१४",
            "AGE_15_19": "१५-१९",
            "AGE_20_24": "२०-२४",
            "AGE_25_29": "२५-२९",
            "AGE_30_34": "३०-३४",
            "AGE_35_39": "३५-३९",
            "AGE_40_44": "४०-४४",
            "AGE_45_49": "४५-४९",
            "AGE_50_54": "५०-५४",
            "AGE_55_59": "५५-५९",
            "AGE_60_64": "६०-६४",
            "AGE_65_69": "६५-६९",
            "AGE_70_74": "७०-७४",
            "AGE_75_AND_ABOVE": "७५+",
            "AGE_BELOW_15": "१५ वर्ष मुनि",
        }
        return age_group_labels.get(age_group_code, age_group_code)

    def generate_pyramid_svg(
        self, age_gender_data, width=1200, height=800, title_nepali="", title_english=""
    ):
        svg = ET.Element(
            "svg",
            {
                "width": str(width),
                "height": str(height),
                "xmlns": "http://www.w3.org/2000/svg",
                "style": f"background-color: {self.background_color}",
            },
        )

        defs = ET.SubElement(svg, "defs")
        style = ET.SubElement(defs, "style")
        style.text = """
        @import url('https://fonts.googleapis.com/css2?family=Noto+Sans+Devanagari:wght@400;700&display=swap');
        .pyramid-title { font-family: 'Noto Sans Devanagari', Arial, sans-serif; font-weight: 700; }
        .pyramid-label { font-family: 'Noto Sans Devanagari', Arial, sans-serif; font-weight: 400; }
        .pyramid-axis { font-family: 'Noto Sans Devanagari', Arial, sans-serif; font-weight: 400; }
        """

        margin_top = 80
        margin_bottom = 60
        margin_left = 100
        margin_right = 100
        chart_width = width - margin_left - margin_right
        chart_height = height - margin_top - margin_bottom
        center_x = margin_left + chart_width / 2

        age_groups_ordered = [
            "AGE_75_AND_ABOVE",
            "AGE_70_74",
            "AGE_65_69",
            "AGE_60_64",
            "AGE_55_59",
            "AGE_50_54",
            "AGE_45_49",
            "AGE_40_44",
            "AGE_35_39",
            "AGE_30_34",
            "AGE_25_29",
            "AGE_20_24",
            "AGE_15_19",
            "AGE_10_14",
            "AGE_5_9",
            "AGE_0_4",
            "AGE_BELOW_15",
        ]

        # Find maximum population for scaling
        max_population = 0
        for age_group in age_groups_ordered:
            if age_group in age_gender_data:
                male_pop = age_gender_data[age_group]["MALE"]
                female_pop = age_gender_data[age_group]["FEMALE"]
                max_population = max(max_population, male_pop, female_pop)

        scale_factor = (
            (chart_width / 2 - 20) / max_population if max_population > 0 else 1
        )
        bar_height = chart_height / len(age_groups_ordered) - 4

        # Add center line
        center_line = ET.SubElement(
            svg,
            "line",
            {
                "x1": str(center_x),
                "y1": str(margin_top),
                "x2": str(center_x),
                "y2": str(margin_top + chart_height),
                "stroke": self.text_color,
                "stroke-width": "2",
            },
        )

        # Add horizontal grid lines and age group labels
        for i, age_group in enumerate(age_groups_ordered):
            y_pos = margin_top + i * (chart_height / len(age_groups_ordered))
            grid_line = ET.SubElement(
                svg,
                "line",
                {
                    "x1": str(margin_left),
                    "y1": str(y_pos),
                    "x2": str(margin_left + chart_width),
                    "y2": str(y_pos),
                    "stroke": self.grid_color,
                    "stroke-width": "1",
                },
            )
            age_label = self._get_age_group_label(age_group)
            text_y = y_pos + bar_height / 2 + 5
            age_text = ET.SubElement(
                svg,
                "text",
                {
                    "x": str(center_x),
                    "y": str(text_y),
                    "text-anchor": "middle",
                    "class": "pyramid-label",
                    "font-size": str(self.font_size_labels),
                    "fill": self.text_color,
                    "font-weight": "bold",
                },
            )
            age_text.text = age_label
            age_text_left = ET.SubElement(
                svg,
                "text",
                {
                    "x": str(margin_left - 10),
                    "y": str(text_y),
                    "text-anchor": "end",
                    "class": "pyramid-label",
                    "font-size": str(self.font_size_labels),
                    "fill": self.text_color,
                },
            )
            age_text_left.text = age_label

        # Add bars for each age group
        for i, age_group in enumerate(age_groups_ordered):
            if age_group not in age_gender_data:
                continue
            y_pos = margin_top + i * (chart_height / len(age_groups_ordered)) + 2
            male_pop = age_gender_data[age_group]["MALE"]
            female_pop = age_gender_data[age_group]["FEMALE"]
            # Male bar (left side)
            if male_pop > 0:
                ET.SubElement(
                    svg,
                    "rect",
                    {
                        "x": str(center_x - male_pop * scale_factor),
                        "y": str(y_pos),
                        "width": str(male_pop * scale_factor),
                        "height": str(bar_height),
                        "fill": self.male_color,
                        "opacity": "0.85",
                    },
                )
            # Female bar (right side)
            if female_pop > 0:
                ET.SubElement(
                    svg,
                    "rect",
                    {
                        "x": str(center_x),
                        "y": str(y_pos),
                        "width": str(female_pop * scale_factor),
                        "height": str(bar_height),
                        "fill": self.female_color,
                        "opacity": "0.85",
                    },
                )

        # Add scale labels on x-axis
        scale_steps = 5
        for i in range(scale_steps + 1):
            scale_value = int((max_population / scale_steps) * i)
            scale_width = scale_value * scale_factor
            scale_x_left = center_x - scale_width
            scale_text_left = ET.SubElement(
                svg,
                "text",
                {
                    "x": str(scale_x_left),
                    "y": str(margin_top + chart_height + 25),
                    "text-anchor": "middle",
                    "class": "pyramid-axis",
                    "font-size": str(self.font_size_axis),
                    "fill": self.text_color,
                },
            )
            scale_text_left.text = self._convert_number_to_nepali(scale_value)
            tick_left = ET.SubElement(
                svg,
                "line",
                {
                    "x1": str(scale_x_left),
                    "y1": str(margin_top + chart_height),
                    "x2": str(scale_x_left),
                    "y2": str(margin_top + chart_height + 5),
                    "stroke": self.text_color,
                    "stroke-width": "1",
                },
            )
            if i > 0:
                scale_x_right = center_x + scale_width
                scale_text_right = ET.SubElement(
                    svg,
                    "text",
                    {
                        "x": str(scale_x_right),
                        "y": str(margin_top + chart_height + 25),
                        "text-anchor": "middle",
                        "class": "pyramid-axis",
                        "font-size": str(self.font_size_axis),
                        "fill": self.text_color,
                    },
                )
                scale_text_right.text = self._convert_number_to_nepali(scale_value)
                tick_right = ET.SubElement(
                    svg,
                    "line",
                    {
                        "x1": str(scale_x_right),
                        "y1": str(margin_top + chart_height),
                        "x2": str(scale_x_right),
                        "y2": str(margin_top + chart_height + 5),
                        "stroke": self.text_color,
                        "stroke-width": "1",
                    },
                )

        # Add gender labels
        male_label = ET.SubElement(
            svg,
            "text",
            {
                "x": str(center_x - chart_width / 4),
                "y": str(margin_top + chart_height + 50),
                "text-anchor": "middle",
                "class": "pyramid-label",
                "font-size": str(self.font_size_labels),
                "fill": self.male_color,
                "font-weight": "bold",
            },
        )
        male_label.text = "पुरुष"

        female_label = ET.SubElement(
            svg,
            "text",
            {
                "x": str(center_x + chart_width / 4),
                "y": str(margin_top + chart_height + 50),
                "text-anchor": "middle",
                "class": "pyramid-label",
                "font-size": str(self.font_size_labels),
                "fill": self.female_color,
                "font-weight": "bold",
            },
        )
        female_label.text = "महिला"

        # Add legend
        legend_y = 60
        legend_box_size = 15
        male_legend_rect = ET.SubElement(
            svg,
            "rect",
            {
                "x": str(width - 200),
                "y": str(legend_y - 12),
                "width": str(legend_box_size),
                "height": str(legend_box_size),
                "fill": self.male_color,
                "stroke": "#2980b9",
                "stroke-width": "1",
            },
        )
        male_legend_text = ET.SubElement(
            svg,
            "text",
            {
                "x": str(width - 200 + legend_box_size + 8),
                "y": str(legend_y),
                "class": "pyramid-label",
                "font-size": str(self.font_size_axis),
                "fill": self.text_color,
            },
        )
        male_legend_text.text = "पुरुष"
        female_legend_rect = ET.SubElement(
            svg,
            "rect",
            {
                "x": str(width - 120),
                "y": str(legend_y - 12),
                "width": str(legend_box_size),
                "height": str(legend_box_size),
                "fill": self.female_color,
                "stroke": "#c0392b",
                "stroke-width": "1",
            },
        )
        female_legend_text = ET.SubElement(
            svg,
            "text",
            {
                "x": str(width - 120 + legend_box_size + 8),
                "y": str(legend_y),
                "class": "pyramid-label",
                "font-size": str(self.font_size_axis),
                "fill": self.text_color,
            },
        )
        female_legend_text.text = "महिला"
        return ET.tostring(svg, encoding="unicode", method="xml")

    def convert_svg_to_png(self, svg_path, png_path=None, dpi=300):
        """Convert SVG to PNG using Inkscape"""
        from pathlib import Path
        import subprocess
        import os

        if png_path is None:
            png_path = Path(svg_path).with_suffix(".png")
        try:
            cmd = [
                "inkscape",
                "--export-type=png",
                f"--export-filename={png_path}",
                f"--export-dpi={dpi}",
                str(svg_path),
            ]
            result = subprocess.run(cmd, capture_output=True, text=True, timeout=30)
            if result.returncode == 0 and Path(png_path).exists():
                print(f"✅ Successfully converted {svg_path} to PNG")
                return png_path
            else:
                print(f"❌ Inkscape conversion failed: {result.stderr}")
                return None
        except subprocess.TimeoutExpired:
            print("❌ Inkscape conversion timed out")
            return None
        except FileNotFoundError:
            print("❌ Inkscape not found. Please install Inkscape for PNG conversion.")
            return None
        except Exception as e:
            print(f"❌ Error during SVG to PNG conversion: {e}")
            return None

    def save_pyramid_to_file(
        self,
        age_gender_data,
        filename,
        width=1200,
        height=800,
        title_nepali="",
        title_english="",
    ):
        """Save population pyramid to SVG file"""
        svg_content = self.generate_pyramid_svg(
            age_gender_data, width, height, title_nepali, title_english
        )
        filepath = Path(filename)
        filepath.parent.mkdir(parents=True, exist_ok=True)
        with open(filepath, "w", encoding="utf-8") as f:
            f.write(svg_content)
        return filepath

    def save_pyramid_to_png(
        self,
        age_gender_data,
        filename,
        width=1200,
        height=800,
        title_nepali="",
        title_english="",
        dpi=300,
    ):
        """Save death pyramid directly to PNG file"""
        from pathlib import Path

        svg_filename = Path(filename).with_suffix(".svg")
        svg_path = self.save_pyramid_to_file(
            age_gender_data, svg_filename, width, height, title_nepali, title_english
        )
        png_path = Path(filename).with_suffix(".png")
        converted_png = self.convert_svg_to_png(svg_path, png_path, dpi)
        # Clean up SVG file if conversion was successful
        if converted_png and svg_path.exists():
            try:
                svg_path.unlink()
            except:
                pass
        return converted_png
