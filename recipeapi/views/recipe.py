from rest_frame import viewsets
from rest_framework.response import Response
from rest_framework import status
from .models import Recipe, Ingredient
from .serializers import RecipeSerializer

class RecipeViewSet(viewsets.ModelViewSet):
    queryset = Recipe.objects.all()
    serializer_class = RecipeSerializer

    def create(self, request, *args, **kwargs):
        serializer = self.get_serializer(data=request.data)
        serializer.is_valid(raise_exception=True)
        self.perform_create(serializer)
        
        # Get the newly created recipe instance
        recipe = serializer.instance

        # Get the list of ingredient IDs from the request data
        ingredient_ids = request.data.get('ingredients', [])

        # Set the ingredients for the recipe
        recipe.ingredients.set(ingredient_ids)

        headers = self.get_success_headers(serializer.data)
        return Response(serializer.data, status=status.HTTP_201_CREATED, headers=headers)
