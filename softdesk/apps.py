from django.apps import AppConfig


class SoftdeskConfig(AppConfig):
    default_auto_field = 'django.db.models.BigAutoField'
    name = 'softdesk'

    def ready(self):
        # Do not delete : implicitly connect signal handlers decorated
        # with @receiver.
        # See Django docs:
        # https://docs.djangoproject.com/en/5.1/topics/signals/#connecting-receiver-functions
        import softdesk.signals
