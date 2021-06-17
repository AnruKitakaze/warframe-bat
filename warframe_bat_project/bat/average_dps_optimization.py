from .models import Weapon, WeaponAttackStats, Target, ResistancesOfDefenceResource, Mod
from django.db.models import Q


def optimize(weapon, target, target_level):
    elemental_mods = Mod.objects.filter(mod_tag__contains='elemental')
    non_elemental_mods = Mod.objects.all().exclude(Q(mod_tag__contains='condition') |
                                                   Q(mod_tag__contains='elemental'))
    weapon_stats = WeaponAttackStats.objects.get(weapon_name=weapon.weapon_name)
    non_elemental_mods.all()
    # Шаг 1
    simple_mods = sorted(non_elemental_mods,
                         key=lambda _mod: get_dps(weapon_stats,
                                                  target,
                                                  target_level,
                                                  [_mod, None, None, None, None, None, None, None]),
                         reverse=True)
    print(simple_mods)
    mods = [simple_mods[i] for i in range(8)]

    # Шаг 2
    mods_to_insert = elemental_mods
    amount_of_inserted_mods = 0
    while amount_of_inserted_mods < 6:
        new_mod_list = mods.copy()
        temp_list = new_mod_list.copy()
        for i in range(amount_of_inserted_mods):
            new_mod_list[7-2-amount_of_inserted_mods] = new_mod_list[7-amount_of_inserted_mods]
        for i in range(len(mods_to_insert)):
            for j in range(len(mods_to_insert)):
                if i != j:
                    temp_list = [new_mod_list[i] for i in range(6)]
                    temp_list.append(mods_to_insert[i])
                    temp_list.append(mods_to_insert[j])
                    if get_dps(weapon_stats, target,
                               target_level, temp_list) > get_dps(weapon_stats, target,
                                                                  target_level, new_mod_list):
                        new_mod_list = temp_list.copy()
        if get_dps(weapon_stats, target,
                   target_level, new_mod_list) <= get_dps(weapon_stats, target,
                                                          target_level, mods):
            break
        else:
            mods = new_mod_list.copy()
            amount_of_inserted_mods += 2

    # Шаг 3
    while amount_of_inserted_mods < 7:
        new_mod_list = mods.copy()
        temp_list = new_mod_list.copy()
        for i in range(amount_of_inserted_mods):
            new_mod_list[7 - 1 - amount_of_inserted_mods] = new_mod_list[7 - amount_of_inserted_mods]
        for i in range(len(mods_to_insert)):
            temp_list = [new_mod_list[i] for i in range(7)]
            temp_list.append(mods_to_insert[i])
            if get_dps(weapon_stats, target,
                       target_level, temp_list) > get_dps(weapon_stats, target,
                                                          target_level, new_mod_list):
                new_mod_list = temp_list.copy()
        if get_dps(weapon_stats, target,
                   target_level, new_mod_list) <= get_dps(weapon_stats, target,
                                                          target_level, mods):
            break
        else:
            mods = new_mod_list.copy()
            amount_of_inserted_mods += 1

    burst_dps = get_dps(weapon_stats, target, target_level, mods)
    burst_dps = round(burst_dps)
    # print("Burst DPS is ", burst_dps)
    mod_list = ', '.join([mods[i].mod_name for i in range(8)])
    return burst_dps, mod_list


# FIXME: Срочный рефактор этой гадости, разбить на отдельные функции
def get_dps(weapon_stats, target, target_level, mods):
    final_stats_of_mods = [0.0 for i in range(26)]
    for i in range(8):
        if mods[i] is not None:
            final_stats_of_mods[0] += mods[i].damage
            final_stats_of_mods[1] += mods[i].crit_chance
            final_stats_of_mods[2] += mods[i].crit_damage
            final_stats_of_mods[3] += mods[i].status_chance
            final_stats_of_mods[4] += mods[i].multishot
            final_stats_of_mods[5] += mods[i].accuracy
            final_stats_of_mods[6] += mods[i].fire_rate
            final_stats_of_mods[7] += mods[i].charge_speed
            final_stats_of_mods[8] += mods[i].magazine_size
            final_stats_of_mods[9] += mods[i].max_ammo
            final_stats_of_mods[10] += mods[i].reload_time
            final_stats_of_mods[11] += mods[i].damage_falloff_percent
            final_stats_of_mods[12] += mods[i].punch_through
            final_stats_of_mods[13] += mods[i].impact
            final_stats_of_mods[14] += mods[i].puncture
            final_stats_of_mods[15] += mods[i].slash
            final_stats_of_mods[16] += mods[i].heat
            final_stats_of_mods[17] += mods[i].cold
            final_stats_of_mods[18] += mods[i].electric
            final_stats_of_mods[19] += mods[i].toxin
            # TODO: Вот сюда надо код для комбинирования урона крч, прямо во время вставки модов тип

    ws = weapon_stats
    weapon_damage = [ws.impact, ws.puncture, ws.slash,
                     ws.heat, ws.cold, ws.electric, ws.toxin,
                     ws.blast, ws.corrosive, ws.gas, ws.magnetic, ws.radiation, ws.viral]
    base_damage = sum(weapon_damage)
    base_damage *= (100 + final_stats_of_mods[0])/100
    # Посчитан квант
    quantum = base_damage / 16
    # Учитывает бонус типа Damage
    for i in range(len(weapon_damage)):
        weapon_damage[i] *= (100 + final_stats_of_mods[0])/100

    # Учитываем все модификации. Ставим 13 + i так как статы урона начинаются с 14ого элемента
    # Получаем значения урона
    for i in range(len(weapon_damage)):
        weapon_damage[i] += base_damage * ((final_stats_of_mods[13 + i])/100)
    for i in range(len(weapon_damage)):
        weapon_damage[i] = round(weapon_damage[i] / quantum) * quantum

    # Крч, сейчас будем получать финальный урон за тычку
    final_damage_per_hit = [weapon_damage[i] for i in range(len(weapon_damage))]
    # FIXME: Добавить функции для скейла брони от уровня
    armor = target.target_armor_base_value
    health = target.target_health_base_value

    # FIXME: Рефактор
    rodr = ResistancesOfDefenceResource.objects.get(defence_resource_name=target.target_armor_type)
    armor_modifiers_list = [rodr.impact, rodr.puncture, rodr.slash,
                            rodr.heat, rodr.cold, rodr.electric, rodr.toxin,
                            rodr.blast, rodr.corrosive, rodr.gas, rodr.magnetic, rodr.radiation, rodr.viral]

    rodr = ResistancesOfDefenceResource.objects.get(defence_resource_name=target.target_health_type)
    health_modifiers_list = [rodr.impact, rodr.puncture, rodr.slash,
                             rodr.heat, rodr.cold, rodr.electric, rodr.toxin,
                             rodr.blast, rodr.corrosive, rodr.gas, rodr.magnetic, rodr.radiation, rodr.viral]

    for i in range(len(weapon_damage)):
        final_damage_per_hit[i] = (300 / (300 + armor * (1 - armor_modifiers_list[i]/100))) \
                                  * (1 + armor_modifiers_list[i]/100) * (1 + health_modifiers_list[i]/100)
        final_damage_per_hit[i] *= weapon_damage[i]

    damage_per_shot = sum(final_damage_per_hit)
    dps = damage_per_shot
    # Теперь надо это домножить на статы, связанные с критом и тп, чтобы посчитать DPS
    final_crit_chance = weapon_stats.crit_chance * (1 + final_stats_of_mods[1]/100)
    final_crit_multiplier = weapon_stats.crit_multiplier * (1 + final_stats_of_mods[2]/100)
    average_crit_multiplier = 1 + final_crit_chance*(final_crit_multiplier - 1)

    # Учитываем криты
    dps *= average_crit_multiplier
    # Учитываем мультишот
    dps *= (weapon_stats.multishot * (1 + final_stats_of_mods[4]/100))

    # Учитываем fire_rate
    final_fire_rate = (weapon_stats.fire_rate * (1 + final_stats_of_mods[6]/100))
    dps *= final_fire_rate

    # Взрывной дпс -- дпс без учёта перезарядки
    burst_dps = dps

    final_magazine_size = (weapon_stats.magazine_size * (1 + final_stats_of_mods[8]/100))
    shooting_time = final_magazine_size / final_fire_rate
    final_reload_time = (weapon_stats.reload_time * (1 - final_stats_of_mods[10]/100))
    dps *= shooting_time / (shooting_time + final_reload_time)

    # Дпс с учётом перезарядок
    sustained_dps = dps

    return burst_dps
