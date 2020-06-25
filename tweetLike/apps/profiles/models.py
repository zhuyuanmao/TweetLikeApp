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

    def ___str___(self):
        return self.author.username

    def get_display_name(self):
        return str(self.firstName)+' '+str(self.lastName)