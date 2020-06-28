

# Create your views here.
from rest_framework import status,serializers
from rest_framework.generics import RetrieveAPIView
from rest_framework.permissions import AllowAny,IsAuthenticated
from rest_framework.response import Response
from rest_framework.views import APIView
from rest_framework.exceptions import NotFound

from .exceptions import ProfileDoesNotExist
from .models import Profile
from .renderers import ProfileJSONRenderer
from .serializers import ProfileSerializer





class ProfileRetrieveAPIView(RetrieveAPIView):
    permission_classes = [AllowAny,]
    renderer_classes = (ProfileJSONRenderer,)
    serializer_class = ProfileSerializer
    def retrieve(self,request,username,*args, **kwargs):
        # Try to retrieve the requested profile and throw an exception if the profile could not found.
        try:
            # We use the 'select_related' method to avoid making unnecessary database calls.
            profile = Profile.objects.select_related('author').get(author__username=username)
        except Profile.DoesNotExist:
            raise ProfileDoesNotExist

        serializer = self.serializer_class(profile)
       
        return Response(serializer.data,status=status.HTTP_200_OK)

class ProfileFollowAPIView(APIView):
    permission_classes = [IsAuthenticated,]
    renderer_classes = (ProfileJSONRenderer,)
    serializer_class = ProfileSerializer

    def post(self,request,username=None):
        follower =  self.request.user.profile
        try:
            followee = Profile.objects.get(author__username=username)
        except Profile.DoesNotExist:
            raise NotFound('A profile with this username does not exist')

        if follower.pk is followee.pk:
            raise serializers.ValidationError("You can not follow yourself.")
        
        follower.follow(followee)

        serializer = self.serializer_class(
            followee,
            context={
                'request':request
                }
            )
        return Response(serializer.data,status= status.HTTP_201_CREATED)
    
    def delete(self,request,username=None):
        follower = self.request.user.profile

        try:
            followee = Profile.objects.get(author__username=username)
        except Profile.DoesNotExist:
            raise NotFound('A profile with this username does not exist')


        follower.unfollow(followee)
        serializer = self.serializer_class(
            followee,
            context = {
                'request':request
            }
        )
        return Response(serializer.data,status=status.HTTP_204_NO_CONTENT)