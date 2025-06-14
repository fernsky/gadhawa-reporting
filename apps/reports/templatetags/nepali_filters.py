"""
Template filters for Nepali number formatting
"""
from django import template
from django.utils.safestring import mark_safe
from ..utils.nepali_numbers import (
    to_nepali_digits, 
    localize_number, 
    format_nepali_number,
    format_nepali_percentage,
    format_nepali_currency,
    format_nepali_date_parts,
    format_nepali_date_full,
    nepali_ordinal,
    format_file_size_nepali
)

register = template.Library()


@register.filter
def nepali_digits(value):
    """Convert digits to Nepali numerals"""
    return to_nepali_digits(value)


@register.filter
def nepali_number(value, decimal_places=None):
    """Format number with Nepali digits"""
    if decimal_places is not None:
        try:
            decimal_places = int(decimal_places)
        except (ValueError, TypeError):
            decimal_places = None
    return format_nepali_number(value, decimal_places)


@register.filter
def nepali_percentage(value, decimal_places=1):
    """Format percentage with Nepali digits"""
    try:
        decimal_places = int(decimal_places)
    except (ValueError, TypeError):
        decimal_places = 1
    return format_nepali_percentage(value, decimal_places)


@register.filter
def nepali_currency(value, symbol='रु.'):
    """Format currency with Nepali digits"""
    return format_nepali_currency(value, symbol)


@register.filter
def nepali_date(value, format_string="Y F j"):
    """Format date with Nepali digits and month names"""
    if not value:
        return ''
    
    if not hasattr(value, 'strftime'):
        return format_nepali_date_full(value)
    
    # Handle Django date format strings (Windows compatible)
    try:
        if format_string == "Y F j":
            # This is the most common Django format: Year Full-month-name day
            formatted = value.strftime("%Y %B %d")
        elif format_string == "Y-m-d":
            formatted = value.strftime("%Y-%m-%d")
        elif format_string == "d F Y":
            formatted = value.strftime("%d %B %Y")
        elif format_string == "F j, Y":
            formatted = value.strftime("%B %d, %Y")
        else:
            # Fallback to default
            formatted = value.strftime("%Y %B %d")
        
        # Now convert to Nepali
        return format_nepali_date_full(formatted)
        
    except Exception as e:
        # Fallback to basic formatting if there's any error
        return format_nepali_date_full(value)


@register.filter
def nepali_date_simple(value):
    """Format date with Nepali digits only (keep original format)"""
    return format_nepali_date_parts(value)


@register.filter
def nepali_ordinal_filter(value):
    """Convert number to Nepali ordinal"""
    return nepali_ordinal(value)


@register.filter
def nepali_file_size(value):
    """Format file size with Nepali digits"""
    return format_file_size_nepali(value)


@register.filter
def localize_digits(value, locale='ne'):
    """Localize digits based on locale"""
    return localize_number(value, locale)


@register.simple_tag
def nepali_range(start, end=None, step=1):
    """Generate range with Nepali digits"""
    if end is None:
        end = start
        start = 0
    
    try:
        start = int(start)
        end = int(end)
        step = int(step)
        
        result = []
        for i in range(start, end, step):
            result.append(to_nepali_digits(str(i)))
        return result
    except (ValueError, TypeError):
        return []


@register.simple_tag
def nepali_counter(value):
    """Convert counter/forloop.counter to Nepali"""
    return to_nepali_digits(value)


@register.inclusion_tag('reports/partials/nepali_pagination.html', takes_context=True)
def nepali_pagination(context, page_obj, paginate_by=10):
    """Render pagination with Nepali numerals"""
    return {
        'page_obj': page_obj,
        'paginate_by': paginate_by,
        'request': context.get('request'),
        'nepali_digits': to_nepali_digits,
    }


@register.filter
def nepali_length(value):
    """Get length of object and convert to Nepali digits"""
    try:
        if hasattr(value, '__len__'):
            return to_nepali_digits(len(value))
        elif hasattr(value, 'count'):
            return to_nepali_digits(value.count())
        else:
            return to_nepali_digits(0)
    except:
        return to_nepali_digits(0)


@register.filter
def nepali_slice_start(value, arg):
    """Convert slice start index to Nepali"""
    try:
        start = int(arg)
        return to_nepali_digits(start + 1)  # +1 for human readable (1-based)
    except:
        return to_nepali_digits(1)


@register.filter
def add_nepali(value, arg):
    """Add two numbers and return in Nepali digits"""
    try:
        result = int(value) + int(arg)
        return to_nepali_digits(result)
    except:
        return value


@register.filter
def multiply_nepali(value, arg):
    """Multiply two numbers and return in Nepali digits"""
    try:
        result = int(value) * int(arg)
        return to_nepali_digits(result)
    except:
        return value


@register.simple_tag
def nepali_page_info(page_obj):
    """Generate page information in Nepali"""
    if not page_obj:
        return ""
    
    start_index = (page_obj.number - 1) * page_obj.paginator.per_page + 1
    end_index = min(start_index + page_obj.paginator.per_page - 1, page_obj.paginator.count)
    
    start_nepali = to_nepali_digits(start_index)
    end_nepali = to_nepali_digits(end_index)
    total_nepali = to_nepali_digits(page_obj.paginator.count)
    
    return f"{start_nepali}-{end_nepali} मध्ये {total_nepali}"


@register.filter
def get_item(dictionary, key):
    """Get item from dictionary by key"""
    if not dictionary or not isinstance(dictionary, dict):
        return None
    return dictionary.get(key)


@register.filter
def get_page_number_nepali(page_num):
    """Format page number in Nepali digits"""
    if not page_num:
        return ""
    
    # Convert to Nepali digits
    nepali_digits = {
        '0': '०', '1': '१', '2': '२', '3': '३', '4': '४',
        '5': '५', '6': '६', '7': '७', '8': '८', '9': '९'
    }
    
    nepali_num = ''
    for digit in str(page_num):
        nepali_num += nepali_digits.get(digit, digit)
    
    return nepali_num


@register.filter
def nepali_section_number(section_number):
    """Convert section number to Nepali digits"""
    if not section_number:
        return ""
    
    # Convert dots and numbers
    nepali_digits = {
        '0': '०', '1': '१', '2': '२', '3': '३', '4': '४',
        '5': '५', '6': '६', '7': '७', '8': '८', '9': '९'
    }
    
    result = ''
    for char in str(section_number):
        if char in nepali_digits:
            result += nepali_digits[char]
        else:
            result += char
    
    return result


@register.filter
def split(value, delimiter):
    """Split string by delimiter"""
    if not value:
        return []
    return str(value).split(delimiter)
