from rest_framework import serializers
from recipeapi.models import Ingredient
from recipeapi.views.measurement_unit import MeasurementUnitSerializer



class IngredientSerializer(serializers.ModelSerializer):
    measurement_unit = MeasurementUnitSerializer()

    class Meta:
        model = Ingredient
        fields = ('id', 'name', 'quantity', 'measurement_unit',)