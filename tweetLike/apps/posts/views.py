from rest_framework import mixins,status,viewsets,generics
from rest_framework.exceptions import NotFound
from rest_framework.permissions import IsAuthenticatedOrReadOnly,IsAuthenticated,AllowAny
from rest_framework.response import Response
from rest_framework.views import APIView

from .models import Post,Comment,Tag
from .renderers import PostJSONRenderer,CommentJSONRenderer
from .serializers import PostSerializer,CommentSerializer,TagSerializer

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

    def list(self,request):
        serializer_context = {'request':request} 
        page = self.paginate_queryset(self.queryset)

        serializer = self.serializer_class(
            page,
            context =serializer_context,
            many = True
        )
        return self.get_paginated_response(serializer.data)

    def retrieve(self, request,slug=None):
        try:
            serializer_instance = self.queryset.get(slug=slug)
        except Post.DoesNotExist:
            raise NotFound('An article with this slug does not exist.')

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

class CommentsListCreateAPIView(generics.ListCreateAPIView):
    lookup_field = 'post__slug' # Indicates the field name for queryset
    lookup_url_kwarg ='post_slug' # Indicates the field name for url

    permission_classes = [IsAuthenticatedOrReadOnly,]
    renderer_classes = [CommentJSONRenderer,]
    serializer_class = CommentSerializer

    queryset = Comment.objects.select_related(
        'post','post__author',
        'post__author__author',
        'author','author__author'
    )

    def filter_queryset(self, queryset):
        # The built-in list fuction calls 'filter_queryset'. Since
        # we only want comments for a specific post, this is a good place 
        # to do that filtering
        filters = {self.lookup_field: self.kwargs[self.lookup_url_kwarg] }
        return queryset.filter(**filters)


    def create(self, request, post_slug = None):
        data = request.data.get('comment',{})
        context = {
            'author':request.user.profile
        }
        try:
            context['post'] = Post.objects.get(slug=post_slug)
        except Post.DoesNotExist:
            raise NotFound('An article with this slug does not exist. ')
        serializer = self.serializer_class(data=data,context=context)
        serializer.is_valid(raise_exception=True)
        serializer.save()
        return Response(serializer.data,status=status.HTTP_201_CREATED)

class CommentDestroyAPIView(generics.RetrieveDestroyAPIView):
    lookup_url_kwarg ='comment_pk'
    permission_classes = [IsAuthenticatedOrReadOnly,]
    renderer_classes = [CommentJSONRenderer,]
    serializer_class = CommentSerializer


    def retrieve(self,request,post_slug=None,comment_pk=None):
        try:
            serializer_instance = Comment.objects.get(pk=comment_pk,post__slug=post_slug)
        except Comment.DoesNotExist:
            raise NotFound('A comment with this ID does not exist.')
        
        serializer = self.serializer_class(serializer_instance)

        return Response(serializer.data,status=status.HTTP_200_OK)

    def destroy(self,request,post_slug=None,comment_pk=None):
        try:
            comment = Comment.objects.get(pk=comment_pk,post__slug=post_slug)
        except Comment.DoesNotExist:
            raise NotFound('A comment with this ID does not exist.')
        
        comment.delete()
        return Response({},status=status.HTTP_204_NO_CONTENT)


class PostFavoriteAPIView(APIView):
    permission_classes = [IsAuthenticated,]
    renderer_classes = [PostJSONRenderer,]
    serializer_class = PostSerializer

    def delete(self,request,post_slug=None):
        profile = self.request.user.profile
        serializer_context = {'request':request}

        try:
            post = Post.objects.get(slug=post_slug)
        except Post.DoesNotExist:
            raise NotFound("An article with this slug was not found")

        profile.unfavorite(post)
        serializer = self.serializer_class(post,context=serializer_context)
        return Response(serializer.data,status=status.HTTP_200_OK)

    def post(self, request, post_slug=None):
        profile = self.request.user.profile
        serializer_context = {'request':request}

        try:
            post = Post.objects.get(slug=post_slug)
        except Post.DoesNotExist:
            raise NotFound("An article with this slug was not found")
        profile.favorite(post)
        serializer = self.serializer_class(post,context=serializer_context)

        return Response(serializer.data,status=status.HTTP_201_CREATED)


class TagListAPIView(generics.ListAPIView):
    queryset = Tag.objects.all()
    pagination_class = None
    permission_classes = [AllowAny,]
    serializer_class = TagSerializer

    def list(self,request):
        serializer_data = self.get_queryset()
        serializer = self.serializer_class(serializer_data,many=True)

        return Response(
            {
                "tags":serializer.data
            },status = status.HTTP_200_OK
        )