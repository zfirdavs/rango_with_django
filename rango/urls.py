from django.conf.urls import url
from rango import views

urlpatterns = [
    url(r'about/$', views.about, name='about'),
    url(r'category/(?P<category_name_slug>[\w\-]+)/$',
        views.show_category, name='show_category'),
    url(r'^add_category/$', views.add_category, name='add_category'),
    url(r'^category/(?P<category_name_slug>[\w\-]+)/add/$',
        views.add_page, name='add_page'),
    url(r'^restricted/', views.restricted, name='restricted'),
    url(r'^goto/$', views.track_url, name='goto'),
    url(r'^register_profile/$', views.register_profile, name='register_profile'),
    url(r'^profile/(?P<username>[\w\-]+)/$', views.profile, name='profile'),
    url(r'^profiles/$', views.list_profiles, name='list_profiles'),
    url(r'^like/$', views.like_category, name='like_category'),
    url(r'^suggest/$', views.suggest_category, name='suggest_category'),
]
