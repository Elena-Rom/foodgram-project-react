from rest_framework import mixins, viewsets

from recipes.models import User

from .serializers import UserSerializer


class ModelViewSetMixins(viewsets.ModelViewSet):
    queryset = User.objects.all()
    serializer_class = UserSerializer
    http_method_names = ['GET', 'POST', 'PATCH', 'DELETE', 'HEAD', 'OPTIONS', ]


class ListRetrieveViewSet(mixins.ListModelMixin,
                          mixins.RetrieveModelMixin,
                          viewsets.GenericViewSet):
    pass
