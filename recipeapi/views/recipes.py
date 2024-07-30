import json
from rest_framework import viewsets, status
from rest_framework import serializers
from rest_framework.response import Response
from recipeapi.models import Recipe, RecipeIngredient, MeasurementUnit, Ingredient
from .ingredients import IngredientSerializer  # Ensure this serializer exists
from decimal import Decimal


class RecipeSerializer(serializers.ModelSerializer):
    is_owner = serializers.SerializerMethodField()
    ingredients = serializers.SerializerMethodField()

    def get_is_owner(self, obj):
        # Check if the authenticated user is the owner
        return self.context["request"].user == obj.user

    def get_ingredients(self, obj):
        # Serialize the ingredients with their associated RecipeIngredient data
        ingredients = []
        for (
            recipe_ingredient
        ) in obj.recipeingredient_set.all():  # Accessing the through model
            ingredient = recipe_ingredient.ingredient
            quantity = recipe_ingredient.quantity
            measurement_unit = recipe_ingredient.measurement_unit
            measurement_unit_id = recipe_ingredient.measurement_unit_id
            measurement_unit_name = MeasurementUnit.objects.get(
                id=measurement_unit.id
            ).name
            ingredients.append(
                {
                    "ingredient": ingredient.name,
                    "quantity": quantity,
                    "measurement_unit_id": measurement_unit_id,
                    "measurement_unit": measurement_unit_name,  # Assuming you want to display the name; adjust as needed
                }
            )
        return ingredients

    class Meta:
        model = Recipe
        fields = [
            "id",
            "name",
            "image",
            "cooking_instructions",
            "is_owner",
            "ingredients",
        ]


class RecipeViewSet(viewsets.ViewSet):

    @staticmethod
    def find_or_create_ingredient(name):
        """
        Tries to find an Ingredient by name. If not found, creates a new Ingredient with the given name.

        :param name: The name of the ingredient.
        :return: An Ingredient object.
        """
        try:
            # Try to find an existing Ingredient by name
            return Ingredient.objects.get(name=name)
        except Ingredient.DoesNotExist:
            # If the Ingredient does not exist, create a new one
            return Ingredient.objects.create(name=name)

    def list(self, request):
        recipes = Recipe.objects.filter(user=request.user)
        serializer = RecipeSerializer(recipes, many=True, context={"request": request})
        return Response(serializer.data)

    def retrieve(self, request, pk=None):
        try:
            recipe = Recipe.objects.get(pk=pk)
            serializer = RecipeSerializer(recipe, context={"request": request})
            return Response(serializer.data)

        except Recipe.DoesNotExist:
            return Response(status=status.HTTP_404_NOT_FOUND)

    def create(self, request):
        # Extract data from request
        name = request.data.get("name")
        image = request.FILES.get("image")  # Handle file uploads
        cooking_instructions = request.data.get("cooking_instructions")

        # Create the recipe instance
        recipe = Recipe.objects.create(
            user=request.user,
            name=name,
            image=image,
            cooking_instructions=cooking_instructions,
        )

        # Handle ingredients if provided
        ingredient_data = request.data.get("ingredients", [])

        if isinstance(ingredient_data, str):
            ingredient_data = json.loads(ingredient_data)

        for ingredient_item in ingredient_data:
            ingredient_name = ingredient_item.get(
                "ingredient"
            )  # Adjust based on actual key
            quantity = ingredient_item.get("quantity")  # Adjust based on actual key
            measurement_unit_id = ingredient_item.get(
                "measurement_unit"
            )  # Adjust based on actual key

            # Find or create the Ingredient object based on the ingredient name
            ingredient = RecipeViewSet.find_or_create_ingredient(ingredient_name)

            # Find the MeasurementUnit object based on the measurement unit ID
            measurement_unit = MeasurementUnit.objects.get(id=measurement_unit_id)

            # Create or update the RecipeIngredient association
            RecipeIngredient.objects.update_or_create(
                recipe=recipe,
                ingredient=ingredient,
                defaults={"quantity": quantity, "measurement_unit": measurement_unit},
            )

        serializer = RecipeSerializer(recipe, context={"request": request})

        return Response(serializer.data, status=status.HTTP_201_CREATED)

    def update(self, request, pk=None):
        try:
            recipe = Recipe.objects.get(pk=pk)
            self.check_object_permissions(request, recipe)  # Check permissions

            # Extract recipe data
            name = request.data.get("name", recipe.name)
            image = request.FILES.get("image", recipe.image)
            cooking_instructions = request.data.get(
                "cooking_instructions", recipe.cooking_instructions
            )

            # Update recipe fields
            recipe.name = name
            recipe.image = image
            recipe.cooking_instructions = cooking_instructions
            recipe.save()

            RecipeIngredient.objects.filter(recipe=recipe).delete()

            # Handle ingredients
            ingredient_data = request.data.get("ingredients", [])
            for ingredient_info in ingredient_data:
                ingredient_name = ingredient_info.get("ingredient")
                quantity = ingredient_info.get("quantity")
                measurement_unit_id = ingredient_info.get("measurement_unit")

                # Find or create the Ingredient object
                ingredient, _ = Ingredient.objects.get_or_create(name=ingredient_name)

                # Find the MeasurementUnit object
                measurement_unit = MeasurementUnit.objects.get(id=measurement_unit_id)

                # Convert quantity to Decimal
                quantity_decimal = Decimal(quantity)

                # Create or update the RecipeIngredient association
                RecipeIngredient.objects.update_or_create(
                    recipe=recipe,
                    ingredient=ingredient,
                    defaults={
                        "quantity": quantity_decimal,
                        "measurement_unit": measurement_unit,
                    },
                )

            serializer = RecipeSerializer(recipe, context={"request": request})
            return Response(serializer.data, status=status.HTTP_200_OK)

        except Recipe.DoesNotExist:
            return Response(
                {"detail": "Recipe not found."}, status=status.HTTP_404_NOT_FOUND
            )

    def upload_image(self, request, pk=None):
        try:
            recipe = Recipe.objects.get(pk=pk)
            image_file = request.FILES["image"]
            recipe.image = image_file
            recipe.save()
            return Response(
                {"message": "Image uploaded successfully"}, status=status.HTTP_200_OK
            )
        except Exception as e:
            return Response({"error": str(e)}, status=status.HTTP_400_BAD_REQUEST)

    def destroy(self, request, pk=None):
        try:
            recipe = Recipe.objects.get(pk=pk)
            self.check_object_permissions(request, recipe)  # Check permissions
            recipe.delete()

            return Response(status=status.HTTP_204_NO_CONTENT)

        except Recipe.DoesNotExist:
            return Response(status=status.HTTP_404_NOT_FOUND)
