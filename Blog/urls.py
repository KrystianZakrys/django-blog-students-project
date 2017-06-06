from django.conf.urls import url
from Blog import views
from django.contrib.auth.views import login
from views import (login_view, logout_view)
urlpatterns = [
    url(r'^$', views.post_list, name='post_list'),
    url(r'^post/(?P<pk>[0-9]+)/$',views.post_details, name='post_details'),
    url(r'^register/$', views.register_view, name='register'),
    url(r'^add_post/$', views.add_post, name='add_post'),
    #url(r'^login/$',login, {'template_name': 'Blog/login.html'})
    url(r'^login/', login_view, name='login'),
    url(r'^logout/', logout_view, name='logout'),
]
