from modeltranslation.translator import register, TranslationOptions
from .models import Hero, About, Service, PortfolioItem, ContactInfo


@register(Hero)
class HeroTranslationOptions(TranslationOptions):
    fields = ('title', 'subtitle', 'description')


@register(About)
class AboutTranslationOptions(TranslationOptions):
    fields = ('title', 'content')


@register(Service)
class ServiceTranslationOptions(TranslationOptions):
    fields = ('title', 'description')


@register(PortfolioItem)
class PortfolioItemTranslationOptions(TranslationOptions):
    fields = ('title', 'description')


@register(ContactInfo)
class ContactInfoTranslationOptions(TranslationOptions):
    fields = ()  # Email and phone don't need translation

