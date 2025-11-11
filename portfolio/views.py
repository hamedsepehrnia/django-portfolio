from django.shortcuts import render, redirect, get_object_or_404
from django.contrib import messages
from django.views.decorators.http import require_http_methods
from django.http import FileResponse, Http404
from django.utils import translation
from django.utils.translation import gettext_lazy as _
import os
from .models import Hero, About, Service, PortfolioItem, ContactInfo, ContactMessage


def index(request):
    """Main portfolio page"""
    # Get active content (modeltranslation handles language automatically)
    heroes = Hero.objects.filter(is_active=True)
    about_items = About.objects.filter(is_active=True)
    services = Service.objects.filter(is_active=True)
    portfolio_items = PortfolioItem.objects.filter(is_active=True)
    contact_info = ContactInfo.objects.filter(is_active=True)
    
    context = {
        'heroes': heroes,
        'about_items': about_items,
        'services': services,
        'portfolio_items': portfolio_items,
        'contact_info': contact_info,
    }
    
    return render(request, 'portfolio/index.html', context)


@require_http_methods(["POST"])
def contact(request):
    """Handle contact form submission"""
    if request.method == 'POST':
        name = request.POST.get('name', '').strip()
        email = request.POST.get('email', '').strip()
        subject = request.POST.get('subject', '').strip()
        message = request.POST.get('message', '').strip()
        
        if name and email and subject and message:
            try:
                ContactMessage.objects.create(
                    name=name,
                    email=email,
                    subject=subject,
                    message=message
                )
                messages.success(request, _('Your message has been sent successfully!'))
            except Exception as e:
                messages.error(request, _('An error occurred. Please try again.'))
        else:
            messages.error(request, _('Please fill in all fields.'))
    
    # Preserve current language in redirect
    from django.utils import translation
    language = translation.get_language()
    return redirect('portfolio:index')


def portfolio_view(request, portfolio_id):
    """View for displaying offline portfolio"""
    portfolio_item = get_object_or_404(PortfolioItem, id=portfolio_id, is_active=True)
    
    if portfolio_item.portfolio_type == 'online':
        # Redirect to the URL for online portfolios
        return redirect(portfolio_item.url)
    
    # For offline portfolios, serve the file
    if not portfolio_item.offline_file:
        raise Http404(_("Portfolio file not found"))
    
    file_path = portfolio_item.offline_file.path
    if not os.path.exists(file_path):
        raise Http404(_("Portfolio file not found"))
    
    # Return the file for download
    return FileResponse(
        open(file_path, 'rb'),
        as_attachment=True,
        filename=os.path.basename(file_path)
    )