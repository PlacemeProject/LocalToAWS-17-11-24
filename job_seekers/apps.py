from django.apps import AppConfig


class JobSeekersConfig(AppConfig):
    default_auto_field = 'django.db.models.BigAutoField'
    name = 'job_seekers'

    def ready(self):
        import job_seekers.signals  # Import the signals module