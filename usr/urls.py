# -*- encoding: utf8 -*-
from django.conf.urls import include, url


urlpatterns = [
    # urls:
    url(r'^login/$', 'usr.views.login'),
    url(r'^login/do/$', 'usr.views.login_do'),
    url(r'^logout/$', 'usr.views.logout'),

]
