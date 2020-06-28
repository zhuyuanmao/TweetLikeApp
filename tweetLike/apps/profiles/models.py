from django.db import models

# Create your models here.
from django.db import models

# Create your models here.
class Profile(models.Model):
    # There is an inherent relationship between the Profile and User models.
    # By creating a one-to-one relationship between the two,
    # We are formalizing this relationship. 
    # Every user will have one -- and only one related Profile model.
    author = models.OneToOneField('authentication.Author',on_delete=models.CASCADE)
    lastName = models.CharField(max_length=48,blank = True)
    firstName = models.CharField(max_length=48,blank = True)
    
    bio = models.TextField(blank=True)
    github =models.URLField(blank=True)
    image = models.URLField(blank=True)

    # This is an example of a Many-To-Many relationship where both sides of the 
    # relationship are of the same model. In this case, the model is 'Profile'.
    # As mentioned in the text, this relationship will be one-way. Just because
    # you are following mean does not mean that I am following you. This is a 
    # what 'symmetrical=False' does for us.

    follows = models.ManyToManyField(
        'self',
        related_name='followed_by',
        symmetrical=False
    )

    def ___str___(self):
        return self.author.username

    def get_display_name(self):
        return str(self.firstName)+' '+str(self.lastName)

    def follow(self, profile):
        """
        Follow 'profile' if we're not already following 'profile' 
        """
        self.follows.add(profile)
        
    def unfollow(self,profile):
        """
        Unfollow 'profile' if we're already following 'profile'
        """

        self.follows.remove(profile)

    def is_friends(self,profile):
        """
        Returns True if we're following each other.
        False otherwise.
        """
        return self.is_following(profile) and self.is_followed(profile)

    def is_following(self,profile):
        """
        Returns True if we're already following 'profile'
        False otherwise.
        """
        return self.follows.filter(pk=profile.pk).exists()

    def is_followed(self,profile):
        """
        Returns True if 'profile' is following us; 
        False otherwise.
        """
        return self.followed_by.filter(pk=profile.pk).exists()
    