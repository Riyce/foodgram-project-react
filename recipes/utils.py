from io import BytesIO

from reportlab.pdfbase import pdfmetrics
from reportlab.pdfbase.ttfonts import TTFont
from reportlab.pdfgen import canvas

from .models import Purchase, RecipeIngredient, Tag

INGREDIENT_STRING = '{name} - {count}({unit})'


def get_ingredients(request):
    ingredients = {}
    for var in request:
        if var.startswith('nameIngredient'):
            ing = request[var]
            _, num = var.split('_')
            ing_count = abs(int(request.get('valueIngredient_' + num)))
            if ing in ingredients.keys():
                ingredients[ing] += ing_count
                continue
            ingredients[ing] = ing_count
    return ingredients


def get_ingredients_from_shoplist(request):
    user = request.user
    ingredients = {}
    for purchase in Purchase.objects.filter(user=user):
        recipe = purchase.recipe
        for ingredient in recipe.ingredients.all():
            try:
                recipe_ingredient = RecipeIngredient.objects.get(
                    recipe=recipe,
                    ingredient=ingredient
                )
                ingredient_count = recipe_ingredient.ingredient_count
                if ingredients.get(ingredient):
                    ingredients[ingredient] += ingredient_count
                    continue
                ingredients[ingredient] = ingredient_count
            except RecipeIngredient.DoesNotExist:
                continue
    return ingredients


def create_pdf(ingredients):
    pdfmetrics.registerFont(TTFont('Vera', 'Vera.ttf'))
    buffer = BytesIO()
    doc = canvas.Canvas(buffer)
    doc.setFont('Vera', 12)
    doc.drawString(250, 800, 'My SHOPLIST')
    h = 600
    for ingredient in ingredients.keys():
        doc.drawString(
            x=100, y=h,
            text=INGREDIENT_STRING.format(name=ingredient.name,
                                          count=ingredients[ingredient],
                                          unit=ingredient.unit),
            charSpace=2, wordSpace=10
        )
        h = h - 20
    doc.showPage()
    doc.save()
    pdf = buffer.getvalue()
    buffer.close()
    return pdf


def get_active_tags(request):
    return (request.GET.getlist('tags') if request.GET.getlist('tags') else
            Tag.objects.values_list('slug'))
