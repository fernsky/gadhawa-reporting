#!/usr/bin/env python3
"""
Test template rendering for infrastructure data
"""
import os
import sys
import django

# Add the project directory to the Python path
sys.path.append(
    "/Users/trilochan/Desktop/final-delivery/digital-profile/lungri/lungri-report"
)

# Configure Django settings
os.environ.setdefault("DJANGO_SETTINGS_MODULE", "lungri_report.settings.development")
django.setup()

from django.template import Template, Context
from apps.infrastructure.processors.manager import get_infrastructure_manager


def test_infrastructure_template():
    print("Testing Infrastructure Template Rendering...")

    # Get infrastructure data
    manager = get_infrastructure_manager()
    all_data = manager.process_all_for_pdf()

    # Create a simple template to test
    template_content = """
    {% load nepali_filters %}
    
    Infrastructure Data Test:
    
    {% if all_infrastructure_data.road_status %}
        Road Status Section: {{ all_infrastructure_data.road_status.section_title }}
        Total Households: {{ all_infrastructure_data.road_status.total_households|nepali_number }}
        
        Municipality Data:
        {% for code, data in all_infrastructure_data.road_status.municipality_data.items %}
        - {{ data.name_nepali }}: {{ data.population|nepali_number }} ({{ data.percentage|nepali_percentage }})
        {% endfor %}
    {% endif %}
    
    {% if all_infrastructure_data.public_transport %}
        Public Transport Section: {{ all_infrastructure_data.public_transport.section_title }}
        Total Households: {{ all_infrastructure_data.public_transport.total_households|nepali_number }}
    {% endif %}
    
    {% if all_infrastructure_data.market_center_time %}
        Market Center Time Section: {{ all_infrastructure_data.market_center_time.section_title }}
        Total Households: {{ all_infrastructure_data.market_center_time.total_households|nepali_number }}
    {% endif %}
    """

    template = Template(template_content)
    context = Context({"all_infrastructure_data": all_data})

    rendered = template.render(context)
    print(rendered)


if __name__ == "__main__":
    test_infrastructure_template()
