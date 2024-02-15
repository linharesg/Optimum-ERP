from django import template
import re

register = template.Library()

@register.filter(name="format_date")
def format_date(value):
    phone_pattern = r"(\d{2}) de (\d+) de (\d{4}) às (\d{5})"
    
    match = re.match(phone_pattern, str(value))
    
    month = match.group(2)
    
    month = {
        "Janeiro": 1, 
        "Fevereiro": 2,
        "Março": 3,
        "Abril": 4,
        "Maio": 5,
        "Junho": 6,
        "Julho": 7,
        "Agosto": 8,
        "Setembro": 9,
        "Outubro": 10,
        "Novembro": 11,
        "Dezembro": 12,
    }[month]

    if match:
        return "{}/{}/{}".format(*match.groups())

    return value