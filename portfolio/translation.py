from modeltranslation.translator import register, TranslationOptions
from .models import Hero, About, TeamSection, TeamMember, Service, PortfolioItem, ContactInfo, SiteSetting


@register(Hero)
class HeroTranslationOptions(TranslationOptions):
    fields = ('title', 'subtitle', 'description')


@register(About)
class AboutTranslationOptions(TranslationOptions):
    fields = ('title', 'content')


@register(TeamMember)
class TeamMemberTranslationOptions(TranslationOptions):
    fields = ('name', 'role', 'bio')


@register(TeamSection)
class TeamSectionTranslationOptions(TranslationOptions):
    fields = ('title', 'subtitle')


@register(Service)
class ServiceTranslationOptions(TranslationOptions):
    fields = ('title', 'description')


@register(PortfolioItem)
class PortfolioItemTranslationOptions(TranslationOptions):
    fields = ('title', 'description')


@register(ContactInfo)
class ContactInfoTranslationOptions(TranslationOptions):
    fields = ()  # Email and phone don't need translation


@register(SiteSetting)
class SiteSettingTranslationOptions(TranslationOptions):
    fields = ('site_title',)

