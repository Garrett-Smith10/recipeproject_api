from django.db import models
from .measurement_unit import MeasurementUnit
from .grocery_list import GroceryList

class GroceryListItem(models.Model):
    grocery_list = models.ForeignKey(GroceryList, on_delete=models.CASCADE)
    ingredient_name = models.CharField(max_length=100)
    measurement_unit = models.ForeignKey(MeasurementUnit, on_delete=models.CASCADE)
    quantity = models.DecimalField(max_digits=5, decimal_places=2)