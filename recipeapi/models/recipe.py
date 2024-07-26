from django.db import models
from django.contrib.auth.models import User
from .ingredient import Ingredient
from .measurement_unit import MeasurementUnit

class Recipe(models.Model):
    name = models.CharField(max_length=100)
    image = models.ImageField(upload_to='recipes')
    cooking_instructions = models.TextField()
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    public = models.BooleanField(default=False)
    ingredients = models.ManyToManyField(Ingredient, through='RecipeIngredient')
