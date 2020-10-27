from tweetLike.apps.core.renderers import TweetLikeJsonRender

class ProfileJSONRenderer(TweetLikeJsonRender):
    object_label = 'profile'
    pagination_object_label ='profiles'
    pagination_count_label = 'profilesCount'