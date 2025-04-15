from django import template
from django.db.models.functions import TruncWeek

register = template.Library()

@register.filter(name = 'currency')
def currency(number):
    return "$ " + str(number)

@register.filter(name = 'multiply')
def multiply(number, number1):
    return number * number1