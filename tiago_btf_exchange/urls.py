"""tiago_btf_exchange URL Configuration

The `urlpatterns` list routes URLs to views. For more information please see:
    https://docs.djangoproject.com/en/1.8/topics/http/urls/
Examples:
Function views
    1. Add an import:  from my_app import views
    2. Add a URL to urlpatterns:  url(r'^$', views.home, name='home')
Class-based views
    1. Add an import:  from other_app.views import Home
    2. Add a URL to urlpatterns:  url(r'^$', Home.as_view(), name='home')
Including another URLconf
    1. Add an import:  from blog import urls as blog_urls
    2. Add a URL to urlpatterns:  url(r'^blog/', include(blog_urls))
"""
from django.conf.urls import include, url
from django.contrib import admin
from bitfinex import views
from bitfinex_demo_feed import urls

urlpatterns = [
    url(r'^admin/', include(admin.site.urls)),
    url(r'^demo_feed/', include(urls)),
    url(r'^$', views.home, name='home'),
    url(r'^stop/$', views.stop, name='stop'),
    url(r'^start/(?P<id>\d+)/(?P<symbol>\w+)/(?P<interval>\w+)$', views.start, name='start'),
    url(r'^bitfinex/(?P<symbol>\w+)/(?P<interval>\w+)$', views.candle, name='candle'),
    url(r'^update_data/(?P<symbol>\w+)$', views.update_data, name='update_data')
]
