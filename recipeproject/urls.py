from django.contrib import admin
from recipeproject import settings
from django.conf.urls.static import static
from django.urls import include, path
from rest_framework.routers import DefaultRouter
from recipeapi.views import UserViewSet, MeasurementUnitViewSet, RecipeViewSet
from rest_framework.parsers import MultiPartParser

router = DefaultRouter(trailing_slash=False)
router.register(r"measurement_units", MeasurementUnitViewSet, "measurement_unit")
router.register(r"recipes", RecipeViewSet, "recipe")

urlpatterns = [
    path("", include(router.urls)),
    path("login", UserViewSet.as_view({"post": "user_login"}), name="login"),
    path(
        "register", UserViewSet.as_view({"post": "register_account"}), name="register"
    ),
]

urlpatterns += [
    path("recipes/<int:pk>/upload-image/", RecipeViewSet.as_view({"post": "upload_image"}), name="upload_image"),
    ]
if settings.DEBUG:
    urlpatterns += static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)
