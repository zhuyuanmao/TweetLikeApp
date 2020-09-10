from rest_framework import serializers

from tweetLike.apps.profiles.serializers import ProfileSerializer

from .models import Post,Comment,Tag
from .relations import TagRelatedField


class PostSerializer(serializers.ModelSerializer):
    author = ProfileSerializer(read_only=True)
    description = serializers.CharField(required=False)
    slug = serializers.SlugField(required=False)

    favorited = serializers.SerializerMethodField(
        method_name="get_favorited"
    )
    favoritesCount = serializers.SerializerMethodField(
        method_name="get_favorites_count"
    )

    tagList = TagRelatedField(many=True,required=False,source='tags')

    created_at  = serializers.SerializerMethodField(method_name='get_created_at')
    updated_at = serializers.SerializerMethodField(method_name='get_updated_at')

    
    class Meta:
        model = Post
        fields = (
            'author',
            'content',
            'description',
            'slug',
            'title',
            'contentType',
            'favorited',
            'favoritesCount',
            'tagList',
            'created_at',
            'updated_at',
        )
    def create(self,validated_data):
        author = self.context.get('author',None)

        tags = validated_data.pop('tags',[])

        post =  Post.objects.create(author=author,**validated_data)

        for tag in tags:
            post.tags.add(post)

        return post

    def get_favorited(self,instance):
        request = self.context.get('request',None)
        if request is None:
            return False
        if not request.user.is_authenticated():
            return False

        return request.user.profiles.has_favorited(instance)

    def get_favorites_count(self,instance):
        return instance.favorited_by.count()

    def get_created_at(self, instance):
        return instance.created_at.isoformat()

    def get_updated_at(self, instance):
        return instance.updated_at.isoformat()

class CommentSerializer(serializers.ModelSerializer):
    author = ProfileSerializer(required=False)
    created_at  = serializers.SerializerMethodField(method_name='get_created_at')
    updated_at = serializers.SerializerMethodField(method_name='get_updated_at')

    class Meta:
        model = Comment
        fields = (
            'id',
            'created_at',
            'updated_at',
            'body',
            'author',
        )

    def create(self,validated_data):
        post = self.context['post']
        author = self.context['author']

        return Comment.objects.create(
            author=author,post = post, **validated_data
        )
    
    def get_created_at(self, instance):
        return instance.created_at.isoformat()

    def get_updated_at(self, instance):
        return instance.updated_at.isoformat()

class TagSerializer(serializers.ModelSerializer):
    class Meta:
        model = Tag
        fields = ('tag',)

    def to_representation(self, instance):
        return instance.tag