from django.contrib import admin
from django.utils.translation import gettext_lazy as _
from modeltranslation.admin import TranslationAdmin
from .models import Hero, About, Service, PortfolioItem, ContactInfo, ContactMessage, SiteSetting


@admin.register(Hero)
class HeroAdmin(TranslationAdmin):
    list_display = ['title', 'subtitle', 'is_active']
    list_filter = ['is_active']
    search_fields = ['title', 'subtitle']


@admin.register(About)
class AboutAdmin(TranslationAdmin):
    list_display = ['title', 'order', 'is_active']
    list_filter = ['is_active']
    search_fields = ['title', 'content']
    ordering = ['order', 'id']


@admin.register(Service)
class ServiceAdmin(TranslationAdmin):
    list_display = ['title', 'order', 'is_active']
    list_filter = ['is_active']
    search_fields = ['title', 'description']
    ordering = ['order', 'id']


@admin.register(PortfolioItem)
class PortfolioItemAdmin(TranslationAdmin):
    list_display = ['title', 'portfolio_type', 'order', 'is_active']
    list_filter = ['portfolio_type', 'is_active']
    search_fields = ['title', 'description']
    ordering = ['order', 'id']
    fieldsets = (
        (_('Basic Information'), {
            'fields': ('title', 'description', 'image', 'order', 'is_active')
        }),
        (_('Portfolio Type'), {
            'fields': ('portfolio_type',)
        }),
        (_('Online Portfolio'), {
            'fields': ('url',),
            'classes': ('online-fields',),
        }),
        (_('Offline Portfolio'), {
            'fields': ('offline_file',),
            'classes': ('offline-fields',),
        }),
    )
    
    class Media:
        js = ('admin/js/portfolio_admin.js',)
        css = {
            'all': ('admin/css/portfolio_admin.css',)
        }


@admin.register(ContactInfo)
class ContactInfoAdmin(admin.ModelAdmin):
    list_display = ['email', 'phone', 'is_active']
    list_filter = ['is_active']


@admin.register(ContactMessage)
class ContactMessageAdmin(admin.ModelAdmin):
    list_display = ['name', 'email', 'subject', 'created_at', 'is_read']
    list_filter = ['is_read', 'created_at']
    search_fields = ['name', 'email', 'subject', 'message']
    readonly_fields = ['created_at']
    ordering = ['-created_at']
    list_editable = ['is_read']
    date_hierarchy = 'created_at'
    fields = ['name', 'email', 'subject', 'message', 'created_at', 'is_read']


@admin.register(SiteSetting)
class SiteSettingAdmin(TranslationAdmin):
    list_display = ['site_title', 'is_active', 'updated_at']
    list_filter = ['is_active']
