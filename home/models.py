
from django import forms
from django.db import models
 
from modelcluster.fields import ParentalKey
from modelcluster.models import ClusterableModel
 
from wagtail.models import Page, Orderable
from wagtail.fields import RichTextField, StreamField
from wagtail.admin.panels import FieldPanel, InlinePanel, MultiFieldPanel
from wagtail.contrib.settings.models import BaseSiteSetting, register_setting
from wagtail.snippets.models import register_snippet
from wagtail import blocks
from wagtail.images.blocks import ImageChooserBlock
from wagtail.documents.blocks import DocumentChooserBlock
from wagtail.embeds.blocks import EmbedBlock
 
 
# ---------------------------------------------------------------------------
# Reusable bilingual field helpers
# ---------------------------------------------------------------------------
def bilingual_char_fields(max_length=255):
    return (
        models.CharField(max_length=max_length, blank=True, verbose_name="(EN)"),
        models.CharField(max_length=max_length, blank=True, verbose_name="(FA/Dari)"),
    )
 
 
# ---------------------------------------------------------------------------
# Color picker widget — renders a real <input type="color"> in the Wagtail
# admin instead of a plain text box, so editors pick colors visually.
# The value is still stored as a normal hex string ("#0b3d91"), so it is
# trivial to print straight into CSS in the template.
# ---------------------------------------------------------------------------
class ColorWidget(forms.TextInput):
    input_type = "color"
 
    def __init__(self, *args, **kwargs):
        attrs = kwargs.pop("attrs", {}) or {}
        attrs.setdefault("style", "width:70px;height:38px;padding:2px;cursor:pointer;")
        kwargs["attrs"] = attrs
        super().__init__(*args, **kwargs)
 
 
def color_field(default):
    """A short-hex color field (#rrggbb), stored as plain text."""
    return models.CharField(max_length=7, default=default)
 
 
# ---------------------------------------------------------------------------
# HOME PAGE
# ---------------------------------------------------------------------------
class HomePage(Page):
    max_count = 1
    parent_page_types = ["wagtailcore.Page"]
    subpage_types = ["home.StandardPage", "home.ContactPage"]
 
    # ---- Hero -------------------------------------------------------
    hero_eyebrow_en = models.CharField("Eyebrow text (EN)", max_length=100, blank=True,
                                        default="International Trade & Logistics")
    hero_eyebrow_fa = models.CharField("Eyebrow text (FA)", max_length=100, blank=True,
                                        default="تجارت و لوجستیک بین‌المللی")
    hero_title_line1_en = models.CharField("Title line 1 (EN)", max_length=100, blank=True,
                                            default="Hanif Aimaq")
    hero_title_line1_fa = models.CharField("Title line 1 (FA)", max_length=100, blank=True,
                                            default="حنیف ایماق")
    hero_title_line2_en = models.CharField("Title line 2 - highlighted (EN)", max_length=100,
                                            blank=True, default="Transit, Forwarding & Trading Company")
    hero_title_line2_fa = models.CharField("Title line 2 - highlighted (FA)", max_length=100,
                                            blank=True, default="ترانزیت، فورواردینگ و شرکت تجارتی")
    hero_tagline_en = models.CharField("Tagline (EN)", max_length=255, blank=True,
                                        default="Connecting Markets. Moving Business Forward.")
    hero_tagline_fa = models.CharField("Tagline (FA)", max_length=255, blank=True,
                                        default="اتصال بازارها. پیشبرد تجارت.")
    hero_description_en = models.TextField("Description (EN)", blank=True)
    hero_description_fa = models.TextField("Description (FA)", blank=True)
    hero_image = models.ForeignKey(
        "wagtailimages.Image", null=True, blank=True,
        on_delete=models.SET_NULL, related_name="+",
        verbose_name="Hero background image",
    )
    # NEW: optional hero background video (self-hosted or YouTube/Vimeo link).
    # If set, the front-end can play this instead of / behind the static
    # hero_image (falls back to hero_image on mobile or if no video given).
    hero_video_file = models.ForeignKey(
        "wagtaildocs.Document", null=True, blank=True,
        on_delete=models.SET_NULL, related_name="+",
        verbose_name="Hero video file (optional, self-hosted .mp4)",
    )
    hero_video_embed_url = models.URLField(
        "Hero video link (optional, YouTube/Vimeo)", blank=True,
        help_text="Paste a YouTube or Vimeo URL. Leave blank to use the video file above or the static image.",
    )
    hero_button1_text_en = models.CharField(max_length=50, blank=True, default="Our Services")
    hero_button1_text_fa = models.CharField(max_length=50, blank=True, default="خدمات ما")
    hero_button1_link = models.URLField(blank=True)
    hero_button2_text_en = models.CharField(max_length=50, blank=True, default="Contact Us")
    hero_button2_text_fa = models.CharField(max_length=50, blank=True, default="تماس با ما")
    hero_button2_link = models.URLField(blank=True)
    hero_badge_en = models.CharField("Side badge text (EN)", max_length=100, blank=True,
                                      default="Fast / Safe / Reliable / Global")
    hero_badge_fa = models.CharField("Side badge text (FA)", max_length=100, blank=True,
                                      default="سریع / مطمئن / قابل اعتماد / جهانی")
 
    # ---- About --------------------------------------------------------
    about_label_en = models.CharField(max_length=100, blank=True, default="About Our Company")
    about_label_fa = models.CharField(max_length=100, blank=True, default="درباره شرکت ما")
    about_title_en = models.CharField(max_length=255, blank=True,
                                       default="Hanif Aimaq Transit, Forwarding & Trading Company")
    about_title_fa = models.CharField(max_length=255, blank=True,
                                       default="حنیف ایماق - شرکت ترانزیت، فورواردینگ و تجارتی")
    about_body_en = RichTextField(blank=True)
    about_body_fa = RichTextField(blank=True)
    about_image = models.ForeignKey(
        "wagtailimages.Image", null=True, blank=True,
        on_delete=models.SET_NULL, related_name="+",
    )
    about_overlay_text_en = models.CharField(max_length=255, blank=True,
                                              default="Bridging Markets Across Borders")
    about_overlay_text_fa = models.CharField(max_length=255, blank=True,
                                              default="پل ارتباطی بازارها فراتر از مرزها")
    about_button_text_en = models.CharField(max_length=50, blank=True, default="Learn More About Us")
    about_button_text_fa = models.CharField(max_length=50, blank=True, default="بیشتر بدانید")
    about_button_link = models.URLField(blank=True)
 
    # ---- Services section header ---------------------------------------
    services_label_en = models.CharField(max_length=100, blank=True, default="Our Services")
    services_label_fa = models.CharField(max_length=100, blank=True, default="خدمات ما")
    services_title_en = models.CharField(max_length=100, blank=True, default="What We Do")
    services_title_fa = models.CharField(max_length=100, blank=True, default="ما چه می‌کنیم")
    services_intro_en = models.CharField(max_length=255, blank=True)
    services_intro_fa = models.CharField(max_length=255, blank=True)
 
    # ---- Routes section header ------------------------------------------
    routes_label_en = models.CharField(max_length=100, blank=True, default="Trade Without Borders")
    routes_label_fa = models.CharField(max_length=100, blank=True, default="تجارت بدون مرز")
    routes_title_en = models.CharField(max_length=150, blank=True, default="Our Key Trade Routes")
    routes_title_fa = models.CharField(max_length=150, blank=True, default="مسیرهای کلیدی تجارت")
    routes_intro_en = models.TextField(blank=True)
    routes_intro_fa = models.TextField(blank=True)
    routes_button_text_en = models.CharField(max_length=50, blank=True, default="View All Routes")
    routes_button_text_fa = models.CharField(max_length=50, blank=True, default="مشاهده همه مسیرها")
    routes_button_link = models.URLField(blank=True)
 
    # ---- Why choose us header -------------------------------------------
    why_label_en = models.CharField(max_length=100, blank=True, default="Why Choose Us")
    why_label_fa = models.CharField(max_length=100, blank=True, default="چرا ما را انتخاب کنید")
    why_title_en = models.CharField(max_length=150, blank=True, default="Your Reliable Trading Partner")
    why_title_fa = models.CharField(max_length=150, blank=True, default="همکار مطمئن تجاری شما")
 
    # ---- Products header -------------------------------------------------
    products_label_en = models.CharField(max_length=100, blank=True,
                                          default="Our Products & Trade Activities")
    products_label_fa = models.CharField(max_length=100, blank=True,
                                          default="محصولات و فعالیت‌های تجاری")
    products_title_en = models.CharField(max_length=150, blank=True, default="Popular Trade Categories")
    products_title_fa = models.CharField(max_length=150, blank=True, default="دسته‌بندی‌های پرطرفدار")
    products_button_text_en = models.CharField(max_length=50, blank=True, default="Explore Our Trade Activities")
    products_button_text_fa = models.CharField(max_length=50, blank=True, default="فعالیت‌های تجاری ما")
    products_button_link = models.URLField(blank=True)
 
    # ---- Media gallery header (NEW) --------------------------------------
    gallery_label_en = models.CharField(max_length=100, blank=True, default="Gallery")
    gallery_label_fa = models.CharField(max_length=100, blank=True, default="گالری")
    gallery_title_en = models.CharField(max_length=150, blank=True, default="Photos & Videos")
    gallery_title_fa = models.CharField(max_length=150, blank=True, default="عکس‌ها و ویدیوها")
 
    # ---- Testimonials / messages header (NEW) ----------------------------
    testimonials_label_en = models.CharField(max_length=100, blank=True, default="Testimonials")
    testimonials_label_fa = models.CharField(max_length=100, blank=True, default="نظرات مشتریان")
    testimonials_title_en = models.CharField(max_length=150, blank=True, default="What Our Clients Say")
    testimonials_title_fa = models.CharField(max_length=150, blank=True, default="مشتریان ما چه می‌گویند")
 
    # ---- Bottom call-to-action banner -------------------------------------
    cta_title_en = models.CharField(max_length=255, blank=True, default="Ready to Start Business With Us?")
    cta_title_fa = models.CharField(max_length=255, blank=True, default="آماده شروع همکاری با ما هستید؟")
    cta_description_en = models.TextField(blank=True)
    cta_description_fa = models.TextField(blank=True)
    cta_button_text_en = models.CharField(max_length=50, blank=True, default="Get in Touch Now")
    cta_button_text_fa = models.CharField(max_length=50, blank=True, default="همین حالا تماس بگیرید")
    cta_button_link = models.URLField(blank=True)
    cta_background = models.ForeignKey(
        "wagtailimages.Image", null=True, blank=True,
        on_delete=models.SET_NULL, related_name="+",
    )
 
    content_panels = Page.content_panels + [
        MultiFieldPanel([
            FieldPanel("hero_eyebrow_en"), FieldPanel("hero_eyebrow_fa"),
            FieldPanel("hero_title_line1_en"), FieldPanel("hero_title_line1_fa"),
            FieldPanel("hero_title_line2_en"), FieldPanel("hero_title_line2_fa"),
            FieldPanel("hero_tagline_en"), FieldPanel("hero_tagline_fa"),
            FieldPanel("hero_description_en"), FieldPanel("hero_description_fa"),
            FieldPanel("hero_image"),
            FieldPanel("hero_video_file"),
            FieldPanel("hero_video_embed_url"),
            FieldPanel("hero_button1_text_en"), FieldPanel("hero_button1_text_fa"),
            FieldPanel("hero_button1_link"),
            FieldPanel("hero_button2_text_en"), FieldPanel("hero_button2_text_fa"),
            FieldPanel("hero_button2_link"),
            FieldPanel("hero_badge_en"), FieldPanel("hero_badge_fa"),
        ], heading="Hero Section"),
 
        InlinePanel("highlight_cards", label="Hero highlight cards (Transportation / Trade / Import-Export / Partnership)"),
 
        MultiFieldPanel([
            FieldPanel("about_label_en"), FieldPanel("about_label_fa"),
            FieldPanel("about_title_en"), FieldPanel("about_title_fa"),
            FieldPanel("about_body_en"), FieldPanel("about_body_fa"),
            FieldPanel("about_image"),
            FieldPanel("about_overlay_text_en"), FieldPanel("about_overlay_text_fa"),
            FieldPanel("about_button_text_en"), FieldPanel("about_button_text_fa"),
            FieldPanel("about_button_link"),
        ], heading="About Section"),
 
        InlinePanel("stats", label="Stats (years of experience, clients, ...)"),
 
        MultiFieldPanel([
            FieldPanel("services_label_en"), FieldPanel("services_label_fa"),
            FieldPanel("services_title_en"), FieldPanel("services_title_fa"),
            FieldPanel("services_intro_en"), FieldPanel("services_intro_fa"),
        ], heading="Services Section Heading"),
        InlinePanel("services", label="Services"),
 
        MultiFieldPanel([
            FieldPanel("routes_label_en"), FieldPanel("routes_label_fa"),
            FieldPanel("routes_title_en"), FieldPanel("routes_title_fa"),
            FieldPanel("routes_intro_en"), FieldPanel("routes_intro_fa"),
            FieldPanel("routes_button_text_en"), FieldPanel("routes_button_text_fa"),
            FieldPanel("routes_button_link"),
        ], heading="Trade Routes Section Heading"),
        InlinePanel("route_stops", label="Route stops (countries, in order)"),
        InlinePanel("route_notes", label="Route detail lines (e.g. China -> Kazakhstan -> ... -> Afghanistan)"),
 
        MultiFieldPanel([
            FieldPanel("why_label_en"), FieldPanel("why_label_fa"),
            FieldPanel("why_title_en"), FieldPanel("why_title_fa"),
        ], heading="Why Choose Us Heading"),
        InlinePanel("why_choose_items", label="Why choose us items"),
 
        MultiFieldPanel([
            FieldPanel("products_label_en"), FieldPanel("products_label_fa"),
            FieldPanel("products_title_en"), FieldPanel("products_title_fa"),
            FieldPanel("products_button_text_en"), FieldPanel("products_button_text_fa"),
            FieldPanel("products_button_link"),
        ], heading="Products Section Heading"),
        InlinePanel("product_categories", label="Product / trade categories"),
 
        # NEW: Media gallery (photos + videos), fully editable per item.
        MultiFieldPanel([
            FieldPanel("gallery_label_en"), FieldPanel("gallery_label_fa"),
            FieldPanel("gallery_title_en"), FieldPanel("gallery_title_fa"),
        ], heading="Media Gallery Heading"),
        InlinePanel("media_gallery", label="Gallery items (photos & videos)"),
 
        # NEW: Customer messages / testimonials.
        MultiFieldPanel([
            FieldPanel("testimonials_label_en"), FieldPanel("testimonials_label_fa"),
            FieldPanel("testimonials_title_en"), FieldPanel("testimonials_title_fa"),
        ], heading="Testimonials Heading"),
        InlinePanel("testimonials", label="Customer messages / testimonials"),
 
        MultiFieldPanel([
            FieldPanel("cta_title_en"), FieldPanel("cta_title_fa"),
            FieldPanel("cta_description_en"), FieldPanel("cta_description_fa"),
            FieldPanel("cta_button_text_en"), FieldPanel("cta_button_text_fa"),
            FieldPanel("cta_button_link"),
            FieldPanel("cta_background"),
        ], heading="Bottom Call-To-Action Banner"),
    ]
 
    class Meta:
        verbose_name = "Home Page"
 
 
class HomeHighlightCard(Orderable):
    page = ParentalKey(HomePage, on_delete=models.CASCADE, related_name="highlight_cards")
    icon = models.ForeignKey("wagtailimages.Image", null=True, blank=True,
                              on_delete=models.SET_NULL, related_name="+",
                              help_text="Small SVG/PNG icon")
    title_en = models.CharField(max_length=100)
    title_fa = models.CharField(max_length=100)
    description_en = models.CharField(max_length=150, blank=True)
    description_fa = models.CharField(max_length=150, blank=True)
 
    panels = [
        FieldPanel("icon"),
        FieldPanel("title_en"), FieldPanel("title_fa"),
        FieldPanel("description_en"), FieldPanel("description_fa"),
    ]
 
 
class HomeStat(Orderable):
    page = ParentalKey(HomePage, on_delete=models.CASCADE, related_name="stats")
    number = models.CharField(max_length=20, help_text="e.g. 10+, 500+, 15+, 1200+")
    label_en = models.CharField(max_length=100)
    label_fa = models.CharField(max_length=100)
 
    panels = [
        FieldPanel("number"),
        FieldPanel("label_en"), FieldPanel("label_fa"),
    ]
 
 
class HomeService(Orderable):
    page = ParentalKey(HomePage, on_delete=models.CASCADE, related_name="services")
    image = models.ForeignKey("wagtailimages.Image", null=True, blank=True,
                               on_delete=models.SET_NULL, related_name="+")
    icon = models.ForeignKey("wagtailimages.Image", null=True, blank=True,
                              on_delete=models.SET_NULL, related_name="+")
    title_en = models.CharField(max_length=100)
    title_fa = models.CharField(max_length=100)
    description_en = models.CharField(max_length=255, blank=True)
    description_fa = models.CharField(max_length=255, blank=True)
    link_page = models.ForeignKey("wagtailcore.Page", null=True, blank=True,
                                   on_delete=models.SET_NULL, related_name="+")
 
    panels = [
        FieldPanel("image"), FieldPanel("icon"),
        FieldPanel("title_en"), FieldPanel("title_fa"),
        FieldPanel("description_en"), FieldPanel("description_fa"),
        FieldPanel("link_page"),
    ]
 
 
class HomeRouteStop(Orderable):
    page = ParentalKey(HomePage, on_delete=models.CASCADE, related_name="route_stops")
    flag_image = models.ForeignKey("wagtailimages.Image", null=True, blank=True,
                                    on_delete=models.SET_NULL, related_name="+")
    country_name_en = models.CharField(max_length=100)
    country_name_fa = models.CharField(max_length=100)
 
    panels = [
        FieldPanel("flag_image"),
        FieldPanel("country_name_en"), FieldPanel("country_name_fa"),
    ]
 
 
class HomeRouteNote(Orderable):
    page = ParentalKey(HomePage, on_delete=models.CASCADE, related_name="route_notes")
    text_en = models.CharField(max_length=255)
    text_fa = models.CharField(max_length=255)
 
    panels = [FieldPanel("text_en"), FieldPanel("text_fa")]
 
 
class HomeWhyChooseItem(Orderable):
    page = ParentalKey(HomePage, on_delete=models.CASCADE, related_name="why_choose_items")
    icon = models.ForeignKey("wagtailimages.Image", null=True, blank=True,
                              on_delete=models.SET_NULL, related_name="+")
    title_en = models.CharField(max_length=100)
    title_fa = models.CharField(max_length=100)
    description_en = models.CharField(max_length=255, blank=True)
    description_fa = models.CharField(max_length=255, blank=True)
 
    panels = [
        FieldPanel("icon"),
        FieldPanel("title_en"), FieldPanel("title_fa"),
        FieldPanel("description_en"), FieldPanel("description_fa"),
    ]
 
 
class HomeProductCategory(Orderable):
    page = ParentalKey(HomePage, on_delete=models.CASCADE, related_name="product_categories")
    image = models.ForeignKey("wagtailimages.Image", null=True, blank=True,
                               on_delete=models.SET_NULL, related_name="+")
    title_en = models.CharField(max_length=100)
    title_fa = models.CharField(max_length=100)
 
    panels = [
        FieldPanel("image"),
        FieldPanel("title_en"), FieldPanel("title_fa"),
    ]
 
 
# ---------------------------------------------------------------------------
# NEW: MEDIA GALLERY (photos AND videos, mixed, in one ordered list)
# ---------------------------------------------------------------------------
class HomeMediaItem(Orderable):
    MEDIA_TYPE_CHOICES = [
        ("image", "Photo"),
        ("video_file", "Video (uploaded file)"),
        ("video_embed", "Video (YouTube / Vimeo link)"),
    ]
 
    page = ParentalKey(HomePage, on_delete=models.CASCADE, related_name="media_gallery")
    media_type = models.CharField(max_length=20, choices=MEDIA_TYPE_CHOICES, default="image")
 
    # Used when media_type == "image": the photo itself.
    # Also used as the poster/thumbnail image for both video types.
    image = models.ForeignKey(
        "wagtailimages.Image", null=True, blank=True,
        on_delete=models.SET_NULL, related_name="+",
        verbose_name="Photo / video thumbnail",
        help_text="Required for photos. For videos, this is shown as the poster/thumbnail before playing.",
    )
    # Used when media_type == "video_file"
    video_file = models.ForeignKey(
        "wagtaildocs.Document", null=True, blank=True,
        on_delete=models.SET_NULL, related_name="+",
        verbose_name="Uploaded video file (.mp4)",
    )
    # Used when media_type == "video_embed"
    video_embed_url = models.URLField(
        "YouTube / Vimeo link", blank=True,
        help_text="Paste the full video URL, e.g. https://www.youtube.com/watch?v=...",
    )
 
    caption_en = models.CharField(max_length=150, blank=True)
    caption_fa = models.CharField(max_length=150, blank=True)
 
    panels = [
        FieldPanel("media_type"),
        FieldPanel("image"),
        FieldPanel("video_file"),
        FieldPanel("video_embed_url"),
        FieldPanel("caption_en"), FieldPanel("caption_fa"),
    ]
 
    class Meta:
        verbose_name = "Gallery item"
 
 
# ---------------------------------------------------------------------------
# NEW: CUSTOMER MESSAGES / TESTIMONIALS
# ---------------------------------------------------------------------------
class HomeTestimonial(Orderable):
    page = ParentalKey(HomePage, on_delete=models.CASCADE, related_name="testimonials")
    photo = models.ForeignKey(
        "wagtailimages.Image", null=True, blank=True,
        on_delete=models.SET_NULL, related_name="+",
        verbose_name="Client photo (optional)",
    )
    client_name_en = models.CharField(max_length=100)
    client_name_fa = models.CharField(max_length=100)
    client_role_en = models.CharField("Company / role (EN)", max_length=150, blank=True)
    client_role_fa = models.CharField("Company / role (FA)", max_length=150, blank=True)
    message_en = models.TextField("Message (EN)")
    message_fa = models.TextField("Message (FA)")
    rating = models.PositiveSmallIntegerField(
        default=5, choices=[(i, f"{i} / 5") for i in range(1, 6)],
    )
 
    panels = [
        FieldPanel("photo"),
        FieldPanel("client_name_en"), FieldPanel("client_name_fa"),
        FieldPanel("client_role_en"), FieldPanel("client_role_fa"),
        FieldPanel("message_en"), FieldPanel("message_fa"),
        FieldPanel("rating"),
    ]
 
    class Meta:
        verbose_name = "Testimonial / customer message"
 
 
# ---------------------------------------------------------------------------
# FLEXIBLE CONTENT BLOCKS for StandardPage (About Us / Services / Trade /
# Logistics / any generic page). Each block is bilingual (EN/FA fields
# inside the same block, matching the rest of the site's convention) and
# has its own front-end template under templates/home/blocks/. Editors can
# drag-and-drop any mix of these, in any order, per page.
# ---------------------------------------------------------------------------
class TextSectionBlock(blocks.StructBlock):
    heading_en = blocks.CharBlock(required=False, label="Heading (EN)")
    heading_fa = blocks.CharBlock(required=False, label="Heading (FA)")
    text_en = blocks.RichTextBlock(required=False, label="Text (EN)")
    text_fa = blocks.RichTextBlock(required=False, label="Text (FA)")
 
    class Meta:
        icon = "doc-full"
        label = "Text Section"
        template = "home/blocks/text_section.html"
 
 
class ImageBlock(blocks.StructBlock):
    image = ImageChooserBlock(label="Photo")
    caption_en = blocks.CharBlock(required=False, label="Caption (EN)")
    caption_fa = blocks.CharBlock(required=False, label="Caption (FA)")
    layout = blocks.ChoiceBlock(
        choices=[
            ("full", "Full width"),
            ("left", "Float left (text wraps on the right)"),
            ("right", "Float right (text wraps on the left)"),
        ],
        default="full",
        label="Layout",
    )
 
    class Meta:
        icon = "image"
        label = "Photo"
        template = "home/blocks/image_block.html"
 
 
class GalleryBlock(blocks.StructBlock):
    images = blocks.ListBlock(ImageChooserBlock(label="Photo"), label="Photos")
 
    class Meta:
        icon = "grip"
        label = "Photo Gallery"
        template = "home/blocks/gallery_block.html"
 
 
class VideoBlock(blocks.StructBlock):
    embed_url = EmbedBlock(
        required=False, label="YouTube / Vimeo link",
        help_text="Paste a video URL. Leave empty if uploading a file below instead.",
    )
    video_file = DocumentChooserBlock(
        required=False, label="Or upload a video file (.mp4)",
    )
    caption_en = blocks.CharBlock(required=False, label="Caption (EN)")
    caption_fa = blocks.CharBlock(required=False, label="Caption (FA)")
 
    class Meta:
        icon = "media"
        label = "Video"
        template = "home/blocks/video_block.html"
 
 
class QuoteBlock(blocks.StructBlock):
    quote_en = blocks.TextBlock(required=False, label="Quote (EN)")
    quote_fa = blocks.TextBlock(required=False, label="Quote (FA)")
    author_en = blocks.CharBlock(required=False, label="Author (EN)")
    author_fa = blocks.CharBlock(required=False, label="Author (FA)")
 
    class Meta:
        icon = "openquote"
        label = "Quote"
        template = "home/blocks/quote_block.html"
 
 
class ColoredBoxBlock(blocks.StructBlock):
    """A "چوکات" (framed/highlight box) with its own background and text
    color, independent of the rest of the page's theme colors."""
    title_en = blocks.CharBlock(required=False, label="Title (EN)")
    title_fa = blocks.CharBlock(required=False, label="Title (FA)")
    text_en = blocks.RichTextBlock(required=False, label="Text (EN)")
    text_fa = blocks.RichTextBlock(required=False, label="Text (FA)")
    background_color = blocks.CharBlock(
        default="#eafbf1", label="Background color (hex)",
        help_text="e.g. #eafbf1",
    )
    text_color = blocks.CharBlock(default="#0f3d24", label="Text color (hex)")
 
    class Meta:
        icon = "pick"
        label = "Colored Highlight Box"
        template = "home/blocks/colored_box.html"
 
 
class ButtonBlock(blocks.StructBlock):
    text_en = blocks.CharBlock(required=False, label="Button text (EN)")
    text_fa = blocks.CharBlock(required=False, label="Button text (FA)")
    link = blocks.URLBlock(required=False, label="Link")
 
    class Meta:
        icon = "link"
        label = "Button"
        template = "home/blocks/button_block.html"
 
 
class PageContentStreamBlock(blocks.StreamBlock):
    text = TextSectionBlock()
    image = ImageBlock()
    gallery = GalleryBlock()
    video = VideoBlock()
    quote = QuoteBlock()
    colored_box = ColoredBoxBlock()
    button = ButtonBlock()
 
 
# ---------------------------------------------------------------------------
# STANDARD PAGE (About Us / Services / Trade / Logistics / generic content)
# ---------------------------------------------------------------------------
class StandardPage(Page):
    subpage_types = ["home.StandardPage", "home.ContactPage"]
 
    intro_en = models.CharField(max_length=255, blank=True)
    intro_fa = models.CharField(max_length=255, blank=True)
 
    # Kept for backward compatibility with pages created before the
    # flexible `content` StreamField existed. New pages should build their
    # layout with `content` below; this can stay empty on new pages.
    body_en = RichTextField(blank=True)
    body_fa = RichTextField(blank=True)
 
    # NEW: flexible page builder — mix text, photos, a gallery, video,
    # quotes, colored highlight boxes and buttons in any order, fully
    # controlled per page from the Wagtail admin.
    content = StreamField(PageContentStreamBlock(), blank=True, use_json_field=True)
 
    banner_image = models.ForeignKey(
        "wagtailimages.Image", null=True, blank=True,
        on_delete=models.SET_NULL, related_name="+",
    )
    # Optional banner video for standard pages too (Services, About, etc.)
    banner_video_embed_url = models.URLField(
        "Banner video link (optional, YouTube/Vimeo)", blank=True,
    )
 
    # NEW: per-page color overrides. Leave blank to inherit the site-wide
    # colors set in Settings -> Site Branding & Settings -> Theme Colors.
    primary_color_override = models.CharField(max_length=7, blank=True)
    background_color_override = models.CharField(max_length=7, blank=True)
    text_color_override = models.CharField(max_length=7, blank=True)
 
    content_panels = Page.content_panels + [
        FieldPanel("banner_image"),
        FieldPanel("banner_video_embed_url"),
        FieldPanel("intro_en"), FieldPanel("intro_fa"),
        FieldPanel("content"),
        MultiFieldPanel([
            FieldPanel("body_en"), FieldPanel("body_fa"),
        ], heading="Simple Body Text (legacy, optional — prefer the blocks above)"),
        MultiFieldPanel([
            FieldPanel("primary_color_override", widget=ColorWidget),
            FieldPanel("background_color_override", widget=ColorWidget),
            FieldPanel("text_color_override", widget=ColorWidget),
        ], heading="Page Color Overrides (optional — leave blank to use site defaults)"),
    ]
 
    class Meta:
        verbose_name = "Standard Page"
 
 
# ---------------------------------------------------------------------------
# CONTACT PAGE (rendered form is defined in home/forms.py, handled by
# home/views.py, POSTs to the url in home/urls.py)
# ---------------------------------------------------------------------------
class ContactPage(Page):
    max_count = 1
 
    intro_en = models.CharField(max_length=255, blank=True, default="Get In Touch")
    intro_fa = models.CharField(max_length=255, blank=True, default="با ما در تماس شوید")
    body_en = RichTextField(blank=True)
    body_fa = RichTextField(blank=True)
    thank_you_text_en = models.CharField(max_length=255, blank=True,
                                          default="Thank you! Your message has been sent.")
    thank_you_text_fa = models.CharField(max_length=255, blank=True,
                                          default="سپاسگزاریم! پیام شما ارسال شد.")
 
    content_panels = Page.content_panels + [
        FieldPanel("intro_en"), FieldPanel("intro_fa"),
        FieldPanel("body_en"), FieldPanel("body_fa"),
        FieldPanel("thank_you_text_en"), FieldPanel("thank_you_text_fa"),
    ]
 
    class Meta:
        verbose_name = "Contact Page"
 
 
class ContactSubmission(models.Model):
    """Stores every submission of the contact form, viewable in Wagtail admin
    via the ModelAdmin/Snippet registration below. This is the *incoming*
    inquiry/contact-form message log (different from the on-page
    HomeTestimonial "customer messages" shown publicly on the home page)."""
    created_at = models.DateTimeField(auto_now_add=True)
    name = models.CharField(max_length=150)
    email = models.EmailField()
    phone = models.CharField(max_length=50, blank=True)
    subject = models.CharField(max_length=200, blank=True)
    message = models.TextField()
 
    panels = [
        FieldPanel("created_at", read_only=True),
        FieldPanel("name"),
        FieldPanel("email"),
        FieldPanel("phone"),
        FieldPanel("subject"),
        FieldPanel("message"),
    ]
 
    class Meta:
        ordering = ["-created_at"]
        verbose_name = "Contact Submission"
 
    def __str__(self):
        return f"{self.name} <{self.email}> - {self.created_at:%Y-%m-%d %H:%M}"
 
 
register_snippet(ContactSubmission)
 
 
# ---------------------------------------------------------------------------
# NAVBAR — standalone Snippet (previously an Orderable tied only to the
# Branding settings page; now manageable from its own entry under Snippets)
# ---------------------------------------------------------------------------
class NavigationItem(models.Model):
    title_en = models.CharField(max_length=50)
    title_fa = models.CharField(max_length=50)
    link_page = models.ForeignKey("wagtailcore.Page", null=True, blank=True,
                                   on_delete=models.SET_NULL, related_name="+",
                                   help_text="Pick an internal page, or leave empty and use the URL field below")
    link_url = models.URLField(blank=True, help_text="Used only if no page is selected above")
    order = models.PositiveIntegerField(default=0, help_text="Lower numbers appear first in the navbar")
 
    panels = [
        FieldPanel("title_en"), FieldPanel("title_fa"),
        FieldPanel("link_page"), FieldPanel("link_url"),
        FieldPanel("order"),
    ]
 
    class Meta:
        ordering = ["order", "pk"]
        verbose_name = "Navigation Menu Item"
        verbose_name_plural = "Navbar"
 
    def __str__(self):
        return self.title_en or self.title_fa or f"Nav item #{self.pk}"
 
    @property
    def url(self):
        if self.link_page:
            return self.link_page.url
        return self.link_url or "#"
 
 
register_snippet(NavigationItem)
 
 
# ---------------------------------------------------------------------------
# SITE-WIDE SETTINGS: logo, footer, contact info, socials, THEME COLORS
# (Header navbar now lives in the NavigationItem snippet above, not here)
# ---------------------------------------------------------------------------
@register_setting(icon="cog")
class SiteBrandingSettings(BaseSiteSetting, ClusterableModel):
    logo = models.ForeignKey(
        "wagtailimages.Image", null=True, blank=True,
        on_delete=models.SET_NULL, related_name="+",
        help_text="Site logo shown in the header and footer",
    )
    site_name_en = models.CharField(max_length=100, default="Hanif Aimaq")
    site_name_fa = models.CharField(max_length=100, default="حنیف ایماق")
    site_tagline_en = models.CharField(max_length=100, blank=True,
                                        default="Transit, Forwarding & Trading Company")
    site_tagline_fa = models.CharField(max_length=100, blank=True,
                                        default="ترانزیت، فورواردینگ و تجارت")
    site_slogan_en = models.CharField(max_length=100, blank=True, default="Trade | Transit | Logistics")
    site_slogan_fa = models.CharField(max_length=100, blank=True, default="تجارت | ترانزیت | لوجستیک")
 
    # ---- NEW: Theme colors (used site-wide via CSS variables) -----------
    primary_color = color_field(default="#0b3d91")     # main brand color (buttons, header, links)
    secondary_color = color_field(default="#d4af37")   # gold accent, used in Wagtail's own admin too
    accent_color = color_field(default="#0f9d58")      # highlights, badges, hover states
    background_color = color_field(default="#ffffff")  # page background
    text_color = color_field(default="#1a1a1a")        # main body text color
 
    quote_button_text_en = models.CharField(max_length=50, blank=True, default="Get a Quote")
    quote_button_text_fa = models.CharField(max_length=50, blank=True, default="درخواست قیمت")
    quote_button_link = models.URLField(blank=True)
 
    address_en = models.CharField(max_length=255, blank=True, default="Kabul, Afghanistan")
    address_fa = models.CharField(max_length=255, blank=True, default="کابل، افغانستان")
    phone_1 = models.CharField(max_length=50, blank=True, default="+93 77 123 4567")
    phone_2 = models.CharField(max_length=50, blank=True)
    email = models.EmailField(blank=True, default="info@hanifaimaq.com")
    whatsapp_number = models.CharField(max_length=50, blank=True)
 
    facebook_url = models.URLField(blank=True)
    linkedin_url = models.URLField(blank=True)
    whatsapp_url = models.URLField(blank=True)
    youtube_url = models.URLField(blank=True)
    instagram_url = models.URLField(blank=True)
 
    footer_about_en = models.TextField(blank=True)
    footer_about_fa = models.TextField(blank=True)
    copyright_text_en = models.CharField(max_length=255, blank=True,
                                          default="\u00a9 2026 Hanif Aimaq Transit, Forwarding & Trading Company. All Rights Reserved.")
    copyright_text_fa = models.CharField(max_length=255, blank=True,
                                          default="\u00a9 2026 حنیف ایماق - شرکت ترانزیت، فورواردینگ و تجارتی. تمامی حقوق محفوظ است.")
 
    panels = [
        MultiFieldPanel([
            FieldPanel("logo"),
            FieldPanel("site_name_en"), FieldPanel("site_name_fa"),
            FieldPanel("site_tagline_en"), FieldPanel("site_tagline_fa"),
            FieldPanel("site_slogan_en"), FieldPanel("site_slogan_fa"),
        ], heading="Logo & Brand"),
 
        # NEW panel: theme colors, with real color-picker widgets.
        MultiFieldPanel([
            FieldPanel("primary_color", widget=ColorWidget),
            FieldPanel("secondary_color", widget=ColorWidget),
            FieldPanel("accent_color", widget=ColorWidget),
            FieldPanel("background_color", widget=ColorWidget),
            FieldPanel("text_color", widget=ColorWidget),
        ], heading="Theme Colors"),
 
        MultiFieldPanel([
            FieldPanel("quote_button_text_en"), FieldPanel("quote_button_text_fa"),
            FieldPanel("quote_button_link"),
        ], heading="Header CTA Button"),
        MultiFieldPanel([
            FieldPanel("address_en"), FieldPanel("address_fa"),
            FieldPanel("phone_1"), FieldPanel("phone_2"),
            FieldPanel("email"), FieldPanel("whatsapp_number"),
        ], heading="Contact Info"),
        MultiFieldPanel([
            FieldPanel("facebook_url"), FieldPanel("linkedin_url"),
            FieldPanel("whatsapp_url"), FieldPanel("youtube_url"),
            FieldPanel("instagram_url"),
        ], heading="Social Links"),
        MultiFieldPanel([
            FieldPanel("footer_about_en"), FieldPanel("footer_about_fa"),
            FieldPanel("copyright_text_en"), FieldPanel("copyright_text_fa"),
        ], heading="Footer"),
        InlinePanel("footer_links", label="Footer quick links"),
    ]
 
    class Meta:
        verbose_name = "Site Branding & Settings"
 
 
class FooterLink(Orderable):
    settings = ParentalKey(SiteBrandingSettings, on_delete=models.CASCADE, related_name="footer_links")
    title_en = models.CharField(max_length=50)
    title_fa = models.CharField(max_length=50)
    link_page = models.ForeignKey("wagtailcore.Page", null=True, blank=True,
                                   on_delete=models.SET_NULL, related_name="+")
    link_url = models.URLField(blank=True)
 
    panels = [
        FieldPanel("title_en"), FieldPanel("title_fa"),
        FieldPanel("link_page"), FieldPanel("link_url"),
    ]
 
    @property
    def url(self):
        if self.link_page:
            return self.link_page.url
        return self.link_url or "#"
 