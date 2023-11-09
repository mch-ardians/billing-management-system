from django.apps import AppConfig


class BioprofileConfig(AppConfig):
    default_auto_field = 'django.db.models.BigAutoField'
    name = 'bioprofile'

    def ready(self):
        import bioprofile.signals