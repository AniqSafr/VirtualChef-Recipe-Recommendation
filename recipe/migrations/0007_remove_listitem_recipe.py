# Generated by Django 3.2 on 2025-01-16 18:13

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('recipe', '0006_listitem_recipe'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='listitem',
            name='recipe',
        ),
    ]
