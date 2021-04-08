from django.urls import path
from . import views

urlpatterns = [
    path('', views.home, name='bat-home'),
    path('about/', views.about, name='bat-about'),
]