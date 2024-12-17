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
    

class LikedRecipe(models.Model):
    recipe_id = models.IntegerField(primary_key=True)
    user = models.ForeignKey(User, on_delete=models.CASCADE, related_name='liked_recipes')  # Relationship to the user
    name = models.CharField(max_length=255)
    author_id = models.IntegerField()
    author_name = models.CharField(max_length=255)
    total_time = models.CharField(max_length=50)  # Time in ISO 8601 duration format
    date_published = models.DateField()
    description = models.TextField()
    images = models.URLField()
    recipe_category = models.CharField(max_length=255)
    keywords = models.TextField()  # Comma-separated keywords
    recipe_ingredient_parts = models.TextField()  # Store as JSON or stringified list
    calories = models.FloatField()
    fat_content = models.FloatField()
    saturated_fat_content = models.FloatField()
    cholesterol_content = models.FloatField()
    sodium_content = models.FloatField()
    carbohydrate_content = models.FloatField()
    fiber_content = models.FloatField()
    sugar_content = models.FloatField()
    protein_content = models.FloatField()
    recipe_servings = models.IntegerField()
    recipe_instructions = models.TextField()
    recipe_ingredients = models.TextField()  # Store as JSON or stringified list

    def __str__(self):
        return f"{self.user.username}'s liked recipe: {self.name}"


