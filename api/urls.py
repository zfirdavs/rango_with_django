from django.conf.urls import url
from rest_framework.urlpatterns import format_suffix_patterns
from .views import CategoryList, CategoryDetail

urlpatterns = [
    url(r'^categories/$', CategoryList.as_view()),
    url(r'^categories/(?P<pk>\d+)/$', CategoryDetail.as_view()),
]

urlpatterns = format_suffix_patterns(urlpatterns)
