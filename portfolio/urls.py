from django.urls import path
from . import views

app_name = 'portfolio'

urlpatterns = [
    path('', views.index, name='index'),
    path('contact/', views.contact, name='contact'),
    path('portfolio/<int:portfolio_id>/', views.portfolio_view, name='view'),
]

