# Generated by Django 3.2 on 2025-01-16 18:33

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('recipe', '0007_remove_listitem_recipe'),
    ]

    operations = [
        migrations.AddField(
            model_name='listitem',
            name='recipe',
            field=models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.CASCADE, related_name='items', to='recipe.likedrecipe'),
        ),
    ]
