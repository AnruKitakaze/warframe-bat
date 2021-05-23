from django.shortcuts import render
from .models import Weapon, Target


def home(request):
    context = {
        'weapons': Weapon.objects.all(),
        'targets': Target.objects.all(),
        'title': 'Home'
    }
    return render(request, 'bat/home.html', context)


def about(request):
    return render(request, 'bat/about.html', {'title': 'About'})
