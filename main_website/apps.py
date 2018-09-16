from django.apps import AppConfig


class MainWebsiteConfig(AppConfig):
    name = 'main_website'

    def ready(self):
        from user_updater import update
        update.start()
