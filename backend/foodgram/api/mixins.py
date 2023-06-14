from recipes.models import User
from rest_framework import mixins, viewsets

from .serializers import UserSerializer


class ModelViewSetMixins(viewsets.ModelViewSet):
    queryset = User.objects.all()
    serializer_class = UserSerializer
    http_method_names = ['GET', 'POST', 'PATCH', 'DELETE', 'HEAD', 'OPTIONS', ]


class ListCreateDestroyViewSet(mixins.ListModelMixin,
                               mixins.CreateModelMixin,
                               mixins.DestroyModelMixin,
                               viewsets.GenericViewSet
                               ):
    pass


class ListCreateFollowViewSet(
    mixins.CreateModelMixin,
    mixins.ListModelMixin,
    viewsets.GenericViewSet
):
    pass


class ListRetrieveViewSet(mixins.ListModelMixin,
                          mixins.RetrieveModelMixin,
                          viewsets.GenericViewSet):
    pass
