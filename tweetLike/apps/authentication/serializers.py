from django.contrib.auth import authenticate
from rest_framework import serializers
from .models import Author

from tweetLike.apps.profiles.serializers import ProfileSerializer

class RegistrationSerializer(serializers.ModelSerializer):
    """
    Serializers registration requets and creates a new user
    """

    # Ensure passwords are at least 8 characters long, no logner
    # than 128 charactesrs, and can not be read by the client.
    password = serializers.CharField(max_length=128,min_length=8,write_only = True)

    #The client should not be able to send a token along with a registration 
    #request. Making 'token' read-only handles that for us.
    token = serializers.CharField(max_length=255, read_only = True)

    class Meta:
        model = Author
        # List all of the fields that could possibly be included in a request
        # or response, including fields specified explicitly above.
        fields = ["email","username","password","token"]
    
    def create(self, validated_data):
        # Use the "create_user" method we wrote earlier to create a new user.
        return Author.objects.create_user(**validated_data)

class LoginSerializer(serializers.Serializer):

    email = serializers.EmailField(max_length=255)
    username = serializers.CharField(max_length=255,read_only = True)
    password = serializers.CharField(max_length=128,write_only = True)
    token = serializers.CharField(max_length=255,read_only = True)

    def validate(self,data):
        # The 'validate' method is where we make sure that the current 
        # instance of 'LoginSerializer' has 'valid'.
        # In this case of logging a user in, this means validating that 
        # they've provided an email and password and that this combination 
        # matches one of the users in out databases. 
        
        email = data.get('email',None)
        password = data.get('password',None)

        # As mentioned above, an email is required. Raise an exception if an
        # email is not provide. 
        # At same time, a password is required. Raise an exception if an password
        # is not provide.

        if email is None:
            raise serializers.ValidationError("An email address is required to log in.")
        if password is None:
            raise serializers.ValidationError("An password is required to log in.")
        
        # The 'authenticate' method provided by Django and handles checking 
        # for a user that matches this email/password combination. Notice how
        # we pass 'email' as the 'username' value. Remember that, in our User 
        # model, we set 'USERNAME_FIELD" as 'email'

        user = authenticate(username=email,password=password)

        # if no user was found matching this email/password combination then 
        # 'authentication' will return 'None'. Raise an exception in this case.
        if user is None:
            raise serializers.ValidationError(
            "A user with this email and password was not found."
        )
        # Django provides a flag on our 'User' model called 'is_active'.
        # The purpose of this flag to tell us whether the user has been banned
        # or otherwise deactived.
        if not user.is_active:
            raise serializers.ValidationError("This user has been deactivated")
        

        # The 'validate' method should return a dictionary of validated data.
        # This is the data that is passed to the "create" and "update" methods.
        return {
            'email':user.email,
            'username':user.username,
            'token':user.token,
        }

class AuthorSerializer(serializers.ModelSerializer):
    """
    Handles serialization and deserilization of User objects.
    """

    # Password must be at least 8 characters, but no more than 128 characters.
    # These values are the default provided by Django.
    # We could change them, but that would create extra work while introducing 
    # no benefits.

    password = serializers.CharField(
        max_length=128,
        min_length=8,
        write_only = True
    )

    # Adding for Profiles modules
    ###########################################################################
    # When a field should be handled as a serializer, we must explicitly say so.
    # Moreover, "AuthorSerilaizer" should never expose profile information,
    # So we set 'write_only=True'
    profile = ProfileSerializer(write_only=True)
    # We want to get the 'bio','image','firstName','lastName' and 'github' 
    # fields from the related Profile model.
    bio = serializers.CharField(source='profile.bio',read_only=True)
    image = serializers.CharField(source='profile.image',read_only=True)

    firstName = serializers.CharField(source='profile.firstName',read_only=True)
    lastName = serializers.CharField(source='profile.lastName',read_only=True)
    github = serializers.CharField(source='profile.github',read_only=True)

    ###########################################################################
    

    class Meta:
        model = Author
        fields = (
            'email','username','password','token','profile','bio','image','firstName','lastName','github'
        )
        # The 'read_only_fields' option is an alternative for explicity specifying the field
        # with 'read_only= True' like we did for password.
        read_only_fields = ('token',)

    def update(self, instance, validated_data):
        """
        Performs an update on a User
        """
        password = validated_data.pop('password',None)
        # Passwords should not be handled with 'setattr', unlike other fields.
        # This is because Django provides a function that handles hashing and salting passwords,
        # which is important for security.
        # What that means here is that we need to remove the password filed from the 
        # 'validate_data' dictionary before iterating over it.

        # Like passwords, we have to handle profiles separately. To do that, 
        # We remove the profile data from the 'validated_data' dictionary.
        profile_data = validated_data.pop('profile',{})

        for (key,value) in validated_data.items():
            # For the keys remaining in 'validated_data', we will set them on 
            # the current 'User' instance at a time.
            setattr(instance,key,value)

        if password is not None:
            instance.set_password(password)


        #Finally, after everthing has been updated, we must explicitly save the model.
        #In this case, '.set_password()' does not save the model.
        instance.save()

        for (key,value) in profile_data.items():
            # Makes changes to the Profile model.
            setattr(instance.profile,key,value)

        instance.profile.save()
        
        return instance


