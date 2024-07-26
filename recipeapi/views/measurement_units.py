from rest_framework import serializers, viewsets
from recipeapi.models import MeasurementUnit
from rest_framework.permissions import IsAuthenticated

class MeasurementUnitSerializer(serializers.ModelSerializer):
    class Meta:
        model = MeasurementUnit
        fields = ('id', 'name')

class MeasurementUnitViewSet(viewsets.ModelViewSet):
    queryset = MeasurementUnit.objects.all()
    serializer_class = MeasurementUnitSerializer
    permission_classes = (IsAuthenticated,)