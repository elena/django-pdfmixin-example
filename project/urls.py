# -*- coding: utf-8 -*-
from django.conf.urls import url, patterns
from pages.views import DetailView

urlpatterns = patterns('',
    url(r'^page/(?P<slug>[\w/-]+)$', DetailView.as_view(),
        name='page_detail'),
)
