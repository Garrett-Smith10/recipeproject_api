from rest_framework import viewsets, status
from rest_framework.response import Response
from rest_framework import serializers
from recipeapi.models import Ingredient




class IngredientSerializer(serializers.ModelSerializer):
    class Meta:
        model = Ingredient
        fields = ('id', 'name')

class IngredientViewSet(viewsets.ViewSet):

    def list(self, request):
        ingredients = Ingredient.objects.all()
        serializer = IngredientSerializer(ingredients, many=True)
        return Response(serializer.data)

    def retrieve(self, request, pk=None):
        try:
            ingredient = Ingredient.objects.get(pk=pk)
            serializer = IngredientSerializer(ingredient)
            return Response(serializer.data)
        except Ingredient.DoesNotExist:
            return Response(status=status.HTTP_404_NOT_FOUND)