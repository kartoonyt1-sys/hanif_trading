from django.conf import settings
from django.core.mail import send_mail
from django.http import HttpResponseRedirect
from django.shortcuts import get_object_or_404, redirect, render
from django.urls import reverse
from django.utils.translation import activate, check_for_language

from .forms import ContactForm
from .models import ContactPage, ContactSubmission
import logging

from django.conf import settings
from django.core.mail import EmailMessage


def set_language(request):
    """Simple language switch: /i18n/set-language/?lang=fa or ?lang=en

    Sets Django's language cookie (read automatically by LocaleMiddleware on
    every future request) so the choice is remembered, then redirects back
    to the page the visitor came from. Used by the EN/FA toggle in the site
    header.
    """
    lang_code = request.GET.get("lang") or request.POST.get("lang")
    next_url = request.META.get("HTTP_REFERER") or "/"

    response = HttpResponseRedirect(next_url)

    if lang_code and check_for_language(lang_code):
        activate(lang_code)
        response.set_cookie(
            settings.LANGUAGE_COOKIE_NAME,
            lang_code,
            max_age=settings.LANGUAGE_COOKIE_AGE if hasattr(settings, "LANGUAGE_COOKIE_AGE") else 365 * 24 * 60 * 60,
        )
    return response

"""
Contact form view — put these imports at the top of home/views.py (keep your
other imports) and replace the old submit_contact_form with the one below.
"""


logger = logging.getLogger(__name__)


def submit_contact_form(request, page_id=None):
    """Handles POST from the Contact page form.

    On success: saves a ContactSubmission (visible in Wagtail admin), emails
    the team, stores a copy in the session so the contact page can show the
    visitor what they sent, then redirects back with ?sent=1.
    """
    if page_id:
        contact_page = get_object_or_404(ContactPage, pk=page_id)
    else:
        contact_page = ContactPage.objects.live().first()

    if request.method == "POST":
        form = ContactForm(request.POST)
        if form.is_valid():
            data = form.cleaned_data

            ContactSubmission.objects.create(
                name=data["name"],
                email=data["email"],
                phone=data.get("phone", ""),
                subject=data.get("subject", ""),
                message=data["message"],
            )

            # Shown once on the contact page after the redirect.
            request.session["last_submission"] = {
                "name": data["name"],
                "email": data["email"],
                "subject": data.get("subject", ""),
                "message": data["message"],
            }

            # --- Email the team. Errors are logged (never hidden) and never
            # break the visitor's experience: the submission is already saved.
            try:
                email = EmailMessage(
                    subject=f"New website enquiry: {data.get('subject') or 'General'}",
                    body=(
                        f"Name: {data['name']}\n"
                        f"Email: {data['email']}\n"
                        f"Phone: {data.get('phone', '')}\n\n"
                        f"{data['message']}"
                    ),
                    from_email=settings.DEFAULT_FROM_EMAIL,
                    to=[settings.CONTACT_FORM_RECIPIENT],
                    reply_to=[data["email"]],   # "Reply" goes straight to the customer
                )
                email.send(fail_silently=False)
            except Exception:
                logger.exception("Contact form email failed")

            # page.url can be None if the page is outside the site tree,
            # so always fall back to a real path.
            url = (contact_page.url if contact_page else None) or "/contact/"
            return redirect(f"{url}?sent=1")
    else:
        form = ContactForm()

    context = {"form": form}
    if contact_page:
        context.update({
            "page": contact_page,
            "self": contact_page,
            # pop => shown only once, right after a successful submission
            "last_submission": request.session.pop("last_submission", None),
        })

    return render(request, "home/contact_page.html", context)
