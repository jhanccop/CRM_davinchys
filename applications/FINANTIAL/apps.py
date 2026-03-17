from django.apps import AppConfig


class FinantialConfig(AppConfig):
    default_auto_field = 'django.db.models.BigAutoField'
    name = 'applications.FINANTIAL'
    verbose_name = 'FINANCIAL - Documentos'
    verbose_name = 'New - Finanzas'

    def ready(self):
        import applications.FINANTIAL.signals  # noqa — registra los signals

 
    