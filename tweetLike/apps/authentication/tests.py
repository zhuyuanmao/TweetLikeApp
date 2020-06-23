from django.test import TestCase
from tweetLike.apps.authentication.models import Author
from .views import RetrieveUpdateAPIView
from rest_framework.test import (
    APIRequestFactory,APIClient,
    APITestCase,
    force_authenticate
    )
from django.contrib.auth import get_user_model


"""
Model Tests
"""
class AuthorModelTest(TestCase):
    def create_author(self,email ="John_Doe@test.com",username="johndoe",password="test"):
        return Author.objects.create_user(email,username,password)

    def test_author_creation(self):
        author = self.create_author()
        self.assertTrue(isinstance(author,Author))
        self.assertEqual(str(author),author.email)
        self.assertEqual(author.get_username(),author.username)
"""
API Tests
"""
class AuthenticationAPITest(APITestCase):
    login_data = {
        "user": {
            "username":"yuanmao",
            "email": "yuanmao@user.com",
            "password":"1997zhu."
        }
    }
    def test_author_registration(self):
        """
        Makes registration by giving user info.
        """
        response = self.client.post('/users/',self.login_data,format='json')
        self.assertEqual(response.status_code,201)

        self.assertEqual(Author.objects.count(),1)
        self.assertEqual(Author.objects.get().username,'yuanmao')
        self.assertEqual(Author.objects.get().email,'yuanmao@user.com')

    def test_author_registration_repeated_account_info(self):
        """
        Registrates user info twice.
        """
        response = self.client.post('/users/',self.login_data,format='json')
        self.assertEqual(response.status_code,201)
        response =  self.client.post('/users/',self.login_data,format='json')
        self.assertEqual(response.status_code,400)
        response.render()
        self.assertEqual(response.content.decode('UTF-8'),'{"errors":{"email":["author with this email already exists."],"username":["author with this username already exists."]}}')
    def test_author_login(self):
        """
        Login with correct user/password pair
        """
        response = self.client.post('/users/',self.login_data,format='json')
        self.assertEqual(response.status_code,201)
        response = self.client.post('/users/login/',self.login_data,format='json')
        self.assertEqual(response.status_code,200)
    def test_author_login_with_doesnonexist_user_info(self):
        """
        Login with does not exist user/password pair
        """
        response = self.client.post('/users/login/',self.login_data,format='json')
        self.assertEqual(response.status_code,400)
    def test_author_login_with_wrong_user_password(self):
        """
        Login with wrong user/password pair
        """
        response = self.client.post('/users/',self.login_data,format='json')
        self.assertEqual(response.status_code,201)

        mask_data =  {
            "user": {
                "username":"yuanmao",
                "email": "yuanmao@user.com",
                "password":"wrong"
            }
        }
        response = self.client.post('/users/login/',mask_data,format='json')
        self.assertEqual(response.status_code,400)


class UserRetrieveUpdateAPITest(APITestCase):

    def setUp(self):
        self.user = get_user_model().objects.create_user(email='john@test.com',username='john',password='secret')
        self.client = APIClient()
        
    def test_get_author_info_successful(self):
        self.client.force_authenticate(user=self.user)
        response = self.client.get('/user/')
        self.assertEqual(response.status_code,200)

    def test_get_user_unauthenticated(self):
        response = self.client.get('/user/')
        self.assertEqual(response.status_code,403)

    def test_post_me_not_allowed(self):
        self.client.force_authenticate(user=self.user)
        response = self.client.post('/user/',{})
        self.assertEqual(response.status_code,405)

    def test_update_user_info_successful(self):
        self.client.force_authenticate(user=self.user)
        payload =  {
            "user": 
                {'username':'johndoe',
                'email':'johndoe@user.com',
                'password':'newpassword'
            }
        }
        #Update all info    
        response = self.client.put('/user/',data=payload,format='json')
        self.user.refresh_from_db()

        self.assertEqual(response.status_code,200)
        self.assertTrue(self.user.check_password(payload['user'].get('password')))
        self.assertEqual(self.user.username,payload['user'].get('username'))
        self.assertEqual(self.user.email,payload['user'].get('email'))

    def test_update_user_info_partially(self):
        self.client.force_authenticate(user=self.user)
        payload =  {
            "user": 
                {'username':'new_username',
            }
        }
        response = self.client.put('/user/',data=payload,format='json')
        self.user.refresh_from_db()
        
        self.assertEqual(response.status_code,200)
        self.assertEqual(self.user.username,payload['user'].get('username'))


     


    

  


