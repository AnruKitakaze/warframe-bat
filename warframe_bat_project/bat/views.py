from django.shortcuts import render


weapons = [
    {
        'name': 'Braton_Prime',
        'type': 'Primary',
        'info': 'Shoot bullets, oof!',
        'tier': 'C-'
    },
    {
        'name': 'Braton',
        'type': 'Primary',
        'info': 'Shoot weak bullets, oof!',
        'tier': 'D-'
    }
]


def home(request):
    context = {
        'weapons': weapons,
        'title': 'Home'
    }
    return render(request, 'bat/home.html', context)


def about(request):
    return render(request, 'bat/about.html', {'title': 'About'})
