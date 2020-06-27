from tweetLike.apps.core.renderers import TweetLikeJsonRender

class PostJSONRenderer(TweetLikeJsonRender):
    object_label = 'post'
    object_label_plural ='posts'

class CommentJSONRenderer(TweetLikeJsonRender):
    object_label = 'comment'
    object_label_plural ='comments'
    