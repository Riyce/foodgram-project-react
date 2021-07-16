from django.shortcuts import get_object_or_404
from recipes.models import Favorite, Follow, Ingredient, Purchase
from rest_framework import mixins, permissions, status, viewsets
from rest_framework.response import Response

from api.serializers import (FavoriteSerializer, FollowSerializer,
                             IngredientSerializer, PurchasesSerializer)


class IngredientViewSet(viewsets.ModelViewSet):
    serializer_class = IngredientSerializer
    permission_classes = (permissions.IsAuthenticatedOrReadOnly,)

    def get_queryset(self):
        part_of_name = self.request.query_params.get('query', '')
        return Ingredient.objects.filter(name__contains=part_of_name)


class CreateDestroyViewSet(mixins.CreateModelMixin,
                           mixins.DestroyModelMixin,
                           viewsets.GenericViewSet):
    permission_classes = (permissions.IsAuthenticated,)

    def get_object(self, *args, **kwargs):
        queryset = self.filter_queryset(self.get_queryset())
        lookup_url_kwarg = self.lookup_url_kwarg or self.lookup_field
        filter_kwargs = {
            self.lookup_field: self.kwargs[lookup_url_kwarg], **kwargs,
        }
        obj = get_object_or_404(queryset, **filter_kwargs)
        self.check_object_permissions(self.request, obj)
        return obj

    def destroy(self, request, *args, **kwargs):
        instance = self.get_object(user=self.request.user)
        success = instance.delete()
        return Response({'success': bool(success)}, status=status.HTTP_200_OK)


class FollowViewSet(CreateDestroyViewSet):
    queryset = Follow.objects.all()
    serializer_class = FollowSerializer
    lookup_field = 'author'


class FavoriteViewSet(CreateDestroyViewSet):
    queryset = Favorite.objects.all()
    serializer_class = FavoriteSerializer
    lookup_field = 'recipe'


class PurchasesViewSet(CreateDestroyViewSet):
    queryset = Purchase.objects.all()
    serializer_class = PurchasesSerializer
    lookup_field = 'recipe'
