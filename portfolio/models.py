import os
from io import BytesIO

from django.core.files.base import ContentFile
from django.db import models
from django.utils.translation import gettext_lazy as _
from PIL import Image

try:
    RESAMPLE_FILTER = Image.Resampling.LANCZOS  # Pillow ≥ 9
except AttributeError:  # pragma: no cover - fallback for older Pillow
    RESAMPLE_FILTER = Image.LANCZOS

MAX_IMAGE_WIDTH = 1920
MAX_IMAGE_HEIGHT = 1920
JPEG_QUALITY = 85
WEBP_QUALITY = 80


class Hero(models.Model):
    """Hero section content"""
    title = models.CharField(max_length=200, blank=True, null=True, verbose_name=_("Title"))
    subtitle = models.CharField(max_length=200, blank=True, null=True, verbose_name=_("Subtitle"))
    description = models.TextField(blank=True, null=True, verbose_name=_("Description"))
    is_active = models.BooleanField(default=True, verbose_name=_("Is Active"))
    
    class Meta:
        verbose_name = _("Hero")
        verbose_name_plural = _("Heroes")
    
    def __str__(self):
        # Try to get title in current language, fallback to any language
        if hasattr(self, 'title_en') and self.title_en:
            return self.title_en
        elif hasattr(self, 'title_fa') and self.title_fa:
            return self.title_fa
        return str(self.id) if self.id else "New"


class About(models.Model):
    """About section content"""
    title = models.CharField(max_length=200, blank=True, null=True, verbose_name=_("Title"))
    content = models.TextField(blank=True, null=True, verbose_name=_("Content"))
    order = models.IntegerField(default=0, verbose_name=_("Order"))
    is_active = models.BooleanField(default=True, verbose_name=_("Is Active"))
    
    class Meta:
        verbose_name = _("About")
        verbose_name_plural = _("About")
        ordering = ['order', 'id']
    
    def __str__(self):
        # Try to get title in current language, fallback to any language
        if hasattr(self, 'title_en') and self.title_en:
            return self.title_en
        elif hasattr(self, 'title_fa') and self.title_fa:
            return self.title_fa
        return str(self.id) if self.id else "New"


class TeamSection(models.Model):
    """Configurable copy for the team showcase"""
    title = models.CharField(max_length=200, blank=True, null=True, verbose_name=_("Title"))
    subtitle = models.TextField(blank=True, null=True, verbose_name=_("Subtitle"))
    is_active = models.BooleanField(default=True, verbose_name=_("Is Active"))

    class Meta:
        verbose_name = _("Team Section")
        verbose_name_plural = _("Team Sections")

    def __str__(self):
        if hasattr(self, 'title_en') and self.title_en:
            return self.title_en
        if hasattr(self, 'title_fa') and self.title_fa:
            return self.title_fa
        return self.title or _("Team Section")


class TeamMember(models.Model):
    """Team member information"""
    name = models.CharField(max_length=120, verbose_name=_("Name"))
    role = models.CharField(max_length=200, blank=True, null=True, verbose_name=_("Role"))
    bio = models.TextField(blank=True, null=True, verbose_name=_("Bio"))
    photo = models.ImageField(upload_to='team/', blank=True, null=True, verbose_name=_("Photo"))
    linkedin_url = models.URLField(blank=True, null=True, verbose_name=_("LinkedIn URL"))
    instagram_url = models.URLField(blank=True, null=True, verbose_name=_("Instagram URL"))
    github_url = models.URLField(blank=True, null=True, verbose_name=_("GitHub URL"))
    order = models.IntegerField(default=0, verbose_name=_("Order"))
    is_active = models.BooleanField(default=True, verbose_name=_("Is Active"))

    class Meta:
        verbose_name = _("Team Member")
        verbose_name_plural = _("Team Members")
        ordering = ['order', 'id']

    def __str__(self):
        if hasattr(self, 'name_en') and self.name_en:
            return self.name_en
        if hasattr(self, 'name_fa') and self.name_fa:
            return self.name_fa
        return self.name or _("Team Member")


class Service(models.Model):
    """Service items"""
    title = models.CharField(max_length=200, blank=True, null=True, verbose_name=_("Title"))
    description = models.TextField(blank=True, null=True, verbose_name=_("Description"))
    icon_svg = models.TextField(help_text=_("SVG code for the icon"), verbose_name=_("Icon SVG"))
    order = models.IntegerField(default=0, verbose_name=_("Order"))
    is_active = models.BooleanField(default=True, verbose_name=_("Is Active"))
    
    class Meta:
        verbose_name = _("Service")
        verbose_name_plural = _("Services")
        ordering = ['order', 'id']
    
    def __str__(self):
        # Try to get title in current language, fallback to any language
        if hasattr(self, 'title_en') and self.title_en:
            return self.title_en
        elif hasattr(self, 'title_fa') and self.title_fa:
            return self.title_fa
        return str(self.id) if self.id else "New"


class PortfolioItem(models.Model):
    """Portfolio items"""
    PORTFOLIO_TYPE_CHOICES = [
        ('online', _('Online')),
        ('offline', _('Offline')),
    ]
    
    title = models.CharField(max_length=200, blank=True, null=True, verbose_name=_("Title"))
    description = models.TextField(blank=True, null=True, verbose_name=_("Description"))
    image = models.ImageField(upload_to='portfolio/', blank=True, null=True, verbose_name=_("Image"))
    portfolio_type = models.CharField(
        max_length=10, 
        choices=PORTFOLIO_TYPE_CHOICES, 
        default='online',
        verbose_name=_("Portfolio Type")
    )
    # For online portfolios
    url = models.URLField(blank=True, null=True, verbose_name=_("URL"), help_text=_("Website URL (only for online portfolios)"))
    # For offline portfolios
    offline_file = models.FileField(
        upload_to='portfolio/offline/', 
        blank=True, 
        null=True, 
        verbose_name=_("Offline File"), 
        help_text=_("Upload ZIP file containing the complete website (only for offline portfolios)")
    )
    order = models.IntegerField(default=0, verbose_name=_("Order"))
    is_active = models.BooleanField(default=True, verbose_name=_("Is Active"))
    
    class Meta:
        verbose_name = _("Portfolio Item")
        verbose_name_plural = _("Portfolio Items")
        ordering = ['order', 'id']
    
    def __str__(self):
        # Try to get title in current language, fallback to any language
        title = None
        if hasattr(self, 'title_en') and self.title_en:
            title = self.title_en
        elif hasattr(self, 'title_fa') and self.title_fa:
            title = self.title_fa
        
        if title:
            return f"{title} - {self.get_portfolio_type_display()}"
        return f"Portfolio Item {self.id if self.id else '(New)'} - {self.get_portfolio_type_display()}"
    
    def clean(self):
        from django.core.exceptions import ValidationError
        if self.portfolio_type == 'online' and not self.url:
            raise ValidationError({'url': _('URL is required for online portfolios.')})
        if self.portfolio_type == 'offline' and not self.offline_file:
            raise ValidationError({'offline_file': _('Offline file is required for offline portfolios.')})

    def save(self, *args, **kwargs):
        if self.image and getattr(self.image, '_file', None):
            self._optimize_image()
        super().save(*args, **kwargs)

    def _optimize_image(self):
        image_field = self.image
        if not image_field:
            return

        image_file = getattr(image_field, 'file', None)
        if not image_file:
            return

        image_file.seek(0)

        try:
            with Image.open(image_file) as img:
                img_format = (img.format or '').upper()
                has_transparency = img.mode in ('RGBA', 'LA') or (img.mode == 'P' and 'transparency' in img.info)

                # Resize if bigger than the limits while preserving aspect ratio
                if img.width > MAX_IMAGE_WIDTH or img.height > MAX_IMAGE_HEIGHT:
                    img.thumbnail((MAX_IMAGE_WIDTH, MAX_IMAGE_HEIGHT), RESAMPLE_FILTER)

                buffer = BytesIO()

                if img_format in ('JPEG', 'JPG'):
                    if img.mode in ('RGBA', 'P', 'LA'):
                        img = img.convert('RGB')
                    img.save(
                        buffer,
                        format='JPEG',
                        quality=JPEG_QUALITY,
                        optimize=True,
                        progressive=True,
                    )
                elif img_format == 'PNG':
                    save_kwargs = {'optimize': True, 'compress_level': 6}
                    if not has_transparency:
                        # For PNG without transparency we can safely leverage JPEG to shrink further
                        img = img.convert('RGB')
                        img.save(
                            buffer,
                            format='JPEG',
                            quality=JPEG_QUALITY,
                            optimize=True,
                            progressive=True,
                        )
                        base, _ = os.path.splitext(image_field.name)
                        image_field.name = f"{base}.jpg"
                    else:
                        img.save(buffer, format='PNG', **save_kwargs)
                elif img_format == 'WEBP':
                    img.save(
                        buffer,
                        format='WEBP',
                        quality=WEBP_QUALITY,
                        method=6,
                    )
                else:
                    if img.mode in ('RGBA', 'P', 'LA'):
                        img = img.convert('RGB')
                    img.save(
                        buffer,
                        format='JPEG',
                        quality=JPEG_QUALITY,
                        optimize=True,
                        progressive=True,
                    )
                    base, _ = os.path.splitext(image_field.name)
                    image_field.name = f"{base}.jpg"
        except OSError:
            image_file.seek(0)
            return

        buffer.seek(0)
        image_field.save(image_field.name, ContentFile(buffer.read()), save=False)
        buffer.close()


class SiteSetting(models.Model):
    """Global site settings"""
    site_title = models.CharField(max_length=200, verbose_name=_("Site Title"))
    is_active = models.BooleanField(default=True, verbose_name=_("Is Active"))
    updated_at = models.DateTimeField(auto_now=True, verbose_name=_("Updated At"))

    class Meta:
        verbose_name = _("Site Setting")
        verbose_name_plural = _("Site Settings")
        ordering = ['-updated_at', '-id']

    def __str__(self):
        return self.site_title or _("Site Setting")


class ContactInfo(models.Model):
    """Contact information"""
    email = models.EmailField(verbose_name=_("Email"))
    phone = models.CharField(max_length=20, verbose_name=_("Phone"))
    telegram_url = models.URLField(blank=True, null=True, verbose_name=_("Telegram URL"))
    instagram_url = models.URLField(blank=True, null=True, verbose_name=_("Instagram URL"))
    is_active = models.BooleanField(default=True, verbose_name=_("Is Active"))
    
    class Meta:
        verbose_name = _("Contact Info")
        verbose_name_plural = _("Contact Info")
    
    def __str__(self):
        return f"Contact - {self.email}"


class ContactMessage(models.Model):
    """Contact form messages"""
    name = models.CharField(max_length=200, verbose_name=_("Name"))
    email = models.EmailField(verbose_name=_("Email"))
    subject = models.CharField(max_length=200, verbose_name=_("Subject"))
    message = models.TextField(verbose_name=_("Message"))
    created_at = models.DateTimeField(auto_now_add=True, verbose_name=_("Created At"))
    is_read = models.BooleanField(default=False, verbose_name=_("Is Read"))
    
    class Meta:
        verbose_name = _("Contact Message")
        verbose_name_plural = _("Contact Messages")
        ordering = ['-created_at']
    
    def __str__(self):
        return f"{self.name} - {self.subject}"
