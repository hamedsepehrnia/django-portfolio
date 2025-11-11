from django import forms
from django.core.exceptions import ValidationError
from django.utils.translation import gettext_lazy as _
from .models import PortfolioItem


class PortfolioItemForm(forms.ModelForm):
    class Meta:
        model = PortfolioItem
        fields = '__all__'
    
    def clean(self):
        cleaned_data = super().clean()
        portfolio_type = cleaned_data.get('portfolio_type')
        url = cleaned_data.get('url')
        offline_file = cleaned_data.get('offline_file')
        
        if portfolio_type == 'online':
            if not url:
                raise ValidationError({
                    'url': _('URL is required for online portfolios.')
                })
            # Clear offline_file if online
            if offline_file:
                cleaned_data['offline_file'] = None
        elif portfolio_type == 'offline':
            if not offline_file:
                raise ValidationError({
                    'offline_file': _('Offline file is required for offline portfolios.')
                })
            # Clear URL if offline
            if url:
                cleaned_data['url'] = ''
        
        return cleaned_data

