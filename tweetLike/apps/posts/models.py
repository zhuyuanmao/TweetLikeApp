from django.db import models
from tweetLike.apps.core.models import TimestampedModel



class Post(TimestampedModel):
    """
        Makes a Post model which is related with an Author model
    """

    '''
    VISIBILITY = [
        ('PUBLIC','Public'),
        ('PRIVATE','Private'),
        ('FRIENDS',"Friends Only"),
        ('FOAF','Private to Friends of Friends'),
    ]
    UNLISTED = (
        (True,'True'),
        (False,'False')
    )
    '''
    CONTENT_TYPE = [
        ('text/plain','Plain Text'),
        ('text/markdown','Markdown'),
        ('image/png','Image with PNG format'),
        ('image/jpeg','Image with JPEG format'),
        ('application/base64','Application')
    ]

    # A slug is the last part of the url containing a unique string which 
    # identifies the resource being served by the web service.
    slug = models.SlugField(db_index=True,max_length=255,unique=True)
    title = models.CharField(max_length=255,db_index=True)
    contentType = models.CharField(max_length=48,default='text/plain',choices=CONTENT_TYPE)
    description = models.TextField()
    content = models.TextField()
    author = models.ForeignKey(
        'profiles.Profile',on_delete=models.CASCADE,related_name='posts'
    )

    tags = models.ManyToManyField(
        'posts.Tag',related_name='posts'
    )

    #visibility = models.CharField(max_length=48,default='PUBLIC',choices = VISIBILITY)
    #unlisted = models.BooleanField(default=False,choices=UNLISTED)
    def __str__(self):
        return self.title

class Comment(TimestampedModel):
    body = models.TextField()
    post = models.ForeignKey(
        'posts.Post',related_name='comments',on_delete=models.CASCADE
    )
    author = models.ForeignKey(
        'profiles.Profile',related_name='comments',on_delete=models.CASCADE
    )

class Tag(TimestampedModel):
    tag = models.CharField(max_length=255)
    slug = models.SlugField(db_index=True,unique=True)
    def __str__(self):
        return self.tag