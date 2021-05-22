from django.contrib import admin
from .models import Weapon, WeaponAttackStats, Mod


admin.site.register(Weapon)
admin.site.register(WeaponAttackStats)
admin.site.register(Mod)
