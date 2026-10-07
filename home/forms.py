from django import forms
from django.utils.translation import gettext_lazy as _


class ContactForm(forms.Form):
    """Contact form used on the Contact page and the footer 'Get a Quote' CTA.
    Labels are translated via Django's own i18n (see locale/ + {% trans %}),
    error messages stay in whichever language the visitor is browsing in.
    """
    name = forms.CharField(
        label=_("Full Name"),
        max_length=150,
        widget=forms.TextInput(attrs={"placeholder": _("Your full name")}),
    )
    email = forms.EmailField(
        label=_("Email Address"),
        widget=forms.EmailInput(attrs={"placeholder": _("you@example.com")}),
    )
    phone = forms.CharField(
        label=_("Phone Number"),
        max_length=50,
        required=False,
        widget=forms.TextInput(attrs={"placeholder": _("+93 7X XXX XXXX")}),
    )
    subject = forms.CharField(
        label=_("Subject"),
        max_length=200,
        required=False,
        widget=forms.TextInput(attrs={"placeholder": _("How can we help?")}),
    )
    message = forms.CharField(
        label=_("Message"),
        widget=forms.Textarea(attrs={"rows": 5, "placeholder": _("Write your message here...")}),
    )

    # simple honeypot anti-spam field, hidden via CSS in the template
    honeypot = forms.CharField(required=False, widget=forms.HiddenInput())

    def clean_honeypot(self):
        value = self.cleaned_data.get("honeypot")
        if value:
            raise forms.ValidationError("Spam detected.")
        return value
