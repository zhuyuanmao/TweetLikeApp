from django.db import models
from django.contrib.auth.models import(
    AbstractBaseUser,BaseUserManager,PermissionsMixin
)

import jwt
from django.conf import settings
from datetime import datetime,timedelta

class AuthorManager(BaseUserManager):
    '''
        Django requires that custom users define their own Manager class.
        By inheriting from "BaseUserManager", we get a lot of the same code used 
        by Django to create a "User" for free.
    '''

    def create_user(self,email,username,password=None):
        '''
        Create and return an Author with an email, username and password.
        '''

        if username is None:
            raise TypeError("Users must have a username.")
        if email is None: 
            raise TypeError("Users must have an email address.")

        user = self.model(email=self.normalize_email(email),username=username)
        user.set_password(password)
        user.save(using=self._db)

        return user

    def create_superuser(self,email,username, password):
        '''
        Create and return a 'User' with superuser powers.

        Superuser powers means that this use is an admin that can do anything they want.
        '''

        if password is None:
            raise TypeError("Superusers must have a password.")
        user = self.create_user(email,username=username,password=password)
        
        user.is_staff = True
        user.is_superuser=True 
        user.save(using=self._db)

        return user

class Author(AbstractBaseUser,PermissionsMixin):
    '''
    Each "User" needs a human-readable unique identifier that we can use to represent the "User" in the UI.
    We want to index this column in the database to improve lookup performance.
    '''
    username = models.CharField(db_index = True, max_length=255, unique = True)

    '''
    We also need a way to contact the user and a way for the user to identify thenselves when logging in. 
    Since we need an email address for contacting the user anyways, we will also use the email for logging 
    in because it is the most common form of login credential at the time of writing.
    '''
    email = models.EmailField(db_index = True, unique=True)
    
    
    '''
    When a user no longer wishes to use our platform, they may try to delete there account.
    we will simple offers users a way to deactivate their account instead of letting them delete it.
    '''
    
    is_active = models.BooleanField(default=True)
    
    '''
    The "is_staff" flag is expected by Django to determine who can and cannot log into the Django admin site.
    For most users, this flag will always be falsed.
    '''
    is_staff = models.BooleanField(default=False)

    
    '''
    Timestamp objects indicate a user signing up time and last loginng in time
    '''
    date_joined = models.DateField(auto_now=True)
    last_login = models.DateField(auto_now=True)

    '''
    The "USERNAME_FIELD" property tells use which field will use to login.
    In this case, we want that to be the email field.
    '''
    USERNAME_FIELD = 'email'
    REQUIRED_FIELDS = ['username']

    '''
    Tells Django that the AuthorManager class defined above should manage objects 
    of this type.
    '''

    objects = AuthorManager()

    def __str__(self):
        '''
        Returns a string representation of this "User".

        This string is used when a "User" is printed in the console.
        '''
        return self.email

    @property
    def token(self):
        """
        Allows us to get a user's token by calling 'user.token' instead of 'user.generate_jwt_token()'.
        """
        return self.__generate__jwt_token()

    def get_username(self):
        """
        This method is requested by Django for things like handling emails.
        Thsis would be the user's username.
        """
        return self.username

    def get_email(self):
        """
        This method is requested by Django for things like handling emails.
        Thsis would be the user's email.
        """
        return self.email
   
    def __generate__jwt_token(self):
        """
        Generates a JSON web Token that stores this user's ID 
        and has an expiry date set to 60 days into the future.
        """
        dt = datetime.now() + timedelta(days = 60)

        token = jwt.encode(
            {
                'id':self.pk,
                'exp':int(dt.strftime('%s'))
            }, settings.SECRET_KEY,algorithm='HS256')
        
        return token.decode('utf-8')

    
