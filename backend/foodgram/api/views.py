from django.shortcuts import get_object_or_404
from django_filters.rest_framework import DjangoFilterBackend
from recipes.models import (Favorite, Follow, Ingredient, Recipe, ShoppingList,
                            Tag)
from rest_framework import status, viewsets
from rest_framework.decorators import action
from rest_framework.filters import SearchFilter
from rest_framework.pagination import PageNumberPagination
from rest_framework.permissions import IsAuthenticated
from rest_framework.response import Response
from rest_framework.viewsets import ReadOnlyModelViewSet

from .mixins import ListCreateFollowViewSet, ListRetrieveViewSet
from .permissions import AdminAuthorOrReadOnly, IsAdminOrReadOnly
from .serializers import (FavoriteSerializer, FollowSerializer,
                          IngredientSerializer, RecipeSerializer,
                          ShoppingListSerializer, SmallRecipeSerializer,
                          TagSerializer)


class FollowViewSet(ListCreateFollowViewSet):
    queryset = Follow.objects.all()
    serializer_class = FollowSerializer
    permission_classes = (IsAuthenticated,)
    filter_backends = (SearchFilter,)
    search_fields = ('user__username', 'following__username',)

    def get_queryset(self):
        return self.request.user.follower.all()

    def perform_create(self, serializer):
        serializer.save(user=self.request.user)


class TagViewSet(ReadOnlyModelViewSet):
    queryset = Tag.objects.all()
    serializer_class = TagSerializer
    permission_classes = (IsAdminOrReadOnly,)


class IngredientViewSet(ListRetrieveViewSet):
    queryset = Ingredient.objects.all()
    serializer_class = IngredientSerializer
    pagination_class = None
    permission_classes = (IsAdminOrReadOnly,)
    filter_backends = [SearchFilter]
    search_fields = ['^name']


class RecipeViewSet(viewsets.ModelViewSet):
    queryset = Recipe.objects.all()
    pagination_class = PageNumberPagination
    permission_classes = (AdminAuthorOrReadOnly,)
    # filterset_class = RecipeFilter
    filter_backends = (DjangoFilterBackend,)

    def get_serializer_class(self):
        if self.request.method == 'GET':
            return SmallRecipeSerializer
        return RecipeSerializer

    @action(
        detail=True,
        methods=["POST", "DELETE"],
        url_path="favorite",
        permission_classes=(AdminAuthorOrReadOnly,),
    )
    def favorite(self, request, pk=None):
        user = request.user
        recipe = get_object_or_404(Recipe, id=pk)
        if request.method == "POST":
            if Favorite.objects.filter(user=user, recipe=recipe).exists():
                return Response(
                    {"error": "Этот рецепт уже в избранном"},
                    status=status.HTTP_400_BAD_REQUEST,
                )
            favorite = Favorite.objects.create(user=user, recipe=recipe)
            serializer = FavoriteSerializer(
                favorite,
                context={"request": request}
            )
            return Response(serializer.data, status=status.HTTP_201_CREATED)

        if request.method == "DELETE":
            favorite = Favorite.objects.filter(user=user, recipe=recipe)
            if favorite.exists():
                favorite.delete()
                return Response(status=status.HTTP_204_NO_CONTENT)
            return Response(status=status.HTTP_400_BAD_REQUEST)

    @action(
        detail=True,
        methods=["POST", "DELETE"],
        url_path="shopping_cart",
        permission_classes=(AdminAuthorOrReadOnly,),
    )
    def shopping_cart(self, request, pk=None):
        user = request.user
        recipe = get_object_or_404(Recipe, id=pk)
        if request.method == "POST":
            if ShoppingList.objects.filter(user=user, recipe=recipe).exists():
                return Response(
                    {"error": "Этот рецепт уже в корзине покупок"},
                    status=status.HTTP_400_BAD_REQUEST,
                )
            shopping_list = ShoppingList.objects.create(
                user=user,
                recipe=recipe
            )
            serializer = ShoppingListSerializer(
                shopping_list, context={"request": request}
            )
            return Response(serializer.data, status=status.HTTP_201_CREATED)

        if request.method == "DELETE":
            delete_shoping_cart = ShoppingList.objects.filter(user=user,
                                                              recipe=recipe)
            if delete_shoping_cart.exists():
                delete_shoping_cart.delete()
                return Response(status=status.HTTP_204_NO_CONTENT)
            return Response(status=status.HTTP_400_BAD_REQUEST)

    def get_serializer_context(self):
        context = super().get_serializer_context()
        context.update({"request": self.request})
        return context
