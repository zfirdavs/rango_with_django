from django.conf.urls import url
from rest_framework.urlpatterns import format_suffix_patterns
from .views import CategoryList, CategoryDetail, api_root

urlpatterns = format_suffix_patterns([
    url(r'^$', api_root, name='api_root'),
    url(r'^categories/$', CategoryList.as_view(), name='category-list'),
    url(r'^categories/(?P<pk>\d+)/$', CategoryDetail.as_view(), name='category-detail'),
])
