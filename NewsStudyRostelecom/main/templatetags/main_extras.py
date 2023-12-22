from django import template
from django.template.defaultfilters import stringfilter
register = template.Library()

@register.filter(name='ladder')
@stringfilter

def ladder(value):
    """Составляет символы ЛеСеНкОй"""
    result=''
    for i in range(len(value)):
        if i % 2 == 0:
            result += value[i].upper()
        else:
            result += value[i].lower()
    return result