from django.db import models


class Weapon(models.Model):
    weapon_name = models.CharField(max_length=100)
    weapon_class = models.CharField(max_length=100)

    def __str__(self):
        return self.weapon_name


class WeaponAttackStats(models.Model):
    weapon_name = models.ForeignKey(Weapon, on_delete=models.CASCADE)
    attack_type = models.CharField(max_length=50)

    def __str__(self):
        return self.weapon_name.__str__()


class WeaponAttackDamageDisposition(models.Model):
    weapon_name = models.ForeignKey(WeaponAttackStats, on_delete=models.CASCADE)
    impact = models.FloatField()
    puncture = models.FloatField()
    slash = models.FloatField()

    def __str__(self):
        return self.weapon_name.__str__()
