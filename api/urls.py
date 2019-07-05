from django.conf.urls import url, include
from rest_framework.routers import DefaultRouter
from rest_framework.schemas import get_schema_view
from .views import CategoryViewSet, PageViewSet

router = DefaultRouter()
router.register(r'categories', CategoryViewSet)
router.register(r'pages', PageViewSet)

schema_view = get_schema_view(title='Pastebin API')

urlpatterns = [
    url(r'^', include(router.urls)),
    url(r'^schema/$', schema_view),
]
