from django.apps import AppConfig
from django.utils.translation import ugettext_lazy as _


class ControlConfig(AppConfig):
    name = 'control'

    def ready(self):
        import control.signals