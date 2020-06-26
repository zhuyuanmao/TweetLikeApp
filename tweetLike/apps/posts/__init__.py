from django.apps import AppConfig

class PostAppConfig(AppConfig):
    name ='tweetLike.apps.posts'
    label = 'posts'
    verbose_name = 'Posts'

    def ready(self):
        import tweetLike.apps.posts.signals

default_app_config = 'tweetLike.apps.posts.PostAppConfig'