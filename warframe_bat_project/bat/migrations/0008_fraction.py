# Generated by Django 3.2.2 on 2021-05-23 17:22

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('bat', '0007_resistancesofdefenceresource'),
    ]

    operations = [
        migrations.CreateModel(
            name='Fraction',
            fields=[
                ('fraction_name', models.CharField(max_length=100, primary_key=True, serialize=False)),
            ],
        ),
    ]
