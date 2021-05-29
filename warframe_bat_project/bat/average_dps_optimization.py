from .models import Weapon, WeaponAttackStats, Target, ResistancesOfDefenceResource

def optimize(weapon, target, target_level):
    print(weapon.weapon_name)
    print(target.target_name)
    print(target_level)
    return 0