from rest_framework import serializers
from recipeapi.models import RecipeIngredient
from .ingredients import IngredientSerializer
from .measurement_units import MeasurementUnitSerializer 

class RecipeIngredientSerializer(serializers.ModelSerializer):
    ingredient = IngredientSerializer(read_only=True)
    measurement_unit = MeasurementUnitSerializer(read_only=True)

    class Meta:
        model = RecipeIngredient
        fields = ('ingredient', 'quantity', 'measurement_unit')