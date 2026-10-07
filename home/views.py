from django.conf import settings
from django.core.mail import send_mail
from django.http import HttpResponseRedirect
from django.shortcuts import get_object_or_404, redirect, render
from django.urls import reverse
from django.utils.translation import activate, check_for_language

from .forms import ContactForm
from .models import ContactPage, ContactSubmission


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


def submit_contact_form(request, page_id=None):
    """Handles POST from the Contact page form (and the header 'Get a Quote'
    button, which links to the contact page). On success, stores a
    ContactSubmission row (visible to admins in Wagtail), emails the team,
    stashes a copy of the submission in the session so the contact page can
    show the visitor what they just sent, and redirects back to the contact
    page with a success flag.
    """
    contact_page = None
    if page_id:
        contact_page = get_object_or_404(ContactPage, pk=page_id)
    else:
        contact_page = ContactPage.objects.live().first()

    if request.method == "POST":
        form = ContactForm(request.POST)
        if form.is_valid():
            ContactSubmission.objects.create(
                name=form.cleaned_data["name"],
                email=form.cleaned_data["email"],
                phone=form.cleaned_data.get("phone", ""),
                subject=form.cleaned_data.get("subject", ""),
                message=form.cleaned_data["message"],
            )

            # Stash a copy of what was submitted so the contact page can
            # show it back to the visitor as a confirmation, right after
            # the redirect below. Read once and discarded (see the GET
            # branch), so it never lingers in the session.
            request.session["last_submission"] = {
                "name": form.cleaned_data["name"],
                "email": form.cleaned_data["email"],
                "subject": form.cleaned_data.get("subject", ""),
                "message": form.cleaned_data["message"],
            }

            try:
                send_mail(
                    subject=f"New website enquiry: {form.cleaned_data.get('subject') or 'General'}",
                    message=(
                        f"Name: {form.cleaned_data['name']}\n"
                        f"Email: {form.cleaned_data['email']}\n"
                        f"Phone: {form.cleaned_data.get('phone', '')}\n\n"
                        f"{form.cleaned_data['message']}"
                    ),
                    from_email=None,
                    recipient_list=[settings.CONTACT_FORM_RECIPIENT],
                    fail_silently=True,
                )
            except Exception:
                pass

            url = contact_page.url if contact_page else "/"
            return redirect(f"{url}?sent=1")
    else:
        form = ContactForm()

    if contact_page:
        # Render directly (instead of contact_page.serve(request)) so the
        # form and, when present, the just-submitted confirmation data are
        # actually available to home/contact_page.html.
        return render(request, "home/contact_page.html", {
            "page": contact_page,
            "self": contact_page,
            "form": form,
            # Popped (not just read) so it only shows once, right after
            # the redirect from a successful submission.
            "last_submission": request.session.pop("last_submission", None),
        })

    return render(request, "home/contact_page.html", {"form": form})