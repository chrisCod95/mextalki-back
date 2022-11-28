from django.apps import AppConfig


class UsersConfig(AppConfig):
    name = 'src.users'

    def ready(self):
        import src.users.signals
