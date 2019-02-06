# -*- coding: utf-8 -*-
from __future__ import unicode_literals
from django.apps import AppConfig
from django.utils.translation import ugettext_lazy as _



class WebConfig(AppConfig):
    name = 'web'
    verbose_name = _('cableGuy')

    def ready(self):
        import web.signals  # noqa
