# Generated by Django 5.0.6 on 2024-05-18 19:17

import django.db.models.deletion
from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('main_app', '0002_huntinstance_item_participation_and_more'),
    ]

    operations = [
        migrations.AlterField(
            model_name='riddleitem',
            name='item',
            field=models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='main_app.item'),
        ),
    ]
