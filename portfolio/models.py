from django.db import models
from django.utils.translation import gettext_lazy as _


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


class ContactInfo(models.Model):
    """Contact information"""
    email = models.EmailField(verbose_name=_("Email"))
    phone = models.CharField(max_length=20, verbose_name=_("Phone"))
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
