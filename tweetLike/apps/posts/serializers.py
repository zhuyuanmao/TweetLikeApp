from rest_framework import serializers

from tweetLike.apps.profiles.serializers import ProfileSerializer

from .models import Post,Comment


class PostSerializer(serializers.ModelSerializer):
    author = ProfileSerializer(read_only=True)
    description = serializers.CharField(required=False)
    slug = serializers.SlugField(required=False)
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
            'created_at',
            'updated_at',
        )
    def create(self,validated_data):
        author = self.context.get('author',None)

        return Post.objects.create(author=author,**validated_data)

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
