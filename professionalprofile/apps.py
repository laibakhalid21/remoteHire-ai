from django.apps import AppConfig


class ProfessionalProfileConfig(AppConfig):
    name = 'professionalprofile'

    def ready(self):
        import professionalprofile.signals