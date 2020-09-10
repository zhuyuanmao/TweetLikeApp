import json
from rest_framework.renderers import JSONRenderer
from rest_framework.utils.serializer_helpers import ReturnList

class TweetLikeJsonRender(JSONRenderer):
    charset = 'utf-8'
    object_label = 'object'
    object_label_plural = 'objects'
    pagination_object_label ='objects'
    pagination_count_label = 'count'

    def render(self,data,media_type=None,render_context= None):
        if isinstance(data,ReturnList):
            _data = json.loads(
                super(TweetLikeJsonRender,self).render(data).decode('utf-8')
            )
            return json.dumps({
                self.object_label_plural: _data
            }
            )
        else:
            # If the view throws an error (such as the user can't be authenticated)
            # or something similar), 'data' will contain an 'errors' key. We want 
            # the default JSONRender to handle rendering errors, so we need to 
            # check for this case.
            errors = data.get('error',None)

            if errors is not None:
                # We will let the default JSONRenderer handle rendering errors.
                return super(TweetLikeJsonRender,self).render(data)
                
            return json.dumps(
                {
                    self.object_label:data
                }
            )