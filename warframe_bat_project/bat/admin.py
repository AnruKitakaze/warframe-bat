from django.contrib import admin
from .models import Weapon, WeaponAttackStats, Mod, ResistancesOfDefenceResource, Fraction, Target


admin.site.register(Weapon)
admin.site.register(WeaponAttackStats)
admin.site.register(Mod)
admin.site.register(ResistancesOfDefenceResource)
admin.site.register(Fraction)
admin.site.register(Target)
