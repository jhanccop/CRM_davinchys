from django.apps import AppConfig

class QuotesConfig(AppConfig):
    default_auto_field = 'django.db.models.BigAutoField'
    name = 'applications.COMERCIAL.purchase'

    def ready(self):
        import applications.COMERCIAL.purchase.signals
