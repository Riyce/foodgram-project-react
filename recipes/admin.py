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
    inlines = (RecipeIngredientInLine,)
    list_filter = ('tags',)
    list_display = ('title', 'author', 'tag_list', 'added')
    search_fields = ('title', 'author')

    def tag_list(self, obj):
        return ', '.join([tag.display_name for tag in obj.tags.all()])

    def added(self, obj):
        return obj.favorites.all().count()


@admin.register(Tag)
class TagAdmin(admin.ModelAdmin):
    list_display = ('slug', 'display_name', 'color')


@admin.register(RecipeIngredient)
class RecipeIngredientAdmin(admin.ModelAdmin):
    list_display = ('recipe', 'ingredient', 'count')
    search_fields = ('recipe', 'ingredient')

    def count(self, obj):
        return f'{obj.ingredient_count}-{obj.ingredient.unit}'


@admin.register(Follow)
class FollowAdmin(admin.ModelAdmin):
    list_filter = ('user', 'author')
    list_display = ('user', 'author')
    search_fields = ('user', 'author')


@admin.register(Favorite)
class FavoriteAdmin(admin.ModelAdmin):
    list_display = ('user', 'recipe')
    search_fields = ('user', 'recipe')


@admin.register(Purchase)
class ShopListAdmin(admin.ModelAdmin):
    pass
