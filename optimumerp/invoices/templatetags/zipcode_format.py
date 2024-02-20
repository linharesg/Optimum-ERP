from django import template
import re

register = template.Library()

@register.filter(name="format_zipcode")
def format_zipcode(value):
    cnpj_pattern = r"(\d{5})(\d{3})"
    
    match = re.match(cnpj_pattern, value)

    if match:
        return "{}-{}".format(*match.groups())

    return value