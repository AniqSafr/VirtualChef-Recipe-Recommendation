from django.contrib import admin
from .models import EditNutrition

@admin.register(EditNutrition)
class EditNutritionAdmin(admin.ModelAdmin):
    list_display = ('user', 'calories', 'fat', 'protein')  # Display key fields in the admin panel
