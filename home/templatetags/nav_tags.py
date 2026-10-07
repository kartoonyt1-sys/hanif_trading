from django import template

from home.models import NavigationItem

register = template.Library()


@register.simple_tag
def get_nav_items():
    """Returns the navbar items snippet, in their configured order.

    Usage in a template:
        {% load nav_tags %}
        {% get_nav_items as nav_items %}
        {% for item in nav_items %}...{% endfor %}
    """
    return NavigationItem.objects.all().order_by("order", "pk")