from django.contrib import admin
from django.urls import include, path
from rest_framework import routers
from recipeapi.views.register import login_user, register_user

router = routers.DefaultRouter(trailing_slash=False)

urlpatterns = [
    path('', include(router.urls)),
    path('login', login_user, name='login'),
    path('users', register_user, name='register_user')
]

