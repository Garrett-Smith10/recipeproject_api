from django.db import models
from .recipe import Recipe
from .ingredient import Ingredient
from .measurement_unit import MeasurementUnit

class RecipeIngredient(models.Model): 
    recipe = models.ForeignKey(Recipe, on_delete=models.CASCADE)
    ingredient = models.ForeignKey(Ingredient, on_delete=models.CASCADE)
    measurement_unit = models.ForeignKey(MeasurementUnit, on_delete=models.CASCADE)
    quantity = models.DecimalField(max_digits=5, decimal_places=2)
    