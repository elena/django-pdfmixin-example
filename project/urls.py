# -*- coding: utf-8 -*-
from django.conf.urls import url, patterns, include
from pages.views import DetailView

from django.contrib import admin
admin.autodiscover()


urlpatterns = patterns('',
    url(r'^page/(?P<slug>[\w/-]+)$', DetailView.as_view(),
        name='page_detail'),

    (r'^admin/', include(admin.site.urls)),
)
