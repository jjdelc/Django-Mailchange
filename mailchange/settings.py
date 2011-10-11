# -*- coding: utf-8 -*-

from django.conf import settings

NOTIFY_NEW_ADDRESS = getattr(settings, 'NOTIFY_NEW_ADDRESS', True)
CHANGE_MAIL_FROM = getattr(settings, 'CHANGE_MAIL_FROM', 
    settings.DEFAULT_FROM_EMAIL)
