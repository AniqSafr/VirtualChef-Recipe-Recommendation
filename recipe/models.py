from django.db import models
from django.contrib.auth.models import User  # Import the User model

class EditNutrition(models.Model):
    user = models.OneToOneField(User, on_delete=models.CASCADE, primary_key=True)  # Relationship with auth_user
    calories = models.DecimalField(max_digits=10, decimal_places=2)
    fat = models.DecimalField(max_digits=10, decimal_places=2)
    saturated_fat = models.DecimalField(max_digits=10, decimal_places=2)
    cholesterol = models.DecimalField(max_digits=10, decimal_places=2)
    sodium = models.DecimalField(max_digits=10, decimal_places=2)
    carbohydrate = models.DecimalField(max_digits=10, decimal_places=2)
    fiber = models.DecimalField(max_digits=10, decimal_places=2)
    sugar = models.DecimalField(max_digits=10, decimal_places=2)
    protein = models.DecimalField(max_digits=10, decimal_places=2)

    def __str__(self):
        return f"{self.user.username}'s Nutrition Data"
    
class ListItem(models.Model):
    id = models.AutoField(primary_key=True)  # AutoField handles IDs automatically; no need for a default
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    item_name = models.CharField(max_length=255)

    def __str__(self):
        return f"{self.user.username}'s item: {self.item_name}"

