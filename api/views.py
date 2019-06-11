from rango.models import Category
from .serializers import CategorySerializer
from rest_framework import generics, permissions
from rest_framework.decorators import api_view
from rest_framework.response import Response
from rest_framework.reverse import reverse


@api_view(['GET'])
def api_root(request, format=None):
    return Response({
        'categories': reverse('category-list', request=request, format=format)
    })


class CategoryList(generics.ListCreateAPIView):
    queryset = Category.objects.all()
    serializer_class = CategorySerializer

    permission_classes = (permissions.IsAuthenticatedOrReadOnly,)


class CategoryDetail(generics.RetrieveUpdateDestroyAPIView):
    queryset = Category.objects.all()
    serializer_class = CategorySerializer

    permission_classes = (permissions.IsAuthenticatedOrReadOnly,)
