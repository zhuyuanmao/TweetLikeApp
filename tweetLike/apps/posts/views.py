from django.shortcuts import render
from rest_framework import mixins,status,viewsets
from rest_framework.exceptions import NotFound
from rest_framework.permissions import IsAuthenticatedOrReadOnly
from rest_framework.response import Response

from .models import Post
from .renderers import PostJSONRenderer
from .serializers import PostSerializer

class PostViewSet(mixins.CreateModelMixin,
                 mixins.ListModelMixin,
                 mixins.RetrieveModelMixin,
                 viewsets.GenericViewSet):
    lookup_field = 'slug'
    queryset = Post.objects.select_related('author','author__author')
    permission_classes = [IsAuthenticatedOrReadOnly,]
    renderer_classes = [PostJSONRenderer,]
    serializer_class = PostSerializer

    def create(self,request):
        serializer_context = {'author':request.user.profile} 
        serializer_data = request.data.get('post',{})

        serializer = self.serializer_class(
            data=serializer_data, 
            context= serializer_context
        )
        serializer.is_valid(raise_exception=True)
        serializer.save()
        
        return Response(serializer.data,status=status.HTTP_201_CREATED)

    def retrieve(self, request,slug=None):
        try:
            serializer_instance = self.queryset.get(slug=slug)
        except Post.DoesNotExist:
            raise NotFound('An artile with this slug does not exist.')

        serializer = self.serializer_class(serializer_instance)

        return Response(serializer.data,status=status.HTTP_200_OK)

    def update(self,request,slug):
        try:
            serializer_instance = self.queryset.get(slug=slug)
        except Post.DoesNotExist:
            raise NotFound('An article with this slug does not exist.',status_code=404)
        
        serializer_data = request.data.get('post',{})

        serializer = self.serializer_class(
            serializer_instance,data=serializer_data,partial = True
        )
        serializer.is_valid(raise_exception=True)
        serializer.save()

        return Response(serializer.data,status=status.HTTP_200_OK)
        

