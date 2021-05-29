from django.shortcuts import render
from django.urls import reverse
from django.http import HttpResponseRedirect, HttpResponse
from .models import Weapon, Target
from .forms import OptimizeAverageDpsForm
from .average_dps_optimization import optimize


def home(request):
    if request.method == 'POST':
        form = OptimizeAverageDpsForm(request.POST)

        if form.is_valid():
            weapon_name_data = form.cleaned_data['weapon']
            target_name_data = form.cleaned_data['target']
            target_level_data = form.cleaned_data['target_level']

            # FIXME: This is shit, need to add log and rework it
            current_weapon = Weapon.objects.get(weapon_name=weapon_name_data)
            current_target = Target.objects.get(target_name=target_name_data)
            # print(current_weapon.weapon_name)
            # print(current_target.target_name)
            # print(target_level_data)
            # print('sent')
            optimize(current_weapon, current_target, target_level_data)
    else:
        form = OptimizeAverageDpsForm()

    context = {
        'weapons': Weapon.objects.all(),
        'targets': Target.objects.all(),
        'title': 'Home',
        'form': form
    }

    return render(request, 'bat/home.html', context)


def about(request):
    return render(request, 'bat/about.html', {'title': 'About'})
