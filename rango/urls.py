from django.conf.urls import url
from rango import views

urlpatterns = [
    url(r'^categories/$', views.CategoryList.as_view(), name='category_list'),
    url(r'^category/(?P<category_name_slug>[\w\-]+)/$',
        views.show_category, name='show_category'),
    url(r'^add_category/$', views.CategoryAdd.as_view(), name='add_category'),
    url(r'^category/(?P<category_name_slug>[\w\-]+)/add/$',
        views.PageAdd.as_view(), name='add_page'),
    url(r'^goto/$', views.track_url, name='goto'),
    url(r'^register_profile/$', views.register_profile, name='register_profile'),
    url(r'^profile/(?P<username>[\w\-]+)/$', views.profile, name='profile'),
    url(r'^profiles/$', views.ProfilesList.as_view(), name='list_profiles'),
    url(r'^like/$', views.like_category, name='like_category'),
    url(r'^suggest/$', views.suggest_category, name='suggest_category'),
]
