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
        return demographics_dict[gender].get('population', 0)
    return 0

@register.filter
def get_percentage(demographics_dict, gender):
    """Get percentage for a specific gender from demographics dict"""
    if isinstance(demographics_dict, dict) and gender in demographics_dict:
        return demographics_dict[gender].get('percentage', 0.0)
    return 0.0
