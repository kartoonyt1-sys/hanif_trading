from django import template
from django.utils import translation

register = template.Library()


@register.filter(name="bi")
def bilingual_field(obj, field_base_name):
    """Usage in templates: {{ page|bi:"hero_title_line1" }}

    Returns obj.<field_base_name>_fa when the current language is Farsi,
    otherwise obj.<field_base_name>_en. Falls back to the English value if
    the Farsi one is empty (and vice versa), so partially-translated
    content never renders blank.
    """
    if obj is None:
        return ""

    lang = translation.get_language() or "en"
    suffix = "fa" if lang == "fa" else "en"
    other_suffix = "en" if suffix == "fa" else "fa"

    value = getattr(obj, f"{field_base_name}_{suffix}", "")
    if not value:
        value = getattr(obj, f"{field_base_name}_{other_suffix}", "")
    return value
