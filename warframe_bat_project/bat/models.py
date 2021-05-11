from django.db import models


class Weapon(models.Model):
    weapon_name = models.CharField(primary_key=True, max_length=100)
    weapon_class = models.CharField(max_length=100)

    def __str__(self):
        return self.weapon_name


class WeaponAttackStats(models.Model):
    weapon_name = models.ForeignKey(Weapon, on_delete=models.CASCADE)
    attack_type = models.IntegerField()

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
