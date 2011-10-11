# -*- coding: utf-8 -*-

from django.conf.urls.defaults import patterns, include, url

from mailchange import views

UUID_REGEX = '[a-f0-9]{8}-[a-f0-9]{4}-[a-f0-9]{4}-[a-f0-9]{4}-[a-f0-9]{12}'

urlpatterns = patterns('',
    url(r'^$',
        views.change_mail,
        name='change_mail'),

    url(r'^sent/$',
        views.change_request_sent,
        name='change_request_sent'),

    url(r'^confirm/(?P<uuid>%s)/$' % UUID_REGEX,
        views.confirm,
        name='change_mail_confirm'),

)
