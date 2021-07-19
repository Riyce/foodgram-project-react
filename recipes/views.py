from django.conf import settings
from django.contrib.auth.decorators import login_required
from django.core.paginator import Paginator
from django.http import HttpResponse
from django.shortcuts import get_object_or_404, redirect, render

from .forms import RecipeForm
from .models import Follow, Ingredient, Recipe, RecipeIngredient, User
from .utils import (create_pdf, get_active_tags, get_ingredients,
                    get_ingredients_from_shoplist)


def index(request):
    active_tags = get_active_tags(request)
    list = Recipe.objects.filter(
        tags__slug__in=active_tags
    ).select_related('author').prefetch_related('tags').distinct()
    paginator = Paginator(list, settings.RECIPES_PER_PAGE)
    page_number = request.GET.get('page')
    page = paginator.get_page(page_number)
    return render(
        request,
        'index.html',
        {'page': page, 'paginator': paginator}
    )


def profile(request, username):
    author = get_object_or_404(User, username=username)
    active_tags = get_active_tags(request)
    list = Recipe.objects.filter(
        tags__slug__in=active_tags, author=author
    ).select_related('author').prefetch_related('tags').distinct()
    paginator = Paginator(list, settings.RECIPES_PER_PAGE)
    page_number = request.GET.get('page')
    page = paginator.get_page(page_number)
    return render(
        request,
        'index.html',
        {'page': page, 'paginator': paginator, 'author': author}
    )


@login_required
def follows(request):
    user_follows = Follow.objects.filter(user=request.user)
    paginator = Paginator(user_follows, settings.RECIPES_PER_PAGE)
    page_number = request.GET.get('page')
    page = paginator.get_page(page_number)
    return render(
        request,
        'follows.html',
        {'page': page, 'paginator': paginator}
    )


@login_required
def create_or_update_recipe(request, username=None, recipe_id=None):
    recipe = None
    if username and recipe_id:
        recipe = get_object_or_404(Recipe, id=recipe_id,
                                   author__username=username)
    form = RecipeForm(
        data=request.POST or None,
        files=request.FILES or None,
        instance=recipe
    )
    if recipe and request.user != recipe.author:
        return redirect('recipe', recipe_id=recipe_id, username=username)
    if form.is_valid():
        if recipe:
            recipe.recipe_ingredients.all().delete()
            form.save()
        else:
            recipe = form.save(commit=False)
            recipe.author = request.user
            recipe.save()
            recipe.tags.set(form.cleaned_data['tags'])
            recipe.save()
        ingredients = get_ingredients(request.POST)
        for name, ingredient_count in ingredients.items():
            ingredient = get_object_or_404(Ingredient, name=name)
            RecipeIngredient.objects.create(
                recipe=recipe, ingredient=ingredient,
                ingredient_count=ingredient_count
            )
        return redirect('recipe', recipe_id=recipe.id,
                        username=recipe.author.username)
    return render(
        request,
        'form_recipe.html',
        {'form': form, 'creation': recipe is None, 'recipe': recipe}
    )


@login_required
def delete_recipe(request, username, recipe_id):
    recipe = get_object_or_404(Recipe, id=recipe_id, author__username=username)
    recipe.delete()
    return redirect('index')


def recipe_page(request, username, recipe_id):
    recipe = get_object_or_404(Recipe, id=recipe_id, author__username=username)
    following = (
        request.user.is_authenticated
        and Follow.objects.filter(
            user=request.user,
            author__username=username
        ).exists()
    )
    return render(request, 'recipe_page.html', {'recipe': recipe,
                                                'following': following})


@login_required
def favorites(request):
    active_tags = get_active_tags(request)
    recipes = Recipe.objects.filter(favorites__user=request.user,
                                    tags__slug__in=active_tags).distinct()
    paginator = Paginator(recipes, settings.RECIPES_PER_PAGE)
    page_number = request.GET.get('page')
    page = paginator.get_page(page_number)
    return render(
        request,
        'index.html',
        {'paginator': paginator, 'page': page}
    )


@login_required
def purchases(request):
    purchases = request.user.purchases.all()
    return render(request, 'shop_list.html', {'purchases': purchases})


@login_required
def download_shopping_list(request):
    response = HttpResponse(content_type='application/pdf')
    response['Content-Disposition'] = 'attachment; filename="shoplist.pdf"'
    ingredients = get_ingredients_from_shoplist(request)
    pdf = create_pdf(ingredients)
    response.write(pdf)
    return response
