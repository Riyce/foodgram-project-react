from django.urls import include, path
from rest_framework import routers

from .views import (FavoriteViewSet, FollowViewSet, IngredientViewSet,
                    PurchasesViewSet)

router = routers.DefaultRouter()

router.register(r'ingredients', IngredientViewSet, basename='ingredients')
router.register(r'subscriptions', FollowViewSet, basename='follow')
router.register(r'favorites', FavoriteViewSet, basename='favorite')
router.register(r'purchases', PurchasesViewSet, basename='purchases')

urlpatterns = [
    path('v1/', include(router.urls)),
]
