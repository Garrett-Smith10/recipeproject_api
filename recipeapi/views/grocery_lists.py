from decimal import Decimal
from rest_framework import serializers, viewsets, status
from rest_framework.response import Response
from rest_framework.decorators import action
from recipeapi.views import GroceryListItemSerializer
from recipeapi.models import GroceryList, GroceryListItem, Recipe, MeasurementUnit

class GroceryListSerializer(serializers.ModelSerializer):
    items = serializers.SerializerMethodField()

    class Meta:
        model = GroceryList
        fields = ['id', 'user', 'name', 'items']

    @staticmethod
    def convert_quantity(quantity, from_unit, to_unit="Cup (c)"):
        conversion_factors = {
            "Teaspoon (tsp)": Decimal('0.16667'),  # 1 tsp = 0.16667 c
            "Tablespoon (tbsp)": Decimal('0.5'),   # 1 tbsp = 0.5 c
            "Fluid ounce (fl oz)": Decimal('0.125'),  # 1 fl oz = 0.125 c
            "Cup (c)": Decimal('1'),               # 1 c = 1 c
            "Pint (pt)": Decimal('0.5'),           # 1 pt = 0.5 c
            "Quart (qt)": Decimal('0.25'),         # 1 qt = 0.25 c
            "Gallon (gal)": Decimal('0.00423'),    # 1 gal = 0.00423 c
            "Milliliter (ml)": Decimal('0.00042'), # 1 ml = 0.00042 c
            "Liter (l)": Decimal('0.00118'),       # 1 l = 0.00118 c
            "Gram (g)": Decimal('0.00000352'),     # 1 g = 0.00000352 c
            "Kilogram (kg)": Decimal('0.00224'),   # 1 kg = 0.00224 c
            "Ounce (oz)": Decimal('0.02957'),      # 1 oz = 0.02957 c
            "Pound (lb)": Decimal('0.00423'),      # 1 lb = 0.00423 c
        }

        if isinstance(quantity, str):  # Assuming quantity is sometimes a string
            try:
                quantity = Decimal(quantity)
            except ValueError:
                pass  # Handle case where quantity cannot be converted to Decimal

        if from_unit in conversion_factors:
            return quantity * conversion_factors[from_unit]
        else:
            return quantity

    def get_items(self, obj):
        items = []
        for grocery_list_item in obj.grocerylistitem_set.all():
            ingredient = grocery_list_item.ingredient_name
            quantity = grocery_list_item.quantity
            measurement_unit = grocery_list_item.measurement_unit
            measurement_unit_name = MeasurementUnit.objects.get(id=measurement_unit.id).name
            
            # Convert quantity to cups if possible
            if measurement_unit_name in ["Teaspoon (tsp)", "Tablespoon (tbsp)", "Fluid ounce (fl oz)", "Cup (c)", "Pint (pt)", "Quart (qt)", "Gallon (gal)", "Milliliter (ml)", "Liter (l)", "Gram (g)", "Kilogram (kg)", "Ounce (oz)", "Pound (lb)"]:
                converted_quantity = self.convert_quantity(quantity, measurement_unit_name, "Cup (c)")
                items.append({
                    "ingredient": ingredient,
                    "quantity": converted_quantity,
                    "measurement_unit": "Cup (c)",
                })
            else:
                items.append({
                    "ingredient": ingredient,
                    "quantity": quantity,
                    "measurement_unit": measurement_unit_name,
                })
        return items

class GroceryListViewSet(viewsets.ViewSet):
    serializer_class = GroceryListSerializer

    

    def list(self, request):
        queryset = GroceryList.objects.filter(user=request.user)
        serializer = GroceryListSerializer(queryset, many=True, context={"request": request})
        return Response(serializer.data)

    def create(self, request):
        selected_recipe_ids = request.data.get('selectedRecipes', [])

    # Retrieve the name from the request data
        name = request.data.get('name', "Default Grocery List Name")

    # Create a new GroceryList instance with the name from the request data
        grocery_list = GroceryList.objects.create(user=request.user, name=name)
        
        # Iterate through selected recipes
        for recipe_id in selected_recipe_ids:
            recipe = Recipe.objects.get(id=recipe_id)
            
            # Extract ingredients from the recipe
            for recipe_ingredient in recipe.recipeingredient_set.all():
                # Check if the ingredient already exists in the grocery list
                grocery_list_item, created = GroceryListItem.objects.get_or_create(
                    grocery_list=grocery_list,
                    ingredient_name=recipe_ingredient.ingredient.name,
                    defaults={
                        "quantity": recipe_ingredient.quantity,
                        "measurement_unit": recipe_ingredient.measurement_unit,
                    }
                )
                
                # If the item was created, update the quantity; otherwise, increment it
                if created:
                    grocery_list_item.quantity = recipe_ingredient.quantity
                else:
                    grocery_list_item.quantity += recipe_ingredient.quantity
                
                grocery_list_item.save()

        # Serialize and return the grocery list
        serializer = GroceryListSerializer(grocery_list, context={'request': request})
        return Response(serializer.data, status=status.HTTP_201_CREATED)

    def retrieve(self, request, pk=None):
        try:
            grocery_list = GroceryList.objects.prefetch_related('grocerylistitem_set').get(pk=pk)
            serializer = GroceryListSerializer(grocery_list, context={"request": request})
            return Response(serializer.data)
        except GroceryList.DoesNotExist:
            return Response(status=status.HTTP_404_NOT_FOUND)

    def destroy(self, request, pk=None):
        try:
            grocery_list = GroceryList.objects.get(pk=pk)
            grocery_list.delete()
            return Response(status=status.HTTP_204_NO_CONTENT)
        except GroceryList.DoesNotExist:
            return Response(status=status.HTTP_404_NOT_FOUND)

    @action(detail=True, methods=['post'], url_path='add-item')
    def add_item(self, request, pk=None):
        grocery_list = self.get_object()
        item_data = request.data
        item_serializer = GroceryListItemSerializer(data=item_data)
        if item_serializer.is_valid():
            item_serializer.save(grocery_list=grocery_list)
            return Response(item_serializer.data, status=status.HTTP_201_CREATED)
        return Response(item_serializer.errors, status=status.HTTP_400_BAD_REQUEST)
