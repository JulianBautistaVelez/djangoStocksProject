# Generated by Django 2.2.3 on 2019-07-28 14:42

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('groups', '0002_group_grouptype'),
    ]

    operations = [
        migrations.AlterField(
            model_name='group',
            name='grouptype',
            field=models.CharField(blank=True, choices=[('BVC', 'Bitcoin value chart'), ('CI', 'Companie info'), ('DJC', 'Dow jones companies'), ('CSC', 'Company stock chart')], max_length=3),
        ),
    ]
