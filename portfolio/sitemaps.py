from django.contrib.sitemaps import Sitemap
from django.urls import reverse

from .models import PortfolioItem


class StaticViewSitemap(Sitemap):
    """Sitemap entries for static pages."""

    changefreq = "weekly"
    priority = 1.0
    i18n = True

    def items(self):
        return ["portfolio:index"]

    def location(self, item):
        return reverse(item)


class PortfolioItemSitemap(Sitemap):
    """Sitemap entries for individual portfolio items."""

    changefreq = "monthly"
    priority = 0.8
    i18n = True

    def items(self):
        return PortfolioItem.objects.filter(is_active=True)

    def location(self, obj):
        return reverse("portfolio:view", kwargs={"portfolio_id": obj.pk})


sitemaps = {
    "static": StaticViewSitemap,
    "portfolio": PortfolioItemSitemap,
}

