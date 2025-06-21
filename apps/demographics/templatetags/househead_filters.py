"""
Custom template filters for househead demographics
"""

from django import template

register = template.Library()


@register.filter
def get_item(dictionary, key):
    """Get item from dictionary using key"""
    if isinstance(dictionary, dict):
        return dictionary.get(key, {})
    return {}


@register.filter
def get_population(demographics_dict, gender):
    """Get population for a specific gender from demographics dict"""
    if isinstance(demographics_dict, dict) and gender in demographics_dict:
        return demographics_dict[gender].get("population", 0)
    return 0


@register.filter
def get_percentage(demographics_dict, gender):
    """Get percentage for a specific gender from demographics dict"""
    if isinstance(demographics_dict, dict) and gender in demographics_dict:
        return demographics_dict[gender].get("percentage", 0.0)
    return 0.0


@register.filter
def calculate_ward_total(ward_demographics):
    """Calculate total population for a ward from demographics dict"""
    if not isinstance(ward_demographics, dict):
        return 0

    total = 0
    for gender_data in ward_demographics.values():
        if isinstance(gender_data, dict) and "population" in gender_data:
            total += gender_data.get("population", 0)
    return total
