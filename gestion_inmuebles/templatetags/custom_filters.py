from django import template

register = template.Library()


@register.filter
def chilean_peso(value):
    try:
        value = int(value)
        return f"{value:,.0f}".replace(",", ".")
    except (ValueError, TypeError):
        return value
