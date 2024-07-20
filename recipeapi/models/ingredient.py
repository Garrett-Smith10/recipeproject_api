from django.db import models
from django.contrib.auth.models import User

class Ingredient (models.Model):
    name = models.CharField(max_length=100, unique=True)