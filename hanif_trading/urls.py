from django.conf import settings
from django.contrib import admin
from django.urls import include, path
from django.conf.urls.static import static

from wagtail.admin import urls as wagtailadmin_urls
from wagtail.documents import urls as wagtaildocs_urls
from wagtail import urls as wagtail_urls

urlpatterns = [
    path("django-admin/", admin.site.urls),
    path("admin/", include(wagtailadmin_urls)),
    path("documents/", include(wagtaildocs_urls)),

    # app-level urls: language switch + contact form POST handling.
    # MUST come before the Wagtail catch-all below, otherwise Wagtail's
    # page-serving pattern intercepts these paths first (its regex matches
    # any "word/word/..." path, including "i18n/set-language/").
    path("", include("home.urls")),
]

if settings.DEBUG:
    urlpatterns += static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)
    urlpatterns += static(settings.STATIC_URL, document_root=settings.STATIC_ROOT)
    from django.views import defaults as default_views

    urlpatterns += [
        path(
            "400/",
            default_views.bad_request,
            kwargs={"exception": Exception("Bad Request!")},
        ),
        path(
            "403/",
            default_views.permission_denied,
            kwargs={"exception": Exception("Permission Denied")},
        ),
        path(
            "404/",
            default_views.page_not_found,
            kwargs={"exception": Exception("Page not Found")},
        ),
        path("500/", default_views.server_error),
    ]

# Wagtail's page-serving mechanism must come last - it tries to match
# every remaining URL against the page tree.
urlpatterns += [
    path("", include(wagtail_urls)),
]