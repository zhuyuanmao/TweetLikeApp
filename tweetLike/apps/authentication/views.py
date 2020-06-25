from rest_framework import status
from rest_framework.generics import RetrieveUpdateAPIView
from rest_framework.permissions import AllowAny, IsAuthenticated
from rest_framework.response import Response
from rest_framework.views import APIView

from .renderers import UserJSONRenderer
from .serializers import (LoginSerializer,RegistrationSerializer,AuthorSerializer)


class RegistrationAPIView(APIView):
    """
    Allow any user (authenticated or not) to hit this endpoint.
    """

    permission_classes = [AllowAny,]
    renderer_classes = [UserJSONRenderer,]
    serializer_class = RegistrationSerializer

    def post(self, request):
        user = request.data.get('user',{})

        # The create serializer, validate serializer, save serilaier pattern
        serializer = self.serializer_class(data=user)
        serializer.is_valid(raise_exception=True)
        serializer.save()

        return Response(serializer.data,status=status.HTTP_201_CREATED)

class LoginAPIView(APIView):
    """
    Allow any user to hit this endpoint.
    But authenticated user will recieve a 200 status code.
    """

    permisson_classes = [AllowAny,]
    renderer_classess = [UserJSONRenderer,]
    serializer_class = LoginSerializer

    def post(self,request):
        user = request.data.get('user',{})

        # Notice here that we do not call "serializer.save()" like we did for
        # the registration endpoint. This is because we don't actually have 
        # anything to save. Instead, the "validate" method on our serializer
        # handles everything we need.

        serializer = self.serializer_class(data=user)
        serializer.is_valid(raise_exception=True)

        return Response(serializer.data,status=status.HTTP_200_OK)

class UserRetrieveUpdateAPIView(RetrieveUpdateAPIView):
    
    permission_classes = [IsAuthenticated,]
    renderer_classess = (UserJSONRenderer,)
    serializer_class = AuthorSerializer

    def retrieve(self,request,*args,**kwargs):
        # There is nothing to validate or save here, Instead, we just want the 
        # serializer to handle turning our 'User' object into something that
        # can be JSONified and sent to the client.
        serializer = self.serializer_class(request.user)

        return Response(serializer.data,status=status.HTTP_200_OK)

    def update(self, request, *args, **kwargs):
        user_data = request.data.get('user',{})
        serializer_data = {
            'username':user_data.get('username',request.user.username),
            'email':user_data.get('email',request.user.email),
            # ? Need a new functionality to change password?
            'password':user_data.get('password',request.user.password),
            'profile':{
                'bio':user_data.get('bio',request.user.profile.bio),
                'image': user_data.get('image',request.user.profile.image),
                'firstName':user_data.get('firstName',request.user.profile.firstName),
                'lastName':user_data.get('lastName',request.user.profile.lastName),
                'github':user_data.get('github',request.user.profile.github)
            }
        }
        #Here is that serialize, validate,save pattern.
        serializer = self.serializer_class(
            request.user,data=serializer_data,partial = True
        )
        serializer.is_valid(raise_exception=True)
        serializer.save()

        return Response(serializer_data,status=status.HTTP_200_OK)
