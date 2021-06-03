from .models import Weapon, WeaponAttackStats, Target, ResistancesOfDefenceResource, Mod
from django.db.models import Q


def optimize(weapon, target, target_level):
    print(weapon.weapon_name)
    print(target.target_name)
    print(target_level)

    mod_list = Mod.objects.all().exclude(mod_tag__contains='condition')
    non_elemental_mods = Mod.objects.all().exclude(Q(mod_tag__contains='condition') | Q(mod_tag__contains='elemental'))
    weapon_stats = WeaponAttackStats.objects.get(weapon_name=weapon.weapon_name)
    mods = non_elemental_mods.all()
    total_mods_stats = [0.0 for i in range(25)]
    # Сначала поместим моды в первые 4 ячейки, только не-элементальные моды
    for i in range(0, 1):
        for mod in mods:
            current_mods_stats = total_mods_stats
            dps = get_dps(weapon_stats, target, target_level, current_mods_stats)
    return 0


# FIXME: Срочный рефактор этой гадости, разбить на отдельные функции
def get_dps(weapon_stats, target, target_level, stats):
    # FIXME: Кажись, stats надо заменить просто на лист модов, чтобы определять порядок модов ниже,
    # а сам статс уже создавать тут
    damage_per_shot = 0
    ws = weapon_stats

    total_damage = ws.impact + ws.puncture + ws.slash \
                   + ws.heat + ws.cold + ws.electric + ws.toxin \
                   + ws.blast + ws.corrosive + ws.gas + ws.magnetic + ws.radiation + ws.viral

    quantum = total_damage / 16
    # Подготовка к получению квантированного урона
    weapon_quantized_damage = [ws.impact, ws.puncture, ws.slash,
                               ws.heat, ws.cold, ws.electric, ws.toxin,
                               ws.blast, ws.corrosive, ws.gas, ws.magnetic, ws.radiation, ws.viral]
    # Учитываем все модификации. Ставим 12 + i так как статы урона начинаются с 13ого элемента
    for i in range(len(weapon_quantized_damage)):
        weapon_quantized_damage[i] = weapon_quantized_damage[i] * (1 + stats[12 + i] / 100)
    # TODO: Сюда вставить код, который будет отвечать за комбинирование элементального урона
    for i in range(len(weapon_quantized_damage)):
        weapon_quantized_damage[i] = round(weapon_quantized_damage[i] / quantum) * quantum

    # Крч, тут получим финальный урон за тычку
    final_damage_per_hit = [0.0 for i in range(len(weapon_quantized_damage))]
    armor = target.target_armor_base_value
    health = target.target_health_base_value
    # FIXME: Заполнить листы ниже
    print("Target is ", target.target_name)
    print("Armor type is ", target.target_armor_type)
    print("Armor base value is ", target.target_armor_base_value)
    # armor_modifiers_list = list(ResistancesOfDefenceResource.objects.get(defence_resource_name=target.target_armor_type).values())
    #
    # health_modifiers_list = list(ResistancesOfDefenceResource.objects.get(defence_resource_name=target.target_health_type).values())
    # for i in range(len(weapon_quantized_damage)):
    #     final_damage_per_hit[i] = (300 / (300 + armor * (1 - armor_modifiers_list[i]))) * (1 * health_modifiers_list[i])

    dps = damage_per_shot

    return dps
