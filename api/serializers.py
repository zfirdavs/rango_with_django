from rest_framework import serializers
from rango.models import Category


class CategorySerializer(serializers.HyperlinkedModelSerializer):
    slug = serializers.SlugField(read_only=True)

    class Meta:
        model = Category
        fields = ('url', 'id', 'name', 'views', 'likes', 'slug')
