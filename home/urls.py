from django.urls import path

from . import views

app_name = "home"

urlpatterns = [
    path("i18n/set-language/", views.set_language, name="set_language"),
    path("contact/submit/", views.submit_contact_form, name="submit_contact_form"),
    path("contact/<int:page_id>/submit/", views.submit_contact_form, name="submit_contact_form_for_page"),
]