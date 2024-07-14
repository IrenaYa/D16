from django.apps import AppConfig


class NewappConfig(AppConfig):
    default_auto_field = 'django.db.models.BigAutoField'
    name = 'news'

    def ready(self):
        from . import signals  # выполнение модуля -> регистрация сигналов
