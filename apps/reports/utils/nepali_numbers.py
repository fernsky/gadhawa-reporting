"""
Utility functions for converting numbers to Nepali numerals
"""

# Map of English to Nepali numerals
NEPALI_DIGITS = {
    '0': '०',
    '1': '१',
    '2': '२',
    '3': '३',
    '4': '४',
    '5': '५',
    '6': '६',
    '7': '७',
    '8': '८',
    '9': '९',
}

# Reverse mapping for converting Nepali to English
ENGLISH_DIGITS = {v: k for k, v in NEPALI_DIGITS.items()}


def to_nepali_digits(value):
    """
    Convert a number or string containing digits to its Nepali equivalent
    
    Args:
        value: Number or string to convert
        
    Returns:
        String with Nepali digits
    """
    if value is None:
        return ''
    
    string_value = str(value)
    result = ''
    
    for char in string_value:
        if char in NEPALI_DIGITS:
            result += NEPALI_DIGITS[char]
        else:
            result += char
    
    return result


def to_english_digits(value):
    """
    Convert a string containing Nepali digits to English digits
    
    Args:
        value: String with Nepali digits
        
    Returns:
        String with English digits
    """
    if value is None:
        return ''
    
    string_value = str(value)
    result = ''
    
    for char in string_value:
        if char in ENGLISH_DIGITS:
            result += ENGLISH_DIGITS[char]
        else:
            result += char
    
    return result


def localize_number(value, locale='ne'):
    """
    Convert a number or string to localized digits based on the specified locale
    
    Args:
        value: Number or string to convert
        locale: Current locale ('ne' for Nepali, any other value for English)
        
    Returns:
        String with localized digits
    """
    if locale == 'ne':
        return to_nepali_digits(value)
    else:
        return str(value) if value is not None else ''


def format_nepali_number(value, decimal_places=None):
    """
    Format a number with Nepali numerals and proper formatting
    
    Args:
        value: Number to format
        decimal_places: Number of decimal places (None for automatic)
        
    Returns:
        Formatted string with Nepali digits
    """
    if value is None:
        return ''
    
    try:
        # Handle decimal formatting
        if decimal_places is not None:
            formatted_value = f"{float(value):.{decimal_places}f}"
        else:
            # Convert to float first to handle string numbers
            num_value = float(value)
            # Check if it's a whole number
            if num_value.is_integer():
                formatted_value = str(int(num_value))
            else:
                formatted_value = str(num_value)
        
        # Convert to Nepali digits
        return to_nepali_digits(formatted_value)
        
    except (ValueError, TypeError):
        # If conversion fails, just convert to Nepali digits as string
        return to_nepali_digits(str(value))


def format_nepali_percentage(value, decimal_places=1):
    """
    Format a percentage with Nepali numerals
    
    Args:
        value: Number to format as percentage
        decimal_places: Number of decimal places
        
    Returns:
        Formatted percentage string with Nepali digits
    """
    if value is None:
        return ''
    
    try:
        percentage = float(value)
        formatted = f"{percentage:.{decimal_places}f}%"
        return to_nepali_digits(formatted)
    except (ValueError, TypeError):
        return to_nepali_digits(str(value))


def format_nepali_currency(value, currency_symbol='रु.', decimal_places=2):
    """
    Format currency with Nepali numerals
    
    Args:
        value: Amount to format
        currency_symbol: Currency symbol
        decimal_places: Number of decimal places
        
    Returns:
        Formatted currency string with Nepali digits
    """
    if value is None:
        return ''
    
    try:
        amount = float(value)
        formatted = f"{currency_symbol} {amount:,.{decimal_places}f}"
        return to_nepali_digits(formatted)
    except (ValueError, TypeError):
        return f"{currency_symbol} {to_nepali_digits(str(value))}"


def format_nepali_date_parts(date_obj):
    """
    Convert date parts to Nepali numerals while keeping month names in original language
    
    Args:
        date_obj: Date object or formatted date string
        
    Returns:
        Date string with Nepali numerals for day and year
    """
    if not date_obj:
        return ''
    
    if hasattr(date_obj, 'strftime'):
        # If it's a date object, format it first
        formatted_date = date_obj.strftime('%Y-%m-%d')
        return to_nepali_digits(formatted_date)
    else:
        # If it's already a string, just convert digits
        return to_nepali_digits(str(date_obj))


def format_nepali_date_full(date_obj, format_string=None):
    """
    Format date with full Nepali numerals and optionally Nepali month names
    
    Args:
        date_obj: Date object or string
        format_string: Optional format string (e.g., '%Y %B %d')
        
    Returns:
        Fully formatted date with Nepali numerals
    """
    if not date_obj:
        return ''
    
    # Nepali month names mapping
    nepali_months = {
        'January': 'जनवरी', 'February': 'फेब्रुअरी', 'March': 'मार्च',
        'April': 'अप्रिल', 'May': 'मे', 'June': 'जुन',
        'July': 'जुलाई', 'August': 'अगस्त', 'September': 'सेप्टेम्बर',
        'October': 'अक्टोबर', 'November': 'नोभेम्बर', 'December': 'डिसेम्बर'
    }
    
    # Short month names
    nepali_months_short = {
        'Jan': 'जन', 'Feb': 'फेब', 'Mar': 'मार्च',
        'Apr': 'अप्रिल', 'May': 'मे', 'Jun': 'जुन',
        'Jul': 'जुलाई', 'Aug': 'अग', 'Sep': 'सेप्ट',
        'Oct': 'अक्ट', 'Nov': 'नोभ', 'Dec': 'डिस'
    }
    
    try:
        if hasattr(date_obj, 'strftime'):
            # If it's a date object, format it
            if format_string:
                formatted = date_obj.strftime(format_string)
            else:
                formatted = date_obj.strftime('%Y %B %d')  # Windows compatible
        else:
            # If it's already a string, use it directly
            formatted = str(date_obj)
        
        # Replace English month names with Nepali
        for eng_month, nep_month in nepali_months.items():
            formatted = formatted.replace(eng_month, nep_month)
        
        for eng_month, nep_month in nepali_months_short.items():
            formatted = formatted.replace(eng_month, nep_month)
        
        # Convert all digits to Nepali
        nepali_formatted = to_nepali_digits(formatted)
        
        # Clean up day padding (e.g., "०१" -> "१")
        return clean_day_padding(nepali_formatted)
            
    except Exception:
        # Fallback to basic digit conversion
        return to_nepali_digits(str(date_obj))


def nepali_ordinal(number):
    """
    Convert number to Nepali ordinal (१म, २रो, ३रो, etc.)
    
    Args:
        number: Number to convert to ordinal
        
    Returns:
        Nepali ordinal string
    """
    if not number:
        return ''
    
    try:
        num = int(number)
        nepali_num = to_nepali_digits(str(num))
        
        # Simple ordinal rules for Nepali
        if num == 1:
            return f"{nepali_num}म"
        elif num == 2:
            return f"{nepali_num}रो" 
        elif num == 3:
            return f"{nepali_num}रो"
        else:
            return f"{nepali_num}औं"
            
    except (ValueError, TypeError):
        return to_nepali_digits(str(number))


def format_file_size_nepali(size_bytes):
    """
    Format file size in Nepali numerals
    
    Args:
        size_bytes: Size in bytes
        
    Returns:
        Formatted file size with Nepali numerals
    """
    if not size_bytes:
        return '० बाइट'
    
    try:
        size = float(size_bytes)
        
        if size < 1024:
            return f"{to_nepali_digits(int(size))} बाइट"
        elif size < 1024 * 1024:
            kb = size / 1024
            return f"{to_nepali_digits(f'{kb:.1f}')} KB"
        elif size < 1024 * 1024 * 1024:
            mb = size / (1024 * 1024)
            return f"{to_nepali_digits(f'{mb:.1f}')} MB"
        else:
            gb = size / (1024 * 1024 * 1024)
            return f"{to_nepali_digits(f'{gb:.1f}')} GB"
            
    except (ValueError, TypeError):
        return to_nepali_digits(str(size_bytes))


def clean_day_padding(date_string):
    """
    Remove leading zeros from day numbers in formatted date strings
    E.g., "२०२५ जुन ०१" -> "२०२५ जुन १"
    """
    import re
    # Pattern to match Nepali digits with leading zero for days (space before the zero)
    # This will match patterns like " ०१", " ०२", etc. and replace with " १", " २", etc.
    pattern = r' ०([१-९])'
    return re.sub(pattern, r' \1', date_string)
