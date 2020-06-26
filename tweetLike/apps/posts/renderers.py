from tweetLike.apps.core.renderers import TweetLikeJsonRender

class PostJSONRenderer(TweetLikeJsonRender):
    object_label = 'post'
    object_label_plural ='posts'
    