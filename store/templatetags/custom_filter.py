from django import template
from django.db.models.functions import TruncWeek

register = template.Library()

@register.filter(name = 'currency')
def currency(number):
    return "$ " + str(number)