from django.contrib import admin
from django.urls import include, path
from rest_framework.routers import DefaultRouter
from recipeapi.views import UserViewSet, MeasurementUnitViewSet

router = DefaultRouter(trailing_slash=False)
router.register(r'measurement_units', MeasurementUnitViewSet)

urlpatterns = [
    path('', include(router.urls)),
    path('login', UserViewSet.as_view({'post': 'user_login'}), name='login'),
    path('register', UserViewSet.as_view({'post': 'register_account'}), name='register'),
]