from django.apps import AppConfig


class MailappConfig(AppConfig):
    default_auto_field = 'django.db.models.BigAutoField'
    name = 'mailApp'
    def ready(self):
        import mailApp.signals
