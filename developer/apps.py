from django.apps import AppConfig
class DeveloperConfig(AppConfig):
    default_auto_field = 'django.db.models.BigAutoField'
    name = 'developer'

    def ready(self):
        import developer.signals
        import developer.handlers