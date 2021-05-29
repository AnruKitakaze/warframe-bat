from django import forms
from .models import Weapon, WeaponAttackStats, Target, ResistancesOfDefenceResource


class OptimizeAverageDpsForm(forms.Form):
    weapon = forms.ModelChoiceField(queryset=Weapon.objects.all())
    target = forms.ModelChoiceField(queryset=Target.objects.all())
    target_level = forms.IntegerField(min_value=1, max_value=180)
