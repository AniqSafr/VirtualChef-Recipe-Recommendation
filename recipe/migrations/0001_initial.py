# Generated by Django 3.2 on 2024-12-14 02:29

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    initial = True

    dependencies = [
        ('auth', '0013_alter_user_username'),
    ]

    operations = [
        migrations.CreateModel(
            name='EditNutrition',
            fields=[
                ('user', models.OneToOneField(on_delete=django.db.models.deletion.CASCADE, primary_key=True, serialize=False, to='auth.user')),
                ('calories', models.DecimalField(decimal_places=2, max_digits=10)),
                ('fat', models.DecimalField(decimal_places=2, max_digits=10)),
                ('saturated_fat', models.DecimalField(decimal_places=2, max_digits=10)),
                ('cholesterol', models.DecimalField(decimal_places=2, max_digits=10)),
                ('sodium', models.DecimalField(decimal_places=2, max_digits=10)),
                ('carbohydrate', models.DecimalField(decimal_places=2, max_digits=10)),
                ('fiber', models.DecimalField(decimal_places=2, max_digits=10)),
                ('sugar', models.DecimalField(decimal_places=2, max_digits=10)),
                ('protein', models.DecimalField(decimal_places=2, max_digits=10)),
            ],
        ),
    ]
