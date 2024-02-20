from django import template
import re

register = template.Library()

@register.filter(name="format_cnpj")
def format_cnpj(value):
    cnpj_pattern = r"(\d{2})(\d{3})(\d{3})(\d{4})(\d{2})"
    
    match = re.match(cnpj_pattern, value)

    if match:
        return "{}.{}.{}/{}-{}".format(*match.groups())

    return value