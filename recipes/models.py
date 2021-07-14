from django.contrib.auth import get_user_model
from django.db import models

User = get_user_model()


class Tag(models.Model):
    slug = models.CharField(verbose_name='Слаг', max_length=50)
    display_name = models.CharField(
        verbose_name='Название тега', unique=True, max_length=50
    )
    color = models.CharField(verbose_name='Цвет', max_length=10)

    class Meta:
        verbose_name = 'Тег'
        verbose_name_plural = 'Теги'

    def __str__(self) -> str:
        return self.slug


class Ingredient(models.Model):
    name = models.CharField(verbose_name='Название', max_length=128)
    unit = models.CharField(verbose_name='Единица измерения', max_length=32)

    class Meta:
        ordering = ['name']
        verbose_name = 'Ингредиент'
        verbose_name_plural = 'Ингредиенты'

    def __str__(self) -> str:
        return f'{self.name} - {self.unit}'


class Recipe(models.Model):
    author = models.ForeignKey(
        User, on_delete=models.CASCADE,
        verbose_name='Автор', related_name='recipies'
    )
    title = models.CharField(verbose_name='Название', max_length=128)
    image = models.ImageField(verbose_name='Изображение', upload_to='recipes/')
    description = models.TextField(verbose_name='Описание')
    cooking_time = models.PositiveSmallIntegerField(
        verbose_name='Время приготовления'
    )
    ingredients = models.ManyToManyField(
        Ingredient, verbose_name='Ингридиенты', through='RecipeIngredient'
    )
    tags = models.ManyToManyField(Tag, verbose_name='Теги')

    class Meta:
        ordering = ['title']
        verbose_name = 'Рецепт'
        verbose_name_plural = 'Рецепты'

    def __str__(self) -> str:
        return self.title


class RecipeIngredient(models.Model):
    recipe = models.ForeignKey(
        Recipe, on_delete=models.CASCADE, verbose_name='Рецепт',
        related_name='recipe_ingredients',
    )
    ingredient = models.ForeignKey(
        Ingredient, on_delete=models.CASCADE, verbose_name='Ингредиент',
        related_name='ingredient_recipes',
    )
    ingredient_count = models.PositiveIntegerField(verbose_name='Количество')

    class Meta:
        ordering = ['recipe']
        verbose_name = 'Ингредиент рецепта'
        verbose_name_plural = 'Ингредиенты рецептов'


class Follow(models.Model):
    user = models.ForeignKey(
        User, on_delete=models.CASCADE,
        verbose_name='Подписчик', related_name='follower'
    )
    author = models.ForeignKey(
        User, on_delete=models.CASCADE,
        verbose_name='Автор', related_name='following'
    )

    class Meta:
        verbose_name = 'Подписка'
        verbose_name_plural = 'Подписки'
        unique_together = ('user', 'author')
        ordering = ('user', 'author')
        constraints = [
            models.UniqueConstraint(
                fields=['user', 'author'], name='user_author')
        ]

    def __str__(self):
        return f'{self.user} - {self.author}'


class Favorite(models.Model):
    user = models.ForeignKey(
        User, on_delete=models.CASCADE,
        verbose_name='Пользователь', related_name='favorites'
    )
    recipe = models.ForeignKey(
        Recipe, on_delete=models.CASCADE,
        verbose_name='Рецепт', related_name='favorites'
    )
    created = models.DateTimeField(
        auto_now_add=True, db_index=True, verbose_name='Время подписки'
    )

    class Meta:
        verbose_name = 'Избранный рецепт'
        verbose_name_plural = 'Избранные рецепты'
        unique_together = ['user', 'recipe']
        ordering = ['-created']

    def __str__(self):
        return f'{self.user} - {self.recipe}'


class Purchase(models.Model):
    recipe = models.ForeignKey(Recipe, on_delete=models.CASCADE,
                               related_name='recipe_to_purchase')
    user = models.ForeignKey(User, on_delete=models.CASCADE,
                             related_name='purchases')

    class Meta:
        verbose_name = 'Список покупок'
        verbose_name_plural = 'Списки покупок'
        constraints = [
            models.UniqueConstraint(
                fields=['user', 'recipe'], name='user_purchases')
        ]

    def __str__(self) -> str:
        return f'{self.user} - {self.recipe}'
