from django import template
import math
import numbers
import pandas as pd

register = template.Library()

@register.filter
def is_nan(value):
    # return math.isnan(value)
    return pd.isna(value)


@register.filter(name='add_class')
def add_class(field, css_class):
    return field.as_widget(attrs={'class': css_class})


# Get the value for a key in an dictionary
@register.filter
def get(mapping, key):
    return mapping.get(key, '')


# Rounds float values to two decimal places 
@register.filter
def format_float(value, decimal_places=None):
    if not isinstance(value, numbers.Integral) and isinstance(value, numbers.Real):
        return f"{value:.{decimal_places}f}" if decimal_places is not None else f"{value:.2f}"
    
    return value


@register.filter
def to_percentage(value):
    if isinstance(value, (int, float)) and value is not None:
        return f"{value * 100:.2f}%"
    return value
