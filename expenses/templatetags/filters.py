from django import template

register = template.Library()


@register.filter
def sum_list(arr: list) -> int:
    return sum(arr)
