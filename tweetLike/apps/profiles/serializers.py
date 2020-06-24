from rest_framework import serializers

from .models import Profile

class ProfileSerializer(serializers.ModelSerializer):
    username = serializers.CharField(source='author.username')
    bio = serializers.CharField(allow_blank=True,required=False)
    firstName = serializers.CharField(allow_blank=True,required=False)
    lastName = serializers.CharField(allow_blank=True,required=False)
    image = serializers.SerializerMethodField('get_image')
    github = serializers.CharField(allow_blank=True,required=False)

    class Meta:
        model = Profile
        fields = '__all__'
        read_only_fields = ('username',)
    def get_image(self,object):
        if object.image:
            return object.image
        return 'https://static.productionready.io/images/smiley-cyrus.jpg'