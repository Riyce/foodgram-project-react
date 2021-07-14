from django import template

register = template.Library()


@register.filter
def favorite_by_user(recipe, user):
    return user.favorites.filter(recipe=recipe).exists()


@register.filter
def get_purchases_count(user):
    return user.purchases.all().count()
