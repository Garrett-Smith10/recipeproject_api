# Generated by Django 4.2.14 on 2024-07-24 17:01

from django.conf import settings
from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    initial = True

    dependencies = [
        migrations.swappable_dependency(settings.AUTH_USER_MODEL),
    ]

    operations = [
        migrations.CreateModel(
            name='GroceryList',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('name', models.CharField(max_length=100)),
                ('user', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to=settings.AUTH_USER_MODEL)),
            ],
        ),
        migrations.CreateModel(
            name='Ingredient',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('name', models.CharField(max_length=100, unique=True)),
            ],
        ),
        migrations.CreateModel(
            name='MeasurementUnit',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('name', models.CharField(max_length=50)),
            ],
        ),
        migrations.CreateModel(
            name='Recipe',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('name', models.CharField(max_length=100)),
                ('image', models.ImageField(upload_to='recipes/')),
                ('cooking_instructions', models.TextField()),
                ('public', models.BooleanField(default=False)),
            ],
        ),
        migrations.CreateModel(
            name='UserRecipe',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('recipe', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='recipeapi.recipe')),
                ('user', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to=settings.AUTH_USER_MODEL)),
            ],
        ),
        migrations.CreateModel(
            name='RecipeIngredient',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('quantity', models.DecimalField(decimal_places=2, max_digits=5)),
                ('ingredient', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='recipeapi.ingredient')),
                ('measurement_unit', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='recipeapi.measurementunit')),
                ('recipe', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='recipeapi.recipe')),
            ],
        ),
        migrations.AddField(
            model_name='recipe',
            name='ingredients',
            field=models.ManyToManyField(through='recipeapi.RecipeIngredient', to='recipeapi.ingredient'),
        ),
        migrations.AddField(
            model_name='recipe',
            name='user',
            field=models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to=settings.AUTH_USER_MODEL),
        ),
        migrations.CreateModel(
            name='GroceryListItem',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('ingredient_name', models.CharField(max_length=100)),
                ('quantity', models.DecimalField(decimal_places=2, max_digits=5)),
                ('grocery_list', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='recipeapi.grocerylist')),
                ('measurement_unit', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='recipeapi.measurementunit')),
            ],
        ),
    ]
