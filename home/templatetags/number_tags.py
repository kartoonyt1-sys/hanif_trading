"""
Template filter to convert Latin (English) digits to Persian (Farsi) digits
for display when the site is in RTL/Farsi mode — e.g. phone numbers, which
are stored as a single plain text field (not bilingual like address_en/fa),
so the conversion has to happen at display time instead.

Usage in a template:
    {% load number_tags %}
    {{ branding.phone_1|fa_digits }}

Typically combined with IS_RTL so English digits still show in EN mode:
    {% if IS_RTL %}{{ branding.phone_1|fa_digits }}{% else %}{{ branding.phone_1 }}{% endif %}
"""
from django import template

register = template.Library()

_EN_TO_FA_DIGITS = str.maketrans("0123456789", "۰۱۲۳۴۵۶۷۸۹")


@register.filter(name="fa_digits")
def fa_digits(value):
    """Convert any Latin digits (0-9) found in `value` to Persian digits.
    Leaves all other characters (+, spaces, dashes, letters) untouched, so
    phone numbers like '+93 77 123 4567' become '+۹۳ ۷۷ ۱۲۳ ۴۵۶۷'."""
    if value is None:
        return value
    return str(value).translate(_EN_TO_FA_DIGITS)