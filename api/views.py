from rest_framework import permissions, viewsets
from rest_framework.decorators import action
from rango.models import Category, Page
from .serializers import CategorySerializer, PageSerializer


class CategoryViewSet(viewsets.ModelViewSet):
    """
        Category ViewSet
    """
    queryset = Category.objects.order_by('-likes')
    serializer_class = CategorySerializer
    permission_classes = (permissions.IsAuthenticatedOrReadOnly,)


class PageViewSet(viewsets.ModelViewSet):
    """
        Page ViewSet
    """
    queryset = Page.objects.order_by('-views')
    serializer_class = PageSerializer
    permission_classes = (permissions.IsAuthenticatedOrReadOnly,)
