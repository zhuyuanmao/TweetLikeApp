import json
from rest_framework.renderers import JSONRenderer

class TweetLikeJsonRender(JSONRenderer):
    charset = 'utf-8'
    object_label = 'object'

    def render(self,data,media_type=None,render_context= None):
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