import json
from rest_framework.renderers import JSONRenderer

class UserJSONRenderer(JSONRenderer):
    charset = 'utf-8'
    object_label = 'user'
    pagination_object_label ='users'
    pagination_count_label = 'usersCount'

    def render(self,data,media_type=None, render_context = None):
        # If the view throws an error (such as the user can't be authenticated
        # or something similar ), 'data' will contain an 'errors' key. We want 
        # the default JSONRender to handle rendering errors, so we need to check
        # for  this case.
        errors = data.get('errors',None)

        # If we recieve a 'token' key as part of the response, it will by a 
        # byte object. Byte objects don't serializer well, so we need to 
        # decode it before rendering the User object.

        token = data.get('token',None)

        if errors is not None:
            # we will let the default JSONRender handle rendering errors
            return super(UserJSONRenderer,self).render(data)
            
        if token is not None and isinstance(token,bytes):
            # we will decode 'token' if it is of type bytes.
            data['token'] = token.decode('utf-8')
        
        # Finally, we can render our data under the 'user' namespace.
        return json.dumps(
            {
                'user':data
            }
        )
            