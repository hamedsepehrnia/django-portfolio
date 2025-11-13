from django.utils.translation import gettext_lazy as _

from .models import SiteSetting


def site_settings(request):
    """
    Provide site-wide settings such as the translated site title.
    """
    settings_obj = (
        SiteSetting.objects.filter(is_active=True)
        .order_by('-updated_at', '-id')
        .first()
    )

    site_title = settings_obj.site_title if settings_obj else _("SkyPardaz - Creative Studio")

    return {
        'site_settings': settings_obj,
        'site_title': site_title,
    }

