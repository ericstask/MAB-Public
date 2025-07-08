from django.apps import AppConfig


class ClientrelationsConfig(AppConfig):
    # default_auto_field = 'django.db.models.BigAutoField'
    name = 'clientrelations'

    def ready(self):
        import mab.tasks
