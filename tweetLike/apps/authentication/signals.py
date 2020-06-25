from django.db.models.signals import post_save
from django.dispatch import receiver

from tweetLike.apps.profiles.models import Profile

from .models import Author

@receiver(post_save,sender=Author)
def create_related_profile(sender,instance,created,*args,**kwargs):
    # Notice that we're checking for 'created' here.
    # We only want to do this the first time the 'Author' instance is created.
    # If the save that caused
    # this signal to be run was an update action, we know the user already
    # has a profile.
    if instance and created:
        instance.profile = Profile.objects.create(author=instance)