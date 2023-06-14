from api.views import (FollowViewSet, IngredientViewSet, RecipeViewSet,
                       TagViewSet)
from django.urls import include, path
from rest_framework.routers import DefaultRouter

app_name = 'api'


router_v1 = DefaultRouter()
router_v1.register('tags', TagViewSet, 'tags')
router_v1.register('ingredients', IngredientViewSet, 'ingredients')
router_v1.register('recipes', RecipeViewSet, 'recipes')
router_v1.register('users', FollowViewSet, 'users')

urlpatterns = (
    path('', include(router_v1.urls)),
    path('', include('djoser.urls')),
    path('auth/', include('djoser.urls.authtoken')),
)
