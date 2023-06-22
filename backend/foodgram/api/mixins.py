from recipes.models import User
from rest_framework import mixins, viewsets

from .serializers import UserSerializer


class ModelViewSetMixins(viewsets.ModelViewSet):
    queryset = User.objects.all()
    serializer_class = UserSerializer


class ListRetrieveViewSet(mixins.ListModelMixin,
                          mixins.RetrieveModelMixin,
                          viewsets.GenericViewSet):
    pass
