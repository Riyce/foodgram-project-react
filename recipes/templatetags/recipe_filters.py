from django import template

from recipes.models import Follow

register = template.Library()


@register.filter
def favorite_by_user(recipe, user):
    return user.favorites.filter(recipe=recipe).exists()


@register.filter
def get_purchases_count(user):
    return user.purchases.all().count()


@register.filter
def add_to_user_purchases(recipe, user):
    return user.purchases.filter(recipe=recipe).exists()


@register.filter()
def follow_by_user(author, user):
    return Follow.objects.filter(user=user, author=author).exists()
