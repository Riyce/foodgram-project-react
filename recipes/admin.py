from django.contrib import admin

from .models import (Favorite, Follow, Ingredient, Purchase, Recipe,
                     RecipeIngredient, Tag)


class RecipeIngredientInLine(admin.TabularInline):
    model = Recipe.ingredients.through
    extra = 2


@admin.register(Ingredient)
class IngredientAdmin(admin.ModelAdmin):
    pass


@admin.register(Recipe)
class RecipeAdmin(admin.ModelAdmin):
    inlines = (RecipeIngredientInLine, )


@admin.register(Tag)
class TagAdmin(admin.ModelAdmin):
    pass


@admin.register(RecipeIngredient)
class RecipeIngredientAdmin(admin.ModelAdmin):
    pass


@admin.register(Follow)
class FollowAdmin(admin.ModelAdmin):
    pass


@admin.register(Favorite)
class FavoriteAdmin(admin.ModelAdmin):
    pass


@admin.register(Purchase)
class ShopListAdmin(admin.ModelAdmin):
    pass
