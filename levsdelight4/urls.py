from django.conf.urls import include, url
from django.contrib import admin
from levsdelight_app.views import *

urlpatterns = [
    # Examples:
    # url(r'^$', 'levsdelight4.views.home', name='home'),
    # url(r'^blog/', include('blog.urls')),

    url(r'^admin/', include(admin.site.urls)),

    # url(r'^$', 'levsdelight_app.views.main.home', name='home'),
    url(r'^api/slideshow/(?P<year>\d{4})/(?P<month>[^/]+)/$', 'levsdelight_app.views.main.slideshow', name='slideshow'),
    url(r'^api/monthlist/$', 'levsdelight_app.views.main.monthlist', name='monthlist'),
    url(r'^api/allslides/(?P<limit>[0-9]{1,3})/$', 'levsdelight_app.views.main.allslides', name='allslides'),
    url(r'^api/allslides/$', 'levsdelight_app.views.main.allslides', name='allslides'),
    url(r'^api/uploadimage/$', 'levsdelight_app.views.main.uploadimage', name='uploadimage'),


]
