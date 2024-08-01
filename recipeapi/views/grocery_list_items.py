from rest_framework import serializers, viewsets
from recipeapi.views import MeasurementUnitSerializer
from recipeapi.models import GroceryListItem


class GroceryListItemSerializer(serializers.ModelSerializer):
    measurement_unit = MeasurementUnitSerializer(read_only=True)

    class Meta:
        model = GroceryListItem
        fields = ['id', 'grocery_list', 'ingredient_name', 'measurement_unit', 'quantity']