# Generated by Django 5.0.6 on 2024-05-19 20:03

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('main_app', '0003_alter_riddleitem_item'),
    ]

    operations = [
        migrations.AddField(
            model_name='item',
            name='category',
            field=models.CharField(default='', max_length=100),
            preserve_default=False,
        ),
    ]
