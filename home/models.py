from django.db import models
from modelcluster.fields import ParentalKey
from datetime import date

from wagtail.models import Page
from wagtail.fields import RichTextField, StreamField
from wagtail.admin.panels import FieldPanel, MultiFieldPanel, InlinePanel
from wagtail import blocks
from wagtail.images.blocks import ImageChooserBlock
from wagtail.contrib.forms.models import AbstractEmailForm, AbstractFormField
from wagtail.contrib.forms.panels import FormSubmissionsPanel
from wagtail.contrib.settings.models import BaseGenericSetting, register_setting
from wagtail.snippets.models import register_snippet

# ==========================================
# 📦 BLOCS RÉUTILISABLES
# ==========================================

class ShowBlock(blocks.StructBlock):
    title = blocks.CharBlock(label="Titre du spectacle", max_length=255)
    date = blocks.DateBlock(label="Date du spectacle")
    time = blocks.TimeBlock(label="Heure", required=False)
    venue = blocks.CharBlock(label="Nom du lieu", max_length=255)
    city = blocks.CharBlock(label="Ville", max_length=100)
    description = blocks.TextBlock(label="Description", required=False)
    poster = ImageChooserBlock(label="Affiche", required=False)
    ticket_link = blocks.URLBlock(label="Lien billetterie", required=False)

    class Meta:
        icon = 'date'
        label = "Spectacle"

class PressArticleBlock(blocks.StructBlock):
    publication_name = blocks.CharBlock(label="Nom de la publication", max_length=255)
    # AJOUT : Image pour le logo du journal ou scan
    publication_logo = ImageChooserBlock(label="Logo ou Photo de l'article", required=False)
    article_type = blocks.ChoiceBlock(choices=[
        ('paper', '📰 Article papier (PDF ou image)'),
        ('online', '🌐 Article en ligne (lien)'),
    ], label="Type d'article")
    article_url = blocks.URLBlock(label="Lien vers l'article", required=False)
    publication_date = blocks.DateBlock(label="Date de publication", required=False)
    excerpt = blocks.TextBlock(label="Extrait / Citation", required=False)

    class Meta:
        icon = 'doc-full'
        label = "Article de presse"

# ==========================================
# 💎 SNIPPETS (Témoignages)
# ==========================================

@register_snippet
class Testimonial(models.Model):
    quote = models.TextField(verbose_name="Avis / Remarque")
    author = models.CharField(max_length=255, verbose_name="Nom du spectateur")
    
    panels = [
        FieldPanel('quote'),
        FieldPanel('author'),
    ]

    def __str__(self):
        return f"{self.author} - {self.quote[:30]}..."

    class Meta:
        verbose_name = "Témoignage"
        verbose_name_plural = "Témoignages"

# ==========================================
# 🏠 PAGES DU SITE
# ==========================================

class HomePage(Page):
    hero_title = models.CharField(max_length=255, default="Wassim El Fath")
    hero_subtitle = models.CharField(max_length=255, default="Comédien Stand-Up")
    hero_description = RichTextField(blank=True)
    hero_image = models.ForeignKey(
        'wagtailimages.Image', 
        null=True, 
        blank=True, 
        on_delete=models.SET_NULL, 
        related_name='+'
    )
    
    featured_shows_title = models.CharField(max_length=255, default="Prochains Spectacles")
    spectacle_page = models.ForeignKey(
        'wagtailcore.Page',
        null=True,
        blank=True,
        on_delete=models.SET_NULL,
        related_name='+',
        verbose_name="Lien vers la page Spectacles"
    )

    content_panels = Page.content_panels + [
        MultiFieldPanel([
            FieldPanel('hero_title'),
            FieldPanel('hero_subtitle'),
            FieldPanel('hero_description'),
            FieldPanel('hero_image'),
        ], heading="Section Hero"),
        
        MultiFieldPanel([
            FieldPanel('featured_shows_title'),
            FieldPanel('spectacle_page'),
        ], heading="Lien vers les Spectacles"),
    ]

    # AJOUT : Cette fonction permet d'afficher les témoignages sur la Home
    def get_context(self, request):
        context = super().get_context(request)
        context['testimonials'] = Testimonial.objects.all()
        return context

    max_count = 1
    subpage_types = ['ShowsPage', 'GalleryPage', 'PressPage', 'AboutPage', 'ContactPage']


class ShowsPage(Page):
    intro = RichTextField(blank=True)
    shows = StreamField([('show', ShowBlock())], blank=True, use_json_field=True)

    content_panels = Page.content_panels + [
        FieldPanel('intro'),
        FieldPanel('shows'),
    ]

    def get_upcoming_shows(self):
        today = date.today()
        upcoming = [s for s in self.shows if s.value.get('date') and s.value.get('date') >= today]
        upcoming.sort(key=lambda x: x.value.get('date'))
        return upcoming


class GalleryPage(Page):
    intro = RichTextField(blank=True)
    gallery_images = StreamField([
        ('photo_cliche', blocks.StructBlock([
            ('image', ImageChooserBlock(label="Photo")),
            ('caption', blocks.CharBlock(label="Légende marrante", required=False)),
        ], label="Cliché avec légende"))
    ], blank=True, use_json_field=True)

    content_panels = Page.content_panels + [
        FieldPanel('intro'),
        FieldPanel('gallery_images'),
    ]


class PressPage(Page):
    intro = RichTextField(blank=True)
    press_articles = StreamField([('article', PressArticleBlock())], blank=True, use_json_field=True)

    content_panels = Page.content_panels + [
        FieldPanel('intro'),
        FieldPanel('press_articles'),
    ]


class AboutPage(Page):
    body = RichTextField()
    portrait_image = models.ForeignKey(
        'wagtailimages.Image', 
        null=True, 
        blank=True, 
        on_delete=models.SET_NULL, 
        related_name='+'
    ) # Assurez-vous que cette parenthèse est bien là

    funny_pdf = models.ForeignKey(
        'wagtaildocs.Document',
        null=True,
        blank=True,
        on_delete=models.SET_NULL,
        related_name='+'
    ) # Et celle-ci aussi

    content_panels = Page.content_panels + [
        FieldPanel('portrait_image'),
        FieldPanel('body'),
        FieldPanel('funny_pdf'),
    ]

# ==========================================
# 📧 CONTACT
# ==========================================

class FormField(AbstractFormField):
    page = ParentalKey('ContactPage', on_delete=models.CASCADE, related_name='form_fields')


class ContactPage(AbstractEmailForm):
    contact_image = models.ForeignKey(
        'wagtailimages.Image', 
        null=True, 
        blank=True, 
        on_delete=models.SET_NULL, 
        related_name='+'
    ) # Cette parenthèse fermait mal le bloc sur votre erreur
    
    intro = RichTextField(blank=True)
    thank_you_text = RichTextField(blank=True)

    content_panels = AbstractEmailForm.content_panels + [
        FormSubmissionsPanel(),
        FieldPanel('contact_image'),
        FieldPanel('intro'),
        InlinePanel('form_fields', label="Champs du formulaire"),
        FieldPanel('thank_you_text'),
        MultiFieldPanel([
            FieldPanel('to_address'),
            FieldPanel('from_address'),
            FieldPanel('subject'),
        ], heading="Configuration Email"),
    ]
# ==========================================
# ⚙️ RÉGLAGES GLOBAUX (Réseaux Sociaux)
# ==========================================

@register_setting
class SiteSettings(BaseGenericSetting):
    instagram_url = models.URLField(verbose_name="Instagram (URL)", blank=True, null=True)
    tiktok_url = models.URLField(verbose_name="TikTok (URL)", blank=True, null=True)
    youtube_url = models.URLField(verbose_name="YouTube (URL)", blank=True, null=True)
    facebook_url = models.URLField(verbose_name="Facebook (URL)", blank=True, null=True)
    linktree_url = models.URLField(verbose_name="Linktree (URL)", blank=True, null=True, default="https://linktr.ee/wassimelfath")

    panels = [
        MultiFieldPanel([
            FieldPanel('instagram_url'),
            FieldPanel('tiktok_url'),
            FieldPanel('youtube_url'),
            FieldPanel('facebook_url'),
            FieldPanel('linktree_url'),
        ], heading="Liens des réseaux sociaux")
    ]