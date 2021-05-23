from django.contrib import admin
from .models import Weapon, WeaponAttackStats, Mod, ResistancesOfDefenceResource


admin.site.register(Weapon)
admin.site.register(WeaponAttackStats)
admin.site.register(Mod)
admin.site.register(ResistancesOfDefenceResource)
