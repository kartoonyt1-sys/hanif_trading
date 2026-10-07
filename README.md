# Hanif Aimaq Trading Ltd — Wagtail Website
# وب‌سایت حنیف ایماق ترایدینگ لمیتد — Wagtail

A bilingual (English / Persian-Dari) Wagtail CMS website for an international
trade & logistics company: hero section, services, trade routes, product
categories, and a contact form — everything editable from the Wagtail admin,
including the logo, images, and both languages of every text field.

## 1. Setup / نصب

```bash
python3 -m venv venv
source venv/bin/activate        # Windows: venv\Scripts\activate
pip install -r requirements.txt

python manage.py migrate
python manage.py createsuperuser
python manage.py runserver
```

Then open:
- Site: http://127.0.0.1:8000/
- Wagtail admin: http://127.0.0.1:8000/admin/

## 2. First-time content setup

1. Log into `/admin/`.
2. Under **Pages**, open the root page and add a **Home Page** — publish it,
   then in **Settings → Sites** make sure it's set as the site's root page.
3. Add child pages under Home: **Standard Page** (About Us, Services, Trade,
   Logistics, Routes...) and one **Contact Page**.
4. Go to **Settings → Site Branding & Settings** to:
   - Upload your **logo** (replaces the placeholder "HA" badge)
   - Fill in company name/tagline in English and Farsi
   - Add navigation menu items (linked to the pages you created)
   - Add footer quick links, phone, email, address, social links
5. Open the Home Page and fill in every section (Hero, About, Services,
   Trade Routes, Why Choose Us, Products, CTA banner) — every field has an
   **(EN)** and **(FA/Dari)** version side by side.

## 3. How the bilingual system works / سیستم دوزبانه

Every text field is stored twice: `field_en` and `field_fa`. The front-end
picks the right one automatically based on the visitor's language choice
(EN/FA switch in the header, top right), using the `bi` template filter:

```django
{{ page|bi:"hero_title_line1" }}
```

This resolves to `page.hero_title_line1_fa` when Farsi is active, otherwise
`page.hero_title_line1_en` (falling back to whichever one isn't empty).
Farsi automatically switches the whole layout to right-to-left (`dir="rtl"`)
with the Vazirmatn font.

## 4. Project structure

```
hanif_trading/
  hanif_trading/settings.py   # Django + Wagtail settings, LANGUAGES = en/fa
  hanif_trading/urls.py       # root URL routing
  home/
    models.py                 # HomePage, StandardPage, ContactPage, SiteBrandingSettings...
    forms.py                  # ContactForm
    views.py                  # contact form submit handler + language switch
    urls.py                   # /i18n/set-language/, /contact/<id>/submit/
    context_processors.py     # exposes branding/nav/language to all templates
    templatetags/bilingual_tags.py  # the `bi` filter
    templates/home/*.html     # base, home_page, standard_page, contact_page
    static/home/css/style.css # dark/green theme + animations, RTL-aware
    static/home/js/main.js    # scroll-reveal, counters, mobile nav
```

## 5. Notes

- Contact form submissions are saved as `ContactSubmission` snippets,
  visible/exportable from the Wagtail admin (Snippets menu), and are also
  emailed to `CONTACT_FORM_RECIPIENT` (set in settings.py or via env var).
  In development, email is printed to the console (`EmailBackend` = console).
- For production: set `DJANGO_SECRET_KEY`, `DJANGO_DEBUG=false`,
  `DJANGO_ALLOWED_HOSTS`, a real `DJANGO_EMAIL_BACKEND`/SMTP settings, and
  swap SQLite for Postgres if needed.
- Replace `home/static/home/images/logo-placeholder.svg` by uploading a real
  logo in **Site Branding & Settings** — no code change needed.
