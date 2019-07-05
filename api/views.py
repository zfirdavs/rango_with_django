from rango.models import Category, Page
from .serializers import CategorySerializer, PageSerializer
from rest_framework import permissions, viewsets


class CategoryViewSet(viewsets.ModelViewSet):
    """
        Category ViewSet
    """
    queryset = Category.objects.all()
    serializer_class = CategorySerializer
    permission_classes = (permissions.IsAuthenticatedOrReadOnly,)


class PageViewSet(viewsets.ModelViewSet):
    """
        Page ViewSet
    """
    queryset = Page.objects.all()
    serializer_class = PageSerializer
    permission_classes = (permissions.IsAuthenticatedOrReadOnly,)
