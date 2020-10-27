from tweetLike.apps.core.renderers import TweetLikeJsonRender

class PostJSONRenderer(TweetLikeJsonRender):
    object_label = 'post'
    object_label_plural ='posts'
    pagination_count_label = 'postCount'

class CommentJSONRenderer(TweetLikeJsonRender):
    object_label = 'comment'
    object_label_plural ='comments'
    pagination_count_label ='commentsCount'
    