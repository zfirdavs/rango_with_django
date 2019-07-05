from rest_framework import serializers
from rango.models import Category, Page


class CategorySerializer(serializers.HyperlinkedModelSerializer):
    slug = serializers.SlugField(read_only=True)
    pages = serializers.HyperlinkedRelatedField(many=True,
                                                read_only=True,
                                                view_name='page-detail')

    class Meta:
        model = Category
        fields = ('instance_url', 'id', 'name', 'views', 'likes', 'slug', 'pages')


class PageSerializer(serializers.HyperlinkedModelSerializer):
    class Meta:
        model = Page
        fields = ('instance_url', 'id', 'title', 'url', 'views', 'url')
