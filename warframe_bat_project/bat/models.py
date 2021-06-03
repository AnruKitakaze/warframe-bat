from django.db import models


class Weapon(models.Model):
    weapon_name = models.CharField(primary_key=True, max_length=100)

    weapon_slot = models.CharField(max_length=100, default='Primary')
    weapon_type = models.CharField(max_length=100, default='Rifle')

    def __str__(self):
        return self.weapon_name


class WeaponAttackStats(models.Model):
    weapon_name = models.ForeignKey(Weapon, on_delete=models.CASCADE)
    attack_type = models.CharField(null=False, max_length=100, default='Primary')

    crit_chance = models.FloatField(null=False, default=0.0)
    crit_multiplier = models.FloatField(null=False, default=0.0)
    status_chance = models.FloatField(null=False, default=0.0)
    multishot = models.FloatField(null=False, default=1.0)
    
    accuracy = models.FloatField(null=False, default=0.0)
    fire_rate = models.FloatField(null=False, default=0.0)
    charge_speed = models.FloatField(null=False, default=0.0)
    magazine_size = models.FloatField(null=False, default=0.0)
    max_ammo = models.FloatField(null=False, default=0.0)
    reload_time = models.FloatField(null=False, default=0.0)
    damage_falloff_percent = models.FloatField(null=False, default=0.0)
    punch_through = models.FloatField(null=False, default=0.0)

    impact = models.FloatField(null=False, default=0.0)
    puncture = models.FloatField(null=False, default=0.0)
    slash = models.FloatField(null=False, default=0.0)

    heat = models.FloatField(null=False, default=0.0)
    cold = models.FloatField(null=False, default=0.0)
    electric = models.FloatField(null=False, default=0.0)
    toxin = models.FloatField(null=False, default=0.0)

    blast = models.FloatField(null=False, default=0.0)
    corrosive = models.FloatField(null=False, default=0.0)
    gas = models.FloatField(null=False, default=0.0)
    magnetic = models.FloatField(null=False, default=0.0)
    radiation = models.FloatField(null=False, default=0.0)
    viral = models.FloatField(null=False, default=0.0)

    class Meta:
        constraints = [
            models.UniqueConstraint(fields=['weapon_name', 'attack_type'], name='unique_attack')
        ]

    def __str__(self):
        return self.weapon_name.__str__()


class Mod(models.Model):
    mod_name = models.CharField(primary_key=True, max_length=100)
    mod_info = models.CharField(max_length=100, default='')
    mod_tag = models.CharField(max_length=100, default='')

    target_weapon_name = models.CharField(max_length=100)
    target_weapon_slot = models.CharField(max_length=100)
    target_weapon_type = models.CharField(max_length=100)

    damage = models.FloatField(null=False, default=0.0)

    crit_chance = models.FloatField(null=False, default=0.0)
    crit_damage = models.FloatField(null=False, default=0.0)
    status_chance = models.FloatField(null=False, default=0.0)
    multishot = models.FloatField(null=False, default=0.0)

    accuracy = models.FloatField(null=False, default=0.0)
    fire_rate = models.FloatField(null=False, default=0.0)
    charge_speed = models.FloatField(null=False, default=0.0)
    magazine_size = models.FloatField(null=False, default=0.0)
    max_ammo = models.FloatField(null=False, default=0.0)
    reload_time = models.FloatField(null=False, default=0.0)
    damage_falloff_percent = models.FloatField(null=False, default=0.0)
    punch_through = models.FloatField(null=False, default=0.0)

    impact = models.FloatField(null=False, default=0.0)
    puncture = models.FloatField(null=False, default=0.0)
    slash = models.FloatField(null=False, default=0.0)

    heat = models.FloatField(null=False, default=0.0)
    cold = models.FloatField(null=False, default=0.0)
    electric = models.FloatField(null=False, default=0.0)
    toxin = models.FloatField(null=False, default=0.0)

    def __str__(self):
        return self.mod_name


class ResistancesOfDefenceResource(models.Model):
    defence_resource_name = models.CharField(primary_key=True, max_length=100)

    impact = models.FloatField(null=False, default=0.0)
    puncture = models.FloatField(null=False, default=0.0)
    slash = models.FloatField(null=False, default=0.0)

    heat = models.FloatField(null=False, default=0.0)
    cold = models.FloatField(null=False, default=0.0)
    electric = models.FloatField(null=False, default=0.0)
    toxin = models.FloatField(null=False, default=0.0)

    blast = models.FloatField(null=False, default=0.0)
    corrosive = models.FloatField(null=False, default=0.0)
    gas = models.FloatField(null=False, default=0.0)
    magnetic = models.FloatField(null=False, default=0.0)
    radiation = models.FloatField(null=False, default=0.0)
    viral = models.FloatField(null=False, default=0.0)

    def __str__(self):
        return self.defence_resource_name


class Fraction(models.Model):
    fraction_name = models.CharField(primary_key=True, max_length=100)

    def __str__(self):
        return self.fraction_name


class Target(models.Model):
    target_name = models.CharField(primary_key=True, max_length=100)
    target_fraction = models.ForeignKey(Fraction, on_delete=models.CASCADE)

    target_shield_type = models.ForeignKey(ResistancesOfDefenceResource,
                                           on_delete=models.CASCADE, related_name='shield_type', default='None')
    target_shield_base_value = models.FloatField(null=False, default=0)

    target_health_type = models.ForeignKey(ResistancesOfDefenceResource,
                                           on_delete=models.CASCADE, related_name='health_type', default='None')
    target_health_base_value = models.FloatField(null=False, default=0)

    target_armor_type = models.ForeignKey(ResistancesOfDefenceResource,
                                          on_delete=models.CASCADE, related_name='armor_type', default='None')
    target_armor_base_value = models.FloatField(null=False, default=0)

    def __str__(self):
        return self.target_name

