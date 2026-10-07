from django.utils import translation

from .models import SiteBrandingSettings, ContactPage


def site_navigation(request):
    """Makes branding/settings, nav items and current language/direction
    available in every template without repeating {% get_settings %} calls.
    """
    lang = translation.get_language() or "en"
    is_rtl = lang in ("fa", "ar", "ps", "ur")

    try:
        branding = SiteBrandingSettings.for_request(request)
    except Exception:
        branding = None

    contact_page = ContactPage.objects.live().first()

    return {
        "branding": branding,
        "CURRENT_LANG": lang,
        "IS_RTL": is_rtl,
        "TEXT_DIR": "rtl" if is_rtl else "ltr",
        "contact_page": contact_page,
        "contact_url": contact_page.url if contact_page else "#",
    }
