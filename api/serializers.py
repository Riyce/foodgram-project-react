from rest_framework import serializers

from recipes.models import Favorite, Follow, Ingredient, Purchase


class IngredientSerializer(serializers.ModelSerializer):
    class Meta:
        model = Ingredient
        fields = '__all__'


class Serializer(serializers.ModelSerializer):
    def create(self, validated_data):
        validated_data['user'] = self.context['request'].user
        return super().create(validated_data)


class FollowSerializer(Serializer):
    class Meta:
        model = Follow
        fields = ('author',)

    def validate(self, data):
        context = self.context['request']
        if data['author'] == context.user and context.method == 'POST':
            raise serializers.ValidationError(
                'Вы не можете подписываться на самого себя!'
            )
        if Follow.objects.filter(
            user=context.user, author=data['author']
        ).exists():
            raise serializers.ValidationError(
                'Такая подписка уже существует!'
            )
        return data


class FavoriteSerializer(Serializer):
    class Meta:
        model = Favorite
        fields = ('recipe',)

    def validate(self, data):
        if Favorite.objects.filter(
            user=self.context['request'].user, recipe=data['recipe']
        ).exists():
            raise serializers.ValidationError(
                'Вы уже добавили этот рецепт в избранное!'
            )
        return data


class PurchasesSerializer(Serializer):
    class Meta:
        model = Purchase
        fields = ('recipe',)

    def validate(self, data):
        if Purchase.objects.filter(
            user=self.context['request'].user, recipe=data['recipe']
        ).exists():
            raise serializers.ValidationError(
                'Вы уже добавили этот рецепт в покупки!'
            )
        return data
