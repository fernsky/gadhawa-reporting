"""
Nepali template filters for number conversion and formatting
"""

from django import template
from django.template.defaultfilters import floatformat
import re

register = template.Library()

# Nepali digit mapping
NEPALI_DIGITS = {
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

ENGLISH_DIGITS = {v: k for k, v in NEPALI_DIGITS.items()}


@register.filter
def nepali_number(value):
    """Convert English digits to Nepali digits"""
    if value is None:
        return ""

    # Convert to string and handle comma formatting
    if isinstance(value, (int, float)):
        formatted_value = f"{value:,}"
    else:
        formatted_value = str(value)

    # Replace each English digit with Nepali digit
    for english, nepali in NEPALI_DIGITS.items():
        formatted_value = formatted_value.replace(english, nepali)

    return formatted_value


@register.filter
def english_number(value):
    """Convert Nepali digits to English digits"""
    if value is None:
        return ""

    str_value = str(value)

    # Replace each Nepali digit with English digit
    for nepali, english in ENGLISH_DIGITS.items():
        str_value = str_value.replace(nepali, english)

    return str_value


@register.filter
def lookup(dictionary, key):
    """Lookup a key in a dictionary"""
    if isinstance(dictionary, dict):
        return dictionary.get(key)
    return None


@register.filter
def subtract(value, arg):
    """Subtract arg from value"""
    try:
        return int(value) - int(arg)
    except (ValueError, TypeError):
        return 0


@register.filter
def percentage(value, total):
    """Calculate percentage"""
    try:
        if total == 0:
            return 0
        return (float(value) / float(total)) * 100
    except (ValueError, TypeError, ZeroDivisionError):
        return 0


@register.filter
def format_currency(value):
    """Format currency in Nepali style"""
    if value is None:
        return ""

    try:
        # Convert to float and format with 2 decimal places
        amount = float(value)
        formatted = f"{amount:,.2f}"

        # Convert to Nepali digits
        for english, nepali in NEPALI_DIGITS.items():
            formatted = formatted.replace(english, nepali)

        return f"रु. {formatted}"
    except (ValueError, TypeError):
        return str(value)


@register.filter
def nepali_date(value, format_str=None):
    """Format date in Nepali style"""
    if value is None:
        return ""

    try:
        # Basic date formatting (can be extended for full Nepali calendar)
        if hasattr(value, "strftime"):
            if format_str:
                formatted = value.strftime(format_str)
            else:
                formatted = value.strftime("%Y-%m-%d")

            # Convert digits to Nepali
            for english, nepali in NEPALI_DIGITS.items():
                formatted = formatted.replace(english, nepali)

            return formatted
        else:
            return str(value)
    except (ValueError, TypeError):
        return str(value)


@register.filter
def format_population(value):
    """Format population numbers with appropriate suffixes"""
    if value is None:
        return ""

    try:
        num = int(value)
        if num >= 100000:
            return f"{num/100000:.1f} लाख"
        elif num >= 1000:
            return f"{num/1000:.1f} हजार"
        else:
            return nepali_number(num)
    except (ValueError, TypeError):
        return str(value)


@register.filter
def ward_number(value):
    """Format ward number with Nepali text"""
    try:
        return f"वडा नं. {nepali_number(value)}"
    except:
        return str(value)


@register.simple_tag
def percentage_of(part, total):
    """Calculate and format percentage as a template tag"""
    try:
        if total == 0:
            return "0.0%"
        pct = (float(part) / float(total)) * 100
        return f"{nepali_number(f'{pct:.1f}')}%"
    except (ValueError, TypeError, ZeroDivisionError):
        return "0.0%"


@register.filter
def round_to(value, decimal_places=2):
    """Round to specified decimal places"""
    try:
        return round(float(value), int(decimal_places))
    except (ValueError, TypeError):
        return value


@register.filter
def default_if_zero(value, default="०"):
    """Return default value if the value is zero"""
    try:
        if float(value) == 0:
            return default
        return nepali_number(value)
    except (ValueError, TypeError):
        return default


@register.filter
def get_item(dictionary, key):
    """Get item from dictionary by key"""
    if isinstance(dictionary, dict):
        return dictionary.get(key)
    return None


@register.filter
def sub(value, arg):
    """Subtract arg from value (alias for subtract)"""
    try:
        return float(value) - float(arg)
    except (ValueError, TypeError):
        return 0


@register.filter
def div(value, arg):
    """Divide value by arg"""
    try:
        if float(arg) == 0:
            return 0
        return float(value) / float(arg)
    except (ValueError, TypeError, ZeroDivisionError):
        return 0


@register.filter
def mul(value, arg):
    """Multiply value by arg"""
    try:
        return float(value) * float(arg)
    except (ValueError, TypeError):
        return 0
